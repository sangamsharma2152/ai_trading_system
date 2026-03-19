import re

# Predefined location keywords (expandable)
LOCATION_KEYWORDS = {
    "usa": (37.0902, -95.7129),
    "america": (37.0902, -95.7129),
    "china": (35.8617, 104.1954),
    "russia": (61.5240, 105.3188),
    "ukraine": (48.3794, 31.1656),
    "india": (20.5937, 78.9629),
    "europe": (54.5260, 15.2551),
    "middle east": (25.276987, 55.296249),
    "iran": (32.4279, 53.6880),
    "iraq": (33.2232, 43.6793),
    "israel": (31.0461, 34.8516),
    "saudi": (23.8859, 45.0792),
}

def extract_locations(text):
    text = text.lower()
    found_locations = []

    for key in LOCATION_KEYWORDS:
        if re.search(rf"\b{key}\b", text):
            found_locations.append(key)

    return found_locations


def get_coordinates(location):
    return LOCATION_KEYWORDS.get(location, (None, None))
