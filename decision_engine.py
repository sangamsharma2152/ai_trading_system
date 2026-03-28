def generate_decision(prediction, confidence):
    decisions = {}

    for asset, action in prediction.items():
        decisions[asset] = {
            "action": action,
            "confidence": round(abs(confidence) * 100, 2)
        }

    return decisions
    
