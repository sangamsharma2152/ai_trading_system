import yfinance as yf

def safe_fetch(symbol):
    try:
        data = yf.download(symbol, period="1d", interval="1m")

        if data.empty:
            data = yf.download(symbol, period="5d")  # fallback

        if data.empty or "Close" not in data:
            return None

        return float(data["Close"].dropna().iloc[-1])

    except:
        return None


def get_prices():
    return {
        "gold": safe_fetch("GC=F"),
        "silver": safe_fetch("SI=F"),
        "oil": safe_fetch("CL=F")
    }
    
