"""
Step 1: Simple Data Fetcher
This is our foundation - everything starts with getting stock data
"""
import yfinance as yf
import pandas as pd
from datetime import datetime

class DataFetcher:
    """Simple class to fetch stock data from Yahoo Finance"""
    
    def __init__(self):
        print("📊 Data Fetcher initialized")
    
    def get_stock_data(self, symbol, period="6mo"):
        """
        Get stock data for a symbol
        
        Args:
            symbol: Stock symbol like 'AAPL', 'TSLA'
            period: How much data to get ('1mo', '3mo', '6mo', '1y')
        
        Returns:
            DataFrame with stock data (Open, High, Low, Close, Volume)
        """
        print(f"📥 Fetching {symbol} data for {period}...")
        
        try:
            # This is the magic line - yfinance does all the work
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            
            if data.empty:
                print(f"❌ No data found for {symbol}")
                return None
            
            print(f"✅ Got {len(data)} days of data for {symbol}")
            return data
            
        except Exception as e:
            print(f"❌ Error getting data: {e}")
            return None
    
    def show_basic_info(self, data, symbol):
        """Display basic information about the stock data"""
        if data is None:
            return
        
        print(f"\n📊 {symbol} - Basic Info")
        print("-" * 30)
        print(f"Date range: {data.index[0].strftime('%Y-%m-%d')} to {data.index[-1].strftime('%Y-%m-%d')}")
        print(f"Total days: {len(data)}")
        print(f"Current price: ${data['Close'].iloc[-1]:.2f}")
        print(f"Highest price: ${data['High'].max():.2f}")
        print(f"Lowest price: ${data['Low'].min():.2f}")
        
        # Show last 5 days
        print(f"\nLast 5 days:")
        print(data[['Close']].tail().round(2))