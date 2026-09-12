from services.pipeline_service import get_pipeline_kanban_data, move_pipeline_stage
from services.lead_service import get_leads
import config


def test_pipeline_kanban_data_structure():
    """Test retrieving 10-stage Kanban data structure."""
    kanban = get_pipeline_kanban_data()
    assert isinstance(kanban, dict)
    for stage in config.PIPELINE_STAGES:
        assert stage in kanban


def test_pipeline_stage_transition():
    """Test moving a lead to a new stage."""
    leads = get_leads()
    first_lead = leads[0]

    res = move_pipeline_stage(
        lead_id=first_lead["id"],
        new_stage="Discovery Booked",
        next_action="Conduct discovery call with COO",
        deal_value=4000000.0
    )
    assert res["new_stage"] == "Discovery Booked"
    assert res["probability"] == 0.50
    assert res["deal_value"] == 4000000.0

    # Verify updated Kanban
    updated_kanban = get_pipeline_kanban_data()
    assert any(card["id"] == first_lead["id"] for card in updated_kanban["Discovery Booked"])
