from datetime import datetime, timezone
import config
from core.database import get_db
from core.models import Lead, Pipeline, Activity


def move_pipeline_stage(
    lead_id: int,
    new_stage: str,
    next_action: str = None,
    next_follow_up: datetime = None,
    deal_value: float = None
) -> dict:
    """
    Move a lead to a new pipeline stage, update probability, log stage change activity, and adjust follow-up date.
    """
    if new_stage not in config.PIPELINE_STAGES:
        raise ValueError(f"Invalid pipeline stage: '{new_stage}'. Must be one of {config.PIPELINE_STAGES}")

    now = datetime.now(timezone.utc).replace(tzinfo=None)
    prob = config.STAGE_PROBABILITIES.get(new_stage, 0.05)

    with get_db() as session:
        lead = session.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            raise ValueError(f"Lead with ID {lead_id} not found.")

        old_stage = lead.pipeline_stage

        # Update lead fields
        lead.pipeline_stage = new_stage
        lead.probability = prob
        if deal_value is not None:
            lead.deal_value = float(deal_value)

        if next_follow_up is not None:
            if isinstance(next_follow_up, datetime) and next_follow_up.tzinfo is not None:
                next_follow_up = next_follow_up.replace(tzinfo=None)
            lead.next_follow_up = next_follow_up

        lead.updated_at = now

        # Add Pipeline record
        pipe_rec = Pipeline(
            lead_id=lead.id,
            stage=new_stage,
            deal_value=lead.deal_value,
            probability=prob,
            next_action=next_action or f"Moved to {new_stage}",
            next_follow_up=next_follow_up,
            entered_stage_at=now
        )
        session.add(pipe_rec)

        # Log Stage Change Activity
        act = Activity(
            lead_id=lead.id,
            activity_type="Stage Change",
            outcome=f"Moved from '{old_stage}' to '{new_stage}'",
            notes=f"Next Action: {next_action or 'Not specified'}. Probability updated to {prob*100:.0f}%.",
            created_at=now
        )
        session.add(act)

        session.commit()
        return {
            "lead_id": lead.id,
            "company_name": lead.company_name,
            "old_stage": old_stage,
            "new_stage": new_stage,
            "probability": prob,
            "deal_value": lead.deal_value,
            "next_follow_up": lead.next_follow_up
        }


def get_pipeline_kanban_data() -> dict:
    """
    Fetch all active leads grouped by pipeline stage for Kanban rendering.
    """
    with get_db() as session:
        leads = session.query(Lead).order_by(Lead.priority.asc(), Lead.icp_score.desc()).all()

        kanban = {stage: [] for stage in config.PIPELINE_STAGES}

        for l in leads:
            card = {
                "id": l.id,
                "company_name": l.company_name,
                "contact_name": l.contact_name,
                "title": l.title,
                "industry": l.industry,
                "priority": l.priority,
                "icp_score": l.icp_score,
                "deal_value": l.deal_value,
                "deal_health": l.deal_health,
                "next_follow_up": l.next_follow_up
            }
            if l.pipeline_stage in kanban:
                kanban[l.pipeline_stage].append(card)

        return kanban
