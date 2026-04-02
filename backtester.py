import logging
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from config import STOP_LOSS_PERCENTAGE, TAKE_PROFIT_PERCENTAGE

logger = logging.getLogger(__name__)

class Portfolio:
    """Portfolio management class for tracking trades"""
    
    def __init__(self, initial_balance=10000):
        """Initialize portfolio"""
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.holdings = {"gold": 0, "silver": 0, "oil": 0}
        self.trades = []
        self.performance_history = []
        
        logger.info(f"Portfolio initialized with balance: ${initial_balance}")
    
    def buy(self, asset, price, quantity):
        """Execute a buy order"""
        try:
            cost = price * quantity
            if cost <= self.balance:
                self.holdings[asset] += quantity
                self.balance -= cost
                
                trade = {
                    "type": "BUY",
                    "asset": asset,
                    "price": price,
                    "quantity": quantity,
                    "cost": cost,
                    "timestamp": datetime.now()
                }
                self.trades.append(trade)
                logger.info(f"BUY: {quantity} units of {asset} at ${price} = ${cost}")
                return True
            else:
                logger.warning(f"Insufficient balance for {asset} purchase. Need ${cost}, have ${self.balance}")
                return False
        except Exception as e:
            logger.error(f"Error executing buy order: {e}")
            return False
    
    def sell(self, asset, price, quantity):
        """Execute a sell order"""
        try:
            if self.holdings[asset] >= quantity:
                revenue = price * quantity
                self.holdings[asset] -= quantity
                self.balance += revenue
                
                trade = {
                    "type": "SELL",
                    "asset": asset,
                    "price": price,
                    "quantity": quantity,
                    "revenue": revenue,
                    "timestamp": datetime.now()
                }
                self.trades.append(trade)
                logger.info(f"SELL: {quantity} units of {asset} at ${price} = ${revenue}")
                return True
            else:
                logger.warning(f"Insufficient {asset} holdings. Have {self.holdings[asset]}, need {quantity}")
                return False
        except Exception as e:
            logger.error(f"Error executing sell order: {e}")
            return False
    
    def get_portfolio_value(self, current_prices):
        """Calculate total portfolio value at current prices"""
        try:
            value = self.balance
            for asset, quantity in self.holdings.items():
                if current_prices[asset]:
                    value += quantity * current_prices[asset]
            return value
        except Exception as e:
            logger.error(f"Error calculating portfolio value: {e}")
            return self.balance
    
    def get_returns(self, current_prices):
        """Calculate portfolio returns"""
        try:
            current_value = self.get_portfolio_value(current_prices)
            returns = current_value - self.initial_balance
            return_percentage = (returns / self.initial_balance) * 100
            return returns, return_percentage
        except Exception as e:
            logger.error(f"Error calculating returns: {e}")
            return 0, 0


class Backtester:
    """Backtesting engine for trading strategies"""
    
    def __init__(self, initial_balance=10000):
        """Initialize backtester"""
        self.portfolio = Portfolio(initial_balance)
        self.results = []
        logger.info("Backtester initialized")
    
    def run_backtest(self, symbol, start_date, end_date, strategy, period="1y"):
        """Run backtest on historical data"""
        try:
            logger.info(f"Running backtest for {symbol} from {start_date} to {end_date}")
            
            # Fetch historical data
            data = yf.download(symbol, start=start_date, end=end_date, progress=False)
            
            if data.empty:
                logger.error(f"No data available for {symbol}")
                return None
            
            data['Daily_Return'] = data['Close'].pct_change()
            
            # Simulate trading
            for idx, row in data.iterrows():
                signal = strategy(row)
                
                if signal == "BUY":
                    # Buy with 50% of available balance
                    quantity = (self.portfolio.balance * 0.5) / row['Close']
                    self.portfolio.buy(symbol, row['Close'], quantity)
                
                elif signal == "SELL":
                    # Sell all holdings
                    if self.portfolio.holdings[symbol] > 0:
                        self.portfolio.sell(symbol, row['Close'], self.portfolio.holdings[symbol])
            
            # Calculate results
            final_prices = {symbol: data['Close'].iloc[-1]}
            final_value = self.portfolio.get_portfolio_value(final_prices)
            returns, return_pct = self.portfolio.get_returns(final_prices)
            
            result = {
                "symbol": symbol,
                "initial_balance": self.portfolio.initial_balance,
                "final_value": final_value,
                "returns": returns,
                "return_percentage": return_pct,
                "trades": len(self.portfolio.trades),
                "period": f"{start_date} to {end_date}"
            }
            
            self.results.append(result)
            logger.info(f"Backtest completed: {return_pct:.2f}% return")
            return result
        
        except Exception as e:
            logger.error(f"Error running backtest: {e}")
            return None
    
    def get_max_drawdown(self):
        """Calculate maximum drawdown"""
        try:
            if not self.portfolio.trades:
                return 0
            
            peak = self.portfolio.initial_balance
            max_drawdown = 0
            
            for trade in self.portfolio.trades:
                if trade["type"] == "SELL":
                    current_value = trade["revenue"]
                    if current_value > peak:
                        peak = current_value
                    drawdown = (peak - current_value) / peak
                    if drawdown > max_drawdown:
                        max_drawdown = drawdown
            
            return max_drawdown * 100
        except Exception as e:
            logger.error(f"Error calculating max drawdown: {e}")
            return 0
    
    def get_sharpe_ratio(self, risk_free_rate=0.02):
        """Calculate Sharpe ratio"""
        try:
            if len(self.portfolio.trades) < 2:
                return 0
            
            # Calculate daily returns
            returns = []
            for trade in self.portfolio.trades:
                if trade["type"] == "SELL":
                    daily_return = (trade["revenue"] - trade["cost"]) / trade["cost"]
                    returns.append(daily_return)
            
            if not returns:
                return 0
            
            mean_return = sum(returns) / len(returns)
            variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
            std_dev = variance ** 0.5
            
            if std_dev == 0:
                return 0
            
            sharpe_ratio = (mean_return - (risk_free_rate / 252)) / std_dev
            return sharpe_ratio
        
        except Exception as e:
            logger.error(f"Error calculating Sharpe ratio: {e}")
            return 0


def simple_moving_average_strategy(row, window=10):
    """Simple moving average trading strategy"""
    try:
        # This is a placeholder - implement your strategy here
        if row['Close'] > row.get('SMA', row['Close']):
            return "BUY"
        else:
            return "SELL"
    except Exception as e:
        logger.error(f"Error in strategy: {e}")
        return "HOLD"


if __name__ == "__main__":
    # Example backtesting
    backtester = Backtester(initial_balance=10000)
    
    result = backtester.run_backtest(
        symbol="GC=F",  # Gold futures
        start_date="2023-01-01",
        end_date="2024-01-01",
        strategy=simple_moving_average_strategy
    )
    
    if result:
        print(f"\nBacktest Results:")
        print(f"Final Value: ${result['final_value']:.2f}")
        print(f"Returns: {result['return_percentage']:.2f}%")
        print(f"Total Trades: {result['trades']}")
        print(f"Max Drawdown: {backtester.get_max_drawdown():.2f}%")
        print(f"Sharpe Ratio: {backtester.get_sharpe_ratio():.2f}")
