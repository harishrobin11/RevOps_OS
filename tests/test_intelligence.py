from datetime import datetime, timedelta, timezone
from core.scoring import calculate_icp_score, classify_icp_fit
from core.qualification import calculate_bant_score, classify_bant_priority, explain_bant_qualification
from core.priority import calculate_combined_priority_score, calculate_engagement_score
from core.health import calculate_deal_health


def test_icp_scoring_engine():
    """
    Test 100-Point ICP scoring calculations and fit tier classification.
    """
    # Ideal Bangalore B2B SaaS account profile
    score, fit_label, breakdown = calculate_icp_score(
        industry="SaaS",
        employee_count=150,
        location="Outer Ring Road",
        title="Chief Operating Officer",
        pain_points="Struggling with manual workflows and fragmented CRM tracking.",
        growth_signal=True
    )
    assert score == 100.0
    assert fit_label == "Excellent Fit"
    assert breakdown["industry_fit"] == 20.0
    assert breakdown["company_size_fit"] == 15.0
    assert breakdown["territory_fit"] == 15.0
    assert breakdown["decision_maker_fit"] == 20.0
    assert breakdown["pain_point_fit"] == 20.0
    assert breakdown["growth_signal"] == 10.0

    # Non-target / weak fit profile
    score_weak, fit_label_weak, _ = calculate_icp_score(
        industry="Retail",
        employee_count=5,
        location="Delhi",
        title="Intern",
        pain_points="None",
        growth_signal=False
    )
    assert score_weak < 50.0
    assert fit_label_weak == "Weak Fit"


def test_bant_qualification_engine():
    """
    Test BANT scoring weights, priority tier classification, and rationale explanations.
    """
    # All 4 confirmed (100 pts)
    score_full = calculate_bant_score(budget=True, authority=True, need=True, timeline=True)
    assert score_full == 100.0
    assert classify_bant_priority(score_full) == "Priority A"

    # Authority + Need confirmed (60 pts)
    score_med = calculate_bant_score(budget=False, authority=True, need=True, timeline=False)
    assert score_med == 60.0
    assert classify_bant_priority(score_med) == "Priority B"

    # Need only (25 pts)
    score_low = calculate_bant_score(budget=False, authority=False, need=True, timeline=False)
    assert score_low == 25.0
    assert classify_bant_priority(score_low) == "Priority C"

    # Explanation generator (Budget False, Authority + Need True = 60 pts -> Priority B)
    exp = explain_bant_qualification(budget=False, authority=True, need=True, timeline=False)
    assert exp["score"] == 60.0
    assert exp["priority"] == "Priority B"
    assert "Budget" in exp["missing_criteria"][0]


def test_combined_lead_priority_engine():
    """
    Test Combined Lead Priority formula: (BANT * 0.55) + (ICP * 0.30) + (Engagement * 0.15).
    """
    # High BANT (90), High ICP (90), High Engagement (80)
    score, tier, components = calculate_combined_priority_score(
        bant_score=90.0,
        icp_score=90.0,
        activities_count=6,
        last_contacted_days_ago=2,
        stage="Proposal",
        outreach_responded=True
    )
    # (90 * 0.55 = 49.5) + (90 * 0.30 = 27.0) + (100 * 0.15 = 15.0) = 91.5
    assert score >= 85.0
    assert tier == "Critical"
    assert components["raw_bant_score"] == 90.0

    # Low BANT (30), Low ICP (40), Low Engagement (10)
    score_low, tier_low, _ = calculate_combined_priority_score(
        bant_score=30.0,
        icp_score=40.0,
        activities_count=0,
        last_contacted_days_ago=45,
        stage="Identified"
    )
    assert score_low < 50.0
    assert tier_low == "Low"


def test_deal_health_engine():
    """
    Test Deal Health state calculations (Healthy, At Risk, Stalled, Lost).
    """
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    # Won stage -> Healthy
    assert calculate_deal_health("Won") == "Healthy"

    # Lost stage -> Lost
    assert calculate_deal_health("Lost") == "Lost"

    # Overdue follow-up by 7 days -> Stalled
    stalled_health = calculate_deal_health(
        stage="Proposal",
        next_follow_up=now - timedelta(days=7),
        last_contacted_days_ago=8
    )
    assert stalled_health == "Stalled"

    # Overdue follow-up by 2 days -> At Risk
    at_risk_health = calculate_deal_health(
        stage="Engaged",
        next_follow_up=now - timedelta(days=2),
        last_contacted_days_ago=5
    )
    assert at_risk_health == "At Risk"

    # Upcoming follow-up -> Healthy
    healthy_res = calculate_deal_health(
        stage="Qualified",
        next_follow_up=now + timedelta(days=3),
        last_contacted_days_ago=2
    )
    assert healthy_res == "Healthy"
