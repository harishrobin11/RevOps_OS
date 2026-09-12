import streamlit as st
import pandas as pd

import config
from services.lead_service import get_leads, create_lead, delete_lead
from ui.components import render_header, render_priority_badge, render_empty_state
from ui.dashboard import format_currency


def render_leads_page():
    """
    Render Lead Intelligence Registry View.
    """
    render_header(
        title="Lead Intelligence Registry",
        subtitle=f"Centralized account directory, prospecting filters, and lead scoring for {config.COMPANY_NAME}.",
        badge="Lead Registry"
    )

    # 1. ADD NEW LEAD EXPANDER FORM
    with st.expander("➕ Provision New Target Account", expanded=False):
        st.markdown("<h5 style='color: #F8FAFC; margin-bottom: 12px; font-weight: 600;'>Account & Decision Maker Profile</h5>", unsafe_allow_html=True)
        with st.form("add_lead_form", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)

            with col1:
                company_name = st.text_input("Company Name*", placeholder="e.g. Acme Tech Solutions")
                contact_name = st.text_input("Contact Name*", placeholder="e.g. Rahul Sharma")
                title = st.text_input("Job Title", placeholder="e.g. Head of Operations")

            with col2:
                email = st.text_input("Email Address", placeholder="e.g. rahul@acmetech.com")
                phone = st.text_input("Phone Number", placeholder="e.g. +91 98450 12345")
                website = st.text_input("Website URL", placeholder="e.g. https://acmetech.com")

            with col3:
                industry = st.selectbox("Industry", config.TARGET_INDUSTRIES, index=0)
                location = st.selectbox("Location / Territory", config.TARGET_TERRITORIES, index=0)
                employee_count = st.number_input("Employee Count", min_value=1, max_value=10000, value=120)

            col4, col5, col6 = st.columns(3)
            with col4:
                lead_source = st.selectbox("Lead Source", config.LEAD_SOURCES, index=1)
            with col5:
                pipeline_stage = st.selectbox("Initial Pipeline Stage", config.PIPELINE_STAGES, index=0)
            with col6:
                deal_value = st.number_input("Estimated Deal Value (₹)", min_value=0.0, value=2500000.0, step=100000.0)

            notes = st.text_area("Operational Context & Pain Points", placeholder="Describe primary operational bottlenecks, manual processes, or growth signals...")

            submitted = st.form_submit_button("🚀 Save Lead & Calculate ICP Score", type="primary", use_container_width=True)

            if submitted:
                if not company_name.strip() or not contact_name.strip():
                    st.error("⚠️ Company Name and Contact Name are required!")
                else:
                    try:
                        new_lead = create_lead({
                            "company_name": company_name,
                            "contact_name": contact_name,
                            "title": title,
                            "email": email,
                            "phone": phone,
                            "website": website,
                            "industry": industry,
                            "location": location,
                            "employee_count": employee_count,
                            "lead_source": lead_source,
                            "pipeline_stage": pipeline_stage,
                            "deal_value": deal_value,
                            "notes": notes
                        })
                        st.success(f"✅ Lead '{new_lead['company_name']}' created successfully! Calculated ICP Score: {new_lead['icp_score']:.0f}/100 ({new_lead['priority']}).")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error creating lead: {str(e)}")

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. SEARCH & FILTER TOOLBAR
    st.markdown('<div class="section-card"><div class="section-card-title"><span>🔍 Prospecting Filters & Search</span></div>', unsafe_allow_html=True)
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

    with filter_col1:
        search_query = st.text_input("Search Registry", placeholder="Company, Contact, Email...", label_visibility="collapsed")

    with filter_col2:
        ind_options = ["All"] + config.TARGET_INDUSTRIES
        sel_industry = st.selectbox("Filter Industry", ind_options, index=0)

    with filter_col3:
        p_options = ["All", "Priority A", "Priority B", "Priority C"]
        sel_priority = st.selectbox("Filter Priority", p_options, index=0)

    with filter_col4:
        s_options = ["All"] + config.PIPELINE_STAGES
        sel_stage = st.selectbox("Filter Stage", s_options, index=0)

    filter_col5, filter_col6, filter_col7 = st.columns(3)
    with filter_col5:
        loc_options = ["All"] + config.TARGET_TERRITORIES
        sel_location = st.selectbox("Filter Territory", loc_options, index=0)
    with filter_col6:
        src_options = ["All"] + config.LEAD_SOURCES
        sel_source = st.selectbox("Filter Source", src_options, index=0)
    with filter_col7:
        sort_by = st.selectbox("Sort By", ["icp_score", "created_at", "deal_value", "company_name"], index=0)

    st.markdown('</div>', unsafe_allow_html=True)

    # 3. FETCH FILTERED LEADS
    leads = get_leads(
        search_query=search_query,
        industry=sel_industry,
        priority=sel_priority,
        pipeline_stage=sel_stage,
        location=sel_location,
        lead_source=sel_source,
        sort_by=sort_by,
        descending=True if sort_by in ["icp_score", "created_at", "deal_value"] else False
    )

    # 4. REGISTRY TABLE & SELECTION
    st.markdown(f'<div class="section-card"><div class="section-card-title"><span>📋 Accounts Registry ({len(leads)} Matches)</span></div>', unsafe_allow_html=True)

    if leads:
        table_data = []
        for l in leads:
            f_up = l["next_follow_up"].strftime("%Y-%m-%d") if l["next_follow_up"] else "None"
            created = l["created_at"].strftime("%Y-%m-%d") if l["created_at"] else "N/A"

            table_data.append({
                "ID": l["id"],
                "Company": l["company_name"],
                "Contact Person": f"{l['contact_name']} ({l['title']})" if l["title"] else l["contact_name"],
                "Industry": l["industry"],
                "Territory": l["location"],
                "Employees": l["employee_count"],
                "Source": l["lead_source"],
                "ICP Score": f"{l['icp_score']:.0f}/100",
                "Priority": l["priority"],
                "Stage": l["pipeline_stage"],
                "Deal Value": format_currency(l["deal_value"]),
                "Next Follow-up": f_up,
                "Created": created
            })

        df_display = pd.DataFrame(table_data)
        st.dataframe(df_display.drop(columns=["ID"]), use_container_width=True, hide_index=True)

        st.markdown("---")
        # Quick View Account Detail Selector
        sel_col1, sel_col2 = st.columns([3, 1])
        with sel_col1:
            lead_map = {f"{l['company_name']} — {l['contact_name']} ({l['priority']})": l["id"] for l in leads}
            selected_label = st.selectbox("Select Account for Executive CRM View:", list(lead_map.keys()))
        with sel_col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("👁️ Open Account CRM View", type="primary", use_container_width=True):
                st.session_state["selected_lead_id"] = lead_map[selected_label]
                st.rerun()

    else:
        render_empty_state("No Leads Found", "No account records match the selected prospecting filters.")
    st.markdown('</div>', unsafe_allow_html=True)
