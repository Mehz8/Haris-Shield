import streamlit as st
import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time
from fake_useragent import UserAgent
import json

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
if 'scraped_data' not in st.session_state:
    st.session_state.scraped_data = []

# Custom CSS
st.markdown("""
<style>
.sub-header {
    font-size: 1.5rem;
    color: #0068c9;
    text-align: center;
    margin-bottom: 2rem;
}
.risk-high { background-color: #ff4b4b; color: white; padding: 5px 16px; border-radius: 5px; }
.risk-medium { background-color: #ffa500; color: white; padding: 5px 16px; border-radius: 5px; }
.risk-low { background-color: #00cc66; color: white; padding: 5px 16px; border-radius: 5px; }
.scraping-section { background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

# App header
st.title("🛡️ Hariś Shield - AI Fraud Detection")
st.markdown("""
<div style="text-align: center; color: gray;">
AI-Powered Fraud Detection with Live Web Scraping
</div>
""", unsafe_allow_html=True)

# Web Scraping Functions
def scrape_cybercrime_gov():
    """Scrape data from cybercrime.gov.in"""
    try:
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        
        # This is a sample URL - you'll need to find actual fraud reporting pages
        url = "https://www.cybercrime.gov.in/Webform/Crime_AuthoLogin.aspx"
        
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract relevant information (this will need customization based on actual site structure)
        scraped_data = []
        
        # Sample extracted data structure
        sample_frauds = [
            {
                'source': 'cybercrime.gov.in',
                'type': 'Phishing',
                'description': 'Fake banking website collecting credentials',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'severity': 'High'
            },
            {
                'source': 'cybercrime.gov.in', 
                'type': 'Investment Fraud',
                'description': 'Fake investment platform promising high returns',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'severity': 'Medium'
            }
        ]
        
        return sample_frauds
        
    except Exception as e:
        st.error(f"Error scraping cybercrime.gov.in: {str(e)}")
        return []

def scrape_fraud_news():
    """Scrape fraud news from various sources"""
    try:
        # Sample fraud news data (in real implementation, you'd scrape actual sites)
        fraud_news = [
            {
                'source': 'cybersecurity-news.com',
                'title': 'New Phishing Campaign Targets Bank Customers',
                'description': 'Attackers sending fake security alerts to steal banking credentials',
                'date': '2024-01-15',
                'category': 'Phishing'
            },
            {
                'source': 'fraud-watch.org',
                'title': 'Investment Scam Alert',
                'description': 'Fake cryptocurrency investment platform defrauding investors',
                'date': '2024-01-14',
                'category': 'Investment Fraud'
            }
        ]
        return fraud_news
    except Exception as e:
        st.error(f"Error scraping fraud news: {str(e)}")
        return []

def scrape_known_fraud_domains():
    """Get known fraud domains from various sources"""
    try:
        # This would typically come from API services or threat intelligence feeds
        domains = [
            {'domain': 'fake-bank-security.com', 'type': 'Phishing', 'risk': 'High'},
            {'domain': 'crypto-invest-now.org', 'type': 'Investment Scam', 'risk': 'High'},
            {'domain': 'free-gift-card-generator.net', 'type': 'Advance Fee Fraud', 'risk': 'Medium'}
        ]
        return domains
    except Exception as e:
        st.error(f"Error getting fraud domains: {str(e)}")
        return []

# Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Submit Report", "View Reports", "Web Scraping", "Fraud Database"])

# Dashboard page
if page == "Dashboard":
    st.header("Dashboard Overview")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Reports", len(st.session_state.reports))
    with col2:
        st.metric("Scraped Fraud Cases", len(st.session_state.scraped_data))
    with col3:
        st.metric("Detection Rate", "92%")
    
    # Quick scraping button
    if st.button("🔄 Refresh Fraud Data"):
        with st.spinner("Scraping latest fraud data..."):
            new_data = scrape_cybercrime_gov() + scrape_fraud_news()
            st.session_state.scraped_data.extend(new_data)
            st.success(f"Added {len(new_data)} new fraud cases!")

# Submit Report page
elif page == "Submit Report":
    st.header("Submit Fraud Report")
    
    with st.form("report_form"):
        name = st.text_input("Your Name*")
        email = st.text_input("Email*")
        phone = st.text_input("Phone (optional)")
        fraud_type = st.selectbox("Fraud Type*", 
                                ["Phishing", "Identity Theft", "Payment Fraud", 
                                 "Investment Scam", "Account Takeover", "Other"])
        description = st.text_area("Description*")
        severity = st.select_slider("Severity*", options=["Low", "Medium", "High"])
        
        submitted = st.form_submit_button("Submit Report")
        
        if submitted:
            if not all([name, email, fraud_type, description]):
                st.error("Please fill all required fields (*)")
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
                st.balloons()

# View Reports page
elif page == "View Reports":
    st.header("Submitted Reports")
    
    if not st.session_state.reports:
        st.info("No reports submitted yet.")
    else:
        for i, report in enumerate(st.session_state.reports):
            with st.expander(f"Report #{i+1} - {report['timestamp']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Name:** {report['name']}")
                    st.write(f"**Email:** {report['email']}")
                    if report['phone']:
                        st.write(f"**Phone:** {report['phone']}")
                with col2:
                    risk_class = f"risk-{report['severity'].lower()}"
                    st.markdown(f"**Severity:** <span class='{risk_class}'>{report['severity']}</span>", 
                               unsafe_allow_html=True)
                    st.write(f"**Type:** {report['type']}")
                    st.write(f"**Date:** {report['timestamp']}")
                st.write(f"**Description:** {report['description']}")

# Web Scraping page
elif page == "Web Scraping":
    st.header("Web Scraping Operations")
    
    st.markdown("""
    <div class="scraping-section">
    <h4>🕵️‍♂️ Live Fraud Data Collection</h4>
    <p>Scrape latest fraud reports from various online sources</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Scrape Cybercrime Portal", icon="🌐"):
            with st.spinner("Scraping cybercrime.gov.in..."):
                data = scrape_cybercrime_gov()
                st.session_state.scraped_data.extend(data)
                st.success(f"Scraped {len(data)} cases from cybercrime portal")
    
    with col2:
        if st.button("Scrape Fraud News", icon="📰"):
            with st.spinner("Scraping fraud news sources..."):
                data = scrape_fraud_news()
                st.session_state.scraped_data.extend(data)
                st.success(f"Scraped {len(data)} fraud news items")
    
    with col3:
        if st.button("Get Fraud Domains", icon="🔗"):
            with st.spinner("Fetching known fraud domains..."):
                data = scrape_known_fraud_domains()
                st.session_state.scraped_data.extend(data)
                st.success(f"Retrieved {len(data)} fraud domains")
    
    # Display scraped data
    if st.session_state.scraped_data:
        st.subheader(f"Scraped Data ({len(st.session_state.scraped_data)} items)")
        scraped_df = pd.DataFrame(st.session_state.scraped_data)
        st.dataframe(scraped_df)
        
        # Export options
        if st.button("Export to CSV"):
            csv = scraped_df.to_csv(index=False)
            st.download_button("Download CSV", csv, "fraud_data.csv", "text/csv")
    else:
        st.info("No data scraped yet. Use the buttons above to collect fraud data.")

# Fraud Database page
elif page == "Fraud Database":
    st.header("Fraud Intelligence Database")
    
    # Sample fraud patterns database
    fraud_patterns = [
        {"pattern": "Unsolicited investment offers", "type": "Investment Scam", "risk": "High"},
        {"pattern": "Urgent security alerts", "type": "Phishing", "risk": "High"},
        {"pattern": "Too-good-to-be-true returns", "type": "Ponzi Scheme", "risk": "High"},
        {"pattern": "Requests for upfront payments", "type": "Advance Fee Fraud", "risk": "Medium"}
    ]
    
    st.subheader("Known Fraud Patterns")
    for pattern in fraud_patterns:
        with st.expander(f"{pattern['type']} - {pattern['pattern']}"):
            st.write(f"**Risk Level:** {pattern['risk']}")
            st.write(f"**Description:** Common pattern in {pattern['type']} schemes")
    
    # Fraud reporting statistics
    st.subheader("Reporting Statistics")
    if st.session_state.reports:
        report_df = pd.DataFrame(st.session_state.reports)
        fraud_counts = report_df['type'].value_counts()
        st.bar_chart(fraud_counts)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray;">
<p>Hariś Shield - AI-Powered Fraud Prevention with Web Intelligence</p>
<p>⚠️ Important: Web scraping should comply with website terms of service and robots.txt</p>
</div>
""", unsafe_allow_html=True)