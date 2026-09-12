from datetime import datetime, timezone
from sqlalchemy import func
import config
from core.database import get_db
from core.models import Lead, Qualification, Activity


def get_executive_kpis() -> dict:
    """
    Compute core Executive Dashboard KPIs directly from SQLite.
    """
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    with get_db() as session:
        total_accounts = session.query(Lead).count()
        contacted_accounts = session.query(Lead).filter(Lead.pipeline_stage != "Identified").count()

        qualified_leads = session.query(Lead).filter(
            (Lead.priority == "Priority A") | (Lead.pipeline_stage.in_(["Qualified", "Discovery Booked", "Proposal", "Negotiation", "Won"]))
        ).count()

        discovery_meetings = session.query(Lead).filter(
            Lead.pipeline_stage.in_(["Discovery Booked", "Proposal", "Negotiation", "Won"])
        ).count()

        open_opportunities = session.query(Lead).filter(
            ~Lead.pipeline_stage.in_(["Won", "Lost"])
        ).count()

        pipeline_val_res = session.query(func.sum(Lead.deal_value)).filter(
            ~Lead.pipeline_stage.in_(["Won", "Lost"])
        ).scalar()
        pipeline_value = float(pipeline_val_res) if pipeline_val_res else 0.0

        won_count = session.query(Lead).filter(Lead.pipeline_stage == "Won").count()
        win_rate = (won_count / total_accounts * 100.0) if total_accounts > 0 else 0.0

        overdue_followups = session.query(Lead).filter(
            Lead.next_follow_up < now,
            ~Lead.pipeline_stage.in_(["Won", "Lost"])
        ).count()

        due_today_followups = session.query(Lead).filter(
            func.date(Lead.next_follow_up) == func.date(now),
            ~Lead.pipeline_stage.in_(["Won", "Lost"])
        ).count()

        priority_a_count = session.query(Lead).filter(Lead.priority == "Priority A").count()

        return {
            "total_accounts": total_accounts,
            "contacted_accounts": contacted_accounts,
            "qualified_leads": qualified_leads,
            "discovery_meetings": discovery_meetings,
            "open_opportunities": open_opportunities,
            "pipeline_value": pipeline_value,
            "won_count": won_count,
            "win_rate": win_rate,
            "overdue_followups": overdue_followups,
            "due_today_followups": due_today_followups,
            "priority_a_count": priority_a_count
        }


def get_funnel_distribution() -> list[dict]:
    """
    Get lead counts grouped by pipeline stage.
    """
    with get_db() as session:
        stage_counts = session.query(
            Lead.pipeline_stage, func.count(Lead.id)
        ).group_by(Lead.pipeline_stage).all()

        return [{"stage": s, "count": c} for s, c in stage_counts]


def get_industry_distribution() -> list[dict]:
    """
    Get lead counts grouped by industry.
    """
    with get_db() as session:
        industry_counts = session.query(
            Lead.industry, func.count(Lead.id)
        ).group_by(Lead.industry).all()

        return [{"industry": ind, "count": c} for ind, c in industry_counts]


def get_priority_accounts_summary(limit: int = 10) -> list[dict]:
    """
    Fetch top priority accounts formatted for UI rendering.
    """
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    with get_db() as session:
        priority_leads = session.query(Lead).filter(
            Lead.priority.in_(["Priority A", "Priority B"])
        ).order_by(Lead.icp_score.desc()).limit(limit).all()

        result = []
        for acc in priority_leads:
            f_up_str = acc.next_follow_up.strftime("%Y-%m-%d") if acc.next_follow_up else "None set"
            is_overdue = bool(acc.next_follow_up and acc.next_follow_up < now)
            status_tag = "⚠️ OVERDUE" if is_overdue else "OK"
            result.append({
                "id": acc.id,
                "Company": acc.company_name,
                "Contact Person": f"{acc.contact_name} ({acc.title})" if acc.title else acc.contact_name,
                "Industry": acc.industry,
                "Stage": acc.pipeline_stage,
                "Priority": acc.priority,
                "ICP Score": f"{acc.icp_score:.0f}/100",
                "Deal Value": f"₹{acc.deal_value/100000:.1f}L",
                "Next Follow-up": f_up_str,
                "Status": status_tag
            })
        return result


