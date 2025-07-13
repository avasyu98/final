import requests
import os
import logging

def fetch_news_trends():
    api_key = os.getenv("NEWS_API_KEY")
    url = f"https://newsapi.org/v2/top-headlines?language=en&pageSize=5&apiKey={api_key}"
    r = requests.get(url)
    if r.status_code == 200:
        articles = r.json().get("articles", [])
        return [
            {"title": a["title"], "category": "news", "description": a.get("description", "")} 
            for a in articles if a.get("title")
        ]
    else:
        logging.error(f"News API failed: {r.text}")
        return []

def fetch_trending_topics():
    try:
        news = fetch_news_trends()
        return news
    except Exception as e:
        logging.error(f"Error fetching trends: {e}")
        return []