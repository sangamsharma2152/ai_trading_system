# 🚀 Quick Start Guide - AI Trading System

## Installation & Startup (All at Once)

### **Option 1: Automatic Setup (Recommended)**

#### 🪟 **Windows**
```bash
# Double-click this file in File Explorer:
start.bat

# OR run from PowerShell:
.\start.bat
```

#### 🍎 **macOS / Linux**
```bash
# Give permission and run:
chmod +x start.sh
./start.sh
```

#### 🐍 **Python Script (All Platforms)**
```bash
python start.py
```

This will automatically:
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Create `.env` file from template
- ✅ Setup logs directory
- ✅ Run tests (optional)
- ✅ Run backtesting (optional)
- ✅ Launch the Streamlit dashboard

---

## Manual Setup (Step by Step)

If you prefer manual control, follow these steps:

### **Step 1: Create Virtual Environment**

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### **Step 2: Install Dependencies**
```bash
pip install -r requirements.txt
```

This will install:
- `streamlit` - Web dashboard
- `transformers` & `torch` - AI/ML models (FinBERT)
- `yfinance` - Market data
- `pandas`, `numpy` - Data processing
- `plotly`, `pydeck` - Visualizations
- `pytest` - Testing
- And 10+ other packages

⏳ **Takes 5-10 minutes on first install (downloading ML models)**

### **Step 3: Configure API Keys**

```bash
# Copy template
cp .env.example .env

# Edit with your keys:
# - Windows: notepad .env
# - macOS/Linux: nano .env
```

**Get API Keys:**
- 🔑 **NewsAPI**: https://newsapi.org (free tier: 100 requests/day)
- 🔑 **Alpha Vantage**: https://alphavantage.co (free tier: 5 requests/min)
- 🔑 **HuggingFace** (optional): https://huggingface.co

### **Step 4: Run the Application**

#### Start Dashboard
```bash
streamlit run trading_app.py
```

Dashboard opens at: **http://localhost:8501**

---

## Running Individual Components

### **Run Tests**
```bash
# All tests
pytest test_core_functions.py -v

# Specific test
pytest test_core_functions.py::TestPredictModel::test_predict_with_positive_sentiments -v

# With coverage
pytest test_core_functions.py --cov=. --cov-report=html
```

### **Run Backtesting**
```bash
python backtester.py
```

Output example:
```
Backtest Results:
Final Value: $12,450.75
Returns: 24.51%
Total Trades: 42
Max Drawdown: 8.30%
Sharpe Ratio: 1.85
```

### **Check Logs**
```bash
# View main log
tail -f logs/trading_app.log

# View errors only
tail -f logs/errors.log

# Windows: 
# type logs\trading_app.log
```

---

## Environment Variables (`.env`)

```env
# API Keys
NEWS_API_KEY=your_key_here
ALPHA_VANTAGE_API_KEY=your_key_here
HUGGINGFACE_API_KEY=your_key_here (optional)

# News Config
NEWS_LIMIT=20
REFRESH_INTERVAL=60000

# Trading Thresholds
POS_THRESHOLD=0.2
NEG_THRESHOLD=-0.2

# Advanced
DEBUG=False
LOG_LEVEL=INFO
API_TIMEOUT=10
MAX_POSITION_SIZE=1000
STOP_LOSS_PERCENTAGE=5.0
TAKE_PROFIT_PERCENTAGE=10.0
```

---

## File Structure

```
ai_trading_/
├── 📄 start.py          ← Python startup script (all OS)
├── 📄 start.bat         ← Windows batch script
├── 📄 start.sh          ← Linux/macOS shell script
├── 📄 trading_app.py    ← Main Streamlit app
├── 📄 .env              ← Your API keys (edit this!)
├── 📄 .env.example      ← API keys template
├── 📄 requirements.txt   ← Python dependencies
├── 📁 logs/             ← Log files
│   ├── trading_app.log
│   └── errors.log
├── 📁 venv/             ← Virtual environment (created)
└── [Core modules, tests, config files...]
```

---

## Common Issues & Solutions

### ❌ **"Python not found"**
```bash
# Ensure Python is in PATH
python --version     # Windows/macOS
python3 --version    # Linux
```

### ❌ **"No module named streamlit"**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### ❌ **"API key invalid"**
```bash
# Check .env file exists and has valid keys
# Don't use quotes around keys: 
# ✅ NEWS_API_KEY=abc123xyz
# ❌ NEWS_API_KEY="abc123xyz"
```

### ❌ **"Connection timeout"**
```bash
# Check internet connection
# Increase timeout in .env:
API_TIMEOUT=20
```

### ❌ **"ModuleNotFoundError: No module named 'torch'"**
```bash
# PyTorch requires specific installation
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

---

## Dashboard Features

Once running, the dashboard shows:

📊 **Live Market Prices**
- Gold, Silver, Oil current prices
- Real-time updates every 60 seconds

📈 **Market Charts**
- 1-year price history
- Interactive Plotly charts

🤖 **AI Signals**
- BUY/SELL/HOLD recommendations
- Confidence levels

🌍 **Global Event Map**
- Heatmap of geopolitical events
- News sentiment by region

📰 **Intelligence Feed**
- Real-time news analysis
- Event detection and impact

---

## Performance Tips

### **Faster Loading**
```bash
# Skip auto-refresh while testing
# Edit trading_app.py line 35:
# st_autorefresh(interval=600000)  # 10 minutes instead of 1
```

### **Lower Resource Usage**
```env
# Use CPU instead of GPU
# Edit config.py or .env:
SENTIMENT_MODEL=distilbert-base-uncased
```

### **Offline Mode**
```env
# Would require caching, not currently supported
```

---

## Next Steps

1. ✅ Run `start.bat` / `start.sh` / `python start.py`
2. ✅ Edit `.env` with your API keys
3. ✅ Open http://localhost:8501
4. ✅ Explore the dashboard
5. ✅ Run tests: `pytest test_core_functions.py -v`
6. ✅ Try backtesting: `python backtester.py`

---

## Getting Help

- 📖 See `README.md` for full documentation
- 🧪 Run tests: `pytest -v` to check everything works
- 📊 Check logs: `logs/trading_app.log`
- 🐛 Debug mode: Set `DEBUG=True` in `.env`

---

## Summary

| Task | Command |
|------|---------|
| **One-click startup** | `start.bat` (Windows) or `./start.sh` (Mac/Linux) |
| **Manual setup** | `python -m venv venv && pip install -r requirements.txt` |
| **Run app** | `streamlit run trading_app.py` |
| **Run tests** | `pytest test_core_functions.py -v` |
| **Backtest** | `python backtester.py` |
| **View logs** | `tail -f logs/trading_app.log` |

**That's it! 🚀**
