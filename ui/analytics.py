import streamlit as st
import pandas as pd
import plotly.express as px

import config
from services.analytics_service import (
    get_executive_kpis,
    get_funnel_conversion_rates,
    get_conversion_by_industry,
    get_conversion_by_lead_source,
    get_at_risk_opportunities_audit
)
from ui.components import render_header, render_metric_card, render_empty_state
from ui.dashboard import format_currency


def render_analytics_page():
    """
    Render Executive Revenue Analytics & Funnel Leakage View.
    """
    render_header(
        title="Revenue Analytics & Funnel Leakage",
        subtitle=f"Conversion performance, funnel drop-off analysis, and at-risk pipeline audit for {config.COMPANY_NAME}.",
        badge="Analytics Active"
    )

    kpis = get_executive_kpis()
    funnel_rates = get_funnel_conversion_rates()
    industry_perf = get_conversion_by_industry()
    source_perf = get_conversion_by_lead_source()
    at_risk_audit = get_at_risk_opportunities_audit()

    # 1. TOP METRICS ROW
    a_col1, a_col2, a_col3, a_col4 = st.columns(4)
    with a_col1:
        render_metric_card("Total Prospects", f"{kpis['total_accounts']}", "Registry Total Accounts", "#3B82F6")
    with a_col2:
        qual_rate = (kpis['qualified_leads'] / kpis['total_accounts'] * 100.0) if kpis['total_accounts'] > 0 else 0
        render_metric_card("Qualification Rate", f"{qual_rate:.1f}%", f"{kpis['qualified_leads']} Qualified Leads", "#06B6D4")
    with a_col3:
        disc_rate = (kpis['discovery_meetings'] / kpis['qualified_leads'] * 100.0) if kpis['qualified_leads'] > 0 else 0
        render_metric_card("Discovery Conversion", f"{disc_rate:.1f}%", f"{kpis['discovery_meetings']} Meetings Booked", "#10B981")
    with a_col4:
        render_metric_card("Closed Win Rate", f"{kpis['win_rate']:.1f}%", f"{kpis['won_count']} Deals Won", "#8B5CF6")

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. FUNNEL CONVERSION & DROP-OFF ANALYSIS
    st.markdown('<div class="section-card"><h3>📉 Funnel Conversion & Drop-off Analysis</h3>', unsafe_allow_html=True)
    if funnel_rates:
        df_funnel = pd.DataFrame(funnel_rates)
        df_funnel.columns = ["Stage Transition", "Accounts Count", "Conversion Rate (%)"]

        f_col1, f_col2 = st.columns([3, 2])
        with f_col1:
            fig_conv = px.bar(
                df_funnel,
                x="Stage Transition",
                y="Conversion Rate (%)",
                text="Conversion Rate (%)",
                color="Conversion Rate (%)",
                color_continuous_scale=px.colors.sequential.Viridis
            )
            fig_conv.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig_conv.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#9CA3AF"),
                xaxis=dict(title="", tickangle=-25),
                yaxis=dict(title="Conversion Rate (%)", range=[0, 115]),
                margin=dict(l=10, r=10, t=10, b=10)
            )
            st.plotly_chart(fig_conv, use_container_width=True)

        with f_col2:
            st.markdown("##### Stage Conversion Breakdown")
            st.dataframe(df_funnel, use_container_width=True, hide_index=True)
            st.info("💡 **Leakage Insight**: Drop-off rates indicate where prospects stall between discovery calls and commercial proposal submissions.")
    st.markdown('</div>', unsafe_allow_html=True)

    # 3. INDUSTRY & LEAD SOURCE CONVERSION BREAKDOWN
    st.markdown('<div class="section-card"><h3>🏢 Market Performance & Channel Attribution</h3>', unsafe_allow_html=True)
    perf_col1, perf_col2 = st.columns(2)

    with perf_col1:
        st.subheader("Win Rate & Volume by Industry")
        if industry_perf:
            df_ind = pd.DataFrame(industry_perf)
            df_ind = df_ind.rename(columns={
                "industry": "Industry",
                "total_accounts": "Total Accounts",
                "won_accounts": "Won",
                "win_rate": "Win Rate (%)",
                "total_value": "Total Value (₹)"
            })
            fig_ind_win = px.bar(
                df_ind,
                x="Industry",
                y="Win Rate (%)",
                color="Win Rate (%)",
                text="Win Rate (%)",
                color_continuous_scale=px.colors.sequential.Teal
            )
            fig_ind_win.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig_ind_win.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#9CA3AF"),
                xaxis=dict(title="", tickangle=-30),
                yaxis=dict(title="Win Rate (%)", range=[0, 115]),
                margin=dict(l=10, r=10, t=10, b=10)
            )
            st.plotly_chart(fig_ind_win, use_container_width=True)

    with perf_col2:
        st.subheader("Pipeline Value by Lead Source Channel")
        if source_perf:
            df_src = pd.DataFrame(source_perf)
            df_src = df_src.rename(columns={
                "lead_source": "Lead Source",
                "total_accounts": "Total Accounts",
                "won_accounts": "Won",
                "win_rate": "Win Rate (%)",
                "total_value": "Total Value (₹)"
            })
            fig_src_val = px.pie(
                df_src,
                names="Lead Source",
                values="Total Value (₹)",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_src_val.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#9CA3AF"),
                margin=dict(l=10, r=10, t=10, b=10)
            )
            st.plotly_chart(fig_src_val, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 4. AT-RISK & STALLED OPPORTUNITY AUDIT TABLE
    st.markdown('<div class="section-card"><h3>⚠️ At-Risk & Stalled Pipeline Intervention Audit</h3>', unsafe_allow_html=True)
    if at_risk_audit:
        df_risk = pd.DataFrame(at_risk_audit)
        if "id" in df_risk.columns:
            df_risk = df_risk.drop(columns=["id"])
        st.dataframe(df_risk, use_container_width=True, hide_index=True)
        st.warning(f"⚠️ **Executive Action Required**: {len(at_risk_audit)} opportunities are currently flagged as At Risk or Stalled. Review recommended next actions to prevent deal loss.")
    else:
        st.success("🎉 Excellent deal health! No active opportunities are currently flagged as At Risk or Stalled.")
    st.markdown('</div>', unsafe_allow_html=True)
