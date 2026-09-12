from core.cadence import get_cadence_steps, get_cadence_step_by_day
from core.templates import (
    generate_cold_call_script,
    generate_email,
    generate_linkedin_message,
    get_objection_library
)


def test_cadence_schedule():
    """Test cadence steps schedule."""
    steps = get_cadence_steps()
    assert len(steps) == 4
    days = [s["day"] for s in steps]
    assert days == [1, 3, 6, 9]

    step3 = get_cadence_step_by_day(3)
    assert step3["channels"] == ["Email"]


def test_script_and_template_generation():
    """Test script generation for Cold Calls, Emails, and LinkedIn."""
    dummy_lead = {
        "company_name": "VertexCloud Technologies",
        "contact_name": "Rajesh Varma",
        "title": "Chief Operating Officer",
        "industry": "SaaS",
        "location": "Outer Ring Road",
        "notes": "Scaling engineer team"
    }

    # Cold Call
    call_obj = generate_cold_call_script(dummy_lead)
    assert "Rajesh Varma" in call_obj["opening"]
    assert "SaaS" in call_obj["reason"]
    assert "full_script" in call_obj

    # Email Consultative
    email_cons = generate_email(dummy_lead, tone="Consultative", cadence_step="Day 3")
    assert "Rajesh" in email_cons["body"]
    assert "VertexCloud" in email_cons["body"]

    # Email Professional
    email_prof = generate_email(dummy_lead, tone="Professional", cadence_step="Day 3")
    assert "Dear Rajesh Varma" in email_prof["body"]

    # Email Concise
    email_conc = generate_email(dummy_lead, tone="Concise", cadence_step="Day 3")
    assert len(email_conc["body"]) < len(email_prof["body"])

    # LinkedIn (must be <= 300 chars)
    li_msg = generate_linkedin_message(dummy_lead)
    assert len(li_msg) <= 300
    assert "Rajesh" in li_msg


def test_objection_library():
    """Test objection handling battlecards lookup."""
    obj_lib = get_objection_library()
    assert isinstance(obj_lib, dict)
    assert "We already have a solution." in obj_lib
    assert "Not interested." in obj_lib

    card = obj_lib["We already have a solution."]
    assert "CRM" in card["response"]
    assert "follow_up_question" in card
