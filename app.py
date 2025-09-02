# AI Analysis Functions with corrected implementation
def ai_text_analysis(text):
    """AI-powered text analysis for fraud detection"""
    try:
        if text_classifier and text.strip():
            # Process text through AI model
            results = text_classifier(text[:512])  # Limit text length
            
            # Handle different response formats from the model
            spam_score = 0
            
            # Check if results is a list of lists (nested structure)
            if isinstance(results, list) and len(results) > 0:
                if isinstance(results[0], list):
                    # Nested structure
                    for result_group in results:
                        for score_dict in result_group:
                            if score_dict.get('label', '').upper() == 'SPAM':
                                spam_score = max(spam_score, score_dict.get('score', 0))
                else:
                    # Flat structure
                    for score_dict in results:
                        if score_dict.get('label', '').upper() == 'SPAM':
                            spam_score = max(spam_score, score_dict.get('score', 0))
            
            return spam_score * 100
            
    except Exception as e:
        st.warning(f"AI text analysis encountered an issue: {str(e)}")
        return fallback_text_analysis(text)
    
    return 50

def fallback_text_analysis(text):
    """Fallback analysis when AI model fails"""
    if not text.strip():
        return 50
    
    fraud_keywords = [
        'free', 'win', 'prize', 'urgent', 'password', 'verify', 'account', 
        'bank', 'pay', 'security', 'update', 'login', 'suspend', 'limited',
        'offer', 'claim', 'reward', 'bonus', 'selected', 'winner'
    ]
    
    text_lower = text.lower()
    keyword_count = sum(1 for word in fraud_keywords if word in text_lower)
    
    words = text_lower.split()
    if len(words) > 0:
        keyword_density = keyword_count / len(words)
        return min(95, keyword_density * 300)
    
    return 50

def ai_pattern_analysis(query):
    """AI-powered pattern analysis"""
    features = []
    
    # Length features
    features.append(len(query))
    
    # Digit ratio
    digit_count = sum(1 for char in query if char.isdigit())
    features.append(digit_count / len(query) if query else 0)
    
    # Special character ratio
    special_chars = sum(1 for char in query if not char.isalnum() and not char.isspace())
    features.append(special_chars / len(query) if query else 0)
    
    # Keyword analysis
    fraud_keywords = ['free', 'win', 'prize', 'urgent', 'password', 'verify', 
                     'account', 'bank', 'pay', 'security', 'update', 'login']
    keyword_count = sum(1 for word in fraud_keywords if word in query.lower())
    features.append(keyword_count)
    
    return features

def comprehensive_ai_analysis(query):
    """Comprehensive AI analysis of the query"""
    # Text analysis
    text_score = ai_text_analysis(query)
    
    # Pattern analysis
    pattern_features = ai_pattern_analysis(query)
    pattern_risk = sum(pattern_features) * 5  # Reduced weight
    
    # Web scraping verification
    scraped_matches = []
    for item in st.session_state.scraped_data:
        if query.lower() in str(item['value']).lower():
            scraped_matches.append(item)
    
    web_risk = len(scraped_matches) * 15  # Reduced weight
    
    # Risk calculation with balanced weights
    total_risk = min(100, text_score * 0.6 + pattern_risk + web_risk)
    
    if total_risk > 85:
        risk_level = "Critical"
    elif total_risk > 65:
        risk_level = "High"
    elif total_risk > 40:
        risk_level = "Medium"
    else:
        risk_level = "Low"
    
    return {
        "risk_score": round(total_risk, 1),
        "risk_level": risk_level,
        "text_analysis_score": round(text_score, 1),
        "pattern_analysis_score": round(pattern_risk, 1),
        "web_matches": len(scraped_matches),
        "scraped_data": scraped_matches
    }