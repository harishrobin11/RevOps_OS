import streamlit as st
import pandas as pd

import config
from services.lead_service import get_lead_by_id
from services.qualification_service import update_qualification
from core.qualification import explain_bant_qualification
from services.activity_service import log_activity, get_activities_for_lead, add_note, get_notes_for_lead
from services.pipeline_service import move_pipeline_stage
from ui.components import render_header, render_priority_badge, render_health_badge, render_empty_state
from ui.dashboard import format_currency


def render_lead_detail_page(lead_id: int):
    """
    Render 3-Column Executive CRM Account Detail View.
    """
    lead = get_lead_by_id(lead_id)

    if not lead:
        render_empty_state("Lead Not Found", f"No account record found for ID {lead_id}.")
        if st.button("🔙 Back to Lead Registry", type="primary"):
            st.session_state["selected_lead_id"] = None
            st.rerun()
        return

    # TOP NAVIGATION BAR
    top_col1, top_col2 = st.columns([4, 1])
    with top_col1:
        render_header(
            title=f"🏢 {lead['company_name']}",
            subtitle=f"{lead['industry']} | {lead['location']} | Account ID #{lead['id']}",
            badge=lead['priority']
        )
    with top_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔙 Back to Registry", type="secondary", use_container_width=True):
            st.session_state["selected_lead_id"] = None
            st.rerun()

    # 3-COLUMN CRM EXECUTIVE CARDS
    st.markdown('<div class="section-card"><div class="section-card-title"><span>📌 Executive Account Intelligence</span></div>', unsafe_allow_html=True)
    card_col1, card_col2, card_col3 = st.columns(3)

    with card_col1:
        st.markdown("<h5 style='color: #38BDF8; font-weight: 600; margin-bottom: 12px;'>🏢 Company Intelligence</h5>", unsafe_allow_html=True)
        st.markdown(f"**Industry:** `{lead['industry']}`")
        st.markdown(f"**Territory:** `{lead['location']}`")
        st.markdown(f"**Employee Count:** `{lead['employee_count']} employees`")
        st.markdown(f"**Website:** [{lead['website']}]({lead['website']})" if lead['website'] else "**Website:** N/A")
        st.markdown(f"**Lead Source:** `{lead['lead_source']}`")

        # ICP Score Bar
        icp_score = lead['icp_score']
        st.markdown(f"**ICP Score:** <span style='color:#38BDF8; font-weight:700;'>{icp_score:.0f}/100</span>", unsafe_allow_html=True)
        st.progress(min(icp_score / 100.0, 1.0))

    with card_col2:
        st.markdown("<h5 style='color: #38BDF8; font-weight: 600; margin-bottom: 12px;'>👤 Contact Intelligence</h5>", unsafe_allow_html=True)
        st.markdown(f"**Contact Person:** `{lead['contact_name']}`")
        st.markdown(f"**Title:** `{lead['title'] or 'N/A'}`")
        st.markdown(f"**Email:** `{lead['email'] or 'N/A'}`")
        st.markdown(f"**Phone:** `{lead['phone'] or 'N/A'}`")
        st.markdown(f"**Persona:** `Decision Maker`")

    with card_col3:
        qual = lead.get("qualification") or {}
        bant_score = qual.get("bant_score", 0.0)

        st.markdown("<h5 style='color: #38BDF8; font-weight: 600; margin-bottom: 12px;'>📊 Qualification & Deal Metrics</h5>", unsafe_allow_html=True)
        st.markdown(f"**Priority Tier:** {render_priority_badge(lead['priority'])}", unsafe_allow_html=True)
        st.markdown(f"**Deal Health:** {render_health_badge(lead['deal_health'])}", unsafe_allow_html=True)
        st.markdown(f"**Pipeline Stage:** `{lead['pipeline_stage']}`")
        st.markdown(f"**Deal Value:** `{format_currency(lead['deal_value'])}`")

        # BANT Score Bar
        st.markdown(f"**BANT Score:** <span style='color:#10B981; font-weight:700;'>{bant_score:.0f}/100</span>", unsafe_allow_html=True)
        st.progress(min(bant_score / 100.0, 1.0))

    st.markdown('</div>', unsafe_allow_html=True)

    # NEXT BEST ACTION RECOMMENDATION CARD
    st.markdown('<div class="section-card"><div class="section-card-title"><span>⚡ Recommended Next Action</span></div>', unsafe_allow_html=True)
    rec_col1, rec_col2 = st.columns([3, 1])
    with rec_col1:
        if bant_score >= 80:
            rec_title = "Schedule Executive Discovery Meeting & Demo"
            rec_reason = "High BANT score (80+) and strong authority confirmation."
        elif bant_score >= 50:
            rec_title = "Execute Cadence Day 3 Value Email Outreach"
            rec_reason = "Moderate qualification score. Share case studies & workflow ROI metrics."
        else:
            rec_title = "Initiate Cold Call & LinkedIn Connection Note"
            rec_reason = "Initial profile identified. Establish budget & decision-maker contact."

        st.markdown(f"<h4 style='color: #F8FAFC; margin: 0 0 6px 0;'>🎯 {rec_title}</h4>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #94A3B8; margin: 0;'><strong>Rationale:</strong> {rec_reason}</p>", unsafe_allow_html=True)
    with rec_col2:
        st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
        st.markdown(f"<span class='badge badge-info'>Timing: Today</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # CONTEXT & PAIN POINTS CARD
    st.markdown('<div class="section-card"><div class="section-card-title"><span>📝 Operational Context & Pain Points</span></div>', unsafe_allow_html=True)
    st.info(lead["notes"] if lead["notes"] else "No operational context or pain points documented yet.")
    st.markdown('</div>', unsafe_allow_html=True)

    # BANT QUALIFICATION EVALUATOR FORM
    st.markdown('<div class="section-card"><div class="section-card-title"><span>🎯 BANT Qualification Evaluator</span></div>', unsafe_allow_html=True)

    qual_data = lead.get("qualification") or {}
    curr_budget = qual_data.get("budget_confirmed", False)
    curr_authority = qual_data.get("authority_confirmed", False)
    curr_need = qual_data.get("need_confirmed", False)
    curr_timeline = qual_data.get("timeline_confirmed", False)

    with st.form("bant_eval_form"):
        st.markdown("<h5 style='color: #F8FAFC; margin-bottom: 12px;'>Evaluate BANT Parameters</h5>", unsafe_allow_html=True)
        b_col1, b_col2, b_col3, b_col4 = st.columns(4)

        with b_col1:
            budget_chk = st.checkbox("💰 Budget Confirmed (+25 pts)", value=curr_budget)
        with b_col2:
            auth_chk = st.checkbox("👑 Authority Confirmed (+35 pts)", value=curr_authority)
        with b_col3:
            need_chk = st.checkbox("🔥 Need Confirmed (+25 pts)", value=curr_need)
        with b_col4:
            time_chk = st.checkbox("⏱️ Timeline < 90 Days (+15 pts)", value=curr_timeline)

        qual_notes_input = st.text_input("Qualification Notes / Evidence", value=qual_data.get("qualification_notes", ""))

        save_qual = st.form_submit_button("💾 Update BANT Qualification & Recalculate Priority", type="primary", use_container_width=True)

        if save_qual:
            updated_qual = update_qualification(
                lead_id=lead["id"],
                budget_confirmed=budget_chk,
                authority_confirmed=auth_chk,
                need_confirmed=need_chk,
                timeline_confirmed=time_chk,
                qualification_notes=qual_notes_input
            )
            st.success(f"✅ Qualification updated! New BANT Score: {updated_qual['bant_score']:.0f}/100 ({updated_qual['priority']}).")
            st.rerun()

    # Explanation summary
    explanation = explain_bant_qualification(curr_budget, curr_authority, curr_need, curr_timeline)
    st.caption(f"**Sales Rationale:** {explanation['rationale']}")
    st.markdown('</div>', unsafe_allow_html=True)

    # LOG ACTIVITY & NOTES SECTION
    st.markdown('<div class="section-card"><div class="section-card-title"><span>⚡ Log Activity & Add Notes</span></div>', unsafe_allow_html=True)
    act_tab, note_tab = st.tabs(["📞 Log Sales Activity", "📝 Add Note"])

    with act_tab:
        with st.form("log_activity_form", clear_on_submit=True):
            a_col1, a_col2 = st.columns(2)
            with a_col1:
                act_type = st.selectbox("Activity Type", ["Call", "Email", "LinkedIn", "Meeting", "Follow-up"], index=0)
            with a_col2:
                outcome = st.text_input("Outcome / Result", placeholder="e.g. Connected with COO, demo requested")
            act_notes = st.text_area("Activity Details", placeholder="Enter call notes or discussion key takeaways...")

            submit_act = st.form_submit_button("Log Activity", type="primary", use_container_width=True)
            if submit_act:
                log_activity(lead["id"], act_type, outcome, act_notes)
                st.success("✅ Sales activity logged!")
                st.rerun()

    with note_tab:
        with st.form("add_note_form", clear_on_submit=True):
            note_body = st.text_area("Note Body", placeholder="Enter internal rep note...")
            submit_note = st.form_submit_button("Save Note", type="primary", use_container_width=True)
            if submit_note:
                if note_body.strip():
                    add_note(lead["id"], note_body.strip())
                    st.success("✅ Note added!")
                    st.rerun()
                else:
                    st.error("Note body cannot be empty.")
    st.markdown('</div>', unsafe_allow_html=True)

    # CHRONOLOGICAL ACTIVITY TIMELINE
    st.markdown('<div class="section-card"><div class="section-card-title"><span>📜 Activity Timeline & Audit History</span></div>', unsafe_allow_html=True)
    activities = get_activities_for_lead(lead["id"])
    notes_list = get_notes_for_lead(lead["id"])

    if activities:
        act_data = [{
            "Timestamp": a["created_at"].strftime("%Y-%m-%d %H:%M"),
            "Type": a["activity_type"],
            "Outcome": a["outcome"] or "N/A",
            "Notes": a["notes"] or ""
        } for a in activities]
        st.dataframe(pd.DataFrame(act_data), use_container_width=True, hide_index=True)
    else:
        st.info("No sales activities recorded yet.")

    if notes_list:
        st.markdown("<h5 style='color: #F8FAFC; margin-top: 16px;'>📝 Internal Notes Log</h5>", unsafe_allow_html=True)
        for n in notes_list:
            st.markdown(f"> **{n['author']}** ({n['created_at'].strftime('%Y-%m-%d %H:%M')}): {n['body']}")
    st.markdown('</div>', unsafe_allow_html=True)
