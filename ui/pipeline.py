from datetime import datetime, timezone, timedelta
import streamlit as st
import pandas as pd

import config
from services.pipeline_service import get_pipeline_kanban_data, move_pipeline_stage
from services.lead_service import get_leads
from ui.components import render_header, render_priority_badge, render_empty_state
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
        st.metric("Open Opportunities", f"{len(open_leads)} Deals", delta=f"{len(all_leads)} Total Accounts")
    with p_col2:
        st.metric("Active Pipeline Value", format_currency(total_open_value))
    with p_col3:
        st.metric("Weighted Pipeline Value", format_currency(weighted_value), help="Sum of (Deal Value × Stage Probability)")
    with p_col4:
        st.metric("Average Deal Size", format_currency(avg_deal_value))

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. INTERACTIVE STAGE TRANSITION FORM
    with st.expander("🔄 Move Opportunity Stage & Action Update", expanded=False):
        st.markdown("##### Update Stage & Set Next Action")
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

                submit_move = st.form_submit_button("🚀 Update Pipeline Stage & Log Activity", use_container_width=True)

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

    # 3. KANBAN BOARD GRID VIEW
    st.markdown('<div class="section-card"><h3>📋 Pipeline Kanban Board View</h3>', unsafe_allow_html=True)

    kanban_data = get_pipeline_kanban_data()

    # Stage Filter
    sel_kanban_stage = st.selectbox("Filter Kanban Columns", ["Show All 10 Stages"] + config.PIPELINE_STAGES, index=0)

    if sel_kanban_stage == "Show All 10 Stages":
        display_stages = config.PIPELINE_STAGES
    else:
        display_stages = [sel_kanban_stage]

    # Render columns in scrollable horizontal layout
    cols = st.columns(len(display_stages))

    for idx, stage in enumerate(display_stages):
        cards = kanban_data.get(stage, [])
        stage_total_val = sum(c["deal_value"] for c in cards)

        with cols[idx]:
            # Stage Header
            st.markdown(f"""
                <div style="background-color: #0F172A; border: 1px solid #1E293B; border-radius: 8px; padding: 10px; margin-bottom: 12px; text-align: center;">
                    <div style="font-weight: 700; color: #F8FAFC; font-size: 13px;">{stage}</div>
                    <div style="font-size: 11px; color: #3B82F6; font-weight: 600;">{len(cards)} Deals</div>
                    <div style="font-size: 11px; color: #94A3B8;">{format_currency(stage_total_val)}</div>
                </div>
            """, unsafe_allow_html=True)

            if cards:
                for card in cards:
                    h_color = "#10B981" if card["deal_health"] == "Healthy" else ("#F59E0B" if card["deal_health"] == "At Risk" else "#EF4444")
                    f_up_str = card["next_follow_up"].strftime("%b %d") if card["next_follow_up"] else "None"

                    st.markdown(f"""
                        <div style="background-color: #111827; border: 1px solid #1F2937; border-left: 4px solid {h_color}; border-radius: 8px; padding: 12px; margin-bottom: 10px;">
                            <div style="font-weight: 600; color: #F9FAFB; font-size: 13px;">{card['company_name']}</div>
                            <div style="font-size: 11px; color: #9CA3AF;">{card['contact_name']} ({card['title'] or 'N/A'})</div>
                            <div style="margin: 6px 0;">
                                <span class="badge badge-priority-c">{card['priority']}</span>
                                <span style="font-size: 10px; color: {h_color}; margin-left: 4px; font-weight: 600;">● {card['deal_health']}</span>
                            </div>
                            <div style="display: flex; justify-content: space-between; font-size: 11px; color: #E5E7EB; margin-top: 6px;">
                                <span>ICP: <strong>{card['icp_score']:.0f}</strong></span>
                                <span>Val: <strong>{format_currency(card['deal_value'])}</strong></span>
                            </div>
                            <div style="font-size: 10px; color: #6B7280; margin-top: 4px;">📅 Next: {f_up_str}</div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="text-align: center; padding: 20px 8px; color: #4B5563; font-size: 11px; border: 1px dashed #1F2937; border-radius: 8px;">
                        No deals in this stage
                    </div>
                """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
