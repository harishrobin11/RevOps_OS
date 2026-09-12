from services.lead_service import get_leads, get_lead_by_id
from services.qualification_service import update_qualification


def test_lead_registry_data_fetch():
    """Test retrieving leads for registry view with filters."""
    leads = get_leads()
    assert len(leads) >= 28

    filtered = get_leads(industry="SaaS")
    assert len(filtered) > 0
    assert all(l["industry"] == "SaaS" for l in filtered)

    filtered_priority = get_leads(priority="Priority A")
    assert len(filtered_priority) == 6


def test_lead_detail_view_data():
    """Test lead detail data fetching and qualification evaluation."""
    leads = get_leads()
    first_id = leads[0]["id"]

    detail = get_lead_by_id(first_id)
    assert detail is not None
    assert "company_name" in detail
    assert "qualification" in detail

    # Update qualification via service
    updated = update_qualification(
        lead_id=first_id,
        budget_confirmed=True,
        authority_confirmed=True,
        need_confirmed=True,
        timeline_confirmed=True,
        qualification_notes="Test update"
    )
    assert updated["bant_score"] == 100.0
    assert updated["priority"] == "Priority A"
