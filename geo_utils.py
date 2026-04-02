import logging
from geopy.geocoders import Nominatim
from functools import lru_cache

logger = logging.getLogger(__name__)

try:
    geolocator = Nominatim(user_agent="ai_trading_app", timeout=10)
except Exception as e:
    logger.error(f"Failed to initialize geocoder: {e}")
    geolocator = None

@lru_cache(maxsize=100)
def get_coordinates(location):
    """Get coordinates with error handling"""
    try:
        if not location or len(str(location).strip()) == 0:
            logger.warning("Empty location provided")
            return None, None
        
        if not geolocator:
            logger.error("Geocoder not initialized")
            return None, None
        
        loc = geolocator.geocode(str(location))
        if loc:
            logger.debug(f"Found coordinates for {location}: ({loc.latitude}, {loc.longitude})")
            return loc.latitude, loc.longitude
        else:
            logger.warning(f"No coordinates found for {location}")
            return None, None
    
    except Exception as e:
        logger.error(f"Error getting coordinates for {location}: {e}")
        return None, None
