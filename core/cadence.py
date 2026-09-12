def get_cadence_steps() -> list[dict]:
    """
    Get default 9-day B2B outbound outreach cadence steps.
    """
    return [
        {
            "day": 1,
            "step_name": "Day 1: Multi-touch Cold Call & LinkedIn",
            "channels": ["Cold Call", "LinkedIn"],
            "objective": "Establish direct contact with decision maker and send LinkedIn connection note.",
            "cta": "Request 10-minute exploratory conversation.",
            "next_step": "Day 3 Value Email"
        },
        {
            "day": 3,
            "step_name": "Day 3: Value-Driven Email",
            "channels": ["Email"],
            "objective": "Share industry-specific operational case study or process improvement insight.",
            "cta": "Ask if handling workflow bottlenecks is a current operational focus.",
            "next_step": "Day 6 Follow-up Call"
        },
        {
            "day": 6,
            "step_name": "Day 6: Follow-up Call & Voice Message",
            "channels": ["Cold Call"],
            "objective": "Reference previous email and offer brief operational benchmark audit.",
            "cta": "Schedule 15-minute discovery call.",
            "next_step": "Day 9 Breakup Email"
        },
        {
            "day": 9,
            "step_name": "Day 9: Permission-to-Close File (Breakup Email)",
            "channels": ["Email"],
            "objective": "Politely offer permission to close file if timing is not right.",
            "cta": "Ask if timing is bad or if topic should be revisited next quarter.",
            "next_step": "Nurture Pipeline"
        }
    ]


def get_cadence_step_by_day(day_number: int) -> dict:
    """
    Fetch a specific cadence step by day number.
    """
    steps = get_cadence_steps()
    for s in steps:
        if s["day"] == day_number:
            return s
    return steps[-1]
