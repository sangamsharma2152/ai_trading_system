import streamlit as st
from streamlit_autorefresh import st_autorefresh
import yfinance as yf
import plotly.graph_objects as go
import pydeck as pdk
import datetime
import logging

# Setup logging first
import logging_config
logger = logging.getLogger(__name__)

from news_fetcher import get_news
from sentiment import analyze_sentiment
from market_data import get_prices
from model import predict
from decision_engine import generate_decision
from event_detector import detect_event
from impact_model import map_impact
from map_data import get_event_locations

# ==============================
# ⚙️ PAGE CONFIG
# ==============================
st.set_page_config(page_title="AI Trading System", layout="wide")

# ==============================
# 🎨 WAR DASHBOARD UI
# ==============================
st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: white;
}
h1, h2, h3 {
    color: #00ffcc;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# 🔄 AUTO REFRESH
# ==============================
st_autorefresh(interval=60000, key="refresh")

# ==============================
# 🏷️ TITLE
# ==============================
st.title("🌍 WAR INTELLIGENCE TRADING DASHBOARD")

# ==============================
# 🕒 TIME
# ==============================
st.write(f"🕒 Last Updated: {datetime.datetime.now().strftime('%H:%M:%S')}")

# ==============================
# 📡 FETCH DATA
# ==============================
try:
    logger.info("Starting data fetch...")
    
    news = get_news()
    if not news:
        st.warning("⚠️ Unable to fetch news. Please check your API configuration.")
        logger.warning("No news fetched")
        news = []
    else:
        logger.info(f"Fetched {len(news)} news articles")
    
    sentiments = analyze_sentiment(news)
    if not sentiments:
        st.warning("⚠️ Unable to analyze sentiment. No sentiment data available.")
        logger.warning("No sentiments analyzed")
        sentiments = []
    else:
        logger.info(f"Analyzed sentiment for {len(sentiments)} articles")
    
    prices = get_prices()
    if not prices or all(v is None for v in prices.values()):
        st.error("❌ Unable to fetch market prices. Please try again later.")
        logger.error("Failed to fetch market prices")
        st.stop()
    
    prediction, confidence = predict(sentiments)
    decisions = generate_decision(prediction, confidence)
    
    logger.info(f"Generated decisions with confidence: {confidence:.4f}")

except Exception as e:
    logger.error(f"Error during data fetch: {e}", exc_info=True)
    st.error(f"❌ Error fetching data: {e}")
    st.stop()

# ==============================
# 🚨 ALERT SYSTEM
# ==============================
if confidence > 0.5:
    st.error("🚨 HIGH RISK MARKET — VOLATILITY EXPECTED")
else:
    st.success("🟢 MARKET STABLE")

# ==============================
# 💰 LIVE PRICES (SAFE)
# ==============================
st.header("💰 LIVE MARKET")

col1, col2, col3 = st.columns(3)

col1.metric("Gold", prices["gold"] if prices["gold"] else "N/A")
col2.metric("Silver", prices["silver"] if prices["silver"] else "N/A")
col3.metric("Oil", prices["oil"] if prices["oil"] else "N/A")

# ==============================
# 📊 INTERACTIVE CHART
# ==============================
st.header("📊 MARKET ANALYSIS (1 YEAR)")

def plot_chart(symbol, title):
    data = yf.download(symbol, period="1y")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data.index,
        y=data["Close"],
        mode='lines',
        name='Price'
    ))

    fig.update_layout(
        template="plotly_dark",
        title=title
    )

    st.plotly_chart(fig, use_container_width=True)

c1, c2 = st.columns(2)

with c1:
    plot_chart("GC=F", "Gold - 1 Year")

with c2:
    plot_chart("CL=F", "Oil - 1 Year")

# ==============================
# 🎯 AI SIGNALS
# ==============================
st.header("🎯 AI SIGNAL MATRIX")

for asset, data in decisions.items():
    color = "🟢" if data["action"] == "BUY" else "🔴" if data["action"] == "SELL" else "🟡"

    st.markdown(f"""
    ### {asset.upper()}
    Signal: {color} **{data['action']}** 

    Confidence: {data['confidence']}%
    """)

# ==============================
# 🌍 GLOBAL MAP (HEATMAP)
# ==============================
st.header("🌍 GLOBAL EVENT MAP")

map_df = get_event_locations(news)

if not map_df.empty:
    layer = pdk.Layer(
        "HeatmapLayer",
        data=map_df,
        get_position='[lon, lat]',
        radiusPixels=80,
    )

    view_state = pdk.ViewState(
        latitude=20,
        longitude=0,
        zoom=1,
    )

    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state
    ))

else:
    st.warning("No location data available")

# ==============================
# 🧠 NEWS INTELLIGENCE
# ==============================
st.header("🧠 GLOBAL INTELLIGENCE FEED")

for s in sentiments:
    event = detect_event(s["text"])
    impact = map_impact(event)

    color = "🔴" if s["label"] == "NEGATIVE" else "🟢"

    st.markdown(f"""
    {color} **{s['text']}**  
    📍 Source: {s['source']}  
    🧠 Event: {event}  
    🎯 Impact: {impact}  
    """)

    st.markdown("---")
