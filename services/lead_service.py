import re
from datetime import datetime, timezone
from sqlalchemy import or_, desc, asc
import config
from core.database import get_db
from core.models import Lead, Qualification, Pipeline, Activity, Note


def validate_lead_data(data: dict, is_create: bool = False) -> tuple[bool, list[str]]:
    """
    Validate lead data input before database operations.
    Returns (is_valid, list_of_error_messages).
    """
    errors = []

    if is_create or "company_name" in data:
        company_name = str(data.get("company_name", "")).strip()
        if not company_name:
            errors.append("Company name is required.")

    if is_create or "contact_name" in data:
        contact_name = str(data.get("contact_name", "")).strip()
        if not contact_name:
            errors.append("Contact name is required.")

    if "email" in data and data["email"]:
        email = str(data["email"]).strip()
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, email):
            errors.append(f"Invalid email address format: '{email}'.")

    if "employee_count" in data and data["employee_count"] is not None:
        try:
            emp_val = int(data["employee_count"])
            if emp_val < 0:
                errors.append("Employee count cannot be negative.")
        except (ValueError, TypeError):
            errors.append("Employee count must be a valid integer.")

    if "deal_value" in data and data["deal_value"] is not None:
        try:
            val = float(data["deal_value"])
            if val < 0:
                errors.append("Deal value cannot be negative.")
        except (ValueError, TypeError):
            errors.append("Deal value must be a valid number.")

    return (len(errors) == 0, errors)


from core.scoring import calculate_icp_score, classify_icp_fit
from core.health import calculate_deal_health
from core.qualification import calculate_bant_score, classify_bant_priority


def create_lead(lead_data: dict) -> dict:
    """
    Create a new Lead with default Qualification and Pipeline records.
    Automatically calculates ICP Score and Deal Health via Intelligence Engine.
    """
    is_valid, errors = validate_lead_data(lead_data, is_create=True)
    if not is_valid:
        raise ValueError("; ".join(errors))

    now = datetime.now(timezone.utc).replace(tzinfo=None)

    # Compute ICP Score via Intelligence Engine
    icp_score, fit_label, _ = calculate_icp_score(
        industry=lead_data.get("industry", "SaaS"),
        employee_count=lead_data.get("employee_count", 0),
        location=lead_data.get("location", "Outer Ring Road"),
        title=lead_data.get("title", ""),
        pain_points=lead_data.get("notes", "")
    )

    stage = lead_data.get("pipeline_stage", "Identified")
    prob = config.STAGE_PROBABILITIES.get(stage, 0.05)
    health = calculate_deal_health(stage=stage)

    with get_db() as session:
        # Check duplicate company + contact
        existing = session.query(Lead).filter(
            Lead.company_name.ilike(lead_data["company_name"].strip()),
            Lead.contact_name.ilike(lead_data["contact_name"].strip())
        ).first()

        if existing:
            raise ValueError(f"A lead for company '{lead_data['company_name']}' with contact '{lead_data['contact_name']}' already exists.")

        lead = Lead(
            company_name=lead_data["company_name"].strip(),
            contact_name=lead_data["contact_name"].strip(),
            title=lead_data.get("title", ""),
            email=lead_data.get("email", ""),
            phone=lead_data.get("phone", ""),
            industry=lead_data.get("industry", "SaaS"),
            location=lead_data.get("location", "Outer Ring Road"),
            employee_count=int(lead_data.get("employee_count", 0)),
            website=lead_data.get("website", ""),
            lead_source=lead_data.get("lead_source", "Outbound Cold Outreach"),
            notes=lead_data.get("notes", ""),
            icp_score=icp_score,
            priority=lead_data.get("priority", "Priority C"),
            pipeline_stage=stage,
            deal_value=float(lead_data.get("deal_value", 0.0)),
            probability=prob,
            deal_health=health,
            created_at=now,
            updated_at=now
        )
        session.add(lead)
        session.flush()

        # Initialize Qualification
        qual = Qualification(
            lead_id=lead.id,
            budget_confirmed=False,
            authority_confirmed=False,
            need_confirmed=False,
            timeline_confirmed=False,
            bant_score=0.0,
            qualification_notes="Initial lead creation.",
            updated_at=now
        )
        session.add(qual)

        # Initialize Pipeline
        pipe = Pipeline(
            lead_id=lead.id,
            stage=stage,
            deal_value=lead.deal_value,
            probability=prob,
            next_action="Initial contact",
            entered_stage_at=now
        )
        session.add(pipe)

        # Log creation activity
        act = Activity(
            lead_id=lead.id,
            activity_type="System Event",
            outcome="Lead Created",
            notes=f"Created lead '{lead.company_name}' via {lead.lead_source}.",
            created_at=now
        )
        session.add(act)

        session.commit()
        return _serialize_lead(lead)


