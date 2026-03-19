import streamlit as st
from streamlit_autorefresh import st_autorefresh

# Core modules
from news_fetcher import get_news
from sentiment import analyze_sentiment
from market_data import get_prices
from model import predict
from decision_engine import generate_decision
from event_detector import detect_event
from impact_model import map_impact

# Map + NLP
from map_data import get_event_locations

# Charts
import yfinance as yf
import pydeck as pdk

# ==============================
# ⚙️ PAGE CONFIG
# ==============================
st.set_page_config(page_title="AI Trading System", layout="wide")

# 🔄 Auto Refresh (every 60 sec)
st_autorefresh(interval=60000, key="refresh")

st.title("🌍 AI Commodity Intelligence Dashboard")

# ==============================
# 📡 FETCH DATA
# ==============================
news = get_news()
sentiments = analyze_sentiment(news)
prices = get_prices()
prediction, confidence = predict(sentiments)
decisions = generate_decision(prediction, confidence)

# ==============================
# 💰 LIVE PRICES
# ==============================
st.header("💰 Live Market Prices")

col1, col2, col3 = st.columns(3)
col1.metric("Gold", prices["gold"])
col2.metric("Silver", prices["silver"])
col3.metric("Oil", prices["oil"])

# ==============================
# 📊 CHARTS
# ==============================
st.header("📊 Live Charts")

def plot_chart(symbol):
    data = yf.download(symbol, period="1d", interval="5m")
    st.line_chart(data["Close"], height=200)

c1, c2 = st.columns(2)

with c1:
    st.subheader("Gold Price")
    plot_chart("GC=F")

with c2:
    st.subheader("Oil Price")
    plot_chart("CL=F")

# ==============================
# 🤖 AI SIGNALS
# ==============================
st.header("🤖 AI Trading Signals")

for asset, data in decisions.items():
    st.subheader(asset.upper())
    st.write(f"Action: {data['action']}")
    st.write(f"Confidence: {data['confidence']}%")

if confidence > 0.5:
    st.error("🚨 Strong Market Signal Detected!")

# ==============================
# 🌍 GLOBAL EVENT MAP (ADVANCED)
# ==============================
st.header("🌍 Global Event Intelligence Map")

map_df = get_event_locations(news)

if not map_df.empty:

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_df,
        get_position='[lon, lat]',
        get_color='[255, 0, 0, 180]',  # red points
        get_radius=300000,
        pickable=True
    )

    view_state = pdk.ViewState(
        latitude=20,
        longitude=0,
        zoom=1,
    )

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={
            "html": "<b>Location:</b> {location}<br/><b>Event:</b> {event}",
            "style": {"backgroundColor": "black", "color": "white"}
        }
    )

    st.pydeck_chart(deck)

else:
    st.warning("No location data available from news")

# ==============================
# 📰 GLOBAL NEWS FEED
# ==============================
st.header("📰 Global News Intelligence")

for s in sentiments:
    event = detect_event(s["text"])
    impact = map_impact(event)

    st.write(f"📰 {s['text']}")
    st.write(f"Source: {s['source']}")
    st.write(f"Sentiment: {s['label']} ({round(s['score'],2)})")
    st.write(f"Event Type: {event}")
    st.write(f"Market Impact: {impact}")
    st.write("---")
