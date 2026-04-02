@echo off
REM AI Trading System - Windows Startup Script

echo.
echo ========================================================
echo   AI TRADING SYSTEM - AUTOMATIC STARTUP
echo ========================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

echo ^[OK^] Python found
echo.

REM Create virtual environment if needed
if not exist "venv" (
    echo ^[*^] Creating virtual environment...
    python -m venv venv
    echo ^[OK^] Virtual environment created
) else (
    echo ^[OK^] Virtual environment already exists
)

echo.
echo ^[*^] Activating virtual environment...
call venv\Scripts\activate.bat

echo ^[*^] Installing dependencies...
pip install -r requirements.txt

echo.
echo ^[*^] Checking .env file...
if not exist ".env" (
    echo ^[*^] Creating .env from template...
    copy .env.example .env
    echo ^[!^] IMPORTANT: Edit .env with your API keys!
    echo     - NEWS_API_KEY from https://newsapi.org
    echo     - ALPHA_VANTAGE_API_KEY from https://alphavantage.co
    pause
)

echo ^[OK^] .env file exists
echo.

REM Create logs directory
if not exist "logs" (
    mkdir logs
    echo ^[OK^] Created logs directory
)

echo.
echo ========================================================
echo   STARTUP COMPLETE - LAUNCHING DASHBOARD
echo ========================================================
echo.
echo Opening: http://localhost:8501
echo.
echo ^[*^] Press Ctrl+C to stop the server
echo.

REM Start the app
streamlit run trading_app.py

pause
