import streamlit as st
import pandas as pd
import os

# Import the scraping function
try:
    from scraper import scrape_fraud_samples
except ImportError:
    st.error("Could not import scraper. Please ensure scraper.py exists.")
    
# Define the load_data function
def load_data():
    """
    Load data from CSV if available, otherwise scrape
    """
    csv_file = 'fraud_data.csv'
    
    if os.path.exists(csv_file):
        try:
            df = pd.read_csv(csv_file)
            # Check if the CSV has the required 'title' column
            if 'title' not in df.columns:
                st.error("CSV file missing 'title' column. Falling back to scraping.")
                return scrape_fraud_samples()
            return df
        except Exception as e:
            st.error(f"Error reading CSV: {e}. Falling back to scraping.")
            return scrape_fraud_samples()
    else:
        st.info("fraud_data.csv not found. Scraping data...")
        return scrape_fraud_samples()

# Define the main function
def main():
    st.title("AI-Powered Fraud Detection System")
    
    # Load data
    fraud_data = load_data()
    
    # Display data
    st.subheader("Fraud Samples Database")
    st.dataframe(fraud_data)
    
    # Search functionality
    search_term = st.text_input("Search fraud samples by title:")
    if search_term:
        results = fraud_data[fraud_data['title'].str.contains(search_term, case=False, na=False)]
        st.write(f"Found {len(results)} matching records:")
        st.dataframe(results)
    
    # AI integration section
    st.subheader("AI Analysis")
    if st.button("Run Fraud Pattern Analysis"):
        with st.spinner("Analyzing patterns with AI..."):
            # Your AI integration code here
            st.success("Analysis complete!")

# This ensures main() is only called when the script is run directly
if __name__ == "__main__":
    main()