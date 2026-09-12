from datetime import datetime, timezone
from core.database import get_db
from core.models import Activity, Note, Lead


def log_activity(
    lead_id: int,
    activity_type: str,
    outcome: str = None,
    notes: str = None
) -> dict:
    """
    Log a sales activity for a lead and update the lead's last_contacted timestamp.
    """
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    with get_db() as session:
        lead = session.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            raise ValueError(f"Lead with ID {lead_id} not found.")

        act = Activity(
            lead_id=lead_id,
            activity_type=activity_type,
            outcome=outcome,
            notes=notes,
            created_at=now
        )
        session.add(act)

        # Update last_contacted on Lead
        if activity_type in ["Call", "Email", "LinkedIn", "Meeting"]:
            lead.last_contacted = now

        lead.updated_at = now
        session.commit()

        return {
            "id": act.id,
            "lead_id": act.lead_id,
            "activity_type": act.activity_type,
            "outcome": act.outcome,
            "notes": act.notes,
            "created_at": act.created_at
        }


def get_activities_for_lead(lead_id: int, limit: int = 50) -> list[dict]:
    """
    Retrieve chronological activity timeline for a lead (newest first).
    """
    with get_db() as session:
        activities = session.query(Activity).filter(
            Activity.lead_id == lead_id
        ).order_by(Activity.created_at.desc()).limit(limit).all()

        return [
            {
                "id": a.id,
                "lead_id": a.lead_id,
                "activity_type": a.activity_type,
                "outcome": a.outcome,
                "notes": a.notes,
                "created_at": a.created_at
            }
            for a in activities
        ]


def add_note(lead_id: int, body: str, author: str = "BDA Harish") -> dict:
    """
    Add a note to a lead.
    """
    if not body or not body.strip():
        raise ValueError("Note body cannot be empty.")

    now = datetime.now(timezone.utc).replace(tzinfo=None)

    with get_db() as session:
        lead = session.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            raise ValueError(f"Lead with ID {lead_id} not found.")

        note = Note(
            lead_id=lead_id,
            body=body.strip(),
            author=author,
            created_at=now
        )
        session.add(note)
        session.commit()

        return {
            "id": note.id,
            "lead_id": note.lead_id,
            "body": note.body,
            "author": note.author,
            "created_at": note.created_at
        }


def get_notes_for_lead(lead_id: int) -> list[dict]:
    """
    Retrieve all notes for a lead (newest first).
    """
    with get_db() as session:
        notes = session.query(Note).filter(
            Note.lead_id == lead_id
        ).order_by(Note.created_at.desc()).all()

        return [
            {
                "id": n.id,
                "lead_id": n.lead_id,
                "body": n.body,
                "author": n.author,
                "created_at": n.created_at
            }
            for n in notes
        ]
