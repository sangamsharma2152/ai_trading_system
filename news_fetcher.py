import requests
from config import NEWS_API_KEY

def get_news():
    url = f"https://newsapi.org/v2/top-headlines?category=business&language=en&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()

    articles = []
    for article in data["articles"][:10]:
        articles.append(article["title"])

    return articles
