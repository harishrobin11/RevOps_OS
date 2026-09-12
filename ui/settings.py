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


def render_import_export_page():
    st.markdown("""
        <div style="margin-bottom: 25px;">
            <h1 style="color: #F8FAFC; margin-bottom: 5px; font-size: 1.8rem; font-weight: 700;">
                ⚙️ Data Management & Settings
            </h1>
            <p style="color: #94A3B8; font-size: 0.95rem; margin-top: 0;">
                Bulk import B2B leads via CSV with validation, export CRM data, and manage pipeline configuration.
            </p>
        </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["📥 CSV Lead Import", "📤 Data Export", "🎯 Target ICP Configuration"])

    # TAB 1: CSV LEAD IMPORT
    with tabs[0]:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("### 📥 Bulk Lead Import")
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
                            st.dataframe(err_df, hide_index=True)

        with col2:
            st.markdown("### 📄 Sample CSV Template")
            st.markdown("Download the official CSV format template to structure your bulk leads correctly.")

            sample_csv_data = generate_sample_csv()
            st.download_button(
                label="📥 Download Sample CSV Template",
                data=sample_csv_data,
                file_name="revops_os_lead_import_template.csv",
                mime="text/csv",
                use_container_width=True
            )

            st.markdown("---")
            st.markdown("""
                **Mandatory Columns:**
                - `Company`: Company Name (Required)
                - `Email`: Contact Email (Must be valid format)

                **Recommended Columns:**
                - `Contact`, `Title`, `Phone`, `Industry`
                - `Location` (Bangalore tech hubs)
                - `Employees` (50 - 300)
                - `Deal Value`, `Notes`
            """)

    # TAB 2: DATA EXPORT
    with tabs[1]:
        st.markdown("### 📤 Export CRM & Pipeline Data")
        st.markdown("Download raw pipeline, lead intelligence, or activity timeline logs for external analysis.")

        ex_col1, ex_col2 = st.columns(2)

        with ex_col1:
            st.markdown("""
                <div style="background-color: #1E293B; padding: 20px; border-radius: 8px; border: 1px solid #334155;">
                    <h4 style="color: #38BDF8; margin-top: 0;">📋 Export Lead Registry & Opportunities</h4>
                    <p style="color: #94A3B8; font-size: 0.85rem;">Export active leads, ICP scores, BANT status, and pipeline stages.</p>
            """, unsafe_allow_html=True)

            exp_stage = st.selectbox("Filter Stage for Export", ["All"] + config.PIPELINE_STAGES, key="exp_stage")
            exp_industry = st.selectbox("Filter Industry for Export", ["All"] + config.TARGET_INDUSTRIES, key="exp_ind")

            leads_csv_data = export_leads_to_csv(stage_filter=exp_stage, industry_filter=exp_industry)

            st.download_button(
                label="📥 Download Leads CSV",
                data=leads_csv_data,
                file_name=f"revops_leads_export_{exp_stage.lower()}_{exp_industry.lower()}.csv",
                mime="text/csv",
                use_container_width=True
            )
            st.markdown("</div>", unsafe_allow_html=True)

        with ex_col2:
            st.markdown("""
                <div style="background-color: #1E293B; padding: 20px; border-radius: 8px; border: 1px solid #334155;">
                    <h4 style="color: #38BDF8; margin-top: 0;">📜 Export Full Activity Timeline</h4>
                    <p style="color: #94A3B8; font-size: 0.85rem;">Export complete touchpoint log (calls, emails, meeting notes, stage updates).</p>
            """, unsafe_allow_html=True)

            act_csv_data = export_activities_to_csv()

            st.download_button(
                label="📥 Download Activity Log CSV",
                data=act_csv_data,
                file_name="revops_activity_log_export.csv",
                mime="text/csv",
                use_container_width=True
            )
            st.markdown("</div>", unsafe_allow_html=True)

    # TAB 3: TARGET ICP CONFIGURATION
    with tabs[2]:
        st.markdown("### 🎯 Target ICP Rule Parameters")
        st.markdown("RevOps OS intelligence rules for Bangalore B2B Tech market segment.")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown("#### 🏢 Target Industries")
            for ind in config.TARGET_INDUSTRIES:
                st.markdown(f"- `{ind}`")

        with c2:
            st.markdown("#### 📍 Target Bangalore Hubs")
            for loc in config.TARGET_LOCATIONS:
                st.markdown(f"- `{loc}`")

        with c3:
            st.markdown("#### 👥 Company Size Criteria")
            st.info(f"**Optimal Employee Range:** {config.COMPANY_SIZE_MIN} – {config.COMPANY_SIZE_MAX} employees")
            st.markdown("Target Decision Makers: COO, VP Operations, Head of Delivery, Founder.")
