# AI Trading System

A comprehensive AI-powered trading system that analyzes global news sentiment and market conditions to generate trading signals for commodities (Gold, Silver, Oil).

## Features

✅ **News Sentiment Analysis** - Real-time financial news analysis using FinBERT  
✅ **Geopolitical Intelligence** - Detects global events and their market impact  
✅ **Live Market Data** - Fetches real-time commodity prices  
✅ **AI Signal Generation** - ML-based trading recommendations  
✅ **Interactive Dashboard** - Beautiful Streamlit UI with visualizations  
✅ **Global Event Mapping** - Heatmap of event locations and impacts  
✅ **Error Handling & Logging** - Comprehensive error handling and logging  
✅ **Backtesting Engine** - Test strategies on historical data  
✅ **Unit Tests** - Full test coverage for all modules  

## Project Structure

```
ai_trading_system/
├── config.py                    # Configuration and environment variables
├── logging_config.py            # Logging setup
├── news_fetcher.py             # Fetch news articles
├── sentiment.py                # Sentiment analysis (FinBERT)
├── event_detector.py           # Detect geopolitical events
├── nlp_engine.py               # NLP utilities
├── market_data.py              # Fetch market prices
├── model.py                    # Prediction model
├── decision_engine.py          # Generate trading decisions
├── impact_model.py             # Map events to market impacts
├── map_data.py                 # Geolocation data extraction
├── trading_app.py              # Main Streamlit application
├── backtester.py               # Backtesting engine
├── database.py                 # Database operations
├── test_core_functions.py      # Unit tests
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore file
└── README.md                  # This file
```

## Installation

### Prerequisites
- Python 3.8+
- pip or conda

### Setup

1. **Clone and setup:**
```bash
cd ai_trading_system
```

2. **Create virtual environment:**
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. **Required API Keys:**
   - **NewsAPI Key**: Get from [https://newsapi.org](https://newsapi.org)
   - **Alpha Vantage Key**: Get from [https://www.alphavantage.co](https://www.alphavantage.co)
   - **HuggingFace Key** (Optional): Get from [https://huggingface.co](https://huggingface.co)

## Configuration

Edit `.env` file:

```env
# NEWS API
NEWS_API_KEY=your_newsapi_key_here
NEWS_LIMIT=20
REFRESH_INTERVAL=60000

# MARKET DATA
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here

# TRADING CONFIG
POS_THRESHOLD=0.2
NEG_THRESHOLD=-0.2
MAX_POSITION_SIZE=1000
STOP_LOSS_PERCENTAGE=5.0
TAKE_PROFIT_PERCENTAGE=10.0

# APP CONFIG
DEBUG=False
LOG_LEVEL=INFO
```

## Usage

### Run the Dashboard

```bash
streamlit run trading_app.py
```

The dashboard will open at `http://localhost:8501`

### Run Tests

```bash
pytest test_core_functions.py -v
```

### Run Backtesting

```bash
python backtester.py
```

### View Logs

Logs are stored in `logs/`:
- `trading_app.log` - Main application log
- `errors.log` - Error log

## How It Works

1. **News Fetching**: Fetches latest financial news using NewsAPI
2. **Sentiment Analysis**: Analyzes news sentiment using FinBERT
3. **Event Detection**: Identifies geopolitical/economic events
4. **Impact Mapping**: Maps events to asset impacts
5. **Market Analysis**: Fetches current market prices
6. **Prediction**: Generates BUY/SELL/HOLD signals
7. **Visualization**: Displays results with charts and maps

## API Modules

### news_fetcher.py
Fetches news articles with retry logic and error handling.

```python
from news_fetcher import get_news
news = get_news()
```

### sentiment.py
Analyzes sentiment using FinBERT model.

```python
from sentiment import analyze_sentiment
sentiments = analyze_sentiment(news)
```

### market_data.py
Gets current commodity prices.

```python
from market_data import get_prices
prices = get_prices()  # {"gold": 2000.50, "silver": 24.30, ...}
```

### model.py
Generates trading predictions.

```python
from model import predict
prediction, confidence = predict(sentiments)
```

### backtester.py
Backtest trading strategies.

```python
from backtester import Backtester, simple_moving_average_strategy
backtester = Backtester(initial_balance=10000)
results = backtester.run_backtest("GC=F", "2023-01-01", "2024-01-01", strategy)
```

## Error Handling

The system includes comprehensive error handling:

- **API Timeouts**: Automatic retries with exponential backoff
- **Missing Data**: Graceful fallbacks and logging
- **Invalid Input**: Input validation and sanitization
- **Network Errors**: Connection error handling

## Logging

Logs include:
- INFO: General information and successful operations
- WARNING: Warnings for recoverable issues
- ERROR: Errors from exceptions
- DEBUG: Detailed debug information

## Performance Metrics

The backtester calculates:

- **Returns**: Profit/loss percentage
- **Max Drawdown**: Largest portfolio decline
- **Sharpe Ratio**: Risk-adjusted returns
- **Trade Count**: Number of executed trades

## Security

- ✅ API keys stored in environment variables (not in code)
- ✅ No hardcoded credentials
- ✅ Input validation and sanitization
- ✅ Error messages don't leak sensitive data

## Testing

Run comprehensive unit tests:

```bash
pytest test_core_functions.py -v --cov=. --cov-report=html
```

Test coverage includes:
- Prediction model
- Decision engine
- Event detection
- Impact mapping
- NLP functions
- Error handling

## Known Limitations

1. **Event Detection**: Keyword-based; can be improved with NER
2. **Sentiment Model**: FinBERT trained on general finance; not specialized
3. **Market Data**: Limited to major commodities
4. **Real-time**: Updates every 60 seconds (configurable)

## Future Improvements

- [ ] Fine-tune FinBERT on trading-specific corpus
- [ ] Add Named Entity Recognition (NER)
- [ ] Integrate technical analysis indicators
- [ ] Add machine learning model training
- [ ] Support for more asset classes
- [ ] Database persistence
- [ ] Risk management rules
- [ ] Portfolio optimization

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file

## Disclaimer

This system is for educational and research purposes only. It does not provide financial advice. Trading involves risk. Always test strategies thoroughly and never risk more than you can afford to lose.

## Support

For issues, questions, or suggestions, open an issue on GitHub.

## Author

Sangam Sharma ([GitHub](https://github.com/sangamsharma2152))

