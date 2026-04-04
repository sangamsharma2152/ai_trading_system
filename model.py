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

def predict(data, commodity=None):
    """
    Generate trading prediction based on sentiment or text
    
    Args:
        data: Either a sentiment dict/str with score, or a list of sentiments, or raw text
        commodity: Optional commodity name (for context)
    
    Returns:
        Prediction object with action and confidence
    """
    try:
        # Handle different input types
        if isinstance(data, str):
            # It's raw text, treat it as a single sentiment item
            scores = [0.0]  # Default score for text
        elif isinstance(data, dict):
            # Single sentiment dict
            if 'score' in data:
                scores = [data['score']]
            else:
                scores = [0.0]
        elif isinstance(data, list):
            # List of sentiments
            scores = []
            for sentiment in data:
                if isinstance(sentiment, dict) and 'score' in sentiment:
                    scores.append(sentiment['score'])
                elif hasattr(sentiment, 'score'):
                    scores.append(sentiment.score)
        else:
            logger.warning(f"Unknown data type for prediction: {type(data)}")
            return Prediction("HOLD", 0.0, {"reason": "Unknown data type"})
        
        if not scores or all(s == 0.0 for s in scores):
            logger.debug(f"No sentiment scores found for {commodity or 'unknown'} commodity")
            return Prediction("HOLD", 50.0, {"reason": "Insufficient data"})
        
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
        
        commodity_str = f" for {commodity}" if commodity else ""
        logger.debug(f"Prediction{commodity_str}: {action} (confidence: {confidence:.2f}%)")
        
        return Prediction(
            action=action,
            confidence=confidence,
            details={
                "avg_sentiment": avg_sentiment,
                "num_scores": len(scores),
                "threshold_pos": POS_THRESHOLD,
                "threshold_neg": NEG_THRESHOLD,
                "commodity": commodity
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
