import config


def calculate_bant_score(budget: bool, authority: bool, need: bool, timeline: bool) -> float:
    """
    Calculate BANT score based on blueprint rules:
    - Budget confirmed: 25 pts
    - Authority confirmed: 35 pts
    - Need confirmed: 25 pts
    - Timeline confirmed: 15 pts
    Total: 100 pts
    """
    score = 0.0
    if budget:
        score += config.BANT_WEIGHTS["budget"]
    if authority:
        score += config.BANT_WEIGHTS["authority"]
    if need:
        score += config.BANT_WEIGHTS["need"]
    if timeline:
        score += config.BANT_WEIGHTS["timeline"]
    return score


def classify_bant_priority(bant_score: float) -> str:
    """
    Classify BANT score into priority tiers:
    - 85-100: Priority A / Hot Lead
    - 60-84: Priority B / Nurture
    - 0-59: Priority C / Low Probability
    """
    score = float(bant_score)
    if score >= 85.0:
        return "Priority A"
    elif score >= 60.0:
        return "Priority B"
    else:
        return "Priority C"


def explain_bant_qualification(budget: bool, authority: bool, need: bool, timeline: bool) -> dict:
    """
    Generate qualification explanation and sales rationale summary.
    """
    score = calculate_bant_score(budget, authority, need, timeline)
    priority = classify_bant_priority(score)

    missing = []
    if not budget:
        missing.append("Budget not confirmed")
    if not authority:
        missing.append("Decision maker authority unverified")
    if not need:
        missing.append("Business pain point/need unconfirmed")
    if not timeline:
        missing.append("Timeline > 90 days or undefined")

    if score >= 85.0:
        rationale = "Hot opportunity. Budget, decision maker authority, and clear pain points confirmed."
    elif score >= 60.0:
        rationale = f"Nurture opportunity. Key qualification gap(s): {', '.join(missing)}."
    else:
        rationale = f"Low probability opportunity. Requires further qualification. Missing: {', '.join(missing)}."

    return {
        "score": score,
        "priority": priority,
        "budget_confirmed": budget,
        "authority_confirmed": authority,
        "need_confirmed": need,
        "timeline_confirmed": timeline,
        "missing_criteria": missing,
        "rationale": rationale
    }
