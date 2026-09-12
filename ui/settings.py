import streamlit as st
import pandas as pd
from services.import_export_service import (
    generate_sample_csv,
    import_leads_from_csv,
    export_leads_to_csv,
    export_activities_to_csv
)
from services import lead_service
import config
from ui.components import render_header


def render_import_export_page():
    render_header(
        title="Data Management & System Settings",
        subtitle=f"Bulk import B2B leads via CSV with validation, export CRM data, and review ICP parameters for {config.COMPANY_NAME}.",
        badge="Settings Active"
    )

    tabs = st.tabs(["📥 CSV Lead Import", "📤 Data Export Engine", "🎯 Target ICP Configuration"])

    # TAB 1: CSV LEAD IMPORT
    with tabs[0]:
        st.markdown('<div class="section-card"><div class="section-card-title"><span>📥 Bulk Account CSV Import</span></div>', unsafe_allow_html=True)
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("""
                Upload your target company list in CSV format. The import engine will automatically:
                - Validate required company names & email formatting
                - Detect duplicate accounts and skip existing records
                - Calculate **ICP Score** & initial priority based on Bangalore ICP rules
                - Provision initial BANT qualification profile
            """)

            uploaded_file = st.file_uploader(
                "Select a CSV file to import",
                type=["csv"],
                help="CSV must include Company column. Optional: Contact, Title, Email, Phone, Industry, Location, Employees, Deal Value, Notes."
            )

            if uploaded_file is not None:
                content = uploaded_file.getvalue()
                if st.button("🚀 Process CSV Import", type="primary"):
                    with st.spinner("Validating and importing leads..."):
                        report = import_leads_from_csv(content)

                    if report["success_count"] > 0:
                        st.success(f"✅ Successfully imported **{report['success_count']}** new leads into the database!")

                    if report["error_count"] > 0:
                        st.warning(f"⚠️ Skipped **{report['error_count']}** rows due to validation issues or duplicate records.")
                        with st.expander("🔍 View Detailed Import Error Log", expanded=True):
                            err_df = pd.DataFrame(report["errors"])
                            st.dataframe(err_df, use_container_width=True, hide_index=True)

        with col2:
            st.markdown("<h5 style='color: #F8FAFC; margin-bottom: 8px;'>📄 CSV Format Template</h5>", unsafe_allow_html=True)
            st.markdown("Download the official CSV format template to structure your bulk leads correctly.")

            sample_csv_data = generate_sample_csv()
            st.download_button(
                label="📥 Download Sample CSV Template",
                data=sample_csv_data,
                file_name="revops_os_lead_import_template.csv",
                mime="text/csv",
                type="secondary",
                use_container_width=True
            )

            st.markdown("---")
            st.markdown("""
                **Mandatory Columns:**
                - `Company`: Company Name (Required)
                - `Email`: Contact Email (Valid format)

                **Recommended Columns:**
                - `Contact`, `Title`, `Phone`, `Industry`
                - `Location` (Bangalore tech hubs)
                - `Employees` (50 - 300)
                - `Deal Value`, `Notes`
            """)
        st.markdown('</div>', unsafe_allow_html=True)

    # TAB 2: DATA EXPORT
    with tabs[1]:
        st.markdown('<div class="section-card"><div class="section-card-title"><span>📤 Export CRM & Pipeline Data</span></div>', unsafe_allow_html=True)
        st.markdown("Download raw pipeline, lead intelligence, or activity timeline logs for external analysis.")

        ex_col1, ex_col2 = st.columns(2)

        with ex_col1:
            st.markdown("<h5 style='color: #38BDF8; font-weight: 600; margin-bottom: 4px;'>📋 Export Lead Registry & Opportunities</h5>", unsafe_allow_html=True)
            st.markdown("<p style='color: #94A3B8; font-size: 0.85rem;'>Export active leads, ICP scores, BANT status, and pipeline stages.</p>", unsafe_allow_html=True)

            exp_stage = st.selectbox("Filter Stage for Export", ["All"] + config.PIPELINE_STAGES, key="exp_stage")
            exp_industry = st.selectbox("Filter Industry for Export", ["All"] + config.TARGET_INDUSTRIES, key="exp_ind")

            leads_csv_data = export_leads_to_csv(stage_filter=exp_stage, industry_filter=exp_industry)

            st.download_button(
                label="📥 Download Leads CSV",
                data=leads_csv_data,
                file_name=f"revops_leads_export_{exp_stage.lower()}_{exp_industry.lower()}.csv",
                mime="text/csv",
                type="primary",
                use_container_width=True
            )

        with ex_col2:
            st.markdown("<h5 style='color: #38BDF8; font-weight: 600; margin-bottom: 4px;'>📜 Export Full Activity Timeline</h5>", unsafe_allow_html=True)
            st.markdown("<p style='color: #94A3B8; font-size: 0.85rem;'>Export complete touchpoint log (calls, emails, meeting notes, stage updates).</p>", unsafe_allow_html=True)

            act_csv_data = export_activities_to_csv()

            st.download_button(
                label="📥 Download Activity Log CSV",
                data=act_csv_data,
                file_name="revops_activity_log_export.csv",
                mime="text/csv",
                type="primary",
                use_container_width=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # TAB 3: TARGET ICP CONFIGURATION
    with tabs[2]:
        st.markdown('<div class="section-card"><div class="section-card-title"><span>🎯 Target ICP Rule Parameters</span></div>', unsafe_allow_html=True)
        st.markdown("RevOps OS intelligence rules for Bangalore B2B Tech market segment.")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown("<h5 style='color: #CBD5E1; font-weight: 600;'>🏢 Target Industries</h5>", unsafe_allow_html=True)
            for ind in config.TARGET_INDUSTRIES:
                st.markdown(f"- `{ind}`")

        with c2:
            st.markdown("<h5 style='color: #CBD5E1; font-weight: 600;'>📍 Target Bangalore Hubs</h5>", unsafe_allow_html=True)
            for loc in config.TARGET_TERRITORIES:

                st.markdown(f"- `{loc}`")

        with c3:
            st.markdown("<h5 style='color: #CBD5E1; font-weight: 600;'>👥 Company Size Criteria</h5>", unsafe_allow_html=True)
            st.info(f"**Optimal Employee Range:** {config.COMPANY_SIZE_MIN} – {config.COMPANY_SIZE_MAX} employees")
            st.markdown("Target Decision Makers: COO, VP Operations, Head of Delivery, Founder.")
        st.markdown('</div>', unsafe_allow_html=True)
