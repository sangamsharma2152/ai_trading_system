import yfinance as yf

def get_prices():
    gold = yf.download("GC=F", period="1d", interval="1m")
    silver = yf.download("SI=F", period="1d", interval="1m")
    oil = yf.download("CL=F", period="1d", interval="1m")

    return {
        "gold": gold["Close"].iloc[-1],
        "silver": silver["Close"].iloc[-1],
        "oil": oil["Close"].iloc[-1]
    }
