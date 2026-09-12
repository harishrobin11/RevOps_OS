import streamlit as st
import config
from core.database import init_db
from data.seed_data import seed_database
from ui.components import inject_custom_css, render_header, render_empty_state
from ui.dashboard import render_dashboard_page

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
        <div><strong>Status:</strong> <span style="color: #10B981;">● Dashboard Module Ready</span></div>
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
    render_dashboard_page()
else:
    render_header(
        title=nav_option,
        subtitle=f"Modular architecture view for {nav_option}.",
        badge="Sprint 4 Ready"
    )

    render_empty_state(
        title=f"{nav_option} Module",
        description=f"The {nav_option} module is registered in the Sprint 4 UI system architecture. View pages will be wired in Sprints 5-9.",
        icon="🚀"
    )
