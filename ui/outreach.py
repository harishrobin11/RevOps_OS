import streamlit as st
import pandas as pd

import config
from services.lead_service import get_leads, get_lead_by_id
from services.outreach_service import log_outreach, get_outreach_history_for_lead
from core.cadence import get_cadence_steps
from core.templates import (
    generate_cold_call_script,
    generate_email,
    generate_linkedin_message,
    get_objection_library
)
from ui.components import render_header, render_empty_state


def render_outreach_page():
    """
    Render Multichannel Outreach Engine & Script Generator View.
    """
    render_header(
        title="Outreach Engine & Script Workspace",
        subtitle=f"Multichannel prospecting scripts, outbound cadences, and objection handling for {config.COMPANY_NAME}.",
        badge="Outreach Active"
    )

    all_leads = get_leads()

    if not all_leads:
        render_empty_state("No Target Accounts", "Add leads to the registry to generate personalized outreach scripts.")
        return

    # 1. ACCOUNT & OUTREACH CONTROL TOOLBAR
    st.markdown('<div class="section-card"><div class="section-card-title"><span>⚙️ Outreach Generator Controls</span></div>', unsafe_allow_html=True)

    lead_map = {f"{l['company_name']} — {l['contact_name']} ({l['priority']})": l["id"] for l in all_leads}

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        sel_label = st.selectbox("Target Account*", list(lead_map.keys()), index=0)
        selected_lead_id = lead_map[sel_label]
        selected_lead = get_lead_by_id(selected_lead_id)

    with col2:
        channel = st.selectbox("Outreach Channel*", ["Cold Call", "Email", "LinkedIn"], index=1)

    with col3:
        cadence_step = st.selectbox("Cadence Step", ["Day 1", "Day 3 (Value)", "Day 6 (Follow-up)", "Day 9 (Breakup)"], index=1)

    with col4:
        tone = st.selectbox("Message Tone", ["Consultative", "Professional", "Concise"], index=0) if channel == "Email" else "N/A"

    st.markdown('</div>', unsafe_allow_html=True)

    # 2. GENERATED SCRIPT DISPLAY & ACTIONS
    st.markdown('<div class="section-card"><div class="section-card-title"><span>📜 Generated Script / Message Editor</span></div>', unsafe_allow_html=True)

    if channel == "Cold Call":
        script_obj = generate_cold_call_script(selected_lead)
        st.markdown("<h5 style='color: #F8FAFC; margin-bottom: 8px;'>📞 Cold Call Script & Discovery Prompt</h5>", unsafe_allow_html=True)
        st.code(script_obj["full_script"], language="markdown")

        with st.form("log_call_outreach_form"):
            outcome_input = st.text_input("Call Outcome Notes", placeholder="e.g. Spoke with COO, requested follow-up email")
            submit_log = st.form_submit_button("🚀 Log Cold Call Activity", type="primary", use_container_width=True)
            if submit_log:
                log_outreach(
                    lead_id=selected_lead_id,
                    channel="Cold Call",
                    cadence_step=cadence_step,
                    subject="Cold Call Prospecting",
                    content=script_obj["full_script"],
                    status="Sent"
                )
                st.success("✅ Cold Call activity logged to account timeline!")
                st.rerun()

    elif channel == "Email":
        email_obj = generate_email(selected_lead, tone=tone, cadence_step=cadence_step)
        st.markdown("<h5 style='color: #F8FAFC; margin-bottom: 8px;'>✉️ Email Template Preview & Editor</h5>", unsafe_allow_html=True)

        with st.form("send_email_outreach_form"):
            subj_val = st.text_input("Email Subject Line", value=email_obj["subject"])
            body_val = st.text_area("Email Body", value=email_obj["body"], height=250)

            submit_log = st.form_submit_button("🚀 Log Email Outreach & Record Activity", type="primary", use_container_width=True)
            if submit_log:
                log_outreach(
                    lead_id=selected_lead_id,
                    channel="Email",
                    cadence_step=cadence_step,
                    subject=subj_val,
                    content=body_val,
                    status="Sent"
                )
                st.success("✅ Email outreach logged to account timeline!")
                st.rerun()

    else:  # LinkedIn
        li_msg = generate_linkedin_message(selected_lead)
        st.markdown("<h5 style='color: #F8FAFC; margin-bottom: 8px;'>🔗 LinkedIn Connection Note</h5>", unsafe_allow_html=True)
        char_count = len(li_msg)
        st.caption(f"Character Count: **{char_count} / 300** characters (LinkedIn Limit: 300)")

        with st.form("log_li_outreach_form"):
            li_val = st.text_area("Connection Note", value=li_msg, height=120)
            submit_log = st.form_submit_button("🚀 Log LinkedIn Connection Note", type="primary", use_container_width=True)
            if submit_log:
                log_outreach(
                    lead_id=selected_lead_id,
                    channel="LinkedIn",
                    cadence_step=cadence_step,
                    subject="LinkedIn Connection",
                    content=li_val,
                    status="Sent"
                )
                st.success("✅ LinkedIn outreach logged!")
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # 3. 9-DAY OUTBOUND CADENCE TIMELINE
    st.markdown('<div class="section-card"><div class="section-card-title"><span>📅 9-Day Outbound Cadence Schedule</span></div>', unsafe_allow_html=True)
    cadence_steps = get_cadence_steps()

    c_cols = st.columns(4)
    for idx, s in enumerate(cadence_steps):
        with c_cols[idx]:
            st.markdown(f"""
                <div style="background-color: #0F172A; border: 1px solid #1E293B; border-radius: 8px; padding: 14px; box-shadow: 0 2px 6px rgba(0,0,0,0.2);">
                    <div style="font-weight: 700; color: #38BDF8; font-size: 13px; margin-bottom: 4px;">{s['step_name']}</div>
                    <div style="font-size: 11px; color: #94A3B8; margin-bottom: 8px;">{s['objective']}</div>
                    <div style="font-size: 10px; color: #10B981; font-weight: 600;">CTA: {s['cta']}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # 4. OBJECTION HANDLING LIBRARY
    st.markdown('<div class="section-card"><div class="section-card-title"><span>🛡️ Objection Handling Battlecards</span></div>', unsafe_allow_html=True)
    obj_lib = get_objection_library()

    selected_obj_key = st.selectbox("Select Prospect Objection:", list(obj_lib.keys()), index=0)
    bcard = obj_lib[selected_obj_key]

    obj_col1, obj_col2 = st.columns(2)
    with obj_col1:
        st.markdown("##### Recommended Response Strategy")
        st.info(bcard["response"].format(Name=selected_lead["contact_name"].split()[0], company=selected_lead["company_name"], industry=selected_lead["industry"]))

    with obj_col2:
        st.markdown("##### Follow-up Discovery Question")
        st.warning(bcard["follow_up_question"].format(company=selected_lead["company_name"], industry=selected_lead["industry"]))
        st.markdown(f"**Recommended Next Action:** `{bcard['next_action']}`")

    st.markdown('</div>', unsafe_allow_html=True)

    # 5. OUTREACH HISTORY TIMELINE FOR SELECTED ACCOUNT
    st.markdown(f'<div class="section-card"><div class="section-card-title"><span>📜 Outreach History for {selected_lead["company_name"]}</span></div>', unsafe_allow_html=True)
    history = get_outreach_history_for_lead(selected_lead_id)

    if history:
        h_data = [{
            "Sent At": o["sent_at"].strftime("%Y-%m-%d %H:%M") if o["sent_at"] else "Pending",
            "Channel": o["channel"],
            "Cadence Step": o["cadence_step"] or "N/A",
            "Subject": o["subject"] or "N/A",
            "Status": o["status"]
        } for o in history]
        st.dataframe(pd.DataFrame(h_data), use_container_width=True, hide_index=True)
    else:
        st.info("No outreach messages logged for this account yet.")
    st.markdown('</div>', unsafe_allow_html=True)
