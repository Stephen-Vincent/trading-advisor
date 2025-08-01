"""
Step 2: Simple Moving Averages
This is where trading strategy begins - we calculate trend indicators
"""
import pandas as pd

class SimpleIndicators:
    """Calculate basic trading indicators"""
    
    def __init__(self):
        print("📈 Simple Indicators initialized")
    
    def add_moving_averages(self, data, short_window=20, long_window=50):
        """
        Add moving averages to our stock data
        
        Moving Average = average price over X days
        - Short MA (20 days): Reacts quickly to price changes
        - Long MA (50 days): Shows longer-term trend
        
        Args:
            data: Stock data DataFrame
            short_window: Days for short moving average (default 20)
            long_window: Days for long moving average (default 50)
            
        Returns:
            DataFrame with moving averages added
        """
        if data is None or data.empty:
            print("❌ No data to calculate indicators")
            return None
        
        print(f"📊 Calculating moving averages ({short_window} and {long_window} days)...")
        
        # Make a copy so we don't modify the original data
        result = data.copy()
        
        # Calculate Simple Moving Averages
        # .rolling(window) creates a "rolling window" of X days
        # .mean() calculates the average of those X days
        result[f'SMA_{short_window}'] = result['Close'].rolling(window=short_window).mean()
        result[f'SMA_{long_window}'] = result['Close'].rolling(window=long_window).mean()
        
        print(f"✅ Moving averages calculated")
        return result
    
    def show_latest_values(self, data_with_indicators, symbol):
        """Show the latest price and indicator values"""
        if data_with_indicators is None:
            return
        
        # Get the most recent row (last trading day)
        latest = data_with_indicators.iloc[-1]
        
        print(f"\n📊 {symbol} - Latest Values")
        print("-" * 35)
        print(f"Close Price:    ${latest['Close']:.2f}")
        
        # Check if we have the moving averages (might be NaN for early days)
        if 'SMA_20' in latest and not pd.isna(latest['SMA_20']):
            print(f"20-day Average: ${latest['SMA_20']:.2f}")
        else:
            print(f"20-day Average: Not enough data yet")
            
        if 'SMA_50' in latest and not pd.isna(latest['SMA_50']):
            print(f"50-day Average: ${latest['SMA_50']:.2f}")
        else:
            print(f"50-day Average: Not enough data yet")
    
    def analyze_trend(self, data_with_indicators, symbol):
        """
        Analyze the trend based on moving averages
        This is the foundation of our trading strategy!
        """
        if data_with_indicators is None:
            return
        
        latest = data_with_indicators.iloc[-1]
        
        # Check if we have both moving averages
        if pd.isna(latest.get('SMA_20')) or pd.isna(latest.get('SMA_50')):
            print(f"\n🔍 {symbol} - Trend Analysis")
            print("⏳ Not enough data for full analysis yet (need 50+ days)")
            return
        
        current_price = latest['Close']
        sma_20 = latest['SMA_20']
        sma_50 = latest['SMA_50']
        
        print(f"\n🔍 {symbol} - Trend Analysis")
        print("-" * 35)
        
        # Analyze the relationship between price and moving averages
        if current_price > sma_20 > sma_50:
            trend = "🟢 STRONG BULLISH"
            explanation = "Price above both averages, short MA above long MA"
        elif current_price > sma_20 and sma_20 < sma_50:
            trend = "🟡 MIXED (Price up, but trend weakening)"
            explanation = "Price above short MA, but short MA below long MA"
        elif current_price < sma_20 < sma_50:
            trend = "🔴 STRONG BEARISH"
            explanation = "Price below both averages, short MA below long MA"
        elif current_price < sma_20 and sma_20 > sma_50:
            trend = "🟡 MIXED (Price down, but trend strengthening)"
            explanation = "Price below short MA, but short MA above long MA"
        else:
            trend = "🟡 NEUTRAL"
            explanation = "Mixed signals"
        
        print(f"Trend: {trend}")
        print(f"Logic: {explanation}")
        
        # Show the actual numbers
        print(f"\nNumbers:")
        print(f"  Current Price: ${current_price:.2f}")
        print(f"  20-day MA:     ${sma_20:.2f}")
        print(f"  50-day MA:     ${sma_50:.2f}")