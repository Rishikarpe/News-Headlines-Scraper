import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def scrape_abpnews():
    # News URL:
    url = "https://news.abplive.com/"
    # Downloads HTML
    response = requests.get(url)
    response.raise_for_status()
    # Parsing HTML
    soup = BeautifulSoup(response.text, "lxml") 
    # Creates an empty list where we’ll store dictionaries of scraped news data
    data = []
    # Select hero headlines (main news cards on ABP homepage)
    articles = soup.select("a div.__hero_news_title")
    for article in articles[:12]:  # scrape first 12 headlines
        title = article.get_text(strip=True)
        parent_a = article.find_parent("a")
        link = parent_a["href"] if parent_a and parent_a.has_attr("href") else None
        summary = None
        if link:
            try:
                #Fetch each article page
                article_response = requests.get(link, timeout=10)
                article_response.raise_for_status()
                article_soup = BeautifulSoup(article_response.text, "lxml")
                #ABP articles have content inside <div class="articlebody"> or <p>
                summary_tag = article_soup.select_one("div.articlebody p") or article_soup.find("p")
                if summary_tag:
                    summary = summary_tag.get_text(strip=True)
            except Exception as e:
                print(f"Could not fetch summary for {link}: {e}")
        date = datetime.now().strftime("%Y-%m-%d")
        # Save data in dictionary format
        data.append({"title": title, "summary": summary, "date": date})
    # Converts the list of dictionaries into a Pandas DataFrame
    df = pd.DataFrame(data)
    # Saves the DataFrame into a CSV file
    df.to_csv("abpnews_headlines.csv", index=False, encoding="utf-8")
    # Print number of headlines scraped 
    print(f"Saved {len(df)} headlines!")
scrape_abpnews()