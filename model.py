import logging
from config import POS_THRESHOLD, NEG_THRESHOLD

logger = logging.getLogger(__name__)

def predict(sentiments):
    """Generate trading predictions with error handling"""
    if not sentiments or len(sentiments) == 0:
        logger.warning("No sentiment data provided for prediction")
        return {
            "gold": "HOLD",
            "silver": "HOLD",
            "oil": "HOLD"
        }, 0.0
    
    try:
        score = 0
        
        for s in sentiments:
            try:
                label = s.get("label", "NEUTRAL")
                sentiment_score = s.get("score", 0)
                
                if label == "POSITIVE":
                    score += abs(sentiment_score)
                elif label == "NEGATIVE":
                    score -= abs(sentiment_score)
                # NEUTRAL scores don't contribute
            
            except Exception as e:
                logger.warning(f"Error processing sentiment entry: {e}")
                continue
        
        # Calculate average score
        avg_score = score / len(sentiments) if len(sentiments) > 0 else 0
        
        # Determine action based on thresholds
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
        
        logger.info(f"Prediction generated - Action: {action}, Confidence: {avg_score:.4f}")
        return prediction, avg_score
    
    except Exception as e:
        logger.error(f"Error generating prediction: {e}")
        return {
            "gold": "HOLD",
            "silver": "HOLD",
            "oil": "HOLD"
        }, 0.0
