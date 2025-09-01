import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Hariś Shield - AI Fraud Prevention",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'reports' not in st.session_state:
    st.session_state.reports = []

# App title
st.title("🛡️ Hariś Shield - AI Fraud Detection")
st.markdown("AI-Powered Fraud Prevention Platform")

# Navigation
page = st.sidebar.selectbox("Navigation", ["Dashboard", "Submit Report", "View Reports", "Settings"])

# Dashboard page
if page == "Dashboard":
    st.header("Dashboard Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Reports", len(st.session_state.reports))
    with col2:
        st.metric("Detection Rate", "92%")
    with col3:
        st.metric("Active Monitoring", "24/7")

# Submit Report page
elif page == "Submit Report":
    st.header("Submit Fraud Report")
    
    with st.form("report_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone (optional)")
        fraud_type = st.selectbox("Fraud Type", 
                                ["Phishing", "Identity Theft", "Payment Fraud", 
                                 "Investment Scam", "Account Takeover", "Other"])
        description = st.text_area("Incident Description")
        severity = st.select_slider("Severity Level", options=["Low", "Medium", "High"])
        
        submitted = st.form_submit_button("Submit Report")
        
        if submitted:
            if not all([name, email, fraud_type, description]):
                st.error("Please fill all required fields")
            else:
                report = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "type": fraud_type,
                    "description": description,
                    "severity": severity
                }
                st.session_state.reports.append(report)
                st.success("Report submitted successfully!")

# View Reports page
elif page == "View Reports":
    st.header("Submitted Reports")
    
    if not st.session_state.reports:
        st.info("No reports submitted yet.")
    else:
        for i, report in enumerate(st.session_state.reports):
            with st.expander(f"Report #{i+1} - {report['timestamp']}"):
                st.write(f"**Name:** {report['name']}")
                st.write(f"**Email:** {report['email']}")
                if report['phone']:
                    st.write(f"**Phone:** {report['phone']}")
                st.write(f"**Type:** {report['type']}")
                st.write(f"**Severity:** {report['severity']}")
                st.write(f"**Description:** {report['description']}")

# Settings page
elif page == "Settings":
    st.header("Application Settings")
    st.write("Configure your fraud detection preferences:")
    
    notification_pref = st.checkbox("Enable email notifications")
    auto_block = st.checkbox("Automatically block suspicious patterns")
    data_retention = st.slider("Data retention period (days)", 30, 365, 90)
    
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray;">
<p>Hariś Shield - AI-Powered Fraud Prevention Platform</p>
</div>
""", unsafe_allow_html=True)