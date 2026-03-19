from geopy.geocoders import Nominatim
from functools import lru_cache

geolocator = Nominatim(user_agent="ai_trading_app")

@lru_cache(maxsize=100)
def get_coordinates(location):
    try:
        loc = geolocator.geocode(location)
        if loc:
            return loc.latitude, loc.longitude
    except:
        return None, None

    return None, None
