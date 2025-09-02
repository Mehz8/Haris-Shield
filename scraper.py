import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_fraud_samples():
    """
    Function that returns a DataFrame with a 'title' column
    """
    # Your web scraping code here
    data = {
        'title': [
            'Phishing Email: fraud@example.com',
            'Fake Investment: java.sgvr.gait',
            'Clone Website: www.fakebank.com'
        ],
        'description': [
            'Fake bank email attempting to steal credentials',
            'Investment scam promising unrealistic returns',
            'Fake bank website designed to look legitimate'
        ],
        'source': [
            'Internal Database',
            'Internal Database',
            'Internal Database'
        ]
    }
    
    df = pd.DataFrame(data)
    return df