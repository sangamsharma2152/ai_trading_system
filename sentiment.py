import logging
from transformers import pipeline
import torch
from config import SENTIMENT_MODEL

logger = logging.getLogger(__name__)

# Use FinBERT for financial sentiment analysis
try:
    device = 0 if torch.cuda.is_available() else -1  # Use GPU if available
    logger.info(f"Loading sentiment model: {SENTIMENT_MODEL} on device: {'GPU' if device == 0 else 'CPU'}")
    
    sentiment_model = pipeline(
        "sentiment-analysis",
        model=SENTIMENT_MODEL,
        device=device
    )
    logger.info("Sentiment model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load sentiment model: {e}. Falling back to default model.")
    sentiment_model = pipeline("sentiment-analysis")

def analyze_sentiment(news_list):
    """Analyze sentiment of news articles or text with error handling
    
    Args:
        news_list: Either a string/text or list of news article dicts
    
    Returns:
        For string input: dict with label and score
        For list input: list of dicts with sentiment details
    """
    if not news_list:
        logger.warning("No content provided for sentiment analysis")
        return {"label": "NEUTRAL", "score": 0.0}
    
    # Handle string/text input
    if isinstance(news_list, str):
        try:
            text_to_analyze = news_list[:512] if len(news_list) > 512 else news_list
            result = sentiment_model(text_to_analyze)[0]
            
            label = result["label"]
            score = result["score"]
            
            # Normalize labels
            if label.lower() in ["negative"]:
                normalized_label = "NEGATIVE"
                normalized_score = -score
            elif label.lower() in ["positive"]:
                normalized_label = "POSITIVE"
                normalized_score = score
            else:
                normalized_label = "NEUTRAL"
                normalized_score = 0.0
            
            return {
                "label": normalized_label,
                "score": round(normalized_score, 4)
            }
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {"label": "NEUTRAL", "score": 0.0}
    
    # Handle list of articles input
    results = []
    
    for idx, news in enumerate(news_list):
        try:
            title = news.get("title", "")
            
            if not title or len(title.strip()) == 0:
                logger.warning(f"Article {idx} has empty title, skipping")
                continue
            
            # Truncate long titles for model
            text_to_analyze = title[:512] if len(title) > 512 else title
            
            result = sentiment_model(text_to_analyze)[0]
            
            # Convert model output to standard format
            label = result["label"]
            score = result["score"]
            
            # FinBERT might output different labels, normalize them
            if label.lower() in ["negative"]:
                normalized_label = "NEGATIVE"
                normalized_score = -score
            elif label.lower() in ["positive"]:
                normalized_label = "POSITIVE"
                normalized_score = score
            else:
                normalized_label = "NEUTRAL"
                normalized_score = 0.0
            
            results.append({
                "text": title,
                "label": normalized_label,
                "score": round(normalized_score, 4),
                "source": news.get("source", "Unknown"),
                "url": news.get("url", ""),
                "publishedAt": news.get("publishedAt", "")
            })
        
        except Exception as e:
            logger.error(f"Error analyzing sentiment for article {idx}: {e}")
            continue
    
    logger.info(f"Successfully analyzed sentiment for {len(results)} out of {len(news_list)} articles")
    return results
