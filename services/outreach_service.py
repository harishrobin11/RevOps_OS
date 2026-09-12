from datetime import datetime, timezone
from core.database import get_db
from core.models import Outreach, Lead, Activity


def log_outreach(
    lead_id: int,
    channel: str,
    cadence_step: str = None,
    subject: str = None,
    content: str = None,
    status: str = "Pending"
) -> dict:
    """
    Log an outreach message generation or transmission.
    """
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    with get_db() as session:
        lead = session.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            raise ValueError(f"Lead with ID {lead_id} not found.")

        out = Outreach(
            lead_id=lead_id,
            channel=channel,
            cadence_step=cadence_step,
            subject=subject,
            content=content,
            status=status,
            sent_at=now if status == "Sent" else None
        )
        session.add(out)

        # Log companion activity
        act = Activity(
            lead_id=lead_id,
            activity_type=channel,
            outcome=f"Outreach ({cadence_step or 'Custom'}): {status}",
            notes=f"Subject: {subject or 'N/A'}",
            created_at=now
        )
        session.add(act)

        session.commit()
        return {
            "id": out.id,
            "lead_id": out.lead_id,
            "channel": out.channel,
            "cadence_step": out.cadence_step,
            "subject": out.subject,
            "content": out.content,
            "status": out.status,
            "sent_at": out.sent_at
        }


def update_outreach_status(outreach_id: int, status: str, response: str = None) -> dict:
    """
    Update outreach status (e.g. Sent, Responded, Failed).
    """
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    with get_db() as session:
        out = session.query(Outreach).filter(Outreach.id == outreach_id).first()
        if not out:
            raise ValueError(f"Outreach record {outreach_id} not found.")

        out.status = status
        if response:
            out.response = response

        if status == "Sent" and not out.sent_at:
            out.sent_at = now

        session.commit()
        return {
            "id": out.id,
            "status": out.status,
            "response": out.response,
            "sent_at": out.sent_at
        }


def get_outreach_history_for_lead(lead_id: int) -> list[dict]:
    """
    Get outreach messages for a lead.
    """
    with get_db() as session:
        items = session.query(Outreach).filter(
            Outreach.lead_id == lead_id
        ).order_by(Outreach.id.desc()).all()

        return [
            {
                "id": o.id,
                "lead_id": o.lead_id,
                "channel": o.channel,
                "cadence_step": o.cadence_step,
                "subject": o.subject,
                "content": o.content,
                "status": o.status,
                "sent_at": o.sent_at,
                "response": o.response
            }
            for o in items
        ]
