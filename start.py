#!/usr/bin/env python
"""
Quick startup script for AI Trading System
Run this to setup and start the application
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, description):
    """Run a command and report status"""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")
    print(f"Running: {command}\n")
    
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"❌ Error: {description} failed!")
        return False
    print(f"✅ {description} completed!")
    return True

def check_python():
    """Check Python version"""
    print("\n" + "="*60)
    print("🐍 Python Version")
    print("="*60)
    version = sys.version
    print(f"Running: {version}")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required!")
        return False
    print("✅ Python version OK")
    return True

def main():
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║        🚀 AI TRADING SYSTEM - QUICK START                ║
    ║                                                           ║
    ║  This script will setup and run the entire system        ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Check Python
    if not check_python():
        sys.exit(1)
    
    # Detect OS
    system = platform.system()
    is_windows = system == "Windows"
    
    # 1. Create virtual environment
    venv_name = "venv"
    venv_path = Path(venv_name)
    
    if not venv_path.exists():
        cmd = f"python -m venv {venv_name}"
        if not run_command(cmd, "Creating virtual environment"):
            sys.exit(1)
    else:
        print(f"\n✅ Virtual environment '{venv_name}' already exists, skipping...")
    
    # 2. Activate virtual environment and install dependencies
    if is_windows:
        activate_cmd = f"{venv_name}\\Scripts\\activate.bat && "
        pip_cmd = f"{venv_name}\\Scripts\\pip"
    else:
        activate_cmd = f"source {venv_name}/bin/activate && "
        pip_cmd = f"{venv_name}/bin/pip"
    
    # Install requirements
    cmd = f"{pip_cmd} install -r requirements.txt"
    if not run_command(cmd, "Installing Python dependencies"):
        print("⚠️  Package installation may have failed, but continuing...")
    
    # 3. Setup environment
    env_file = ".env"
    if not Path(env_file).exists():
        print(f"\n{'='*60}")
        print("⚙️  Environment Configuration")
        print(f"{'='*60}")
        print(f"\n📝 .env file not found!")
        print("   Creating from .env.example...")
        
        if Path(".env.example").exists():
            with open(".env.example", "r") as f:
                content = f.read()
            with open(".env", "w") as f:
                f.write(content)
            print("\n✅ .env file created from template")
            print("\n⚠️  IMPORTANT: Edit .env file with your API keys:")
            print("   - NEWS_API_KEY from https://newsapi.org")
            print("   - ALPHA_VANTAGE_API_KEY from https://alphavantage.co")
            print("   - HUGGINGFACE_API_KEY (optional) from https://huggingface.co")
        else:
            print("❌ .env.example not found!")
            sys.exit(1)
    else:
        print(f"\n✅ .env file already exists")
    
    # 4. Verify API keys
    print(f"\n{'='*60}")
    print("🔑 Checking API Configuration")
    print(f"{'='*60}")
    
    with open(".env", "r") as f:
        env_content = f.read()
    
    has_news_key = "NEWS_API_KEY=" in env_content and "your_newsapi_key_here" not in env_content
    has_alpha_key = "ALPHA_VANTAGE_API_KEY=" in env_content and "your_alpha_vantage_key_here" not in env_content
    
    if not has_news_key:
        print("❌ NEWS_API_KEY not configured")
        print("   Edit .env and add your NewsAPI key")
    
    if not has_alpha_key:
        print("❌ ALPHA_VANTAGE_API_KEY not configured")
        print("   Edit .env and add your Alpha Vantage key")
    
    if has_news_key and has_alpha_key:
        print("✅ API keys properly configured")
    else:
        print("\n⚠️  Warning: Some API keys are not configured")
        response = input("Continue anyway? (y/n): ").lower()
        if response != 'y':
            sys.exit(1)
    
    # 5. Create logs directory
    logs_dir = Path("logs")
    if not logs_dir.exists():
        logs_dir.mkdir()
        print("\n✅ Created logs directory")
    
    # 6. Run tests (optional)
    print(f"\n{'='*60}")
    print("🧪 Running Tests (Optional)")
    print(f"{'='*60}")
    response = input("Run unit tests? (y/n): ").lower()
    
    if response == 'y':
        if is_windows:
            test_cmd = f"{venv_name}\\Scripts\\pytest test_core_functions.py -v"
        else:
            test_cmd = f"{venv_name}/bin/pytest test_core_functions.py -v"
        
        run_command(test_cmd, "Running unit tests")
    
    # 7. Run backtesting (optional)
    print(f"\n{'='*60}")
    print("📊 Running Backtests (Optional)")
    print(f"{'='*60}")
    response = input("Run backtesting? (y/n): ").lower()
    
    if response == 'y':
        if is_windows:
            backtest_cmd = f"{venv_name}\\Scripts\\python backtester.py"
        else:
            backtest_cmd = f"{venv_name}/bin/python backtester.py"
        
        run_command(backtest_cmd, "Running backtests")
    
    # 8. Start the app
    print(f"\n{'='*60}")
    print("🎯 Starting Application")
    print(f"{'='*60}")
    
    if is_windows:
        streamlit_cmd = f"{venv_name}\\Scripts\\streamlit run trading_app.py"
    else:
        streamlit_cmd = f"{venv_name}/bin/streamlit run trading_app.py"
    
    print("\n✨ Starting Streamlit dashboard...")
    print("\n📱 The app will open in your browser at: http://localhost:8501")
    print("\n💡 Tips:")
    print("   - Press Ctrl+C to stop the server")
    print("   - Check logs/ folder for detailed logs")
    print("   - Edit config.py or .env to change settings")
    
    print(f"\n{'='*60}\n")
    
    os.system(streamlit_cmd)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
