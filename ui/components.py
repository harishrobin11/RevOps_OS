import streamlit as st
import config


def inject_custom_css():
    """
    Inject custom CSS to create a premium Executive Dark SaaS theme.
    """
    st.markdown("""
        <style>
        /* Import Inter / Outfit Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Main Container Styling */
        .stApp {
            background-color: #0B0F19;
            color: #F9FAFB;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #0F172A !important;
            border-right: 1px solid #1E293B;
        }

        /* Executive Header Banner */
        .revops-header {
            padding: 18px 24px;
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
            border-radius: 12px;
            border: 1px solid #334155;
            margin-bottom: 24px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }

        .revops-header h1 {
            color: #F8FAFC;
            font-weight: 700;
            font-size: 24px;
            margin: 0 0 4px 0;
            letter-spacing: -0.02em;
        }

        .revops-header p {
            color: #94A3B8;
            margin: 0;
            font-size: 14px;
        }

        /* Executive KPI Card */
        .kpi-card {
            background-color: #111827;
            border: 1px solid #1F2937;
            border-radius: 10px;
            padding: 16px 20px;
            margin-bottom: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }

        .kpi-card:hover {
            border-color: #3B82F6;
        }

        .kpi-title {
            color: #9CA3AF;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 6px;
        }

        .kpi-value {
            color: #F9FAFB;
            font-size: 26px;
            font-weight: 700;
            margin-bottom: 4px;
            letter-spacing: -0.02em;
        }

        .kpi-subtitle {
            color: #6B7280;
            font-size: 12px;
        }

        /* Status & Priority Badges */
        .badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 9999px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }

        .badge-priority-a, .badge-critical {
            background-color: rgba(239, 68, 68, 0.15);
            color: #F87171;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }

        .badge-priority-b, .badge-high {
            background-color: rgba(245, 158, 11, 0.15);
            color: #FBBF24;
            border: 1px solid rgba(245, 158, 11, 0.3);
        }

        .badge-priority-c, .badge-medium {
            background-color: rgba(59, 130, 246, 0.15);
            color: #60A5FA;
            border: 1px solid rgba(59, 130, 246, 0.3);
        }

        .badge-healthy {
            background-color: rgba(16, 185, 129, 0.15);
            color: #34D399;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }

        .badge-at-risk {
            background-color: rgba(245, 158, 11, 0.15);
            color: #FBBF24;
            border: 1px solid rgba(245, 158, 11, 0.3);
        }

        .badge-stalled {
            background-color: rgba(239, 68, 68, 0.15);
            color: #F87171;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }

        /* Card Container */
        .section-card {
            background-color: #111827;
            border: 1px solid #1F2937;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }

        .section-card h3 {
            color: #F3F4F6;
            font-size: 16px;
            font-weight: 600;
            margin-top: 0;
            margin-bottom: 16px;
            padding-bottom: 8px;
            border-bottom: 1px solid #1F2937;
        }

        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 40px 20px;
            background-color: #111827;
            border: 1px dashed #374151;
            border-radius: 12px;
            color: #9CA3AF;
        }

        .empty-state h4 {
            color: #E5E7EB;
            margin-bottom: 8px;
        }
        </style>
    """, unsafe_allow_html=True)


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


def render_metric_card(title: str, value: str, subtitle: str = None, color: str = "#3B82F6"):
    """
    Render a stylized metric card.
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
    if "a" in p_lower or "critical" in p_lower:
        cls = "badge-priority-a"
    elif "b" in p_lower or "high" in p_lower:
        cls = "badge-priority-b"
    else:
        cls = "badge-priority-c"
    return f'<span class="badge {cls}">{priority}</span>'


def render_empty_state(title: str, description: str, icon: str = "🔍"):
    """
    Render a clean empty state card.
    """
    st.markdown(f"""
        <div class="empty-state">
            <div style="font-size: 32px; margin-bottom: 12px;">{icon}</div>
            <h4>{title}</h4>
            <p>{description}</p>
        </div>
    """, unsafe_allow_html=True)
