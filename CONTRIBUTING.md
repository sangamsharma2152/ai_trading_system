# Contributing to AI Trading System

Thank you for your interest in contributing! Here's how you can help:

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/ai_trading_system.git
   cd ai_trading_system
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Guidelines

- **Code Style**: Follow PEP 8 using Black formatter (`black .`)
- **Testing**: Add tests for new features in `test_core_functions.py`
- **Logging**: Use `logging.getLogger(__name__)` for logging
- **Error Handling**: Use specific exceptions, not bare `except` blocks
- **Environment Variables**: Use `.env` file, never hardcode API keys

## Running Tests

```bash
pytest test_core_functions.py -v
```

## Submitting Changes

1. **Commit** with clear messages:
   ```bash
   git commit -m "Add: Brief description of changes"
   ```

2. **Push** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request** with:
   - Clear description of changes
   - Reference to any related issues
   - Test results showing no failures

## Reporting Issues

Use GitHub Issues with:
- Clear title and description
- Steps to reproduce (if bug)
- Expected vs actual behavior
- Your environment (Python version, OS)

## Questions?

Open a GitHub Discussion or Issue - we're here to help!

Thank you for contributing! 🎉
