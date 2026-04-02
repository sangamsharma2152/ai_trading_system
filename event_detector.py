import logging

logger = logging.getLogger(__name__)

def detect_event(text):
    """Detect geopolitical and economic events with error handling"""
    try:
        if not text or len(str(text).strip()) == 0:
            logger.warning("Empty text provided for event detection")
            return "GENERAL"
        
        text = str(text).lower()

        if "war" in text or "conflict" in text or "military" in text:
            logger.debug("Geopolitical event detected")
            return "GEOPOLITICAL"
        elif "inflation" in text or "price surge" in text:
            logger.debug("Inflation event detected")
            return "INFLATION"
        elif "interest rate" in text or "fed" in text or "central bank" in text:
            logger.debug("Interest rate event detected")
            return "INTEREST_RATE"
        elif "oil" in text or "crude" in text or "energy" in text:
            logger.debug("Oil market event detected")
            return "OIL_MARKET"
        else:
            logger.debug("General economic event detected")
            return "GENERAL"
    
    except Exception as e:
        logger.error(f"Error detecting event: {e}")
        return "GENERAL"
