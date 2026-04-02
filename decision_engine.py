import logging

logger = logging.getLogger(__name__)

def generate_decision(prediction, confidence):
    """Generate trading decisions with error handling"""
    try:
        if not prediction:
            logger.warning("No prediction data provided")
            return {}
        
        decisions = {}
        
        for asset, action in prediction.items():
            try:
                decisions[asset] = {
                    "action": action,
                    "confidence": round(abs(confidence) * 100, 2),
                    "status": "ACTIVE"
                }
            except Exception as e:
                logger.error(f"Error generating decision for {asset}: {e}")
                decisions[asset] = {
                    "action": "HOLD",
                    "confidence": 0.0,
                    "status": "ERROR"
                }
        
        logger.info(f"Generated decisions for {len(decisions)} assets")
        return decisions
    
    except Exception as e:
        logger.error(f"Error generating decisions: {e}")
        return {}
