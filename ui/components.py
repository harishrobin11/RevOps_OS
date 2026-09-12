import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import config


# ==========================================
# 🎨 COLOR PALETTE & DESIGN SYSTEM CONSTANTS
# ==========================================
COLOR_BG_DARK = "#090D16"
COLOR_SIDEBAR_BG = "#0D1322"
COLOR_CARD_BG = "#131B2E"
COLOR_CARD_BORDER = "#1E293B"
COLOR_CARD_HOVER = "#1E293B"

COLOR_TEXT_PRIMARY = "#F8FAFC"
COLOR_TEXT_SECONDARY = "#94A3B8"
COLOR_TEXT_MUTED = "#64748B"

COLOR_PRIMARY = "#38BDF8"       # Sky Blue
COLOR_ACCENT = "#3B82F6"        # Royal Blue
COLOR_SUCCESS = "#10B981"       # Emerald
COLOR_WARNING = "#F59E0B"       # Amber
COLOR_DANGER = "#EF4444"        # Rose Red
COLOR_PURPLE = "#8B5CF6"        # Violet


def inject_custom_css():
    """
    Inject custom CSS to turn Streamlit into a polished B2B SaaS RevOps System.
    Inspired by Linear, Vercel, Stripe, and modern executive dashboards.
    """
    st.markdown("""
        <style>
        /* -------------------------------------------------- */
        /* 1. TYPOGRAPHY & GLOBAL LAYOUT SETUP               */
        /* -------------------------------------------------- */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            box-sizing: border-box;
        }

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .stApp {
            background-color: #090D16 !important;
            color: #F8FAFC !important;
        }

        /* -------------------------------------------------- */
        /* 2. SIDEBAR STYLING                                 */
        /* -------------------------------------------------- */
        section[data-testid="stSidebar"] {
            background-color: #0D1322 !important;
            border-right: 1px solid #1E293B !important;
            padding-top: 0rem;
        }

        section[data-testid="stSidebar"] .stRadio > label {
            display: none !important;
        }

        section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
            gap: 6px;
        }

        section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
            background-color: transparent !important;
            color: #94A3B8 !important;
            border-radius: 8px !important;
            padding: 8px 14px !important;
            font-weight: 500 !important;
            font-size: 13px !important;
            border: 1px solid transparent !important;
            transition: all 0.15s ease-in-out !important;
            cursor: pointer !important;
        }

        section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
            background-color: rgba(30, 41, 59, 0.6) !important;
            color: #F8FAFC !important;
        }

        section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"] {
            background-color: #1E293B !important;
            color: #38BDF8 !important;
            font-weight: 600 !important;
            border: 1px solid #334155 !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.3);
        }

        /* -------------------------------------------------- */
        /* 3. HEADER BANNER & SECTION CARDS                   */
        /* -------------------------------------------------- */
        .revops-header {
            padding: 20px 24px;
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
            border-radius: 12px;
            border: 1px solid #334155;
            margin-bottom: 20px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.4);
        }

        .revops-header h1 {
            color: #F8FAFC !important;
            font-weight: 700 !important;
            font-size: 24px !important;
            margin: 0 0 4px 0 !important;
            letter-spacing: -0.02em !important;
        }

        .revops-header p {
            color: #94A3B8 !important;
            margin: 0 !important;
            font-size: 13.5px !important;
        }

        .section-card {
            background-color: #131B2E;
            border: 1px solid #1E293B;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.25);
            transition: border-color 0.2s ease;
        }

        .section-card:hover {
            border-color: #334155;
        }

        .section-card-title {
            color: #F8FAFC;
            font-size: 15px;
            font-weight: 600;
            margin: 0 0 14px 0;
            padding-bottom: 10px;
            border-bottom: 1px solid #1E293B;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        /* -------------------------------------------------- */
        /* 4. KPI METRIC CARDS                                */
        /* -------------------------------------------------- */
        .kpi-card {
            background-color: #131B2E;
            border: 1px solid #1E293B;
            border-radius: 10px;
            padding: 16px 18px;
            margin-bottom: 14px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            position: relative;
            overflow: hidden;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }

        .kpi-card:hover {
            border-color: #38BDF8;
            transform: translateY(-1px);
        }

        .kpi-title {
            color: #94A3B8;
            font-size: 11.5px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 6px;
        }

        .kpi-value {
            color: #F8FAFC;
            font-size: 26px;
            font-weight: 700;
            margin-bottom: 4px;
            letter-spacing: -0.02em;
            line-height: 1.1;
        }

        .kpi-subtitle {
            color: #64748B;
            font-size: 12px;
            font-weight: 400;
        }

        /* -------------------------------------------------- */
        /* 5. REUSABLE BADGES & PILLS                         */
        /* -------------------------------------------------- */
        .badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        .badge-priority-a, .badge-critical, .badge-stalled {
            background-color: rgba(239, 68, 68, 0.15);
            color: #F87171;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }

        .badge-priority-b, .badge-high, .badge-at-risk, .badge-warning {
            background-color: rgba(245, 158, 11, 0.15);
            color: #FBBF24;
            border: 1px solid rgba(245, 158, 11, 0.3);
        }

        .badge-priority-c, .badge-medium, .badge-info {
            background-color: rgba(56, 189, 248, 0.15);
            color: #38BDF8;
            border: 1px solid rgba(56, 189, 248, 0.3);
        }

        .badge-healthy, .badge-success, .badge-won {
            background-color: rgba(16, 185, 129, 0.15);
            color: #34D399;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }

        .badge-muted {
            background-color: rgba(100, 116, 139, 0.15);
            color: #94A3B8;
            border: 1px solid rgba(100, 116, 139, 0.3);
        }

        .score-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 3px 8px;
            background-color: #0F172A;
            border: 1px solid #1E293B;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 600;
            color: #CBD5E1;
        }

        .score-pill-value {
            color: #38BDF8;
            font-weight: 700;
        }

        /* -------------------------------------------------- */
        /* 6. STREAMLIT BUTTONS & INPUT OVERRIDES             */
        /* -------------------------------------------------- */
        .stButton > button {
            border-radius: 8px !important;
            font-weight: 500 !important;
            font-size: 13px !important;
            padding: 6px 16px !important;
            transition: all 0.15s ease-in-out !important;
        }

        .stButton > button[kind="primary"] {
            background-color: #2563EB !important;
            color: #FFFFFF !important;
            border: 1px solid #3B82F6 !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.3) !important;
        }

        .stButton > button[kind="primary"]:hover {
            background-color: #1D4ED8 !important;
            border-color: #60A5FA !important;
        }

        .stButton > button[kind="secondary"] {
            background-color: #1E293B !important;
            color: #E2E8F0 !important;
            border: 1px solid #334155 !important;
        }

        .stButton > button[kind="secondary"]:hover {
            background-color: #334155 !important;
            color: #FFFFFF !important;
        }

        /* Form Inputs & Selectboxes */
        div[data-baseweb="input"] > div,
        div[data-baseweb="select"] > div {
            background-color: #0F172A !important;
            border-color: #1E293B !important;
            border-radius: 8px !important;
            color: #F8FAFC !important;
        }

        div[data-baseweb="input"]:focus-within > div,
        div[data-baseweb="select"]:focus-within > div {
            border-color: #38BDF8 !important;
        }

        /* Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: #0F172A;
            padding: 4px;
            border-radius: 8px;
            border: 1px solid #1E293B;
        }

        .stTabs [data-baseweb="tab"] {
            height: 36px;
            border-radius: 6px;
            color: #94A3B8;
            font-weight: 500;
            font-size: 13px;
            padding: 0 16px;
            border: none !important;
        }

        .stTabs [aria-selected="true"] {
            background-color: #1E293B !important;
            color: #38BDF8 !important;
            font-weight: 600 !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
        }

        /* -------------------------------------------------- */
        /* 7. EMPTY STATES & ALERTS                           */
        /* -------------------------------------------------- */
        .empty-state {
            text-align: center;
            padding: 36px 20px;
            background-color: #131B2E;
            border: 1px dashed #334155;
            border-radius: 12px;
            color: #94A3B8;
        }

        .empty-state h4 {
            color: #F8FAFC;
            font-size: 15px;
            font-weight: 600;
            margin: 8px 0 4px 0;
        }

        .empty-state p {
            font-size: 13px;
            margin: 0;
        }

        /* Hide Streamlit Default Top Header & Footer Branding */
        header[data-testid="stHeader"] {
            background-color: rgba(9, 13, 22, 0.8) !important;
            backdrop-filter: blur(8px);
        }

        footer {
            visibility: hidden;
        }
        </style>
    """, unsafe_allow_html=True)


