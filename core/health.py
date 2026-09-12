from datetime import datetime, timezone


def calculate_deal_health(
    stage: str,
    next_follow_up: datetime = None,
    last_contacted_days_ago: int = None,
    bant_score: float = 0.0,
    stage_duration_days: int = 0
) -> str:
    """
    Calculate deal health status based on blueprint section 11:
    - Healthy: On track, active touchpoints, upcoming follow-up.
    - At Risk: Minor delay, overdue follow-up (< 5 days), or no contact for 10-14 days.
    - Stalled: Overdue follow-up (>= 5 days) or inactive in stage for > 30 days.
    - Lost: Formally closed as Lost.
    """
    if stage == "Won":
        return "Healthy"

    if stage == "Lost":
        return "Lost"

    now = datetime.now(timezone.utc).replace(tzinfo=None)

    # Normalize follow-up date
    is_overdue = False
    days_overdue = 0
    if next_follow_up is not None:
        if isinstance(next_follow_up, datetime) and next_follow_up.tzinfo is not None:
            next_follow_up = next_follow_up.replace(tzinfo=None)

        if next_follow_up < now:
            is_overdue = True
            days_overdue = (now - next_follow_up).days

    # Stalled Criteria
    if days_overdue >= 5 or stage_duration_days > 30:
        return "Stalled"

    # At Risk Criteria
    if is_overdue or (last_contacted_days_ago is not None and last_contacted_days_ago > 10) or (bant_score < 50.0 and stage in ["Proposal", "Negotiation"]):
        return "At Risk"

    return "Healthy"
