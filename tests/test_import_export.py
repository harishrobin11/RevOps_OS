import pytest
from services.import_export_service import (
    generate_sample_csv,
    validate_and_parse_csv,
    import_leads_from_csv,
    export_leads_to_csv,
    export_activities_to_csv
)
from core.database import get_db, init_db
from core.models import Lead, Qualification, Activity
from data.seed_data import seed_database



@pytest.fixture(autouse=True)
def setup_database():
    init_db()
    seed_database()


def test_sample_csv_generator():
    csv_str = generate_sample_csv()
    assert "Company" in csv_str
    assert "Contact" in csv_str
    assert "Acme B2B Corp" in csv_str


def test_csv_validation_and_parsing():
    sample_csv = """Company,Contact,Title,Email,Phone,Industry,Location,Employees,Lead Source,Deal Value,Notes
Unique Test Corp 101,Aman Gupta,Head of Operations,aman@uniquetest101.com,+91 99999 11111,SaaS,Outer Ring Road,120,Outreach,1800000,Testing notes
,No Company Contact,VP Operations,nocompany@test.com,+91 99999 22222,FinTech,Koramangala,80,Inbound,1500000,No company
Invalid Email Inc,Suresh,Manager,invalid_email_at_test.com,+91 99999 33333,HealthTech,HSR Layout,50,CSV Import,1000000,Bad email
"""
    valid_rows, error_log = validate_and_parse_csv(sample_csv)

    assert len(valid_rows) == 1
    assert valid_rows[0]["company_name"] == "Unique Test Corp 101"
    assert valid_rows[0]["email"] == "aman@uniquetest101.com"

    assert len(error_log) == 2
    reasons = [e["reason"] for e in error_log]
    assert any("Missing required field: Company Name" in r for r in reasons)
    assert any("Invalid email format" in r for r in reasons)


def test_import_leads_execution():
    test_csv = """Company,Contact,Title,Email,Phone,Industry,Location,Employees,Lead Source,Deal Value,Notes
New Import Co Alpha,Rohan Verma,COO,rohan@alphanew.com,+91 98888 77777,AI & Automation,Electronic City,150,Inbound,2500000,Scaleup operational bottleneck
New Import Co Beta,Simran Kaur,Head of Delivery,simran@betanew.com,+91 98888 66666,SaaS,Whitefield,90,Outreach,1800000,Need process visibility
"""
    report = import_leads_from_csv(test_csv)
    assert report["success_count"] == 2
    assert report["error_count"] == 0

    with get_db() as session:
        lead_alpha = session.query(Lead).filter(Lead.company_name == "New Import Co Alpha").first()
        assert lead_alpha is not None
        assert lead_alpha.title == "COO"
        assert lead_alpha.icp_score > 0
        assert lead_alpha.pipeline_stage == "Identified"

        # Check qualification creation
        qual = session.query(Qualification).filter(Qualification.lead_id == lead_alpha.id).first()
        assert qual is not None
        assert qual.authority_confirmed is True

        # Check activity log creation
        act = session.query(Activity).filter(Activity.lead_id == lead_alpha.id).first()
        assert act is not None
        assert act.activity_type == "System Event"


def test_export_leads_and_activities():
    leads_csv = export_leads_to_csv()
    assert "Company Name" in leads_csv
    assert "ICP Score" in leads_csv
    assert len(leads_csv.splitlines()) > 5

    activities_csv = export_activities_to_csv()
    assert "Activity ID" in activities_csv
    assert "Company Name" in activities_csv
