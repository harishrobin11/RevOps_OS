import streamlit as st
import config
from core.database import init_db
from data.seed_data import seed_database
from ui.components import inject_custom_css, render_header, render_empty_state
from ui.dashboard import render_dashboard_page
from ui.leads import render_leads_page
from ui.lead_detail import render_lead_detail_page
from ui.pipeline import render_pipeline_page
from ui.outreach import render_outreach_page
from ui.analytics import render_analytics_page
from ui.settings import render_import_export_page

# Set Streamlit Page Configuration
st.set_page_config(
    page_title=f"{config.PRODUCT_NAME} — Revenue Operations Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Centralized Executive Dark SaaS Theme CSS
inject_custom_css()


def initialize_app():
    """
    Initialize database schema and seed demo data if empty.
    """
    init_db()
    seed_database()


# Initialize Database & Seed System
initialize_app()

# Session State for Lead Detail View Navigation
if "selected_lead_id" not in st.session_state:
    st.session_state["selected_lead_id"] = None

# ==========================================
# 🏛️ EXECUTIVE SIDEBAR NAVIGATION
# ==========================================
st.sidebar.markdown(f"""
    <div style="padding: 16px 8px 18px 8px; border-bottom: 1px solid #1E293B; margin-bottom: 16px;">
        <div style="font-size: 19px; font-weight: 800; color: #F8FAFC; letter-spacing: -0.03em; display: flex; align-items: center; gap: 8px;">
            <span style="color: #38BDF8;">⚡</span> {config.PRODUCT_NAME}
        </div>
        <div style="font-size: 11px; color: #64748B; font-weight: 500; margin-top: 3px; letter-spacing: 0.02em;">
            B2B Revenue Intelligence System
        </div>
    </div>
""", unsafe_allow_html=True)

nav_option = st.sidebar.radio(
    "NAVIGATION",
    [
        "📊 Executive Dashboard",
        "🎯 Lead Intelligence",
        "📌 Pipeline Management",
        "✉️ Outreach Engine",
        "📈 Revenue Analytics",
        "⚙️ Settings & Data"
    ],
    index=0
)

st.sidebar.markdown("""
    <div style="margin-top: 40px; padding-top: 16px; border-top: 1px solid #1E293B;"></div>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"""
    <div style="font-size: 11px; color: #64748B; line-height: 1.7; padding: 0 8px;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
            <span>System Status:</span>
            <span style="color: #10B981; font-weight: 600;">● Operational</span>
        </div>
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
            <span>Database:</span>
            <span style="color: #CBD5E1;">SQLite Local</span>
        </div>
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
            <span>Target ICP:</span>
            <span style="color: #38BDF8;">Bangalore Tech</span>
        </div>
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <span>Version:</span>
            <span style="color: #64748B;">v{config.VERSION}</span>
        </div>
    </div>
""", unsafe_allow_html=True)


# ==========================================
# 🔀 PAGE ROUTING CONTROLLER
# ==========================================
if "Dashboard" in nav_option:
    st.session_state["selected_lead_id"] = None
    render_dashboard_page()

elif "Lead Intelligence" in nav_option:
    if st.session_state.get("selected_lead_id"):
        render_lead_detail_page(st.session_state["selected_lead_id"])
    else:
        render_leads_page()

elif "Pipeline Management" in nav_option:
    st.session_state["selected_lead_id"] = None
    render_pipeline_page()

elif "Outreach Engine" in nav_option:
    st.session_state["selected_lead_id"] = None
    render_outreach_page()

elif "Revenue Analytics" in nav_option:
    st.session_state["selected_lead_id"] = None
    render_analytics_page()

elif "Settings" in nav_option:
    st.session_state["selected_lead_id"] = None
    render_import_export_page()
