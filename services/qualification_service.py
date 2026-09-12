from datetime import datetime, timezone
import config
from core.database import get_db
from core.models import Qualification, Lead, Activity


def calculate_bant_score(budget: bool, authority: bool, need: bool, timeline: bool) -> float:
    """
    Calculate BANT score based on blueprint rules:
    - Budget confirmed: 25 pts
    - Authority confirmed: 35 pts
    - Need confirmed: 25 pts
    - Timeline confirmed: 15 pts
    Total: 100 pts
    """
    score = 0.0
    if budget:
        score += config.BANT_WEIGHTS["budget"]
    if authority:
        score += config.BANT_WEIGHTS["authority"]
    if need:
        score += config.BANT_WEIGHTS["need"]
    if timeline:
        score += config.BANT_WEIGHTS["timeline"]
    return score


def determine_priority_tier(bant_score: float) -> str:
    """
    Determine priority tier based on BANT score:
    - 85-100: Priority A / Hot Lead
    - 60-84: Priority B / Nurture
    - 0-59: Priority C / Low Probability
    """
    if bant_score >= 85.0:
        return "Priority A"
    elif bant_score >= 60.0:
        return "Priority B"
    else:
        return "Priority C"


def get_qualification_by_lead_id(lead_id: int) -> dict:
    """
    Fetch qualification details for a specific lead.
    """
    with get_db() as session:
        qual = session.query(Qualification).filter(Qualification.lead_id == lead_id).first()
        if not qual:
            return None
        return {
            "id": qual.id,
            "lead_id": qual.lead_id,
            "budget_confirmed": qual.budget_confirmed,
            "authority_confirmed": qual.authority_confirmed,
            "need_confirmed": qual.need_confirmed,
            "timeline_confirmed": qual.timeline_confirmed,
            "bant_score": qual.bant_score,
            "qualification_notes": qual.qualification_notes,
            "updated_at": qual.updated_at
        }


def update_qualification(
    lead_id: int,
    budget_confirmed: bool,
    authority_confirmed: bool,
    need_confirmed: bool,
    timeline_confirmed: bool,
    qualification_notes: str = None
) -> dict:
    """
    Update BANT criteria for a lead, recalculate score & priority, and log qualification activity.
    """
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    new_score = calculate_bant_score(budget_confirmed, authority_confirmed, need_confirmed, timeline_confirmed)
    new_priority = determine_priority_tier(new_score)

    with get_db() as session:
        qual = session.query(Qualification).filter(Qualification.lead_id == lead_id).first()
        lead = session.query(Lead).filter(Lead.id == lead_id).first()

        if not lead:
            raise ValueError(f"Lead with ID {lead_id} not found.")

        if not qual:
            qual = Qualification(
                lead_id=lead_id,
                budget_confirmed=budget_confirmed,
                authority_confirmed=authority_confirmed,
                need_confirmed=need_confirmed,
                timeline_confirmed=timeline_confirmed,
                bant_score=new_score,
                qualification_notes=qualification_notes,
                updated_at=now
            )
            session.add(qual)
        else:
            qual.budget_confirmed = budget_confirmed
            qual.authority_confirmed = authority_confirmed
            qual.need_confirmed = need_confirmed
            qual.timeline_confirmed = timeline_confirmed
            qual.bant_score = new_score
            if qualification_notes is not None:
                qual.qualification_notes = qualification_notes
            qual.updated_at = now

        # Update lead priority & updated timestamp
        lead.priority = new_priority
        lead.updated_at = now

        # Log Activity
        act = Activity(
            lead_id=lead_id,
            activity_type="Qualification",
            outcome=f"BANT Score: {new_score:.0f}/100 ({new_priority})",
            notes=f"Budget: {budget_confirmed}, Authority: {authority_confirmed}, Need: {need_confirmed}, Timeline: {timeline_confirmed}.",
            created_at=now
        )
        session.add(act)

        session.commit()
        return {
            "lead_id": lead_id,
            "bant_score": new_score,
            "priority": new_priority,
            "budget_confirmed": budget_confirmed,
            "authority_confirmed": authority_confirmed,
            "need_confirmed": need_confirmed,
            "timeline_confirmed": timeline_confirmed,
            "qualification_notes": qual.qualification_notes
        }
