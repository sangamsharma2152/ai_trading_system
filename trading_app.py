#!/usr/bin/env python
"""
War Intelligence Trading Dashboard
Analyzes geopolitical news and generates commodity trading signals
"""

import os
import sys
import logging
import traceback
from datetime import datetime, timedelta

# Initialize Streamlit secrets BEFORE any other imports
try:
    import streamlit as st
    if hasattr(st, 'secrets'):
        for key in st.secrets:
            os.environ[key] = st.secrets[key]
except Exception as e:
    print(f"Warning: Could not load Streamlit secrets: {e}")

# Now safe to import other modules
import pandas as pd
import plotly.graph_objects as go
from logging_config import setup_logging
from config import (
    NEWS_API_KEY, ALPHA_VANTAGE_API_KEY, API_TIMEOUT,
    get_config_value
)

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Import trading modules
try:
    from news_fetcher import fetch_geopolitical_news
    from sentiment import analyze_sentiment
    from market_data import get_prices, safe_fetch
    from event_detector import detect_events
    from nlp_engine import extract_locations
    from map_data import create_geopolitical_heatmap
    from model import predict
    from decision_engine import generate_trading_decisions
    from database import log_trade_event, get_recent_trades
except ImportError as e:
    logger.error(f"Import error: {e}")
    sys.exit(1)

