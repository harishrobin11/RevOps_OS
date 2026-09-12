import config


def generate_cold_call_script(lead_data: dict) -> dict:
    """
    Generate structured, personalized Cold Call Script based on blueprint section 14.
    """
    company = lead_data.get("company_name", "your company")
    contact = lead_data.get("contact_name", "there")
    title = lead_data.get("title", "Operations Leader")
    industry = lead_data.get("industry", "B2B Tech")
    location = lead_data.get("location", "Bangalore")
    pain_points = lead_data.get("notes", "scaling operational workflows and lead follow-up visibility")

    opening = f"Hi {contact}, this is Harish calling from Avgova Solutions."
    reason = f"I'm reaching out specifically because we work with growing {industry} leaders in {location} who are scaling their business operations."
    problem = f"We notice many companies at {company}'s stage encounter challenges with {pain_points}."
    discovery_question = f"I'm curious — how is your team currently tracking lead qualification and follow-up deadlines across your pipeline?"
    value_prop = f"We help B2B operations teams automate lead scoring, structure outbound cadences, and eliminate deal leakage."
    qualification_question = f"If there were an opportunity to gain complete visibility into stalled deals and shorten your sales cycle by 30%, would that be relevant for your team this quarter?"
    cta = "If it makes sense, I'd like to suggest a 10-minute exploratory conversation next Tuesday morning. Would 10:30 AM work for you?"

    full_script = f"""{opening}

{reason}

{problem}

{discovery_question}

[If Responded Positive]:
{value_prop}

{qualification_question}

[CTA]:
{cta}"""

    return {
        "opening": opening,
        "reason": reason,
        "problem": problem,
        "discovery_question": discovery_question,
        "value_prop": value_prop,
        "qualification_question": qualification_question,
        "cta": cta,
        "full_script": full_script
    }


def generate_email(lead_data: dict, tone: str = "Consultative", cadence_step: str = "Day 3") -> dict:
    """
    Generate personalized email outreach with support for Professional, Consultative, and Concise tones.
    """
    company = lead_data.get("company_name", "your organization")
    contact = lead_data.get("contact_name", "there")
    title = lead_data.get("title", "Team")
    industry = lead_data.get("industry", "B2B Tech")
    location = lead_data.get("location", "Bangalore")

    if "breakup" in cadence_step.lower() or "day 9" in cadence_step.lower():
        subject = f"Permission to close file — {company}"
        body = f"""Hi {contact},

I've reached out a few times regarding RevOps pipeline management for {company}, but I haven't heard back. I assume improving lead qualification and follow-up tracking isn't a priority for your team right now.

With your permission, I'll close your file for now so I don't crowd your inbox.

If operational workflow automation becomes a priority in the future, please feel free to reach out.

Best regards,

Harish Robin H.
Business Development | Avgova Solutions
harish@avgova-demo.com | +91 98450 00000"""
        return {"subject": subject, "body": body}

    if tone == "Concise":
        subject = f"Streamlining operations at {company}"
        body = f"""Hi {contact},

I noticed {company}'s growth in the {industry} sector across {location}.

We help operations leaders structure lead qualification, track follow-up deadlines, and prevent sales pipeline leakage.

Would you be open to a quick 10-minute chat next week to see how this compares to your current workflow?

Best,

Harish Robin H.
Avgova Solutions"""

    elif tone == "Professional":
        subject = f"Revenue Operations Infrastructure for {company}"
        body = f"""Dear {contact},

I hope this email finds you well.

As {title} at {company}, managing operational efficiency and pipeline accountability is critical for scaling in the {industry} market.

Avgova Solutions provides a unified B2B Revenue Operations platform that enables teams to:
1. Standardize ICP and BANT lead qualification.
2. Automate multichannel outbound cadences.
3. Gain real-time visibility into deal health and funnel leakage.

I would welcome the opportunity to introduce our platform to {company}. Are you available for a brief introductory call this Thursday at 11:00 AM?

Sincerely,

Harish Robin H.
Business Development Associate
Avgova Solutions"""

    else:  # Consultative (Default)
        subject = f"Improving lead qualification efficiency for {company}"
        body = f"""Hi {contact},

I hope your week is going well.

I was researching fast-growing {industry} companies in {location} and noticed {company}'s recent scaling momentum.

In working with B2B operations leaders, we frequently find that as teams scale from 50 to 300 employees, sales follow-up deadlines get missed and qualified leads stall in the middle of the funnel.

We built RevOps OS to solve this exact problem by structuring BANT qualification, scoring accounts objectively, and surfacing stalled deals before they drop out.

Are you open to a brief 15-minute conversation to explore how this approach could benefit {company}?

Best regards,

Harish Robin H.
Business Development Associate | Avgova Solutions
harish@avgova-demo.com"""

    return {"subject": subject, "body": body}


