from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path
import pandas as pd

# Add your existing src to the path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from data.data_fetcher import DataFetcher
from indicators.simple_indicators import SimpleIndicators
from signals.simple_signals import SimpleSignalGenerator

app = FastAPI(title="Trading Advisor API", version="1.0.0")

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize your existing classes
data_fetcher = DataFetcher()
indicators = SimpleIndicators()
signal_generator = SimpleSignalGenerator()

@app.get("/")
async def root():
    return {"message": "Trading Advisor API", "status": "running"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "backend": "python", "frontend": "react"}

@app.get("/api/analyze/{symbol}")
async def analyze_stock(symbol: str, period: str = "6mo"):
    """
    Analyze a stock symbol using your existing trading logic
    """
    try:
        # Use your existing code!
        print(f"🔍 API: Analyzing {symbol} for {period}")
        
        # Step 1: Fetch data
        data = data_fetcher.get_stock_data(symbol, period)
        if data is None:
            raise HTTPException(status_code=404, detail=f"Could not fetch data for {symbol}")
        
        # Step 2: Calculate indicators
        data_with_indicators = indicators.add_moving_averages(data)
        if data_with_indicators is None:
            raise HTTPException(status_code=500, detail="Could not calculate indicators")
        
        # Step 3: Generate signals
        signals = signal_generator.find_crossover_signals(data_with_indicators, symbol)
        
        # Step 4: Prepare data for frontend
        latest_data = data_with_indicators.iloc[-1]
        
        # Calculate trend
        sma_20 = latest_data.get('SMA_20', 0)
        sma_50 = latest_data.get('SMA_50', 0)
        current_price = latest_data['Close']
        
        if pd.isna(sma_20) or pd.isna(sma_50):
            trend = "INSUFFICIENT_DATA"
            trend_strength = 0
        else:
            if current_price > sma_20 > sma_50:
                trend = "STRONG_BULLISH"
                trend_strength = ((sma_20 - sma_50) / sma_50) * 100
            elif current_price > sma_20 and sma_20 < sma_50:
                trend = "MIXED_BULLISH"
                trend_strength = ((sma_50 - sma_20) / sma_50) * 100
            elif current_price < sma_20 < sma_50:
                trend = "STRONG_BEARISH"
                trend_strength = ((sma_50 - sma_20) / sma_50) * 100
            else:
                trend = "MIXED_BEARISH"
                trend_strength = ((sma_20 - sma_50) / sma_50) * 100
        
        # Format signals for frontend
        formatted_signals = []
        for signal in signals:
            formatted_signal = {
                "id": f"{symbol}_{signal['date'].strftime('%Y%m%d')}_{signal['type']}",
                "date": signal['date'].isoformat(),
                "type": signal['type'],
                "price": round(float(signal['price']), 2),
                "reason": signal['reason']
            }
            
            if signal['type'] == 'BUY' and signal.get('stop_loss') and signal.get('take_profit'):
                formatted_signal.update({
                    "stop_loss": round(float(signal['stop_loss']), 2),
                    "take_profit": round(float(signal['take_profit']), 2),
                    "risk_reward_ratio": signal.get('risk_reward_ratio', 0)
                })
            
            formatted_signals.append(formatted_signal)
        
        # Prepare chart data
        chart_data = []
        for date, row in data_with_indicators.iterrows():
            chart_point = {
                "date": date.isoformat(),
                "close": round(float(row['Close']), 2),
                "volume": int(row.get('Volume', 0)),
            }
            
            # Add moving averages if available
            if not pd.isna(row.get('SMA_20', float('nan'))):
                chart_point["sma_20"] = round(float(row['SMA_20']), 2)
            if not pd.isna(row.get('SMA_50', float('nan'))):
                chart_point["sma_50"] = round(float(row['SMA_50']), 2)
                
            chart_data.append(chart_point)
        
        return {
            "symbol": symbol.upper(),
            "period": period,
            "current_price": round(float(current_price), 2),
            "sma_20": round(float(sma_20), 2) if not pd.isna(sma_20) else None,
            "sma_50": round(float(sma_50), 2) if not pd.isna(sma_50) else None,
            "trend": trend,
            "trend_strength": round(trend_strength, 2),
            "data_points": len(data_with_indicators),
            "signals": formatted_signals,
            "signals_count": {
                "total": len(signals),
                "buy": len([s for s in signals if s['type'] == 'BUY']),
                "sell": len([s for s in signals if s['type'] == 'SELL'])
            },
            "chart_data": chart_data,
            "analysis_timestamp": pd.Timestamp.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/api/signals")
async def get_all_signals(symbol: str = None):
    """Get signals for all stocks or specific symbol"""
    # This could be expanded to store/retrieve signals from a database
    return {"message": "Signals endpoint - to be implemented with database"}