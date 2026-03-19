import numpy as np

def predict(sentiments, prices):
    score = 0

    for s in sentiments:
        if s["label"] == "POSITIVE":
            score += s["score"]
        else:
            score -= s["score"]

    avg_score = score / len(sentiments)

    # Simple logic (you can upgrade later)
    prediction = {}

    if avg_score > 0.2:
        prediction["gold"] = "BUY"
        prediction["silver"] = "BUY"
        prediction["oil"] = "BUY"
    elif avg_score < -0.2:
        prediction["gold"] = "SELL"
        prediction["silver"] = "SELL"
        prediction["oil"] = "SELL"
    else:
        prediction["gold"] = "HOLD"
        prediction["silver"] = "HOLD"
        prediction["oil"] = "HOLD"

    return prediction, avg_score
