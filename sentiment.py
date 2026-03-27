from transformers import pipeline

sentiment_model = pipeline("sentiment-analysis")

def analyze_sentiment(news_list):
    results = []

    for news in news_list:
        result = sentiment_model(news["title"])[0]
        results.append({
            "text": news["title"],
            "label": result["label"],
            "score": result["score"],
            "source": news["source"]
        })

    return results
    
