import streamlit as st
from news_fetcher import get_news
from sentiment import analyze_sentiment
from market_data import get_prices
from model import predict
from decision_engine import generate_decision

st.set_page_config(page_title="AI Trading System", layout="wide")

st.title("📈 AI Commodity Trading Assistant")

# Fetch data
news = get_news()
sentiments = analyze_sentiment(news)
prices = get_prices()
prediction, confidence = predict(sentiments, prices)
decisions = generate_decision(prediction, confidence)

# 🔥 Display Prices
st.header("💰 Live Prices")
col1, col2, col3 = st.columns(3)

col1.metric("Gold", prices["gold"])
col2.metric("Silver", prices["silver"])
col3.metric("Oil", prices["oil"])

# 📰 News
st.header("📰 Latest News")
for s in sentiments:
    st.write(f"{s['text']}")
    st.write(f"Sentiment: {s['label']} ({round(s['score'],2)})")
    st.write("---")

# 🤖 Predictions
st.header("🤖 AI Predictions")
for asset, data in decisions.items():
    st.subheader(f"{asset.upper()}")
    st.write(f"Action: {data['action']}")
    st.write(f"Confidence: {data['confidence']}%")
