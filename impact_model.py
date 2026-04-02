import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

# Define event impact mapping
# Maps event types to asset-specific trading actions
IMPACT_MAP = {
    "GEOPOLITICAL": {
        "Gold": "BUY",
        "Oil": "BUY",
        "Silver": "HOLD"
    },
    "INFLATION": {
        "Gold": "BUY",
        "Silver": "BUY",
        "Oil": "HOLD"
    },
    "INTEREST_RATE": {
        "Gold": "SELL",
        "Silver": "SELL",
        "Oil": "HOLD"
    },
    "OIL_MARKET": {
        "Oil": "BUY",
        "Gold": "HOLD",
        "Silver": "HOLD"
    },
    "GENERAL": {
        "Gold": "HOLD",
        "Silver": "HOLD",
        "Oil": "HOLD"
    }
}

def map_impact(event_type: str, assets: List[str] = None) -> Dict:
    """
    Map an event type to specific asset impacts
    
    Args:
        event_type: Type of event (GEOPOLITICAL, INFLATION, etc.)
        assets: List of assets to get impact for (default: all)
    
    Returns:
        Dictionary mapping assets to trading actions
    """
    try:
        if not event_type:
            logger.warning("No event type provided")
            return {}
        
        event_type = event_type.upper()
        
        # Get impact for this event type
        if event_type not in IMPACT_MAP:
            logger.warning(f"Unknown event type: {event_type}, defaulting to GENERAL")
            impact = IMPACT_MAP.get("GENERAL", {})
        else:
            impact = IMPACT_MAP[event_type]
        
        # Filter by assets if provided
        if assets:
            impact = {asset: impact.get(asset, "HOLD") for asset in assets}
        
        logger.info(f"Event {event_type} impacts: {impact}")
        return impact
    
    except Exception as e:
        logger.error(f"Error mapping impact: {str(e)}")
        return {}


def get_asset_action(event_type: str, asset: str) -> str:
    """
    Get the recommended action for a specific asset given an event type
    
    Args:
        event_type: Type of event
        asset: Asset name (Gold, Silver, Oil)
    
    Returns:
        Trading action (BUY, SELL, HOLD)
    """
    try:
        event_type = event_type.upper()
        asset = asset.capitalize()
        
        if event_type not in IMPACT_MAP:
            logger.warning(f"Unknown event type: {event_type}")
            return "HOLD"
        
        action = IMPACT_MAP[event_type].get(asset, "HOLD")
        logger.info(f"Asset {asset} action for {event_type}: {action}")
        return action
    
    except Exception as e:
        logger.error(f"Error getting asset action: {str(e)}")
        return "HOLD"


def get_all_impacts() -> Dict:
    """Get the complete impact mapping"""
    return IMPACT_MAP.copy()