def get_plotly_dark_layout() -> dict:
    """
    Return a standardized Plotly dark theme layout dictionary.
    Ensures 100% visual consistency across all dashboard & analytics charts.
    """
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter, -apple-system, sans-serif",
            size=12,
            color="#94A3B8"
        ),
        margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(
            font=dict(color="#CBD5E1", size=11),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )



def render_header(title: str, subtitle: str, badge: str = None):
    """
    Render executive page header banner.
    """
    badge_html = f'<span class="badge badge-priority-b">{badge}</span>' if badge else ''
    st.markdown(f"""
        <div class="revops-header">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h1>{title}</h1>
                    <p>{subtitle}</p>
                </div>
                {badge_html}
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_metric_card(title: str, value: str, subtitle: str = None, color: str = "#38BDF8"):
    """
    Render a stylized metric card with subtle left accent border.
    """
    sub_html = f'<div class="kpi-subtitle">{subtitle}</div>' if subtitle else ''
    st.markdown(f"""
        <div class="kpi-card" style="border-left: 4px solid {color};">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            {sub_html}
        </div>
    """, unsafe_allow_html=True)


def render_priority_badge(priority: str) -> str:
    """
    Return HTML badge string for priority level.
    """
    p_lower = str(priority).lower()
    if "a" in p_lower or "critical" in p_lower or "hot" in p_lower:
        cls = "badge-priority-a"
    elif "b" in p_lower or "high" in p_lower or "nurture" in p_lower:
        cls = "badge-priority-b"
    else:
        cls = "badge-priority-c"
    return f'<span class="badge {cls}">{priority}</span>'


def render_health_badge(health: str) -> str:
    """
    Return HTML badge string for deal health.
    """
    h_lower = str(health).lower()
    if "healthy" in h_lower:
        cls = "badge-healthy"
    elif "risk" in h_lower:
        cls = "badge-at-risk"
    else:
        cls = "badge-stalled"
    return f'<span class="badge {cls}">{health}</span>'


def render_empty_state(title: str, description: str, icon: str = "🔍"):
    """
    Render a clean empty state card.
    """
    st.markdown(f"""
        <div class="empty-state">
            <div style="font-size: 32px; margin-bottom: 8px;">{icon}</div>
            <h4>{title}</h4>
            <p>{description}</p>
        </div>
    """, unsafe_allow_html=True)
