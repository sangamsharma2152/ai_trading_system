#!/bin/bash

# AI Trading System - Linux/macOS Startup Script

echo ""
echo "========================================================"
echo "   AI TRADING SYSTEM - AUTOMATIC STARTUP"
echo "========================================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed"
    echo "Please install Python 3.8+ using:"
    echo "  macOS: brew install python3"
    echo "  Linux: sudo apt-get install python3"
    exit 1
fi

echo "[OK] Python found: $(python3 --version)"
echo ""

# Create virtual environment if needed
if [ ! -d "venv" ]; then
    echo "[*] Creating virtual environment..."
    python3 -m venv venv
    echo "[OK] Virtual environment created"
else
    echo "[OK] Virtual environment already exists"
fi

echo ""
echo "[*] Activating virtual environment..."
source venv/bin/activate

echo "[*] Installing dependencies..."
pip install -r requirements.txt --quiet

echo ""
echo "[*] Checking .env file..."
if [ ! -f ".env" ]; then
    echo "[*] Creating .env from template..."
    cp .env.example .env
    echo "[!] IMPORTANT: Edit .env with your API keys!"
    echo "    - NEWS_API_KEY from https://newsapi.org"
    echo "    - ALPHA_VANTAGE_API_KEY from https://alphavantage.co"
    read -p "Press Enter to continue..."
fi

echo "[OK] .env file exists"
echo ""

# Create logs directory
if [ ! -d "logs" ]; then
    mkdir logs
    echo "[OK] Created logs directory"
fi

echo ""
echo "========================================================"
echo "   STARTUP COMPLETE - LAUNCHING DASHBOARD"
echo "========================================================"
echo ""
echo "Opening: http://localhost:8501"
echo ""
echo "[*] Press Ctrl+C to stop the server"
echo ""

# Start the app
streamlit run trading_app.py
