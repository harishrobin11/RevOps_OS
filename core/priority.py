import config


def calculate_engagement_score(
    activities_count: int = 0,
    last_contacted_days_ago: int = None,
    stage: str = "Identified",
    outreach_responded: bool = False
) -> float:
    """
    Calculate 0-100 engagement score based on sales activities, recency, and stage progression.
    """
    score = 0.0

    # Activity volume (Max 30 pts)
    if activities_count >= 5:
        score += 30.0
    elif activities_count >= 3:
        score += 20.0
    elif activities_count >= 1:
        score += 10.0

    # Recency (Max 30 pts)
    if last_contacted_days_ago is not None:
        if last_contacted_days_ago <= 3:
            score += 30.0
        elif last_contacted_days_ago <= 7:
            score += 20.0
        elif last_contacted_days_ago <= 14:
            score += 10.0
        elif last_contacted_days_ago <= 30:
            score += 5.0

    # Stage Progression (Max 25 pts)
    high_engagement_stages = ["Engaged", "Qualified", "Discovery Booked", "Proposal", "Negotiation", "Won"]
    medium_engagement_stages = ["Contacted"]

    if stage in high_engagement_stages:
        score += 25.0
    elif stage in medium_engagement_stages:
        score += 15.0

    # Outreach Response (Max 15 pts)
    if outreach_responded:
        score += 15.0

    return min(score, 100.0)


def calculate_combined_priority_score(
    bant_score: float,
    icp_score: float,
    activities_count: int = 0,
    last_contacted_days_ago: int = None,
    stage: str = "Identified",
    outreach_responded: bool = False
) -> tuple[float, str, dict]:
    """
    Calculate Combined Lead Priority Score based on blueprint section 9:
    Overall Score = (BANT × 0.55) + (ICP × 0.30) + (Engagement × 0.15)

    Returns (combined_score, priority_tier, score_components_dict).
    """
    b_score = float(bant_score or 0.0)
    i_score = float(icp_score or 0.0)
    e_score = calculate_engagement_score(activities_count, last_contacted_days_ago, stage, outreach_responded)

    combined_score = (b_score * 0.55) + (i_score * 0.30) + (e_score * 0.15)

    # Classify Priority Tier
    if combined_score >= config.PRIORITY_CRITICAL:
        tier = "Critical"
    elif combined_score >= config.PRIORITY_HIGH:
        tier = "High"
    elif combined_score >= config.PRIORITY_MEDIUM:
        tier = "Medium"
    else:
        tier = "Low"

    components = {
        "bant_contribution": b_score * 0.55,
        "icp_contribution": i_score * 0.30,
        "engagement_contribution": e_score * 0.15,
        "raw_bant_score": b_score,
        "raw_icp_score": i_score,
        "raw_engagement_score": e_score
    }

    return (combined_score, tier, components)
