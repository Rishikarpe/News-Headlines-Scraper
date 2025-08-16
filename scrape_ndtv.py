import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scrape_ndtv_rss():
    url = "https://feeds.feedburner.com/ndtvnews-top-stories"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "xml")

    data = []
    for item in soup.find_all("item")[:12]:
        title = item.title.get_text(strip=True)
        link = item.link.get_text(strip=True)
        summary = item.description.get_text(strip=True) if item.description else None
        date = datetime.now().strftime("%Y-%m-%d")
        data.append({"title": title, "summary": summary, "date": date, "url": link})

    df = pd.DataFrame(data)
    df.to_csv("ndtv_headlines.csv", index=False, encoding="utf-8")
    print(f"Saved {len(df)} headlines from RSS!")

scrape_ndtv_rss()
