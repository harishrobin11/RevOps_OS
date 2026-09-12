import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from core.database import Base
from core.models import Lead, Qualification, Activity, Outreach, Pipeline, Note
from data.seed_data import seed_database


@pytest.fixture(scope="function")
def test_db():
    """
    Provide an isolated in-memory SQLite database for unit testing.
    """
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_models_instantiation(test_db):
    """
    Test creating a lead with related models in SQLite.
    """
    lead = Lead(
        company_name="Test Enterprise Technologies",
        contact_name="Harish Test",
        title="COO",
        email="harish@test.com",
        phone="+91 99000 00000",
        industry="SaaS",
        location="Koramangala",
        employee_count=150,
        lead_source="Inbound Website",
        icp_score=90.0,
        priority="Priority A",
        pipeline_stage="Qualified",
        deal_value=5000000.0
    )
    test_db.add(lead)
    test_db.flush()

    assert lead.id is not None
    assert lead.company_name == "Test Enterprise Technologies"

    # Add qualification
    qual = Qualification(
        lead_id=lead.id,
        budget_confirmed=True,
        authority_confirmed=True,
        need_confirmed=True,
        timeline_confirmed=True,
        bant_score=100.0
    )
    test_db.add(qual)
    test_db.commit()

    saved_lead = test_db.query(Lead).filter_by(id=lead.id).first()
    assert saved_lead is not None
    assert len(saved_lead.qualifications) == 1
    assert saved_lead.qualifications[0].bant_score == 100.0


def test_seed_database(test_db):
    """
    Test that seeding inserts at least 25 records with valid relationships.
    """
    count = seed_database(test_db)
    assert count >= 25

    total_leads = test_db.query(Lead).count()
    assert total_leads >= 25

    priority_a_count = test_db.query(Lead).filter(Lead.priority == "Priority A").count()
    assert priority_a_count == 6

    # Check qualifications count match leads
    total_quals = test_db.query(Qualification).count()
    assert total_quals == total_leads
