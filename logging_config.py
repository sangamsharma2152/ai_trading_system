import logging
import logging.handlers
import os
from config import LOG_LEVEL, DEBUG

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure logging
def setup_logging():
    """Setup logging configuration for the application"""
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL)
    
    # Log format
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler (rotating)
    file_handler = logging.handlers.RotatingFileHandler(
        'logs/trading_app.log',
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(log_format)
    root_logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_level = logging.DEBUG if DEBUG else logging.INFO
    console_handler.setLevel(console_level)
    console_handler.setFormatter(log_format)
    root_logger.addHandler(console_handler)
    
    # Error file handler
    error_handler = logging.handlers.RotatingFileHandler(
        'logs/errors.log',
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(log_format)
    root_logger.addHandler(error_handler)
    
    logging.info("Logging configured successfully")

# Setup logging on import
setup_logging()
