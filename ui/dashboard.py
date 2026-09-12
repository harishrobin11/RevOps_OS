from datetime import datetime, timezone
import streamlit as st
import pandas as pd
import plotly.express as px

import config
from services.analytics_service import (
    get_executive_kpis,
    get_funnel_distribution,
    get_industry_distribution,
    get_priority_accounts_summary
)
from services.lead_service import get_leads
from ui.components import (
    render_header,
    render_metric_card,
    render_priority_badge,
    render_empty_state,
    get_plotly_dark_layout
)


def format_currency(value: float) -> str:
    """
    Format deal value into Indian Lakhs (L) or Crores (Cr).
    """
    val = float(value or 0.0)
    if val >= 10000000:
        return f"₹{val/10000000:.2f} Cr"
    elif val >= 100000:
        return f"₹{val/100000:.1f} Lakhs"

    else:
        return f"₹{val:,.0f}"


def render_dashboard_page():
    """
    Render complete Executive Revenue Operations Dashboard.
    """
    render_header(
        title="Executive Revenue Dashboard",
        subtitle=f"Real-time pipeline health, lead intelligence, and action queues for {config.COMPANY_NAME}.",
        badge="Live Analytics"
    )

    now = datetime.now(timezone.utc).replace(tzinfo=None)

    # 1. FETCH METRICS FROM SERVICE LAYER
    kpis = get_executive_kpis()
    funnel_data = get_funnel_distribution()
    industry_data = get_industry_distribution()
    priority_accounts = get_priority_accounts_summary(limit=10)
    all_leads = get_leads()

    # 2. KPI METRICS GRID (ROW 1 & ROW 2)
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        render_metric_card("Total Accounts", f"{kpis['total_accounts']}", "Target B2B Accounts", "#38BDF8")
    with kpi_col2:
        contact_pct = (kpis['contacted_accounts'] / kpis['total_accounts'] * 100) if kpis['total_accounts'] > 0 else 0
        render_metric_card("Contacted Accounts", f"{kpis['contacted_accounts']}", f"{contact_pct:.1f}% Outreach Rate", "#3B82F6")
    with kpi_col3:
        render_metric_card("Qualified Leads", f"{kpis['qualified_leads']}", f"{kpis['discovery_meetings']} Discovery Meetings", "#10B981")
    with kpi_col4:
        val_str = format_currency(kpis['pipeline_value'])
        render_metric_card("Active Pipeline Value", val_str, f"{kpis['open_opportunities']} Open Deals", "#F59E0B")

    kpi_col5, kpi_col6, kpi_col7, kpi_col8 = st.columns(4)
    with kpi_col5:
        render_metric_card("Win Rate", f"{kpis['win_rate']:.1f}%", f"{kpis['won_count']} Closed Won Deals", "#10B981")
    with kpi_col6:
        render_metric_card(
            "Overdue Follow-ups",
            f"{kpis['overdue_followups']}",
            "Action Required" if kpis['overdue_followups'] > 0 else "Queue Clear",
            "#EF4444" if kpis['overdue_followups'] > 0 else "#10B981"
        )
    with kpi_col7:
        render_metric_card("Due Today", f"{kpis['due_today_followups']}", "Today's Outreach Tasks", "#F59E0B")
    with kpi_col8:
        render_metric_card("Priority A Leads", f"{kpis['priority_a_count']} Accounts", "Hot Prospects", "#8B5CF6")

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. EXECUTIVE CHARTS SECTION
    st.markdown('<div class="section-card"><div class="section-card-title"><span>📈 Revenue Funnel & Market Intelligence</span></div>', unsafe_allow_html=True)
    chart_col1, chart_col2 = st.columns(2)

    plotly_layout = get_plotly_dark_layout()

    with chart_col1:
        st.markdown("<h5 style='color: #CBD5E1; font-weight: 600; margin-bottom: 12px;'>Pipeline Stage Funnel</h5>", unsafe_allow_html=True)
        if funnel_data:
            df_stage = pd.DataFrame(funnel_data)
            df_stage.columns = ["Stage", "Count"]
            df_stage['Stage'] = pd.Categorical(df_stage['Stage'], categories=config.PIPELINE_STAGES, ordered=True)
            df_stage = df_stage.sort_values('Stage')

            fig_funnel = px.bar(
                df_stage,
                x="Stage",
                y="Count",
                color="Stage",
                text="Count",
                color_discrete_sequence=["#38BDF8", "#3B82F6", "#60A5FA", "#818CF8", "#A78BFA", "#C084FC", "#F472B6", "#10B981", "#EF4444", "#64748B"]
            )
            fig_funnel.update_layout(
                **plotly_layout,
                xaxis=dict(title="", tickangle=-30, color="#94A3B8"),
                yaxis=dict(title="Accounts", color="#94A3B8"),
                showlegend=False,
                height=320
            )
            st.plotly_chart(fig_funnel, use_container_width=True)

    with chart_col2:
        st.markdown("<h5 style='color: #CBD5E1; font-weight: 600; margin-bottom: 12px;'>Industry Distribution Mix</h5>", unsafe_allow_html=True)
        if industry_data:
            df_ind = pd.DataFrame(industry_data)
            df_ind.columns = ["Industry", "Count"]
            fig_pie = px.pie(
                df_ind,
                names="Industry",
                values="Count",
                hole=0.5,
                color_discrete_sequence=["#38BDF8", "#3B82F6", "#10B981", "#F59E0B", "#8B5CF6", "#EC4899"]
            )
            fig_pie.update_layout(
                **plotly_layout,
                height=320
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # SECONDARY CHARTS ROW (Priority & Lead Source)
    st.markdown('<div class="section-card"><div class="section-card-title"><span>🎯 BANT Priority & Channel Breakdown</span></div>', unsafe_allow_html=True)
    sec_col1, sec_col2 = st.columns(2)

    with sec_col1:
        st.markdown("<h5 style='color: #CBD5E1; font-weight: 600; margin-bottom: 12px;'>Lead Priority Breakdown</h5>", unsafe_allow_html=True)
        if all_leads:
            p_counts = {}
            for l in all_leads:
                p = l.get("priority", "Priority C")
                p_counts[p] = p_counts.get(p, 0) + 1
            df_p_dist = pd.DataFrame(list(p_counts.items()), columns=["Priority", "Count"])
            fig_p = px.bar(
                df_p_dist,
                x="Priority",
                y="Count",
                color="Priority",
                text="Count",
                color_discrete_map={
                    "Priority A": "#EF4444",
                    "Priority B": "#F59E0B",
                    "Priority C": "#38BDF8"
                }
            )
            fig_p.update_layout(
                **plotly_layout,
                xaxis=dict(title="", color="#94A3B8"),
                yaxis=dict(title="Leads", color="#94A3B8"),
                showlegend=False,
                height=280
            )
            st.plotly_chart(fig_p, use_container_width=True)

    with sec_col2:
        st.markdown("<h5 style='color: #CBD5E1; font-weight: 600; margin-bottom: 12px;'>Lead Source Channel Attribution</h5>", unsafe_allow_html=True)
        if all_leads:
            s_counts = {}
            for l in all_leads:
                src = l.get("lead_source", "Outreach")
                s_counts[src] = s_counts.get(src, 0) + 1
            df_s_dist = pd.DataFrame(list(s_counts.items()), columns=["Source", "Count"])
            fig_s = px.bar(
                df_s_dist,
                x="Count",
                y="Source",
                orientation="h",
                color="Source",
                text="Count",
                color_discrete_sequence=["#38BDF8", "#3B82F6", "#10B981", "#F59E0B", "#8B5CF6"]
            )
            fig_s.update_layout(
                **plotly_layout,
                xaxis=dict(title="Accounts", color="#94A3B8"),
                yaxis=dict(title="", color="#94A3B8"),
                showlegend=False,
                height=280
            )
            st.plotly_chart(fig_s, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 4. PRIORITY TARGET ACCOUNTS TABLE
    st.markdown('<div class="section-card"><div class="section-card-title"><span>🔥 Top Priority Target Accounts</span></div>', unsafe_allow_html=True)
    if priority_accounts:
        df_p = pd.DataFrame(priority_accounts)
        if "id" in df_p.columns:
            df_p = df_p.drop(columns=["id"])
        st.dataframe(df_p, use_container_width=True, hide_index=True)
    else:
        render_empty_state("No Priority Accounts", "No high priority accounts currently flagged.", "🎯")
    st.markdown('</div>', unsafe_allow_html=True)

    # 5. ACTION QUEUE & CADENCE DEADLINES
    st.markdown('<div class="section-card"><div class="section-card-title"><span>⏱️ Action Queue & Cadence Deadlines</span></div>', unsafe_allow_html=True)
    tab_overdue, tab_today, tab_upcoming = st.tabs(["⚠️ Overdue Follow-ups", "📅 Due Today", "⏩ Upcoming"])

    with tab_overdue:
        overdue_leads = [
            l for l in all_leads
            if l.get("next_follow_up") and l["next_follow_up"] < now and l.get("pipeline_stage") not in ["Won", "Lost"]
        ]
        if overdue_leads:
            o_data = [{
                "Company": l["company_name"],
                "Contact Person": f"{l['contact_name']} ({l['title']})",
                "Industry": l["industry"],
                "Priority": l["priority"],
                "Stage": l["pipeline_stage"],
                "Overdue Date": l["next_follow_up"].strftime("%Y-%m-%d"),
                "Deal Value": format_currency(l["deal_value"])
            } for l in overdue_leads]
            st.dataframe(pd.DataFrame(o_data), use_container_width=True, hide_index=True)
        else:
            st.success("🎉 No overdue follow-ups! Pipeline action queue is clear.")

    with tab_today:
        today_leads = [
            l for l in all_leads
            if l.get("next_follow_up") and l["next_follow_up"].date() == now.date() and l.get("pipeline_stage") not in ["Won", "Lost"]
        ]
        if today_leads:
            t_data = [{
                "Company": l["company_name"],
                "Contact Person": f"{l['contact_name']} ({l['title']})",
                "Industry": l["industry"],
                "Priority": l["priority"],
                "Stage": l["pipeline_stage"],
                "Follow-up Date": l["next_follow_up"].strftime("%Y-%m-%d"),
                "Deal Value": format_currency(l["deal_value"])
            } for l in today_leads]
            st.dataframe(pd.DataFrame(t_data), use_container_width=True, hide_index=True)
        else:
            st.info("No follow-ups scheduled for today.")

    with tab_upcoming:
        upcoming_leads = [
            l for l in all_leads
            if l.get("next_follow_up") and l["next_follow_up"].date() > now.date() and l.get("pipeline_stage") not in ["Won", "Lost"]
        ]
        if upcoming_leads:
            u_data = [{
                "Company": l["company_name"],
                "Contact Person": f"{l['contact_name']} ({l['title']})",
                "Industry": l["industry"],
                "Priority": l["priority"],
                "Stage": l["pipeline_stage"],
                "Follow-up Date": l["next_follow_up"].strftime("%Y-%m-%d"),
                "Deal Value": format_currency(l["deal_value"])
            } for l in upcoming_leads]
            st.dataframe(pd.DataFrame(u_data), use_container_width=True, hide_index=True)
        else:
            st.info("No upcoming follow-ups scheduled.")
    st.markdown('</div>', unsafe_allow_html=True)
