import streamlit as st
import pandas as pd
from datetime import datetime
import re
from config import Config
from api_integrations import check_telecom_database, check_cybercrime_database, submit_fraud_report

# Page configuration
st.set_page_config(
    page_title="Haris Shield - AI Fraud Prevention", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown(f"""
<style>
    .main-header {{
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }}
    .sub-header {{
        font-size: 1.5rem;
        color: #0068c9;
        text-align: center;
        margin-bottom: 2rem;
    }}
    .risk-high {{
        background-color: #ff4b4b;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
    }}
    .risk-medium {{
        background-color: #ffa500;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
    }}
    .risk-low {{
        background-color: #00cc00;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
    }}
    .search-box {{
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border-left: 4px solid #1f77b4;
    }}
    .example-text {{
        font-size: 0.9rem;
        color: #6c757d;
        font-style: italic;
    }}
</style>
""", unsafe_allow_html=True)

# App title and description
st.markdown(f'<h1 class="main-header">🛡️ {Config.APP_NAME}</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="sub-header">AI-Powered Fraud Detection Platform</h2>', unsafe_allow_html=True)

# Initialize session state
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'reports' not in st.session_state:
    st.session_state.reports = []

# Enhanced AI analysis function
def enhanced_ai_analysis(query):
    # Determine query type
    query_type = "unknown"
    if re.match(r'^\+?[0-9]{10,12}$', query.replace(" ", "")):
        query_type = "phone"
    elif re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', query):
        query_type = "email"
    elif re.match(r'^(https?://)?(www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}', query):
        query_type = "url"
    elif re.match(r'^[a-zA-Z\s]{3,}$', query):
        query_type = "entity"
    
    # Initialize results
    results = {
        "query": query,
        "type": query_type,
        "risk_score": 0,
        "risk_level": "Low",
        "details": {},
        "sources_checked": []
    }
    
    # Check telecom database for phone numbers
    if query_type == "phone":
        results["sources_checked"].append("Telecom Database")
        telecom_result = check_telecom_database(query)
        results["details"]["telecom_db"] = telecom_result
        
        if telecom_result.get("risk_level") == "High":
            results["risk_score"] = 85
        elif telecom_result.get("risk_level") == "Medium":
            results["risk_score"] = 60
        else:
            results["risk_score"] = 20
    
    # Check cybercrime database
    results["sources_checked"].append("Cybercrime Database")
    cybercrime_result = check_cybercrime_database(query, query_type)
    if cybercrime_result:
        results["details"]["cybercrime_db"] = cybercrime_result
        results["risk_score"] = max(results["risk_score"], 75)
    
    # Pattern analysis
    suspicious_keywords = [
        'free', 'win', 'prize', 'urgent', 'password', 'verify', 'account', 
        'bank', 'pay', 'security', 'investment', 'crypto', 'loan', 'offer',
        'discount', 'limited', 'secure', 'kyc', 'reward', 'lottery', 'jackpot',
        'selected', 'winner', 'claim', 'immediate', 'bitcoin', 'ethereum',
        'stock', 'trading', 'profit', 'return', 'scheme', 'opportunity', 'bonus'
    ]
    
    keyword_count = sum(1 for word in suspicious_keywords if word in query.lower())
    results["details"]["suspicious_keywords"] = keyword_count
    results["risk_score"] = min(100, results["risk_score"] + (keyword_count * 5))
    
    # Determine risk level
    if results["risk_score"] >= 80:
        results["risk_level"] = "High"
    elif results["risk_score"] >= 50:
        results["risk_level"] = "Medium"
    else:
        results["risk_level"] = "Low"
    
    return results

# Main search interface - Single dialog box
st.markdown("""
<div class="search-box">
    <h3>🔍 AI Fraud Detection Search</h3>
    <p class="example-text">Examples: "Quick Gain Investments", "+918888555555", "crypto-profit.com", "investment@secure-kyc.com"</p>
</div>
""", unsafe_allow_html=True)

# Single search input with examples
search_query = st.text_input(
    "**Enter phone number, email, website, or company name to verify:**",
    placeholder="e.g., Quick Gain Investments, +91XXXXXXXXXX, example@email.com, companyname.com",
    key="search_input",
    help="Enter any suspicious contact details, investment offers, or websites to check for fraud risks"
)

analyze_button = st.button("🚀 Analyze with AI", type="primary")

# Analysis results
if analyze_button and search_query:
    st.session_state.search_history.append({
        "query": search_query,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    with st.spinner("🛡️ AI is analyzing across multiple databases..."):
        # Enhanced AI Analysis
        ai_result = enhanced_ai_analysis(search_query)
        
        # Display results
        st.markdown("---")
        st.markdown("## 📋 AI Analysis Results")
        
        result_col1, result_col2 = st.columns(2)
        
        with result_col1:
            st.markdown("### 🔍 Analysis Details")
            st.write(f"**Input Type:** {ai_result['type'].title()}")
            st.write(f"**Risk Score:** {ai_result['risk_score']}/100")
            
            risk_class = f"risk-{ai_result['risk_level'].lower()}"
            st.markdown(f"**Risk Level:** <span class='{risk_class}'>{ai_result['risk_level']}</span>", unsafe_allow_html=True)
            
            st.write(f"**Sources Checked:** {', '.join(ai_result['sources_checked'])}")
            
            # Display specific database matches
            if "telecom_db" in ai_result["details"]:
                telecom_data = ai_result["details"]["telecom_db"]
                if telecom_data.get("risk_level") != "Low":
                    risk_icon = "❌" if telecom_data.get("risk_level") == "High" else "⚠️"
                    st.error(f"**{risk_icon} Telecom Database Match:** {telecom_data.get('risk_level', 'Unknown')} Risk")
            
            if "cybercrime_db" in ai_result["details"]:
                cyber_data = ai_result["details"]["cybercrime_db"]
                risk_icon = "❌" if cyber_data.get('reports', 0) > 10 else "⚠️"
                st.error(f"**{risk_icon} Cybercrime Database Match:** {cyber_data.get('type', 'Unknown')}")
            
            if "suspicious_keywords" in ai_result["details"]:
                st.warning(f"**Suspicious Patterns Detected:** {ai_result['details']['suspicious_keywords']} suspicious elements found")
        
        with result_col2:
            st.markdown("### 🛡️ Recommendations")
            
            if ai_result['risk_level'] == "High":
                st.error("**Immediate Action Required:**")
                st.write("🚨 This entity shows characteristics of known fraud patterns")
                st.write("🚨 Do not engage or share any personal information")
                st.write("📞 Immediately contact your bank if already engaged")
                st.write("📋 Report to cybercrime authorities")
                st.write("📵 Block all communications from this entity")
                
            elif ai_result['risk_level'] == "Medium":
                st.warning("**Exercise Extreme Caution:**")
                st.write("⚠️ This entity shows suspicious characteristics")
                st.write("⚠️ Verify through official channels before proceeding")
                st.write("🔍 Research the entity thoroughly online")
                st.write("📞 Contact through official verified channels only")
                st.write("📝 Check for reviews or complaints from other users")
                
            else:
                st.success("**No High-Risk Indicators Found:**")
                st.write("✅ No matches in fraud databases")
                st.write("🔍 Continue with standard precautions")
                st.write("📱 Verify through official sources when in doubt")
                st.write("📝 Report any suspicious activity")

# Report fraud section
st.markdown("---")
st.markdown("## 📝 Report Suspected Fraud")

with st.form("fraud_report_form"):
    st.write("Help protect others by reporting suspected fraud attempts")
    
    report_type = st.selectbox(
        "Type of Fraud:",
        ["Investment Scam", "Phishing", "UPI Fraud", "Fake Job Offer", "Loan Fraud", "Other"]
    )
    
    fraud_details = st.text_area("Details of the fraud attempt:", height=100,
                                placeholder="Please provide specific details about what happened...")
    
    contact_info = st.text_input("Your Contact Information (optional):",
                                placeholder="Email or phone for follow-up if needed")
    
    submitted = st.form_submit_button("Submit Report")
    
    if submitted:
        if fraud_details:
            report_data = {
                "type": report_type,
                "details": fraud_details,
                "contact": contact_info,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Submit report
            report_result = submit_fraud_report(report_data)
            if report_result.get("status") == "success":
                st.session_state.reports.append(report_data)
                st.success(f"Thank you! Your report has been submitted.")
            else:
                st.error("Failed to submit report. Please try again.")
        else:
            st.warning("Please provide details about the fraud attempt")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>🛡️ Haris Shield - AI-Powered Fraud Prevention Platform</p>
</div>
""", unsafe_allow_html=True)# Haris-Shield
AI-Powered Fraud Detection Platform
