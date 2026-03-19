import yfinance as yf

def get_prices():
    gold = yf.download("GC=F", period="1d", interval="1m")
    silver = yf.download("SI=F", period="1d", interval="1m")
    oil = yf.download("CL=F", period="1d", interval="1m")

    return {
        "gold": float(gold["Close"].iloc[-1]),
        "silver": float(silver["Close"].iloc[-1]),
        "oil": float(oil["Close"].iloc[-1])
    }
