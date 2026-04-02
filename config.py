import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ⚙️ API KEYS (from environment variables for security)
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")

# Validate that critical API keys are set
if not NEWS_API_KEY:
    logging.warning("NEWS_API_KEY not set in environment variables")
if not ALPHA_VANTAGE_API_KEY:
    logging.warning("ALPHA_VANTAGE_API_KEY not set in environment variables")

# ⚙️ NEWS CONFIGURATION
NEWS_LIMIT = int(os.getenv("NEWS_LIMIT", 20))
REFRESH_INTERVAL = int(os.getenv("REFRESH_INTERVAL", 60000))  # in ms

# ⚙️ TRADING THRESHOLDS
POS_THRESHOLD = float(os.getenv("POS_THRESHOLD", 0.2))
NEG_THRESHOLD = float(os.getenv("NEG_THRESHOLD", -0.2))

# ⚙️ API CONFIGURATION
API_TIMEOUT = int(os.getenv("API_TIMEOUT", 10))  # seconds
NEWS_API_RETRY_COUNT = int(os.getenv("NEWS_API_RETRY_COUNT", 3))

# ⚙️ LOGGING CONFIGURATION
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ⚙️ DATABASE CONFIGURATION
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///trading_history.db")

# ⚙️ TRADING PARAMETERS
MAX_POSITION_SIZE = int(os.getenv("MAX_POSITION_SIZE", 1000))
STOP_LOSS_PERCENTAGE = float(os.getenv("STOP_LOSS_PERCENTAGE", 5.0))
TAKE_PROFIT_PERCENTAGE = float(os.getenv("TAKE_PROFIT_PERCENTAGE", 10.0))

# ⚙️ MODEL CONFIGURATION
SENTIMENT_MODEL = os.getenv("SENTIMENT_MODEL", "ProsusAI/finbert")
