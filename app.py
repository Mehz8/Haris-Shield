import streamlit as st
import pandas as pd
import re
import time
from datetime import datetime
from scraper import scrape_fraud_samples

# Page config
st.set_page_config(page_title="FraudShield AI", page_icon="🛡️", layout="wide")

# Load or scrape fraud data
@st.cache_data
def load_data():
    try:
        return pd.read_csv("fraud_data.csv")
    except:
        return scrape_fraud_samples()

fraud_data = load_data()

# ---- Header ----
st.title("🛡️ FraudShield AI Analyzer")
st.write("Search fraud details, check risk levels, and analyze suspicious entries with AI + live data.")

# ---- Search Box ----
search_query = st.text_input("🔍 Enter email, phone, website, or card number:")

if st.button("🚀 Analyze with AI"):
    if search_query:
        st.info("Running AI + Database check...")
        time.sleep(1)

        # --- AI Analysis ---
        patterns = {
            r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b': 'Credit Card Number',
            r'\b\d{3}[- ]?\d{3}[- ]?\d{4}\b': 'Phone Number',
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b': 'Email Address',
            r'\b(https?://)?(www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}\b': 'Website URL'
        }

        detected_type = "Unknown"
        for pattern, t in patterns.items():
            if re.search(pattern, search_query, re.IGNORECASE):
                detected_type = t
                break

        # --- Database Check ---
        matches = fraud_data[fraud_data['title'].str.contains(search_query, case=False, na=False)]

        st.subheader("📋 AI Results")
        st.write(f"**Detected Type:** {detected_type}")
        st.write(f"**Database Matches:** {len(matches)} found")

        if not matches.empty:
            st.error("🚨 Potential fraud detected from scraped sources:")
            st.dataframe(matches)
        else:
            st.success("✅ No direct fraud records found. Remain cautious.")

# ---- Show Webscraped DB ----
st.subheader("🌐 Latest Fraud Reports (Scraped)")
st.dataframe(fraud_data)

# ---- Report Fraud ----
st.subheader("📝 Report New Fraud")
report_text = st.text_area("Describe suspicious activity")
if st.button("📤 Submit Report"):
    st.success("✅ Report submitted. Thank you for helping others!")
