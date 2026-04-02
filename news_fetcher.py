import logging
import requests
from config import NEWS_API_KEY, NEWS_LIMIT, API_TIMEOUT, NEWS_API_RETRY_COUNT
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

def create_session_with_retries():
    """Create a requests session with retry strategy"""
    session = requests.Session()
    retry_strategy = Retry(
        total=NEWS_API_RETRY_COUNT,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def get_news():
    """Fetch news articles with comprehensive error handling"""
    try:
        if not NEWS_API_KEY:
            logger.error("NEWS_API_KEY not configured in environment variables")
            return []
        
        url = f"https://newsapi.org/v2/everything?q=gold OR oil OR inflation OR war OR economy&language=en&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
        
        session = create_session_with_retries()
        
        response = session.get(url, timeout=API_TIMEOUT)
        response.raise_for_status()
        
        data = response.json()
        
        # Check for API errors
        if data.get("status") != "ok":
            logger.error(f"News API error: {data.get('message', 'Unknown error')}")
            return []
        
        articles = []
        for article in data.get("articles", [])[:NEWS_LIMIT]:
            try:
                articles.append({
                    "title": article.get("title", ""),
                    "source": article.get("source", {}).get("name", "Unknown"),
                    "description": article.get("description", ""),
                    "url": article.get("url", ""),
                    "publishedAt": article.get("publishedAt", "")
                })
            except (KeyError, TypeError) as e:
                logger.warning(f"Error parsing article: {e}")
                continue
        
        logger.info(f"Successfully fetched {len(articles)} news articles")
        return articles
    
    except requests.exceptions.Timeout:
        logger.error(f"News API request timed out after {API_TIMEOUT} seconds")
        return []
    except requests.exceptions.ConnectionError:
        logger.error("Connection error while fetching news - check internet connection")
        return []
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
        return []
    except ValueError as e:
        logger.error(f"Invalid JSON response from news API: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error fetching news: {e}")
        return []