def get_lead_by_id(lead_id: int) -> dict:
    """
    Fetch a single lead by ID with details.
    """
    with get_db() as session:
        lead = session.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            return None
        return _serialize_lead(lead, full_details=True)


def get_leads(
    search_query: str = None,
    industry: str = None,
    priority: str = None,
    pipeline_stage: str = None,
    location: str = None,
    lead_source: str = None,
    sort_by: str = "created_at",
    descending: bool = True
) -> list[dict]:
    """
    Fetch, search, filter, and sort leads.
    """
    with get_db() as session:
        query = session.query(Lead)

        if search_query:
            pattern = f"%{search_query.strip()}%"
            query = query.filter(
                or_(
                    Lead.company_name.ilike(pattern),
                    Lead.contact_name.ilike(pattern),
                    Lead.email.ilike(pattern),
                    Lead.notes.ilike(pattern)
                )
            )

        if industry and industry != "All":
            query = query.filter(Lead.industry == industry)

        if priority and priority != "All":
            query = query.filter(Lead.priority == priority)

        if pipeline_stage and pipeline_stage != "All":
            query = query.filter(Lead.pipeline_stage == pipeline_stage)

        if location and location != "All":
            query = query.filter(Lead.location == location)

        if lead_source and lead_source != "All":
            query = query.filter(Lead.lead_source == lead_source)

        # Sorting
        sort_column = getattr(Lead, sort_by, Lead.created_at)
        if descending:
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))

        leads = query.all()
        return [_serialize_lead(l) for l in leads]


def update_lead(lead_id: int, update_data: dict) -> dict:
    """
    Update lead record with validation.
    """
    is_valid, errors = validate_lead_data(update_data)
    if not is_valid:
        raise ValueError("; ".join(errors))

    now = datetime.now(timezone.utc).replace(tzinfo=None)

    with get_db() as session:
        lead = session.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            raise ValueError(f"Lead with ID {lead_id} not found.")

        for key, value in update_data.items():
            if hasattr(lead, key) and key not in ["id", "created_at"]:
                setattr(lead, key, value)

        lead.updated_at = now
        session.commit()
        return _serialize_lead(lead)


def delete_lead(lead_id: int) -> bool:
    """
    Delete lead by ID.
    """
    with get_db() as session:
        lead = session.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            return False
        session.delete(lead)
        session.commit()
        return True


def _serialize_lead(lead: Lead, full_details: bool = False) -> dict:
    """
    Convert Lead SQLAlchemy model instance to clean dictionary.
    """
    data = {
        "id": lead.id,
        "company_name": lead.company_name,
        "contact_name": lead.contact_name,
        "title": lead.title,
        "email": lead.email,
        "phone": lead.phone,
        "industry": lead.industry,
        "location": lead.location,
        "employee_count": lead.employee_count,
        "website": lead.website,
        "lead_source": lead.lead_source,
        "notes": lead.notes,
        "icp_score": lead.icp_score,
        "priority": lead.priority,
        "pipeline_stage": lead.pipeline_stage,
        "deal_value": lead.deal_value,
        "probability": lead.probability,
        "deal_health": lead.deal_health,
        "created_at": lead.created_at,
        "updated_at": lead.updated_at,
        "last_contacted": lead.last_contacted,
        "next_follow_up": lead.next_follow_up
    }

    if full_details:
        if lead.qualifications:
            qual = lead.qualifications[0]
            data["qualification"] = {
                "id": qual.id,
                "budget_confirmed": qual.budget_confirmed,
                "authority_confirmed": qual.authority_confirmed,
                "need_confirmed": qual.need_confirmed,
                "timeline_confirmed": qual.timeline_confirmed,
                "bant_score": qual.bant_score,
                "qualification_notes": qual.qualification_notes
            }
        else:
            data["qualification"] = None

        data["activities_count"] = len(lead.activities)
        data["notes_count"] = len(lead.lead_notes)

    return data
