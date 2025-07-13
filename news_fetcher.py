import os
import requests
import logging

def fetch_trending_news():
    """Fetches trending news headlines using NewsAPI."""
    api_key = os.getenv("NEWS_API_KEY")
    url = f"https://newsapi.org/v2/top-headlines?language=en&pageSize=5&apiKey={api_key}"
    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        trends = []
        for article in data.get("articles", []):
            trends.append({
                "title": article.get("title", ""),
                "description": article.get("description", ""),
                "url": article.get("url", "")
            })
        return trends
    except Exception as e:
        logging.error(f"News fetch failed: {e}")
        return []