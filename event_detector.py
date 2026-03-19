def detect_event(text):
    text = text.lower()

    if "war" in text or "conflict" in text:
        return "GEOPOLITICAL"
    elif "inflation" in text:
        return "INFLATION"
    elif "interest rate" in text:
        return "INTEREST_RATE"
    elif "oil" in text:
        return "OIL_MARKET"
    else:
        return "GENERAL"