# Page configuration
st.set_page_config(
    page_title="War Intelligence Trading Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin: 20px 0;
    }
    .metric-card {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .signal-buy {
        color: #00ff00;
        font-weight: bold;
    }
    .signal-sell {
        color: #ff0000;
        font-weight: bold;
    }
    .signal-hold {
        color: #ffaa00;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Header
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown('<div class="main-header">🌍 WAR INTELLIGENCE TRADING DASHBOARD</div>', unsafe_allow_html=True)

# Last updated timestamp
st.caption(f"⏰ Last Updated: {datetime.now().strftime('%H:%M:%S')}")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    refresh_interval = st.slider("Refresh Interval (seconds)", 10, 300, 60)
    
    show_sections = {
        "Market Prices": st.checkbox("Market Prices", value=True),
        "News Feed": st.checkbox("News Feed", value=True),
        "Sentiment Analysis": st.checkbox("Sentiment Analysis", value=True),
        "Trading Signals": st.checkbox("Trading Signals", value=True),
        "Geopolitical Heatmap": st.checkbox("Geopolitical Heatmap", value=True),
        "Trade History": st.checkbox("Trade History", value=True),
    }
    
    st.markdown("---")
    st.info("💡 This dashboard analyzes geopolitical news to generate commodity trading signals.")

# Main content
try:
    # Fetch market data
    if show_sections["Market Prices"]:
        st.subheader("📊 Market Prices")
        try:
            prices = get_prices()
            
            if prices and any(prices.values()):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if prices.get("gold"):
                        st.metric("Gold", f"${prices['gold']:.2f}", delta="Real-time")
                    else:
                        st.warning("Gold price unavailable")
                
                with col2:
                    if prices.get("silver"):
                        st.metric("Silver", f"${prices['silver']:.2f}", delta="Real-time")
                    else:
                        st.warning("Silver price unavailable")
                
                with col3:
                    if prices.get("oil"):
                        st.metric("Oil (WTI)", f"${prices['oil']:.2f}", delta="Real-time")
                    else:
                        st.warning("Oil price unavailable")
            else:
                st.error("❌ Unable to fetch market prices. Please try again later.")
                st.info("The market data service may be temporarily unavailable. This typically happens due to API rate limits or network issues.")
        except Exception as e:
            logger.error(f"Error fetching prices: {e}\n{traceback.format_exc()}")
            st.error(f"❌ Error fetching market prices: {str(e)}")
        
        st.markdown("---")
    
    # Fetch and display news
    if show_sections["News Feed"]:
        st.subheader("📰 Geopolitical News")
        try:
            news = fetch_geopolitical_news(limit=5)
            
            if news:
                for i, article in enumerate(news, 1):
                    with st.expander(f"📌 {article.get('title', 'No Title')[:80]}..."):
                        st.write(article.get("description", "No description"))
                        st.caption(f"Source: {article.get('source', 'Unknown')} | Published: {article.get('publishedAt', 'Unknown')}")
                        if article.get("url"):
                            st.markdown(f"[Read full article →]({article['url']})")
            else:
                st.info("No recent geopolitical news available.")
        except Exception as e:
            logger.warning(f"Error fetching news: {e}")
            st.warning(f"⚠️ Could not fetch news: {str(e)}")
        
        st.markdown("---")
    
    # Sentiment Analysis
    if show_sections["Sentiment Analysis"]:
        st.subheader("💭 Sentiment Analysis")
        try:
            news = fetch_geopolitical_news(limit=5)
            
            if news:
                sentiments = []
                for article in news:
                    text = f"{article.get('title', '')} {article.get('description', '')}"
                    sentiment = analyze_sentiment(text)
                    sentiments.append({
                        "Title": article.get("title", "Unknown")[:50],
                        "Sentiment": sentiment.get("label", "NEUTRAL"),
                        "Score": sentiment.get("score", 0.0)
                    })
                
                if sentiments:
                    sentiment_df = pd.DataFrame(sentiments)
                    st.dataframe(sentiment_df, use_container_width=True)
                    
                    # Sentiment distribution
                    sentiment_counts = sentiment_df["Sentiment"].value_counts()
                    fig = go.Figure(data=[
                        go.Bar(x=sentiment_counts.index, y=sentiment_counts.values)
                    ])
                    fig.update_layout(title="Sentiment Distribution", xaxis_title="Sentiment", yaxis_title="Count")
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No articles to analyze sentiment.")
        except Exception as e:
            logger.warning(f"Error analyzing sentiment: {e}")
            st.warning(f"⚠️ Sentiment analysis unavailable: {str(e)}")
        
        st.markdown("---")
    
    # Trading Signals
    if show_sections["Trading Signals"]:
        st.subheader("📈 Trading Signals")
        try:
            news = fetch_geopolitical_news(limit=3)
            
            if news and prices and any(prices.values()):
                signals = []
                
                for article in news:
                    text = f"{article.get('title', '')} {article.get('description', '')}"
                    sentiment = analyze_sentiment(text)
                    events = detect_events(text)
                    locations = extract_locations(text)
                    
                    # Generate predictions for each commodity
                    for commodity in ["gold", "silver", "oil"]:
                        try:
                            prediction = predict(text, commodity)
                            decision = generate_trading_decisions(
                                commodity=commodity,
                                sentiment=sentiment,
                                events=events,
                                locations=locations,
                                current_price=prices.get(commodity)
                            )
                            
                            signals.append({
                                "Commodity": commodity.upper(),
                                "Signal": prediction.get("action", "HOLD"),
                                "Confidence": f"{prediction.get('confidence', 0):.1%}",
                                "Event": events[0] if events else "GENERAL",
                                "Location": locations[0] if locations else "Global"
                            })
                        except Exception as e:
                            logger.debug(f"Error predicting for {commodity}: {e}")
                            continue
                
                if signals:
                    signals_df = pd.DataFrame(signals)
                    st.dataframe(signals_df, use_container_width=True)
                    
                    # Log trades
                    for signal in signals:
                        try:
                            log_trade_event(
                                commodity=signal["Commodity"],
                                signal=signal["Signal"],
                                confidence=float(signal["Confidence"].strip('%')) / 100,
                                event=signal["Event"]
                            )
                        except Exception as e:
                            logger.debug(f"Could not log trade: {e}")
                else:
                    st.info("No trading signals generated.")
            else:
                st.info("Waiting for market data and news to generate trading signals...")
        except Exception as e:
            logger.warning(f"Error generating signals: {e}")
            st.warning(f"⚠️ Trading signals unavailable: {str(e)}")
        
        st.markdown("---")
    
    # Geopolitical Heatmap
    if show_sections["Geopolitical Heatmap"]:
        st.subheader("🗺️ Geopolitical Event Heatmap")
        try:
            news = fetch_geopolitical_news(limit=10)
            
            if news:
                locations_list = []
                for article in news:
                    text = f"{article.get('title', '')} {article.get('description', '')}"
                    locations = extract_locations(text)
                    locations_list.extend(locations)
                
                if locations_list:
                    heatmap = create_geopolitical_heatmap(locations_list)
                    st.pydeck_chart(heatmap)
                else:
                    st.info("No location data extracted from news.")
            else:
                st.info("No news available for heatmap generation.")
        except Exception as e:
            logger.warning(f"Error creating heatmap: {e}")
            st.warning(f"⚠️ Heatmap unavailable: {str(e)}")
        
        st.markdown("---")
    
    # Trade History
    if show_sections["Trade History"]:
        st.subheader("📜 Recent Trade History")
        try:
            trades = get_recent_trades(limit=10)
            
            if trades:
                trades_df = pd.DataFrame(trades)
                st.dataframe(trades_df, use_container_width=True)
            else:
                st.info("No trade history available.")
        except Exception as e:
            logger.warning(f"Error fetching trades: {e}")
            st.info("Trade history not available yet.")

except Exception as e:
    logger.error(f"Unhandled error in main app: {e}\n{traceback.format_exc()}")
    st.error("❌ An unexpected error occurred. Please refresh the page.")
    st.error(f"Error details: {str(e)}")

# Auto-refresh
st.markdown(f"<p style='text-align: center; font-size: 0.8rem; color: gray;'>Auto-refreshing every {refresh_interval} seconds</p>", unsafe_allow_html=True)
import time
time.sleep(refresh_interval)
st.rerun()
