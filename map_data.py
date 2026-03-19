import pandas as pd
from nlp_engine import extract_locations, get_coordinates

def get_event_locations(news):
    data = []

    for n in news:
        locations = extract_locations(n["title"])

        for loc in locations:
            lat, lon = get_coordinates(loc)

            if lat and lon:
                data.append({
                    "lat": lat,
                    "lon": lon,
                    "event": n["title"],
                    "location": loc.upper()
                })

    return pd.DataFrame(data)
