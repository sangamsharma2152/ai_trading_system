import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

# Define thresholds for predictions
POS_THRESHOLD = 0.2
NEG_THRESHOLD = -0.2

class Prediction:
    """Trading prediction object"""
    def __init__(self, action: str, confidence: float, details: Dict = None):
        self.action = action  # BUY, SELL, HOLD
        self.confidence = confidence
        self.details = details or {}

def predict(sentiments: List[Dict]) -> Prediction:
    """
    Generate trading prediction based on sentiment analysis
    
    Args:
        sentiments: List of sentiment dictionaries with 'score' and 'label'
    
    Returns:
        Prediction object with action and confidence
    """
    try:
        if not sentiments:
            logger.warning("No sentiments provided for prediction")
            return Prediction("HOLD", 0.0, {"reason": "No sentiment data"})
        
        # Extract scores from sentiment objects
        scores = []
        for sentiment in sentiments:
            if isinstance(sentiment, dict) and 'score' in sentiment:
                scores.append(sentiment['score'])
            elif hasattr(sentiment, 'score'):
                scores.append(sentiment.score)
        
        if not scores:
            logger.warning("No valid sentiment scores found")
            return Prediction("HOLD", 0.0, {"reason": "No valid scores"})
        
        # Calculate average sentiment
        avg_sentiment = sum(scores) / len(scores)
        
        # Determine action based on threshold
        if avg_sentiment > POS_THRESHOLD:
            action = "BUY"
            confidence = min(avg_sentiment * 100, 100)
        elif avg_sentiment < NEG_THRESHOLD:
            action = "SELL"
            confidence = min(abs(avg_sentiment) * 100, 100)
        else:
            action = "HOLD"
            confidence = 50.0 if avg_sentiment >= 0 else 25.0
        
        logger.info(f"Prediction: {action} (confidence: {confidence:.2f}%)")
        
        return Prediction(
            action=action,
            confidence=confidence,
            details={
                "avg_sentiment": avg_sentiment,
                "num_articles": len(scores),
                "threshold_pos": POS_THRESHOLD,
                "threshold_neg": NEG_THRESHOLD
            }
        )
    
    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}")
        return Prediction("HOLD", 0.0, {"error": str(e)})


def get_prediction_details(prediction: Prediction) -> Dict:
    """Get detailed information about a prediction"""
    return {
        "action": prediction.action,
        "confidence": prediction.confidence,
        "details": prediction.details
    }
