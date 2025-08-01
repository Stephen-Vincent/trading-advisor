# 🎯 Trading Advisor

A modern, modular trading analysis tool that generates actionable buy/sell signals with clear entry points, stop losses, and take profit targets. Built with Python for backend analysis and React for the frontend interface.

![Trading Advisor](https://img.shields.io/badge/Status-Active%20Development-green)
![Python](https://img.shields.io/badge/Python-3.12+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![React](https://img.shields.io/badge/React-18+-blue)
![Tests](https://img.shields.io/badge/Tests-100%25%20Passing-brightgreen)

## 🚀 Features

### Current (v1.0)

- **📊 Real-time Stock Analysis** - Fetch and analyze stock data from Yahoo Finance
- **📈 Technical Indicators** - Moving averages (SMA 20/50) with trend analysis
- **🚦 Trading Signals** - Automated buy/sell signal generation based on MA crossovers
- **💰 Risk Management** - Automatic stop loss (5%) and take profit (10%) calculations
- **🌐 REST API** - FastAPI backend serving trading data to frontend
- **🧪 Comprehensive Testing** - 100% test coverage with automated test suite
- **⚡ High Performance** - Sub-second response times for analysis

### Planned (v2.0)

- **📝 Trade Journal** - Automated trade logging with screenshot capture
- **📱 React Frontend** - Modern, responsive web interface
- **📊 Performance Analytics** - Win rate, P&L tracking, and strategy metrics
- **🔔 Alert System** - Email/SMS notifications for signal generation
- **📈 Multiple Strategies** - RSI, MACD, Bollinger Bands integration

## 🏗️ Architecture

```
trading-advisor/
├── backend/                 # Python FastAPI backend
│   ├── src/                # Core trading logic
│   │   ├── data/           # Stock data fetching
│   │   ├── indicators/     # Technical analysis
│   │   └── signals/        # Signal generation
│   ├── api/                # FastAPI endpoints
│   │   └── api.py          # REST API implementation
│   ├── tests/              # Comprehensive test suite
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend (in development)
└── README.md
```

## 🎯 Current Trading Strategy

**SMA Crossover Strategy:**

- **BUY Signal**: 20-day SMA crosses above 50-day SMA
- **SELL Signal**: 20-day SMA crosses below 50-day SMA
- **Stop Loss**: 5% below entry price
- **Take Profit**: 10% above entry price
- **Risk/Reward Ratio**: 1:2

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- pip
- Virtual environment support

### Backend Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/trading-advisor.git
   cd trading-advisor
   ```

2. **Set up Python environment:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Run tests to verify setup:**

   ```bash
   cd tests
   python run_all_tests.py
   ```

5. **Start the API server:**
   ```bash
   cd backend
   python run.py
   ```

The API will be available at `http://localhost:8000`

### Usage Examples

#### Command Line Interface

```bash
cd backend
python main.py --symbol AAPL --period 6mo
```

#### API Endpoints

```bash
# Health check
curl http://localhost:8000/api/health

# Analyze a stock
curl "http://localhost:8000/api/analyze/AAPL?period=6mo"

# Interactive API documentation
open http://localhost:8000/docs
```

#### Python Code

```python
from src.data.data_fetcher import DataFetcher
from src.indicators.simple_indicators import SimpleIndicators
from src.signals.simple_signals import SimpleSignalGenerator

# Initialize components
fetcher = DataFetcher()
indicators = SimpleIndicators()
signal_gen = SimpleSignalGenerator()

# Analyze a stock
data = fetcher.get_stock_data("AAPL", "6mo")
data_with_indicators = indicators.add_moving_averages(data)
signals = signal_gen.find_crossover_signals(data_with_indicators, "AAPL")

print(f"Found {len(signals)} signals")
```

## 📊 Example Output

```
🎯 AAPL Analysis Results
Current Price: $207.57
Trend: MIXED_BEARISH (Price below 20-day MA, but 20-day > 50-day)
20-day MA: $211.40
50-day MA: $205.37

🚦 Latest Signal (July 11, 2025):
Type: BUY at $211.16
🛑 Stop Loss: $200.60 (-5.0%)
🎯 Take Profit: $232.28 (+10.0%)
💰 Risk/Reward: 1:2.0
```

## 🧪 Testing

Comprehensive test suite with 100% pass rate:

```bash
cd backend/tests

# Run all tests
python run_all_tests.py

# Quick smoke tests
python run_all_tests.py --quick

# API tests only
python run_all_tests.py --api-only
```

**Test Coverage:**

- ✅ Data fetching and validation
- ✅ Technical indicator calculations
- ✅ Signal generation logic
- ✅ API endpoint responses
- ✅ Error handling and edge cases
- ✅ Performance benchmarks

## 📈 Performance

- **Response Time**: < 0.2 seconds for stock analysis
- **Data Points**: 250+ days of historical data
- **Signal Detection**: Real-time crossover identification
- **Memory Usage**: Optimized for large datasets
- **Reliability**: 100% uptime in testing

## 🔧 Configuration

### Risk Management (configurable)

```python
# In SimpleSignalGenerator
stop_loss_pct = 0.05    # 5% stop loss
take_profit_pct = 0.10  # 10% take profit
```

### Moving Average Windows (configurable)

```python
# In SimpleIndicators
short_window = 20  # 20-day MA
long_window = 50   # 50-day MA
```

## 🛣️ Roadmap

### Phase 1: Core Backend ✅ (Completed)

- [x] Stock data fetching
- [x] Technical indicators
- [x] Signal generation
- [x] FastAPI integration
- [x] Comprehensive testing

### Phase 2: Frontend Interface (In Progress)

- [ ] React application setup
- [ ] Interactive charts with Recharts/TradingView
- [ ] Signal visualization
- [ ] Real-time updates
- [ ] Responsive design with Tailwind CSS

### Phase 3: Advanced Features (Planned)

- [ ] Automated trade journaling
- [ ] Screenshot capture system
- [ ] Performance analytics dashboard
- [ ] Multiple trading strategies
- [ ] Alert and notification system

### Phase 4: Production Features (Future)

- [ ] Database integration
- [ ] Multi-user support
- [ ] Portfolio tracking
- [ ] Risk management tools
- [ ] Mobile application

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and analysis purposes only. All trading decisions and financial risks are the user's responsibility. Past performance does not guarantee future results. Always do your own research and consider consulting with a financial advisor before making investment decisions.

## 🙏 Acknowledgments

- [yfinance](https://pypi.org/project/yfinance/) for stock data
- [FastAPI](https://fastapi.tiangolo.com/) for the API framework
- [pandas](https://pandas.pydata.org/) for data manipulation
- [matplotlib](https://matplotlib.org/) for visualization

**⭐ Star this repository if you find it helpful!**
