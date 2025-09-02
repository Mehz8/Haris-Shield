import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_fraud_samples():
    url = "https://rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx"  # RBI press releases
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    data = []
    for li in soup.select("a"):
        title = li.get_text(strip=True)
        link = li.get("href")

        if "fraud" in title.lower() or "scam" in title.lower():
            data.append({
                "title": title,
                "link": f"https://rbi.org.in{link}" if link and link.startswith("/") else link,
                "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

    df = pd.DataFrame(data)
    df.to_csv("fraud_data.csv", index=False)
    return df


if __name__ == "__main__":
    df = scrape_fraud_samples()
    print(df.head())
