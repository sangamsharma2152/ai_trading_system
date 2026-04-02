import logging
import yfinance as yf
from config import API_TIMEOUT
import pandas as pd

logger = logging.getLogger(__name__)

# Cached prices as fallback
__price_cache = {
    "GC=F": 2080.00,  # Gold
    "SI=F": 24.50,    # Silver
    "CL=F": 82.00     # Oil
}

def safe_fetch(symbol):
    """Safely fetch market data with error handling and fallbacks"""
    try:
        logger.debug(f"Fetching market data for {symbol}")
        
        # Try 1-day data first
        try:
            data = yf.download(
                symbol,
                period="1d",
                progress=False,
                timeout=API_TIMEOUT,
                show_errors=False
            )
            
            if isinstance(data, pd.DataFrame) and not data.empty and "Close" in data.columns:
                close_price = float(data["Close"].dropna().iloc[-1])
                if close_price > 0:
                    logger.info(f"Successfully fetched price for {symbol}: ${close_price}")
                    __price_cache[symbol] = close_price  # Update cache
                    return close_price
        except Exception as e1:
            logger.debug(f"1D fetch failed for {symbol}: {e1}")
        
        # Try 1 month data
        try:
            data = yf.download(
                symbol,
                period="1mo",
                progress=False,
                timeout=API_TIMEOUT,
                show_errors=False
            )
            
            if isinstance(data, pd.DataFrame) and not data.empty and "Close" in data.columns:
                close_price = float(data["Close"].dropna().iloc[-1])
                if close_price > 0:
                    logger.info(f"Fetched via 1mo fallback for {symbol}: ${close_price}")
                    __price_cache[symbol] = close_price
                    return close_price
        except Exception as e2:
            logger.debug(f"1mo fetch failed for {symbol}: {e2}")
        
        # Use cached price if available
        if symbol in __price_cache:
            logger.warning(f"Using cached price for {symbol}: ${__price_cache[symbol]}")
            return __price_cache[symbol]
            
        logger.warning(f"No valid data found for {symbol}")
        return None

    except Exception as e:
        logger.error(f"Unexpected error fetching {symbol}: {e}")
        # Return cached price as last resort
        return __price_cache.get(symbol)


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
