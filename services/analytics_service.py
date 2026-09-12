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
