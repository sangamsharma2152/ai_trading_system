import logging
import re
from functools import lru_cache
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

logger = logging.getLogger(__name__)

# Initialize geocoder
try:
    geolocator = Nominatim(user_agent="ai_trading_app", timeout=10)
except Exception as e:
    logger.error(f"Failed to initialize geocoder: {e}")
    geolocator = None

LOCATIONS = {
    "usa": (37.09, -95.71),
    "china": (35.86, 104.19),
    "russia": (61.52, 105.31),
    "ukraine": (48.37, 31.16),
    "india": (20.59, 78.96),
    "iran": (32.42, 53.68),
    "israel": (31.04, 34.85),
    "saudi": (23.88, 45.07),
    "uae": (23.42, 53.85),
    "germany": (51.17, 10.45),
    "france": (46.23, 2.21),
    "uk": (55.38, -3.44),
    "japan": (36.20, 138.25),
    "korea": (35.91, 127.77),
    "pakistan": (30.38, 69.35),
    "afghanistan": (33.94, 67.71),
}

def extract_locations(text):
    """Extract location keywords from text"""
    try:
        if not text or len(str(text).strip()) == 0:
            return []
        
        text = str(text).lower()
        locations = [k for k in LOCATIONS if re.search(rf"\b{k}\b", text)]
        logger.debug(f"Extracted locations: {locations}")
        return locations
    
    except Exception as e:
        logger.error(f"Error extracting locations: {e}")
        return []

@lru_cache(maxsize=100)
def get_coordinates(loc):
    """Get latitude and longitude for a location"""
    try:
        loc_lower = str(loc).lower().strip()
        
        # Check predefined locations first
        if loc_lower in LOCATIONS:
            return LOCATIONS[loc_lower]
        
        # Try geocoding
        if geolocator:
            try:
                location = geolocator.geocode(loc_lower)
                if location:
                    logger.debug(f"Geocoded {loc}: ({location.latitude}, {location.longitude})")
                    return location.latitude, location.longitude
            except (GeocoderTimedOut, GeocoderServiceError) as e:
                logger.warning(f"Geocoding error for {loc}: {e}")
        
        logger.warning(f"Could not find coordinates for {loc}")
        return None, None
    
    except Exception as e:
        logger.error(f"Error getting coordinates for {loc}: {e}")
        return None, None
