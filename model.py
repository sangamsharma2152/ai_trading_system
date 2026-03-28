from config import POS_THRESHOLD, NEG_THRESHOLD

def predict(sentiments):
    score = 0

    for s in sentiments:
        if s["label"] == "POSITIVE":
            score += s["score"]
        else:
            score -= s["score"]

    avg_score = score / len(sentiments)

    prediction = {}

    if avg_score > POS_THRESHOLD:
        action = "BUY"
    elif avg_score < NEG_THRESHOLD:
        action = "SELL"
    else:
        action = "HOLD"

    prediction = {
        "gold": action,
        "silver": action,
        "oil": action
    }

    return prediction, avg_score
    
