import logging
import pandas as pd
from nlp_engine import extract_locations, get_coordinates

logger = logging.getLogger(__name__)

def get_event_locations(news):
    """Extract location data from news articles with error handling"""
    try:
        if not news or len(news) == 0:
            logger.warning("No news articles provided for location extraction")
            return pd.DataFrame(columns=["lat", "lon", "event", "location"])
        
        data = []
        
        for idx, n in enumerate(news):
            try:
                title = n.get("title", "")
                if not title:
                    logger.warning(f"Article {idx} has empty title")
                    continue
                
                locs = extract_locations(title)
                
                for loc in locs:
                    try:
                        lat, lon = get_coordinates(loc)
                        if lat is not None and lon is not None:
                            data.append({
                                "lat": lat,
                                "lon": lon,
                                "event": title,
                                "location": loc.upper(),
                                "source": n.get("source", "Unknown")
                            })
                    except Exception as e:
                        logger.debug(f"Error getting coordinates for {loc}: {e}")
                        continue
            
            except Exception as e:
                logger.warning(f"Error processing article {idx}: {e}")
                continue
        
        df = pd.DataFrame(data)
        logger.info(f"Extracted {len(df)} location data points from {len(news)} articles")
        return df
    
    except Exception as e:
        logger.error(f"Error extracting event locations: {e}")
        return pd.DataFrame(columns=["lat", "lon", "event", "location"])
