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
    render_empty_state
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
        subtitle=f"Real-time lead intelligence, pipeline health, and high-priority accounts for {config.COMPANY_NAME}.",
        badge="Live Analytics"
    )

    now = datetime.now(timezone.utc).replace(tzinfo=None)

    # 1. FETCH METRICS FROM SERVICE LAYER
    kpis = get_executive_kpis()
    funnel_data = get_funnel_distribution()
    industry_data = get_industry_distribution()
    priority_accounts = get_priority_accounts_summary(limit=10)

    # 2. KPI METRICS GRID (ROW 1 & ROW 2)
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        render_metric_card("Total Accounts", f"{kpis['total_accounts']}", "Target B2B Accounts", "#3B82F6")
    with kpi_col2:
        contact_pct = (kpis['contacted_accounts'] / kpis['total_accounts'] * 100) if kpis['total_accounts'] > 0 else 0
        render_metric_card("Contacted Accounts", f"{kpis['contacted_accounts']}", f"{contact_pct:.1f}% Outreach Rate", "#06B6D4")
    with kpi_col3:
        render_metric_card("Qualified Opportunities", f"{kpis['qualified_leads']}", f"{kpis['discovery_meetings']} Discovery Meetings", "#10B981")
    with kpi_col4:
        val_str = format_currency(kpis['pipeline_value'])
        render_metric_card("Active Pipeline Value", val_str, f"{kpis['open_opportunities']} Open Deals", "#F59E0B")

    kpi_col5, kpi_col6, kpi_col7, kpi_col8 = st.columns(4)
    with kpi_col5:
        render_metric_card("Conversion Rate", f"{kpis['win_rate']:.1f}%", f"{kpis['won_count']} Closed Won Deals", "#10B981")
    with kpi_col6:
        render_metric_card("Overdue Follow-ups", f"{kpis['overdue_followups']}", "Requires Immediate Action", "#EF4444" if kpis['overdue_followups'] > 0 else "#10B981")
    with kpi_col7:
        render_metric_card("Due Today", f"{kpis['due_today_followups']}", "Today's Action Items", "#F59E0B")
    with kpi_col8:
        render_metric_card("Priority A Leads", f"{kpis['priority_a_count']} Accounts", "Hot Prospects", "#8B5CF6")

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. EXECUTIVE CHARTS SECTION
    st.markdown('<div class="section-card"><h3>📈 Revenue Funnel & Market Intelligence</h3>', unsafe_allow_html=True)
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Pipeline Stage Funnel")
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
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            fig_funnel.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#9CA3AF"),
                xaxis=dict(title="", tickangle=-30),
                yaxis=dict(title="Accounts"),
                margin=dict(l=10, r=10, t=10, b=10),
                showlegend=False
            )
            st.plotly_chart(fig_funnel, use_container_width=True)

    with chart_col2:
        st.subheader("Industry Mix Distribution")
        if industry_data:
            df_ind = pd.DataFrame(industry_data)
            df_ind.columns = ["Industry", "Count"]
            fig_pie = px.pie(
                df_ind,
                names="Industry",
                values="Count",
                hole=0.45,
                color_discrete_sequence=px.colors.sequential.Tealgrn
            )
            fig_pie.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#9CA3AF"),
                margin=dict(l=10, r=10, t=10, b=10)
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # SECONDARY CHARTS ROW (BANT Priority & Lead Source)
    st.markdown('<div class="section-card"><h3>🎯 Lead Qualification & Source Breakdown</h3>', unsafe_allow_html=True)
    sec_col1, sec_col2 = st.columns(2)

    all_leads = get_leads()

    with sec_col1:
        st.subheader("Priority Distribution (BANT)")
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
                    "Priority C": "#3B82F6"
                }
            )
            fig_p.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#9CA3AF"),
                xaxis=dict(title=""),
                yaxis=dict(title="Leads"),
                margin=dict(l=10, r=10, t=10, b=10),
                showlegend=False
            )
            st.plotly_chart(fig_p, use_container_width=True)

    with sec_col2:
        st.subheader("Lead Source Channel Breakdown")
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
                color_discrete_sequence=px.colors.qualitative.Prism
            )
            fig_s.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#9CA3AF"),
                xaxis=dict(title="Accounts"),
                yaxis=dict(title=""),
                margin=dict(l=10, r=10, t=10, b=10),
                showlegend=False
            )
            st.plotly_chart(fig_s, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 4. PRIORITY TARGET ACCOUNTS TABLE
    st.markdown('<div class="section-card"><h3>🔥 Top Priority Target Accounts & Actions</h3>', unsafe_allow_html=True)
    if priority_accounts:
        df_p = pd.DataFrame(priority_accounts)
        if "id" in df_p.columns:
            df_p = df_p.drop(columns=["id"])
        st.dataframe(df_p, use_container_width=True, hide_index=True)
    else:
        render_empty_state("No Priority Accounts", "No high priority accounts currently flagged.")
    st.markdown('</div>', unsafe_allow_html=True)

    # 5. FOLLOW-UP QUEUE TABS
    st.markdown('<div class="section-card"><h3>⏱️ Action Queue & Cadence Deadline Tracking</h3>', unsafe_allow_html=True)
    tab_overdue, tab_today, tab_upcoming = st.tabs(["⚠️ Overdue Follow-ups", "📅 Due Today", "⏩ Upcoming"])

    with tab_overdue:
        overdue_leads = [
            l for l in all_leads
            if l.get("next_follow_up") and l["next_follow_up"] < now and l.get("pipeline_stage") not in ["Won", "Lost"]
        ]
        if overdue_leads:
            o_data = [{
                "Company": l["company_name"],
                "Contact": f"{l['contact_name']} ({l['title']})",
                "Industry": l["industry"],
                "Priority": l["priority"],
                "Stage": l["pipeline_stage"],
                "Overdue Date": l["next_follow_up"].strftime("%Y-%m-%d"),
                "Deal Value": format_currency(l["deal_value"])
            } for l in overdue_leads]
            st.dataframe(pd.DataFrame(o_data), use_container_width=True, hide_index=True)
        else:
            st.success("🎉 No overdue follow-ups! Pipeline action queue is up to date.")

    with tab_today:
        today_leads = [
            l for l in all_leads
            if l.get("next_follow_up") and l["next_follow_up"].date() == now.date() and l.get("pipeline_stage") not in ["Won", "Lost"]
        ]
        if today_leads:
            t_data = [{
                "Company": l["company_name"],
                "Contact": f"{l['contact_name']} ({l['title']})",
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
                "Contact": f"{l['contact_name']} ({l['title']})",
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
