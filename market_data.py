import logging
import yfinance as yf
from config import API_TIMEOUT

logger = logging.getLogger(__name__)

def safe_fetch(symbol):
    """Safely fetch market data with error handling"""
    try:
        logger.debug(f"Fetching market data for {symbol}")
        
        data = yf.download(
            symbol,
            period="1d",
            interval="1m",
            progress=False,
            timeout=API_TIMEOUT
        )

        if data.empty:
            logger.warning(f"No 1-minute data for {symbol}, falling back to 5-day data")
            data = yf.download(symbol, period="5d", progress=False)

        if data.empty or "Close" not in data.columns:
            logger.warning(f"No valid data found for {symbol}")
            return None

        close_price = float(data["Close"].dropna().iloc[-1])
        logger.info(f"Successfully fetched price for {symbol}: ${close_price}")
        return close_price

    except yf.exceptions.YFinanceException as e:
        logger.error(f"YFinance error for {symbol}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error fetching {symbol}: {e}")
        return None


def get_prices():
    """Get current prices for commodities with error handling"""
    try:
        logger.info("Fetching commodity prices")
        
        prices = {
            "gold": safe_fetch("GC=F"),
            "silver": safe_fetch("SI=F"),
            "oil": safe_fetch("CL=F")
        }
        
        # Log which prices were successful
        successful = [k for k, v in prices.items() if v is not None]
        logger.info(f"Successfully fetched prices for: {', '.join(successful) if successful else 'none'}")
        
        return prices
    
    except Exception as e:
        logger.error(f"Error fetching market prices: {e}")
        return {
            "gold": None,
            "silver": None,
            "oil": None
        }
