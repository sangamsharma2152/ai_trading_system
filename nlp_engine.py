import re

LOCATIONS = {
    "usa": (37.09, -95.71),
    "china": (35.86, 104.19),
    "russia": (61.52, 105.31),
    "ukraine": (48.37, 31.16),
    "india": (20.59, 78.96),
    "iran": (32.42, 53.68),
    "israel": (31.04, 34.85),
    "saudi": (23.88, 45.07)
}

def extract_locations(text):
    text = text.lower()
    return [k for k in LOCATIONS if re.search(rf"\b{k}\b", text)]

def get_coordinates(loc):
    return LOCATIONS.get(loc, (None, None))
    
