from datetime import datetime, timezone
import streamlit as st
import pandas as pd
import plotly.express as px

import config
from core.database import init_db
from data.seed_data import seed_database
from services.analytics_service import (
    get_executive_kpis,
    get_funnel_distribution,
    get_industry_distribution,
    get_priority_accounts_summary
)
from ui.components import (
    inject_custom_css,
    render_header,
    render_metric_card,
    render_empty_state
)

# Set Streamlit Page Configuration
st.set_page_config(
    page_title=f"{config.PRODUCT_NAME} — Revenue Operations Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Custom Executive Dark Theme CSS
inject_custom_css()


def initialize_app():
    """
    Initialize database schema and seed demo data if empty.
    """
    init_db()
    seed_database()


# Initialize Database & Seed System
initialize_app()

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
st.sidebar.markdown(f"""
    <div style="padding: 10px 0 20px 0; border-bottom: 1px solid #1E293B; margin-bottom: 20px;">
        <div style="font-size: 20px; font-weight: 700; color: #F8FAFC; letter-spacing: -0.02em;">
            ⚡ {config.PRODUCT_NAME}
        </div>
        <div style="font-size: 11px; color: #64748B; font-weight: 500;">
            B2B Revenue Operations System
        </div>
    </div>
""", unsafe_allow_html=True)

nav_option = st.sidebar.radio(
    "NAVIGATION",
    [
        "Executive Dashboard",
        "Lead Intelligence",
        "Pipeline Management",
        "Outreach Engine",
        "Revenue Analytics",
        "Settings & Import/Export"
    ],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"""
    <div style="font-size: 11px; color: #64748B; line-height: 1.6;">
        <div><strong>Status:</strong> <span style="color: #10B981;">● Service Layer Active</span></div>
        <div><strong>Database:</strong> SQLite Local</div>
        <div><strong>Target ICP:</strong> Bangalore B2B Tech</div>
        <div><strong>Target Role:</strong> BDA — {config.COMPANY_NAME}</div>
        <div><strong>Version:</strong> {config.VERSION}</div>
    </div>
""", unsafe_allow_html=True)


# ==========================================
# PAGE ROUTING
# ==========================================
if nav_option == "Executive Dashboard":
    render_header(
        title="Executive Revenue Dashboard",
        subtitle=f"Real-time lead intelligence, pipeline health, and high-priority accounts for {config.COMPANY_NAME}.",
        badge="Sprint 2 Active"
    )

    # Fetch Metrics via Analytics Service Layer
    kpis = get_executive_kpis()
    funnel_data = get_funnel_distribution()
    industry_data = get_industry_distribution()
    priority_accounts = get_priority_accounts_summary(limit=10)

    # 1. KPI METRICS ROW
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        render_metric_card("Total Accounts", f"{kpis['total_accounts']}", "Target B2B Accounts", "#3B82F6")
    with kpi_col2:
        contact_pct = (kpis['contacted_accounts'] / kpis['total_accounts'] * 100) if kpis['total_accounts'] > 0 else 0
        render_metric_card("Contacted Accounts", f"{kpis['contacted_accounts']}", f"{contact_pct:.1f}% Outreach Rate", "#06B6D4")
    with kpi_col3:
        render_metric_card("Qualified Opportunities", f"{kpis['qualified_leads']}", f"{kpis['discovery_meetings']} Discovery Meetings", "#10B981")
    with kpi_col4:
        val = kpis['pipeline_value']
        val_str = f"₹{val/100000:.1f}L" if val < 10000000 else f"₹{val/10000000:.2f}Cr"
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

    # 2. CHARTS SECTION
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown('<div class="section-card"><h3>📊 Pipeline Stage Funnel</h3>', unsafe_allow_html=True)
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
                color_discrete_sequence=px.colors.qualitative.Dark24
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
        st.markdown('</div>', unsafe_allow_html=True)

    with chart_col2:
        st.markdown('<div class="section-card"><h3>🏢 Industry Mix Distribution</h3>', unsafe_allow_html=True)
        if industry_data:
            df_ind = pd.DataFrame(industry_data)
            df_ind.columns = ["Industry", "Count"]
            fig_pie = px.pie(
                df_ind,
                names="Industry",
                values="Count",
                hole=0.4,
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

    # 3. PRIORITY ACCOUNTS TABLE & ACTIONS
    st.markdown('<div class="section-card"><h3>🔥 Target Priority Accounts & Actions</h3>', unsafe_allow_html=True)
    if priority_accounts:
        df_p = pd.DataFrame(priority_accounts)
        # Drop raw id for presentation
        if "id" in df_p.columns:
            df_p = df_p.drop(columns=["id"])
        st.dataframe(df_p, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    render_header(
        title=nav_option,
        subtitle=f"Service Layer enabled for {nav_option}.",
        badge="Sprint 2 Service Layer Ready"
    )

    render_empty_state(
        title=f"{nav_option} Module",
        description=f"The service layer services for {nav_option} are active. View modules will be wired in Sprints 3-9.",
        icon="⚡"
    )
