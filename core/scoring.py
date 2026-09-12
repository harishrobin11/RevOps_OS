import config


def classify_icp_fit(icp_score: float) -> str:
    """
    Classify ICP score into a human-readable fit category.
    - 85–100: Excellent Fit
    - 70–84: Strong Fit
    - 50–69: Moderate Fit
    - Below 50: Weak Fit
    """
    score = float(icp_score)
    if score >= 85.0:
        return "Excellent Fit"
    elif score >= 70.0:
        return "Strong Fit"
    elif score >= 50.0:
        return "Moderate Fit"
    else:
        return "Weak Fit"


def calculate_icp_score(
    industry: str,
    employee_count: int,
    location: str,
    title: str,
    pain_points: str = None,
    growth_signal: bool = False
) -> tuple[float, str, dict]:
    """
    Calculate 100-Point Weighted ICP Score based on blueprint rules:
    - Industry Fit: 20 pts
    - Company Size Fit (50-300 emp): 15 pts
    - Territory Fit (Bangalore Hubs): 15 pts
    - Decision Maker Fit (COO, VP Ops, Head of Ops, Founder): 20 pts
    - Pain Point Fit (Manual workflows, scaling bottlenecks): 20 pts
    - Growth Signal: 10 pts

    Returns (total_score, fit_label, score_breakdown_dict).
    """
    breakdown = {}

    # 1. Industry Fit (Max 20)
    ind_str = str(industry or "").strip()
    if ind_str in config.TARGET_INDUSTRIES:
        breakdown["industry_fit"] = 20.0
    elif any(t.lower() in ind_str.lower() for t in config.TARGET_INDUSTRIES):
        breakdown["industry_fit"] = 15.0
    elif ind_str:
        breakdown["industry_fit"] = 10.0
    else:
        breakdown["industry_fit"] = 5.0

    # 2. Company Size Fit (Max 15)
    try:
        emp = int(employee_count or 0)
        if 50 <= emp <= 300:
            breakdown["company_size_fit"] = 15.0
        elif 30 <= emp < 50 or 301 <= emp <= 500:
            breakdown["company_size_fit"] = 10.0
        elif emp > 0:
            breakdown["company_size_fit"] = 5.0
        else:
            breakdown["company_size_fit"] = 2.0
    except (ValueError, TypeError):
        breakdown["company_size_fit"] = 0.0

    # 3. Territory Fit (Max 15)
    loc_str = str(location or "").strip()
    if loc_str in config.TARGET_TERRITORIES:
        breakdown["territory_fit"] = 15.0
    elif any(t.lower() in loc_str.lower() for t in config.TARGET_TERRITORIES) or "bangalore" in loc_str.lower() or "bengaluru" in loc_str.lower():
        breakdown["territory_fit"] = 12.0
    elif loc_str:
        breakdown["territory_fit"] = 8.0
    else:
        breakdown["territory_fit"] = 5.0

    # 4. Decision Maker Fit (Max 20)
    title_str = str(title or "").strip().lower()
    decision_maker_keywords = [
        "coo", "chief operating officer", "vp business operations", "vice president of operations",
        "head of operations", "head of delivery", "operations director", "founder", "ceo",
        "chief executive officer", "business unit head", "vp operations"
    ]

    if any(role in title_str for role in decision_maker_keywords):
        breakdown["decision_maker_fit"] = 20.0
    elif any(kw in title_str for kw in ["chief", "vp", "vice president", "head", "director", "founder", "ceo", "coo", "cto"]):
        breakdown["decision_maker_fit"] = 15.0
    elif any(kw in title_str for kw in ["manager", "lead"]):
        breakdown["decision_maker_fit"] = 10.0
    else:
        breakdown["decision_maker_fit"] = 5.0

    # 5. Pain Point Fit (Max 20)
    pp_str = str(pain_points or "").strip().lower()
    high_value_keywords = [
        "manual", "workflow", "bottleneck", "leakage", "scaling", "visibility",
        "cadence", "crm", "tracking", "reporting", "inefficient", "fragmented"
    ]
    if pp_str:
        matches = sum(1 for kw in high_value_keywords if kw in pp_str)
        if matches >= 2:
            breakdown["pain_point_fit"] = 20.0
        elif matches == 1:
            breakdown["pain_point_fit"] = 15.0
        else:
            breakdown["pain_point_fit"] = 10.0
    else:
        breakdown["pain_point_fit"] = 5.0

    # 6. Growth Signal (Max 10)
    breakdown["growth_signal"] = 10.0 if growth_signal else 0.0

    # Total ICP Score
    total_score = sum(breakdown.values())
    fit_label = classify_icp_fit(total_score)

    return (total_score, fit_label, breakdown)
