from datetime import datetime, timezone
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import func

import config
from core.database import init_db, get_db
from core.models import Lead, Qualification, Activity, Pipeline
from data.seed_data import seed_database
from ui.components import (
    inject_custom_css,
    render_header,
    render_metric_card,
    render_priority_badge,
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
    with get_db() as session:
        seed_database(session)


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
        <div><strong>Status:</strong> <span style="color: #10B981;">● System Operational</span></div>
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
        badge="Sprint 1 Active"
    )

    now = datetime.now(timezone.utc).replace(tzinfo=None)

    # Fetch Real Database Queries
    with get_db() as session:
        total_accounts = session.query(Lead).count()
        contacted_accounts = session.query(Lead).filter(Lead.pipeline_stage != "Identified").count()
        
        # Qualified leads: Priority A or high BANT score
        qualified_leads = session.query(Lead).filter(
            (Lead.priority == "Priority A") | (Lead.pipeline_stage.in_(["Qualified", "Discovery Booked", "Proposal", "Negotiation", "Won"]))
        ).count()
        
        discovery_meetings = session.query(Lead).filter(
            Lead.pipeline_stage.in_(["Discovery Booked", "Proposal", "Negotiation", "Won"])
        ).count()
        
        open_opportunities = session.query(Lead).filter(
            ~Lead.pipeline_stage.in_(["Won", "Lost"])
        ).count()

        pipeline_val_res = session.query(func.sum(Lead.deal_value)).filter(
            ~Lead.pipeline_stage.in_(["Won", "Lost"])
        ).scalar()
        pipeline_value = pipeline_val_res if pipeline_val_res else 0.0

        won_count = session.query(Lead).filter(Lead.pipeline_stage == "Won").count()
        win_rate = (won_count / total_accounts * 100) if total_accounts > 0 else 0.0

        overdue_followups = session.query(Lead).filter(
            Lead.next_follow_up < now,
            ~Lead.pipeline_stage.in_(["Won", "Lost"])
        ).count()

        due_today_followups = session.query(Lead).filter(
            func.date(Lead.next_follow_up) == func.date(now),
            ~Lead.pipeline_stage.in_(["Won", "Lost"])
        ).count()

        # Priority Accounts - process inside session to avoid DetachedInstanceError
        priority_leads = session.query(Lead).filter(
            Lead.priority.in_(["Priority A", "Priority B"])
        ).order_by(Lead.icp_score.desc()).limit(10).all()

        priority_accounts = []
        for acc in priority_leads:
            f_up_str = acc.next_follow_up.strftime("%Y-%m-%d") if acc.next_follow_up else "None set"
            is_overdue = bool(acc.next_follow_up and acc.next_follow_up < now)
            status_tag = "⚠️ OVERDUE" if is_overdue else "OK"
            priority_accounts.append({
                "Company": acc.company_name,
                "Contact Person": f"{acc.contact_name} ({acc.title})" if acc.title else acc.contact_name,
                "Industry": acc.industry,
                "Stage": acc.pipeline_stage,
                "Priority": acc.priority,
                "ICP Score": f"{acc.icp_score:.0f}/100",
                "Deal Value": f"₹{acc.deal_value/100000:.1f}L",
                "Next Follow-up": f_up_str,
                "Status": status_tag
            })

        # Pipeline Distribution
        stage_counts = session.query(
            Lead.pipeline_stage, func.count(Lead.id)
        ).group_by(Lead.pipeline_stage).all()

        # Industry Mix
        industry_counts = session.query(
            Lead.industry, func.count(Lead.id)
        ).group_by(Lead.industry).all()

    # 1. KPI METRICS ROW
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        render_metric_card("Total Accounts", f"{total_accounts}", "Target B2B Accounts", "#3B82F6")
    with kpi_col2:
        contact_pct = (contacted_accounts / total_accounts * 100) if total_accounts > 0 else 0
        render_metric_card("Contacted Accounts", f"{contacted_accounts}", f"{contact_pct:.1f}% Outreach Rate", "#06B6D4")
    with kpi_col3:
        render_metric_card("Qualified Opportunities", f"{qualified_leads}", f"{discovery_meetings} Discovery Meetings", "#10B981")
    with kpi_col4:
        val_str = f"₹{pipeline_value/100000:.1f}L" if pipeline_value < 10000000 else f"₹{pipeline_value/10000000:.2f}Cr"
        render_metric_card("Active Pipeline Value", val_str, f"{open_opportunities} Open Deals", "#F59E0B")

    kpi_col5, kpi_col6, kpi_col7, kpi_col8 = st.columns(4)
    with kpi_col5:
        render_metric_card("Conversion Rate", f"{win_rate:.1f}%", f"{won_count} Closed Won Deals", "#10B981")
    with kpi_col6:
        render_metric_card("Overdue Follow-ups", f"{overdue_followups}", "Requires Immediate Action", "#EF4444" if overdue_followups > 0 else "#10B981")
    with kpi_col7:
        render_metric_card("Due Today", f"{due_today_followups}", "Today's Action Items", "#F59E0B")
    with kpi_col8:
        render_metric_card("Priority A Leads", "5 Accounts", "Hot Prospects", "#8B5CF6")

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. CHARTS SECTION
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown('<div class="section-card"><h3>📊 Pipeline Stage Funnel</h3>', unsafe_allow_html=True)
        if stage_counts:
            df_stage = pd.DataFrame(stage_counts, columns=["Stage", "Count"])
            # Reorder stages according to configuration
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
        if industry_counts:
            df_ind = pd.DataFrame(industry_counts, columns=["Industry", "Count"])
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

    # 3. PRIORITY ACCOUNTS TABLE & FOLLOW-UP QUEUE
    st.markdown('<div class="section-card"><h3>🔥 Target Priority Accounts & Actions</h3>', unsafe_allow_html=True)
    if priority_accounts:
        df_p = pd.DataFrame(priority_accounts)
        st.dataframe(df_p, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Modules to be built in Sprints 2 - 10
    render_header(
        title=nav_option,
        subtitle=f"Module roadmap view for {nav_option}.",
        badge="Sprint 1 Foundation Active"
    )
    
    render_empty_state(
        title=f"{nav_option} Module",
        description=f"The {nav_option} engine is registered in the Sprint 1 system architecture and will be populated in subsequent sprint releases.",
        icon="🚀"
    )

    st.info("💡 **Developer Note**: Sprint 1 has successfully established the database schema, models, seeding engine, executive dark UI framework, and live executive dashboard. Modules will be enabled iteratively in future sprints.")
