import pytest
from core.database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from services.lead_service import create_lead, get_lead_by_id, get_leads, update_lead, delete_lead, validate_lead_data
from services.qualification_service import calculate_bant_score, determine_priority_tier, update_qualification
from services.pipeline_service import move_pipeline_stage, get_pipeline_kanban_data
from services.activity_service import log_activity, get_activities_for_lead, add_note
from services.analytics_service import get_executive_kpis, get_priority_accounts_summary
from data.seed_data import seed_database


@pytest.fixture(scope="function", autouse=True)
def setup_test_db(monkeypatch):
    """
    Setup an isolated SQLite in-memory database for testing services.
    """
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def mock_get_db():
        from contextlib import contextmanager
        @contextmanager
        def _session_scope():
            session = TestingSession()
            try:
                yield session
                session.commit()
            except Exception:
                session.rollback()
                raise
            finally:
                session.close()
        return _session_scope()

    monkeypatch.setattr("services.lead_service.get_db", mock_get_db)
    monkeypatch.setattr("services.qualification_service.get_db", mock_get_db)
    monkeypatch.setattr("services.pipeline_service.get_db", mock_get_db)
    monkeypatch.setattr("services.activity_service.get_db", mock_get_db)
    monkeypatch.setattr("services.outreach_service.get_db", mock_get_db)
    monkeypatch.setattr("services.analytics_service.get_db", mock_get_db)
    monkeypatch.setattr("data.seed_data.get_db", mock_get_db)

    # Seed data
    with mock_get_db() as session:
        seed_database(session)


def test_lead_validation():
    """Test lead input data validation rules."""
    is_valid, errors = validate_lead_data({"company_name": "", "contact_name": "John"})
    assert not is_valid
    assert any("Company name" in e for e in errors)

    is_valid, errors = validate_lead_data({"company_name": "Acme", "contact_name": "John", "email": "invalid-email"})
    assert not is_valid
    assert any("Invalid email" in e for e in errors)

    is_valid, errors = validate_lead_data({"company_name": "Acme", "contact_name": "John", "email": "john@acme.com"})
    assert is_valid
    assert len(errors) == 0


def test_lead_crud():
    """Test lead creation, retrieval, filtering, update, and deletion."""
    new_lead = create_lead({
        "company_name": "UnitTest Corp",
        "contact_name": "Test Contact",
        "email": "test@unittest.com",
        "industry": "SaaS",
        "deal_value": 2500000.0
    })
    assert new_lead["id"] is not None
    assert new_lead["company_name"] == "UnitTest Corp"

    # Get single
    fetched = get_lead_by_id(new_lead["id"])
    assert fetched["company_name"] == "UnitTest Corp"
    assert fetched["qualification"] is not None

    # Filter search
    search_res = get_leads(search_query="UnitTest")
    assert len(search_res) == 1
    assert search_res[0]["company_name"] == "UnitTest Corp"

    # Update
    updated = update_lead(new_lead["id"], {"deal_value": 3500000.0})
    assert updated["deal_value"] == 3500000.0

    # Delete
    deleted = delete_lead(new_lead["id"])
    assert deleted
    assert get_lead_by_id(new_lead["id"]) is None


def test_qualification_service():
    """Test BANT calculation and priority tier determination."""
    score = calculate_bant_score(budget=True, authority=True, need=True, timeline=True)
    assert score == 100.0
    assert determine_priority_tier(score) == "Priority A"

    score_low = calculate_bant_score(budget=False, authority=False, need=True, timeline=False)
    assert score_low == 25.0
    assert determine_priority_tier(score_low) == "Priority C"

    # Update qualification for an existing lead
    leads = get_leads()
    lead_id = leads[0]["id"]
    qual_res = update_qualification(
        lead_id=lead_id,
        budget_confirmed=True,
        authority_confirmed=True,
        need_confirmed=True,
        timeline_confirmed=True,
        qualification_notes="Verified via CFO call"
    )
    assert qual_res["bant_score"] == 100.0
    assert qual_res["priority"] == "Priority A"


def test_pipeline_service():
    """Test stage transition and Kanban data rendering."""
    leads = get_leads()
    lead_id = leads[0]["id"]

    moved = move_pipeline_stage(
        lead_id=lead_id,
        new_stage="Proposal",
        next_action="Review pricing options",
        deal_value=5000000.0
    )
    assert moved["new_stage"] == "Proposal"
    assert moved["probability"] == 0.70

    kanban = get_pipeline_kanban_data()
    assert "Proposal" in kanban
    assert any(card["id"] == lead_id for card in kanban["Proposal"])


def test_activity_and_analytics_services():
    """Test activity logging and executive KPI query aggregation."""
    leads = get_leads()
    lead_id = leads[0]["id"]

    act = log_activity(lead_id, "Call", outcome="Connected", notes="Initial discovery call.")
    assert act["id"] is not None

    note = add_note(lead_id, "Special request for SOC2 compliance report.")
    assert note["id"] is not None

    kpis = get_executive_kpis()
    assert kpis["total_accounts"] >= 28
    assert kpis["pipeline_value"] > 0

    priority_list = get_priority_accounts_summary(limit=5)
    assert len(priority_list) > 0