def generate_linkedin_message(lead_data: dict) -> str:
    """
    Generate short LinkedIn connection note (strictly <= 300 characters).
    """
    contact = lead_data.get("contact_name", "").split()[0] if lead_data.get("contact_name") else "there"
    company = lead_data.get("company_name", "your company")
    industry = lead_data.get("industry", "tech")

    note = f"Hi {contact}, noticed your work at {company} in the {industry} space. We help ops leaders automate lead qualification & follow-up cadences. Would love to connect!"

    # Truncate if exceeds 300 chars
    if len(note) > 300:
        note = note[:297] + "..."

    return note


def get_objection_library() -> dict:
    """
    Return objection battlecards based on blueprint section 17.
    """
    return {
        "We already have a solution.": {
            "objection": "We already have a solution / CRM in place.",
            "response": "That makes complete sense — most established companies we talk to already use a CRM like HubSpot or Salesforce. We don't replace your CRM; we sit on top of it as a lightweight RevOps qualification and cadence engine to ensure reps execute follow-ups on time.",
            "follow_up_question": "Curious — how are you currently ensuring that high-priority leads don't sit uncontacted for more than 48 hours in your current setup?",
            "next_action": "Offer a 10-minute comparison audit against their existing CRM workflow."
        },
        "Not interested.": {
            "objection": "Not interested.",
            "response": "I completely respect that, [Name]. Just so I don't reach out unnecessarily in the future — is that because process automation isn't a priority right now, or are you satisfied with your current conversion rates?",
            "follow_up_question": "Would it be alright if I sent a 1-page benchmark report for {industry} companies to keep on file?",
            "next_action": "Move lead to Nurture stage and set follow-up in 90 days."
        },
        "Send me an email.": {
            "objection": "Send me an email.",
            "response": "I'd be glad to send an email over! To make sure I include only relevant information for {company}, what is the #1 operational bottleneck your team is focused on solving this quarter?",
            "follow_up_question": "If I send a tailored 1-pager today, could we reconnect for 5 minutes on Thursday to get your feedback?",
            "next_action": "Send Day 3 Value Email immediately and schedule follow-up call on Day 6."
        },
        "We don't have budget.": {
            "objection": "We don't have budget.",
            "response": "I understand budget constraints are top of mind. Many of our clients actually started evaluating us before their next budget cycle so they could quantify potential ROI before requesting funds.",
            "follow_up_question": "When does your team typically review operational budget allocations for the upcoming fiscal quarter?",
            "next_action": "Log budget timeline in BANT qualification and set reminder for pre-budget review."
        },
        "Now isn't a good time.": {
            "objection": "Now isn't a good time.",
            "response": "I completely understand — timing is everything. I don't want to interrupt your current priorities.",
            "follow_up_question": "Would next month or early next quarter be a better time for a brief 10-minute check-in?",
            "next_action": "Update next follow-up date to 30 days out and log note."
        },
        "We are evaluating internally.": {
            "objection": "We are evaluating internally.",
            "response": "That's great to hear that process improvement is an active internal initiative for your team.",
            "follow_up_question": "What key criteria or metrics is your leadership team using to evaluate potential solutions?",
            "next_action": "Offer custom ROI calculator or feature comparison matrix."
        },
        "We already use another provider.": {
            "objection": "We already use another provider.",
            "response": "Understood! They are a reputable provider. Many of our clients previously used them but switched because they needed faster lead scoring and structured outbound cadences tailored for Bangalore B2B markets.",
            "follow_up_question": "How satisfied are you with their follow-up deadline tracking and deal health visibility?",
            "next_action": "Send competitor comparison battlecard."
        }
    }
