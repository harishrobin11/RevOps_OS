import io
import csv
import re
from datetime import datetime, timezone
from typing import Tuple, List, Dict, Any
import pandas as pd

from core.database import get_db
from core.models import Lead, Qualification, Activity
from core.scoring import calculate_icp_score
from core.priority import calculate_combined_priority_score
import config


def generate_sample_csv() -> str:
    """
    Generates a sample CSV template string for lead import.
    """
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Company", "Contact", "Title", "Email", "Phone",
        "Industry", "Location", "Employees", "Lead Source", "Deal Value", "Notes"
    ])
    writer.writerow([
        "Acme B2B Corp", "Rajesh Sharma", "Head of Operations", "rajesh@acmeb2b.com", "+91 98765 43210",
        "SaaS", "Outer Ring Road", 120, "Inbound", 1500000, "Interested in workflow automation"
    ])
    writer.writerow([
        "NextGen Analytics", "Priya Nair", "VP Operations", "priya@nextgenanalytics.io", "+91 98123 45678",
        "FinTech", "Koramangala", 85, "Outreach", 2200000, "Evaluating operational efficiency tools"
    ])
    return output.getvalue()


def validate_and_parse_csv(file_content: str | bytes) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Validates CSV file content.
    Returns (valid_rows, error_log) where each error_log item is a dict with row, company, and reason.
    """
    if isinstance(file_content, bytes):
        file_content = file_content.decode("utf-8", errors="replace")

    stream = io.StringIO(file_content)
    reader = csv.DictReader(stream)

    valid_rows = []
    error_log = []

    # Simple email regex validation
    email_regex = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    # Fetch existing companies & emails from DB to prevent duplicates
    with get_db() as session:
        existing_companies = {c[0].lower().strip() for c in session.query(Lead.company_name).all() if c[0]}
        existing_emails = {e[0].lower().strip() for e in session.query(Lead.email).all() if e[0]}

    seen_in_batch_companies = set()
    seen_in_batch_emails = set()

    for idx, row in enumerate(reader, start=2): # Line 1 is header
        # Normalize column key lookup (case-insensitive)
        row_norm = {k.strip().lower(): v.strip() for k, v in row.items() if k}

        company = row_norm.get("company", "")
        contact = row_norm.get("contact", "") or row_norm.get("contact name", "") or "Primary Contact"
        title = row_norm.get("title", "") or row_norm.get("job title", "") or "Decision Maker"
        email = row_norm.get("email", "")
        phone = row_norm.get("phone", "") or "+91 90000 00000"
        industry = row_norm.get("industry", "") or "IT Services & Software"
        location = row_norm.get("location", "") or "Outer Ring Road"
        emp_str = row_norm.get("employees", "") or row_norm.get("employee count", "") or "75"
        source = row_norm.get("lead source", "") or row_norm.get("source", "") or "CSV Import"
        deal_val_str = row_norm.get("deal value", "") or row_norm.get("deal_value", "") or "1200000"
        notes = row_norm.get("notes", "")

        # 1. Validation: Missing Company
        if not company:
            error_log.append({"row": idx, "company": "N/A", "reason": "Missing required field: Company Name"})
            continue

        # 2. Duplicate check against DB and current batch
        comp_lower = company.lower()
        if comp_lower in existing_companies or comp_lower in seen_in_batch_companies:
            error_log.append({"row": idx, "company": company, "reason": "Duplicate company already exists"})
            continue

        # 3. Email validation
        if email:
            email_lower = email.lower()
            if not email_regex.match(email_lower):
                error_log.append({"row": idx, "company": company, "reason": f"Invalid email format: {email}"})
                continue
            if email_lower in existing_emails or email_lower in seen_in_batch_emails:
                error_log.append({"row": idx, "company": company, "reason": f"Duplicate email address: {email}"})
                continue
        else:
            email_lower = f"info@{re.sub(r'[^a-z0-9]', '', comp_lower)}.com"

        # 4. Employee count validation
        try:
            employee_count = int(emp_str)
            if employee_count <= 0:
                employee_count = 50
        except ValueError:
            employee_count = 50

        # 5. Deal Value parse
        try:
            deal_value = float(deal_val_str)
        except ValueError:
            deal_value = 1200000.0

        # Mark seen
        seen_in_batch_companies.add(comp_lower)
        seen_in_batch_emails.add(email_lower)

        valid_rows.append({
            "company_name": company,
            "contact_name": contact,
            "title": title,
            "email": email_lower,
            "phone": phone,
            "industry": industry,
            "location": location,
            "employee_count": employee_count,
            "lead_source": source,
            "deal_value": deal_value,
            "notes": notes
        })

    return valid_rows, error_log


def import_leads_from_csv(file_content: str | bytes) -> Dict[str, Any]:
    """
    Processes CSV import into the database.
    Calculates ICP scores, default BANT qualification, and creates initial activity log.
    Returns summary report dict.
    """
    valid_rows, error_log = validate_and_parse_csv(file_content)

    if not valid_rows:
        return {
            "success_count": 0,
            "error_count": len(error_log),
            "errors": error_log,
            "imported_leads": []
        }

    imported_ids = []

    with get_db() as session:
        for item in valid_rows:
            icp_score, fit_class, breakdown = calculate_icp_score(
                industry=item["industry"],
                employee_count=item["employee_count"],
                location=item["location"],
                title=item["title"],
                pain_points=item["notes"],
                growth_signal=True if item["notes"] else False
            )


            # Default initial priority based on ICP score
            if icp_score >= 80:
                priority = "Priority A"
            elif icp_score >= 60:
                priority = "Priority B"
            else:
                priority = "Priority C"

            new_lead = Lead(
                company_name=item["company_name"],
                contact_name=item["contact_name"],
                title=item["title"],
                email=item["email"],
                phone=item["phone"],
                industry=item["industry"],
                location=item["location"],
                employee_count=item["employee_count"],
                lead_source=item["lead_source"],
                deal_value=item["deal_value"],
                notes=item["notes"],
                icp_score=icp_score,
                priority=priority,
                pipeline_stage="Identified",
                deal_health="Healthy",
                created_at=datetime.now(timezone.utc).replace(tzinfo=None)
            )
            session.add(new_lead)
            session.flush()

            # Default qualification
            qual = Qualification(
                lead_id=new_lead.id,
                budget_confirmed=False,
                authority_confirmed=True if "Head" in item["title"] or "VP" in item["title"] or "COO" in item["title"] else False,
                need_confirmed=True if item["notes"] else False,
                timeline_confirmed=False,
                bant_score=35 if ("Head" in item["title"] or "VP" in item["title"] or "COO" in item["title"]) else 0,
                qualification_notes=f"CSV Import initial profile setup on {datetime.now(timezone.utc).strftime('%Y-%m-%d')}"
            )
            session.add(qual)

            # Initial Activity
            act = Activity(
                lead_id=new_lead.id,
                activity_type="System Event",
                outcome="Lead Imported",
                notes=f"Imported via CSV file with initial ICP Score {icp_score:.0f}/100.",
                created_at=datetime.now(timezone.utc).replace(tzinfo=None)
            )
            session.add(act)
            imported_ids.append(new_lead.id)

        session.commit()

    return {
        "success_count": len(valid_rows),
        "error_count": len(error_log),
        "errors": error_log,
        "imported_ids": imported_ids
    }


def export_leads_to_csv(stage_filter: str = "All", industry_filter: str = "All") -> str:
    """
    Exports leads as a CSV formatted string.
    """
    with get_db() as session:
        query = session.query(Lead)
        if stage_filter and stage_filter != "All":
            query = query.filter(Lead.pipeline_stage == stage_filter)
        if industry_filter and industry_filter != "All":
            query = query.filter(Lead.industry == industry_filter)

        leads = query.order_by(Lead.icp_score.desc()).all()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "Lead ID", "Company Name", "Contact Person", "Job Title", "Email", "Phone",
            "Industry", "Location", "Employees", "Lead Source", "Pipeline Stage",
            "ICP Score", "Priority", "Deal Value (₹)", "Deal Health", "Created Date", "Next Follow-up"
        ])

        for l in leads:
            f_up = l.next_follow_up.strftime("%Y-%m-%d") if l.next_follow_up else ""
            created = l.created_at.strftime("%Y-%m-%d") if l.created_at else ""
            writer.writerow([
                l.id, l.company_name, l.contact_name, l.title, l.email, l.phone,
                l.industry, l.location, l.employee_count, l.lead_source, l.pipeline_stage,
                f"{l.icp_score:.0f}", l.priority, l.deal_value, l.deal_health, created, f_up
            ])

        return output.getvalue()


def export_activities_to_csv() -> str:
    """
    Exports full activity history linked to company names.
    """
    with get_db() as session:
        activities = session.query(Activity, Lead.company_name).join(Lead, Activity.lead_id == Lead.id).order_by(Activity.created_at.desc()).all()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Activity ID", "Lead ID", "Company Name", "Activity Type", "Outcome", "Notes", "Timestamp"])

        for act, company_name in activities:
            ts = act.created_at.strftime("%Y-%m-%d %H:%M:%S") if act.created_at else ""
            writer.writerow([act.id, act.lead_id, company_name, act.activity_type, act.outcome, act.notes, ts])

        return output.getvalue()
