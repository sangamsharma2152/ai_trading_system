import logging
import sqlite3
from datetime import datetime
from config import DATABASE_URL

logger = logging.getLogger(__name__)

class TradingDatabase:
    """Database operations for trading history"""
    
    def __init__(self, db_path="trading_history.db"):
        """Initialize database"""
        self.db_path = db_path
        self.init_database()
        logger.info(f"Database initialized: {db_path}")
    
    def init_database(self):
        """Create database tables if they don't exist"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create predictions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    prediction TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    gold_action TEXT,
                    silver_action TEXT,
                    oil_action TEXT
                )
            ''')
            
            # Create prices table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS prices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    asset TEXT NOT NULL,
                    price REAL NOT NULL,
                    UNIQUE(timestamp, asset)
                )
            ''')
            
            # Create trades table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    asset TEXT NOT NULL,
                    action TEXT NOT NULL,
                    price REAL NOT NULL,
                    quantity REAL NOT NULL,
                    total_value REAL NOT NULL
                )
            ''')
            
            # Create events table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    event_type TEXT NOT NULL,
                    description TEXT NOT NULL,
                    impact TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Database tables created successfully")
        
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
    
    def log_prediction(self, prediction, confidence):
        """Log prediction to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO predictions 
                (prediction, confidence, gold_action, silver_action, oil_action)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                str(prediction),
                confidence,
                prediction.get("gold"),
                prediction.get("silver"),
                prediction.get("oil")
            ))
            
            conn.commit()
            conn.close()
            logger.debug("Prediction logged to database")
        
        except Exception as e:
            logger.error(f"Error logging prediction: {e}")
    
    def log_prices(self, prices):
        """Log current prices to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for asset, price in prices.items():
                if price is not None:
                    try:
                        cursor.execute('''
                            INSERT INTO prices (asset, price)
                            VALUES (?, ?)
                        ''', (asset, price))
                    except sqlite3.IntegrityError:
                        # Update if already exists for this timestamp
                        cursor.execute('''
                            UPDATE prices SET price = ? 
                            WHERE asset = ? AND date(timestamp) = date('now')
                        ''', (price, asset))
            
            conn.commit()
            conn.close()
            logger.debug("Prices logged to database")
        
        except Exception as e:
            logger.error(f"Error logging prices: {e}")
    
    def log_trade(self, asset, action, price, quantity):
        """Log executed trade"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            total_value = price * quantity
            
            cursor.execute('''
                INSERT INTO trades (asset, action, price, quantity, total_value)
                VALUES (?, ?, ?, ?, ?)
            ''', (asset, action, price, quantity, total_value))
            
            conn.commit()
            conn.close()
            logger.info(f"Trade logged: {action} {quantity} units of {asset} at ${price}")
        
        except Exception as e:
            logger.error(f"Error logging trade: {e}")
    
    def log_event(self, event_type, description, impact=None):
        """Log detected event"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO events (event_type, description, impact)
                VALUES (?, ?, ?)
            ''', (event_type, description, str(impact) if impact else None))
            
            conn.commit()
            conn.close()
            logger.info(f"Event logged: {event_type} - {description}")
        
        except Exception as e:
            logger.error(f"Error logging event: {e}")
    
    def get_prediction_history(self, days=30):
        """Get prediction history for last N days"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM predictions 
                WHERE timestamp >= datetime('now', '-' || ? || ' days')
                ORDER BY timestamp DESC
            ''', (days,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
        
        except Exception as e:
            logger.error(f"Error retrieving prediction history: {e}")
            return []
    
    def get_price_history(self, asset, days=30):
        """Get price history for asset"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM prices 
                WHERE asset = ? AND timestamp >= datetime('now', '-' || ? || ' days')
                ORDER BY timestamp DESC
            ''', (asset, days))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
        
        except Exception as e:
            logger.error(f"Error retrieving price history: {e}")
            return []
    
    def get_trade_summary(self):
        """Get summary of all trades"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    action,
                    COUNT(*) as count,
                    AVG(price) as avg_price,
                    SUM(total_value) as total_value
                FROM trades
                GROUP BY action
            ''')
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
        
        except Exception as e:
            logger.error(f"Error retrieving trade summary: {e}")
            return []
    
    def cleanup_old_data(self, days=90):
        """Delete data older than N days"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM predictions 
                WHERE timestamp < datetime('now', '-' || ? || ' days')
            ''', (days,))
            
            cursor.execute('''
                DELETE FROM prices 
                WHERE timestamp < datetime('now', '-' || ? || ' days')
            ''', (days,))
            
            conn.commit()
            deleted_count = cursor.rowcount
            conn.close()
            
            logger.info(f"Cleaned up {deleted_count} old records")
        
        except Exception as e:
            logger.error(f"Error cleaning up database: {e}")


# Global database instance
db = TradingDatabase()

if __name__ == "__main__":
    # Example usage
    db = TradingDatabase()
    
    # Log a prediction
    db.log_prediction({"gold": "BUY", "silver": "HOLD", "oil": "SELL"}, 0.85)
    
    # Log prices
    db.log_prices({"gold": 2000.50, "silver": 24.30, "oil": 88.75})
    
    # Log a trade
    db.log_trade("gold", "BUY", 2000.50, 10)
    
    # Log an event
    db.log_event("GEOPOLITICAL", "War in Middle East", {"gold": "BUY", "oil": "BUY"})
    
    # Get history
    predictions = db.get_prediction_history(days=30)
    print(f"Last 30 days predictions: {len(predictions)} records")
    
    # Get summary
    summary = db.get_trade_summary()
    print(f"Trade summary: {summary}")
