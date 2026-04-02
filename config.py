import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Try to import Streamlit secrets for cloud deployment
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

def get_config_value(key, default=""):
    """Get config value from Streamlit secrets or environment variables"""
    try:
        if HAS_STREAMLIT:
            # Try Streamlit secrets first (for Streamlit Cloud)
            return st.secrets.get(key, os.getenv(key, default))
    except:
        pass
    # Fall back to environment variables
    return os.getenv(key, default)

# ⚙️ API KEYS (from environment variables or Streamlit secrets)
NEWS_API_KEY = get_config_value("NEWS_API_KEY", "")
ALPHA_VANTAGE_API_KEY = get_config_value("ALPHA_VANTAGE_API_KEY", "")
HUGGINGFACE_API_KEY = get_config_value("HUGGINGFACE_API_KEY", "")

# Validate that critical API keys are set
if not NEWS_API_KEY:
    logging.warning("NEWS_API_KEY not set in environment variables or Streamlit secrets")
if not ALPHA_VANTAGE_API_KEY:
    logging.warning("ALPHA_VANTAGE_API_KEY not set in environment variables or Streamlit secrets")

# ⚙️ NEWS CONFIGURATION
NEWS_LIMIT = int(get_config_value("NEWS_LIMIT", "20"))
REFRESH_INTERVAL = int(get_config_value("REFRESH_INTERVAL", "60000"))  # in ms

# ⚙️ TRADING THRESHOLDS
POS_THRESHOLD = float(get_config_value("POS_THRESHOLD", "0.2"))
NEG_THRESHOLD = float(get_config_value("NEG_THRESHOLD", "-0.2"))

# ⚙️ API CONFIGURATION
API_TIMEOUT = int(get_config_value("API_TIMEOUT", "10"))  # seconds
NEWS_API_RETRY_COUNT = int(get_config_value("NEWS_API_RETRY_COUNT", "3"))

# ⚙️ LOGGING CONFIGURATION
DEBUG = get_config_value("DEBUG", "False").lower() == "true"
LOG_LEVEL = get_config_value("LOG_LEVEL", "INFO")

# ⚙️ DATABASE CONFIGURATION
DATABASE_URL = get_config_value("DATABASE_URL", "sqlite:///trading_history.db")

# ⚙️ TRADING PARAMETERS
MAX_POSITION_SIZE = int(get_config_value("MAX_POSITION_SIZE", "1000"))
STOP_LOSS_PERCENTAGE = float(get_config_value("STOP_LOSS_PERCENTAGE", "5.0"))
TAKE_PROFIT_PERCENTAGE = float(get_config_value("TAKE_PROFIT_PERCENTAGE", "10.0"))

# ⚙️ MODEL CONFIGURATION
SENTIMENT_MODEL = get_config_value("SENTIMENT_MODEL", "ProsusAI/finbert")