def get_funnel_conversion_rates() -> list[dict]:
    """
    Compute stage-to-stage conversion percentages and drop-off analysis.
    """
    with get_db() as session:
        total = session.query(Lead).count()
        if total == 0:
            return []

        contacted = session.query(Lead).filter(Lead.pipeline_stage != "Identified").count()
        engaged = session.query(Lead).filter(Lead.pipeline_stage.in_(["Engaged", "Qualified", "Discovery Booked", "Proposal", "Negotiation", "Won"])).count()
        qualified = session.query(Lead).filter(Lead.pipeline_stage.in_(["Qualified", "Discovery Booked", "Proposal", "Negotiation", "Won"])).count()
        discovery = session.query(Lead).filter(Lead.pipeline_stage.in_(["Discovery Booked", "Proposal", "Negotiation", "Won"])).count()
        proposal = session.query(Lead).filter(Lead.pipeline_stage.in_(["Proposal", "Negotiation", "Won"])).count()
        won = session.query(Lead).filter(Lead.pipeline_stage == "Won").count()

        return [
            {"stage": "Identified -> Contacted", "count": contacted, "conversion_rate": (contacted / total * 100.0)},
            {"stage": "Contacted -> Engaged", "count": engaged, "conversion_rate": (engaged / contacted * 100.0) if contacted > 0 else 0.0},
            {"stage": "Engaged -> Qualified", "count": qualified, "conversion_rate": (qualified / engaged * 100.0) if engaged > 0 else 0.0},
            {"stage": "Qualified -> Discovery", "count": discovery, "conversion_rate": (discovery / qualified * 100.0) if qualified > 0 else 0.0},
            {"stage": "Discovery -> Proposal", "count": proposal, "conversion_rate": (proposal / discovery * 100.0) if discovery > 0 else 0.0},
            {"stage": "Proposal -> Closed Won", "count": won, "conversion_rate": (won / proposal * 100.0) if proposal > 0 else 0.0}
        ]


def get_conversion_by_industry() -> list[dict]:
    """
    Compute win rate, account volume, and pipeline value grouped by industry.
    """
    with get_db() as session:
        results = []
        for ind in config.TARGET_INDUSTRIES:
            total_ind = session.query(Lead).filter(Lead.industry == ind).count()
            if total_ind > 0:
                won_ind = session.query(Lead).filter(Lead.industry == ind, Lead.pipeline_stage == "Won").count()
                val_res = session.query(func.sum(Lead.deal_value)).filter(Lead.industry == ind).scalar()
                total_val = float(val_res) if val_res else 0.0
                win_rate = (won_ind / total_ind * 100.0)

                results.append({
                    "industry": ind,
                    "total_accounts": total_ind,
                    "won_accounts": won_ind,
                    "win_rate": win_rate,
                    "total_value": total_val
                })
        return results


def get_conversion_by_lead_source() -> list[dict]:
    """
    Compute win rate and pipeline value grouped by acquisition lead source.
    """
    with get_db() as session:
        results = []
        for src in config.LEAD_SOURCES:
            total_src = session.query(Lead).filter(Lead.lead_source == src).count()
            if total_src > 0:
                won_src = session.query(Lead).filter(Lead.lead_source == src, Lead.pipeline_stage == "Won").count()
                val_res = session.query(func.sum(Lead.deal_value)).filter(Lead.lead_source == src).scalar()
                total_val = float(val_res) if val_res else 0.0
                win_rate = (won_src / total_src * 100.0)

                results.append({
                    "lead_source": src,
                    "total_accounts": total_src,
                    "won_accounts": won_src,
                    "win_rate": win_rate,
                    "total_value": total_val
                })
        return results


def get_at_risk_opportunities_audit() -> list[dict]:
    """
    Retrieve stalled or at-risk opportunities requiring executive intervention.
    """
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    with get_db() as session:
        at_risk_leads = session.query(Lead).filter(
            Lead.deal_health.in_(["At Risk", "Stalled"]),
            ~Lead.pipeline_stage.in_(["Won", "Lost"])
        ).order_by(Lead.deal_value.desc()).all()

        results = []
        for l in at_risk_leads:
            is_overdue = l.next_follow_up and l.next_follow_up < now
            risk_reason = "Overdue follow-up" if is_overdue else "Inactivity in pipeline stage"
            intervention = "Re-engage decision maker via Day 3 Value email" if is_overdue else "Review deal parameters with COO"

            results.append({
                "id": l.id,
                "Company": l.company_name,
                "Contact": f"{l.contact_name} ({l.title})",
                "Industry": l.industry,
                "Stage": l.pipeline_stage,
                "Priority": l.priority,
                "Health Status": l.deal_health,
                "Deal Value": f"₹{l.deal_value/100000:.1f}L",
                "Next Follow-up": l.next_follow_up.strftime("%Y-%m-%d") if l.next_follow_up else "None",
                "Risk Factor": risk_reason,
                "Recommended Action": intervention
            })
        return results
