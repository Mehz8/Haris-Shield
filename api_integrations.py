import requests
import pandas as pd
import re
from datetime import datetime

def check_telecom_database(phone_number):
    """Check phone number against fraud patterns"""
    try:
        clean_number = re.sub(r'\D', '', phone_number)
        if len(clean_number) == 10:
            clean_number = '+91' + clean_number
        
        # High risk patterns
        high_risk_patterns = [
            r'\+91[6-9]([0-9]{4})1111$',
            r'\+91[6-9]([0-9]{4})9999$', 
            r'\+91[6-9]4444[0-9]{5}$'
        ]
        
        for pattern in high_risk_patterns:
            if re.match(pattern, clean_number):
                return {
                    "risk_level": "High",
                    "reason": "Matches known fraud pattern",
                    "source": "Telecom Database"
                }
        
        return {
            "risk_level": "Low",
            "reason": "No issues found",
            "source": "Telecom Database"
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

def check_cybercrime_database(query, query_type):
    """Check against cybercrime patterns"""
    try:
        # Sample data
        known_frauds = {
            "phone": {
                "+918888555555": {"type": "SIM Swap Fraud", "reports": 15},
                "+919999111111": {"type": "Impersonation Scam", "reports": 23},
            },
            "email": {
                "investment@quick-gain.com": {"type": "Investment Scam", "reports": 37},
            }
        }
        
        if query_type in known_frauds and query in known_frauds[query_type]:
            return known_frauds[query_type][query]
        
        return None
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

def submit_fraud_report(report_data):
    """Submit fraud reports"""
    try:
        report_id = f"HS{datetime.now().strftime('%Y%m%d%H%M%S')}"
        return {
            "status": "success", 
            "report_id": report_id, 
            "message": "Report submitted successfully"
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}