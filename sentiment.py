from transformers import pipeline

# Load once
sentiment_model = pipeline("sentiment-analysis")

def analyze_sentiment(news_list):
    results = []

    for news in news_list:
        result = sentiment_model(news)[0]
        results.append({
            "text": news,
            "label": result["label"],
            "score": result["score"]
        })

    return results
