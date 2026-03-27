import pandas as pd
from nlp_engine import extract_locations, get_coordinates

def get_event_locations(news):
    data = []

    for n in news:
        locs = extract_locations(n["title"])

        for loc in locs:
            lat, lon = get_coordinates(loc)
            if lat:
                data.append({
                    "lat": lat,
                    "lon": lon,
                    "event": n["title"],
                    "location": loc.upper()
                })

    return pd.DataFrame(data)
    
