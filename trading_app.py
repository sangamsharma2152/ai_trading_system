import streamlit as st
from streamlit_autorefresh import st_autorefresh

from news_fetcher import get_news
from sentiment import analyze_sentiment
from market_data import get_prices
from model import predict
from decision_engine import generate_decision
from event_detector import detect_event
from impact_model import map_impact

import yfinance as yf

# 🔄 Auto Refresh
st_autorefresh(interval=60000, key="refresh")

st.set_page_config(page_title="AI Trading System", layout="wide")
st.title("🌍 AI Commodity Intelligence Dashboard")

# Fetch Data
news = get_news()
sentiments = analyze_sentiment(news)
prices = get_prices()
prediction, confidence = predict(sentiments)
decisions = generate_decision(prediction, confidence)

# ======================
# 💰 LIVE PRICES
# ======================
st.header("💰 Live Market Prices")

col1, col2, col3 = st.columns(3)
col1.metric("Gold", prices["gold"])
col2.metric("Silver", prices["silver"])
col3.metric("Oil", prices["oil"])

# ======================
# 📊 CHARTS
# ======================
st.header("📊 Live Charts")

def plot_chart(symbol):
    data = yf.download(symbol, period="1d", interval="5m")
    st.line_chart(data["Close"], height=200)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Gold")
    plot_chart("GC=F")

with col2:
    st.subheader("Oil")
    plot_chart("CL=F")

# ======================
# 🧠 AI SIGNALS
# ======================
st.header("🤖 AI Trading Signals")

for asset, data in decisions.items():
    st.subheader(asset.upper())
    st.write(f"Action: {data['action']}")
    st.write(f"Confidence: {data['confidence']}%")

if confidence > 0.5:
    st.error("🚨 Strong Market Signal Detected!")

# ======================
# 🌍 NEWS FEED
# ======================
st.header("🌍 Global News Intelligence")

for s in sentiments:
    event = detect_event(s["text"])
    impact = map_impact(event)

    st.write(f"📰 {s['text']}")
    st.write(f"Source: {s['source']}")
    st.write(f"Sentiment: {s['label']} ({round(s['score'],2)})")
    st.write(f"Event: {event}")
    st.write(f"Impact: {impact}")
    st.write("---")
