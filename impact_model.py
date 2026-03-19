def map_impact(event):
    impact = {
        "GEOPOLITICAL": {"gold": "BUY", "oil": "BUY"},
        "INFLATION": {"gold": "BUY"},
        "INTEREST_RATE": {"gold": "SELL"},
        "OIL_MARKET": {"oil": "BUY"}
    }

    return impact.get(event, {})
