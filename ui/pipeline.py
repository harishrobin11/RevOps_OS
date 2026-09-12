from datetime import datetime, timezone, timedelta
import textwrap
import streamlit as st
import pandas as pd

import config
from services.pipeline_service import get_pipeline_kanban_data, move_pipeline_stage
from services.lead_service import get_leads
from ui.components import render_header, render_priority_badge, render_metric_card, render_empty_state
from ui.dashboard import format_currency


def render_pipeline_page():
    """
    Render 10-Stage Kanban Pipeline Board and Stage Transition Control view.
    """
    render_header(
        title="Pipeline Management & Kanban Board",
        subtitle=f"Visual deal stage tracking, probability weighting, and pipeline health for {config.COMPANY_NAME}.",
        badge="Pipeline Active"
    )

    all_leads = get_leads()
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    # 1. TOP PIPELINE METRICS SUMMARY
    open_leads = [l for l in all_leads if l.get("pipeline_stage") not in ["Won", "Lost"]]
    total_open_value = sum(l.get("deal_value", 0.0) for l in open_leads)
    weighted_value = sum(l.get("deal_value", 0.0) * l.get("probability", 0.05) for l in open_leads)
    avg_deal_value = (total_open_value / len(open_leads)) if open_leads else 0.0

    p_col1, p_col2, p_col3, p_col4 = st.columns(4)
    with p_col1:
        render_metric_card("Open Opportunities", f"{len(open_leads)} Deals", f"{len(all_leads)} Total Accounts", "#38BDF8")
    with p_col2:
        render_metric_card("Active Pipeline Value", format_currency(total_open_value), "Unweighted Value", "#3B82F6")
    with p_col3:
        render_metric_card("Weighted Pipeline Value", format_currency(weighted_value), "Probability Weighted", "#10B981")
    with p_col4:
        render_metric_card("Average Deal Size", format_currency(avg_deal_value), "Per Active Account", "#F59E0B")

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. INTERACTIVE STAGE TRANSITION FORM
    with st.expander("🔄 Move Opportunity Stage & Action Update", expanded=False):
        st.markdown("<h5 style='color: #F8FAFC; margin-bottom: 12px;'>Update Stage & Set Next Action</h5>", unsafe_allow_html=True)
        with st.form("move_stage_form"):
            lead_options = {f"{l['company_name']} — Currently: {l['pipeline_stage']} ({format_currency(l['deal_value'])})": l["id"] for l in all_leads}

            if lead_options:
                m_col1, m_col2 = st.columns(2)
                with m_col1:
                    selected_lead_label = st.selectbox("Select Opportunity*", list(lead_options.keys()))
                    selected_lead_id = lead_options[selected_lead_label]

                    target_stage = st.selectbox("Target Pipeline Stage*", config.PIPELINE_STAGES, index=0)

                with m_col2:
                    current_lead_data = next((l for l in all_leads if l["id"] == selected_lead_id), None)
                    curr_val = current_lead_data["deal_value"] if current_lead_data else 2500000.0

                    new_deal_value = st.number_input("Deal Value (₹)", min_value=0.0, value=float(curr_val), step=100000.0)
                    next_follow_up_date = st.date_input("Next Follow-up Date", value=now.date() + timedelta(days=3))

                next_action = st.text_input("Next Action Item", placeholder="e.g. Conduct discovery call with COO, send proposal deck...")

                submit_move = st.form_submit_button("🚀 Update Pipeline Stage & Log Activity", type="primary", use_container_width=True)

                if submit_move:
                    try:
                        f_up_dt = datetime.combine(next_follow_up_date, datetime.min.time())
                        res = move_pipeline_stage(
                            lead_id=selected_lead_id,
                            new_stage=target_stage,
                            next_action=next_action,
                            next_follow_up=f_up_dt,
                            deal_value=new_deal_value
                        )
                        st.success(f"✅ Moved '{res['company_name']}' from '{res['old_stage']}' to '{res['new_stage']}'! Probability: {res['probability']*100:.0f}%.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error moving stage: {str(e)}")

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. KANBAN BOARD VIEW CONTROLS
    st.markdown('<div class="section-card"><div class="section-card-title"><span>📋 Pipeline Kanban Board View</span></div>', unsafe_allow_html=True)

    kanban_data = get_pipeline_kanban_data()

    # Pipeline View Preset Controls
    k_col1, k_col2 = st.columns([2, 2])
    with k_col1:
        view_preset = st.radio(
            "Kanban View Range",
            [
                "🌐 Full 10-Stage Pipeline (Horizontal Scroll)",
                "🔥 Active Stages (Identified -> Negotiation)",
                "🏆 Closed & Nurture (Won, Lost, Nurture)",
                "🎯 Single Stage Focus"
            ],
            index=0,
            horizontal=True
        )

    with k_col2:
        if view_preset == "🎯 Single Stage Focus":
            single_stage = st.selectbox("Select Stage Focus", config.PIPELINE_STAGES, index=0)
        else:
            single_stage = config.PIPELINE_STAGES[0]

    # Determine which stages to display based on preset
    if "Full 10-Stage" in view_preset:
        display_stages = config.PIPELINE_STAGES
    elif "Active Stages" in view_preset:
        display_stages = ["Identified", "Contacted", "Engaged", "Qualified", "Discovery Booked", "Proposal", "Negotiation"]
    elif "Closed & Nurture" in view_preset:
        display_stages = ["Won", "Lost", "Nurture"]
    else:
        display_stages = [single_stage]

    # BUILD HORIZONTAL SCROLLABLE KANBAN BOARD CONTAINER
    # Stripping leading indentation ensures Markdown does not treat HTML as preformatted code blocks
    kanban_html = ['<div style="display: flex; gap: 14px; overflow-x: auto; padding-bottom: 16px; margin-top: 12px; scrollbar-width: thin;">']

    for stage in display_stages:
        cards = kanban_data.get(stage, [])
        stage_total_val = sum(c["deal_value"] for c in cards)

        # Stage Column Header HTML (No 4-space indentation)
        col_header = textwrap.dedent(f'''
            <div style="flex: 0 0 270px; min-width: 270px; background-color: #0F172A; border: 1px solid #1E293B; border-radius: 10px; padding: 12px; display: flex; flex-direction: column;">
            <div style="background-color: #131B2E; border: 1px solid #1E293B; border-radius: 8px; padding: 10px; margin-bottom: 12px; text-align: center;">
            <div style="font-weight: 700; color: #F8FAFC; font-size: 13.5px;">{stage}</div>
            <div style="font-size: 11.5px; color: #38BDF8; font-weight: 600; margin-top: 2px;">{len(cards)} Deals · {format_currency(stage_total_val)}</div>
            </div>
            <div style="display: flex; flex-direction: column; gap: 10px;">
        ''').strip()
        kanban_html.append(col_header)

        if cards:
            for card in cards:
                h_color = "#10B981" if card["deal_health"] == "Healthy" else ("#F59E0B" if card["deal_health"] == "At Risk" else "#EF4444")
                f_up_str = card["next_follow_up"].strftime("%b %d") if card["next_follow_up"] else "None"
                contact_str = f"{card['contact_name']} ({card['title']})" if card['title'] else card['contact_name']

                # Priority Badge Class
                p_lower = str(card['priority']).lower()
                if "a" in p_lower:
                    p_cls = "badge-priority-a"
                elif "b" in p_lower:
                    p_cls = "badge-priority-b"
                else:
                    p_cls = "badge-priority-c"

                card_html = textwrap.dedent(f'''
                    <div style="background-color: #131B2E; border: 1px solid #1E293B; border-left: 4px solid {h_color}; border-radius: 8px; padding: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.3);">
                    <div style="font-weight: 600; color: #F8FAFC; font-size: 13px; line-height: 1.3; margin-bottom: 4px;">{card['company_name']}</div>
                    <div style="font-size: 11px; color: #94A3B8; margin-bottom: 8px;">{contact_str}</div>
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                    <span class="badge {p_cls}">{card['priority']}</span>
                    <span style="font-size: 10.5px; color: {h_color}; font-weight: 600;">● {card['deal_health']}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11.5px; color: #CBD5E1; border-top: 1px solid #1E293B; padding-top: 6px; margin-top: 4px;">
                    <span>ICP: <strong style="color: #38BDF8;">{card['icp_score']:.0f}</strong></span>
                    <span style="font-weight: 700; color: #F8FAFC;">{format_currency(card['deal_value'])}</span>
                    </div>
                    <div style="font-size: 10.5px; color: #64748B; margin-top: 4px;">📅 Next: {f_up_str}</div>
                    </div>
                ''').strip()
                kanban_html.append(card_html)
        else:
            empty_html = textwrap.dedent('''
                <div style="text-align: center; padding: 24px 10px; color: #64748B; font-size: 11.5px; border: 1px dashed #1E293B; border-radius: 8px;">
                No deals in stage
                </div>
            ''').strip()
            kanban_html.append(empty_html)

        kanban_html.append('</div></div>')

    kanban_html.append('</div>')

    st.markdown("\n".join(kanban_html), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
