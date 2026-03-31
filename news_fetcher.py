import requests
from config import NEWS_API_KEY, NEWS_LIMIT

def get_news():
    url = f"https://newsapi.org/v2/everything?q=gold OR oil OR inflation OR war OR economy&language=en&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    
    response = requests.get(url)
    data = response.json()

    articles = []
    for article in data["articles"][:NEWS_LIMIT]:
        articles.append({
            "title": article["title"],
            "source": article["source"]["name"]
        })

    return articles

