#!/usr/bin/env python3
"""
Trading Advisor:
This script analyzes stock data and calculates moving averages.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'src'))

# Import our modules
from data.data_fetcher import DataFetcher
from indicators.simple_indicators import SimpleIndicators
from signals.simple_signals import SimpleSignalGenerator

def main():
    """Main function - now with actual trading signals!"""
    print("🎯 Trading Advisor - Step 3: Signal Generation")
    print("=" * 55)
    
    # Get user input
    symbol = input("Enter a stock symbol (e.g., AAPL, TSLA, MSFT): ").upper().strip()
    
    if not symbol:
        symbol = "AAPL"
        print(f"Using default: {symbol}")
    
    print(f"\n🔍 Analyzing {symbol} for trading signals...")
    
    # Step 1: Get the data (need enough for crossover analysis)
    fetcher = DataFetcher()
    data = fetcher.get_stock_data(symbol, period="1y")  # 1 year for better signal detection
    
    if data is None:
        print("❌ Could not get data. Exiting.")
        return
    
    # Step 2: Calculate moving averages
    indicators = SimpleIndicators()
    data_with_indicators = indicators.add_moving_averages(data, short_window=20, long_window=50)
    
    if data_with_indicators is None:
        print("❌ Could not calculate indicators. Exiting.")
        return
    
    # Step 3: Generate signals
    signal_gen = SimpleSignalGenerator(stop_loss_pct=0.05, take_profit_pct=0.10)
    signals = signal_gen.find_crossover_signals(data_with_indicators, symbol)
    
    # Step 4: Display comprehensive analysis
    display_full_analysis(fetcher, indicators, signal_gen, data_with_indicators, signals, symbol)
    
    # Step 5: Show chart option
    show_chart = input("\n📊 Show chart with signals? (y/n): ").lower().strip()
    if show_chart in ['y', 'yes', '']:
        create_signal_chart(data_with_indicators, signals, symbol)

def display_full_analysis(fetcher, indicators, signal_gen, data_with_indicators, signals, symbol):
    """Display comprehensive trading analysis"""
    current_price = data_with_indicators['Close'].iloc[-1]
    
    # Basic stock info
    fetcher.show_basic_info(data_with_indicators, symbol)
    
    # Current technical status
    indicators.show_latest_values(data_with_indicators, symbol)
    indicators.analyze_trend(data_with_indicators, symbol)
    
    # Signal analysis
    signal_gen.display_signals_summary(signals, current_price)
    
    # Latest signal detailed analysis
    latest_signal = signal_gen.get_latest_signal(signals)
    if latest_signal:
        print(f"\n🎯 LATEST SIGNAL ANALYSIS")
        print("=" * 35)
        
        days_ago = (data_with_indicators.index[-1].date() - latest_signal['date'].date()).days
        print(f"Signal: {latest_signal['type']} on {latest_signal['date'].strftime('%Y-%m-%d')} ({days_ago} days ago)")
        print(f"Entry Price: ${latest_signal['price']:.2f}")
        print(f"Reason: {latest_signal['reason']}")
        
        if latest_signal['type'] == 'BUY':
            print(f"🛑 Stop Loss: ${latest_signal['stop_loss']:.2f} ({-signal_gen.stop_loss_pct*100:.1f}%)")
            print(f"🎯 Take Profit: ${latest_signal['take_profit']:.2f} (+{signal_gen.take_profit_pct*100:.1f}%)")
            print(f"💰 Risk/Reward: 1:{latest_signal['risk_reward_ratio']:.1f}")
            
            # Performance analysis
            performance = signal_gen.analyze_signal_performance(latest_signal, current_price)
            print(f"\n📊 CURRENT PERFORMANCE:")
            print(f"Current Price: ${performance['current_price']:.2f}")
            print(f"Return: {performance['current_return_pct']:+.1f}%")
            print(f"Status: {performance['status']}")
            print(f"Days Holding: {performance['days_holding']}")
    
    # Current recommendation
    current_ma_status = {
        'sma_20': data_with_indicators['SMA_20'].iloc[-1],
        'sma_50': data_with_indicators['SMA_50'].iloc[-1]
    }
    
    recommendation = signal_gen.get_current_recommendation(signals, current_ma_status)
    
    print(f"\n🎯 CURRENT RECOMMENDATION")
    print("=" * 35)
    print(recommendation)
    
    # Next action
    print(f"\n⏳ WHAT TO DO NEXT:")
    if latest_signal and latest_signal['type'] == 'BUY':
        performance = signal_gen.analyze_signal_performance(latest_signal, current_price)
        if performance['outcome'] == 'PENDING':
            print("• Monitor position for take profit or stop loss")
            print("• Set alerts at key levels")
            print(f"• Stop loss trigger: ${latest_signal['stop_loss']:.2f}")
            print(f"• Take profit trigger: ${latest_signal['take_profit']:.2f}")
        elif performance['outcome'] == 'WIN':
            print("• Take profit target reached - consider selling")
            print("• Or trail stop loss to lock in gains")
        elif performance['outcome'] == 'LOSS':
            print("• Stop loss triggered - exit position")
            print("• Wait for new signals")
    else:
        print("• Wait for next crossover signal")
        print("• Monitor moving average relationship")
        print("• Set alert for MA crossover")

def create_signal_chart(data, signals, symbol):
    """Create a chart showing price, moving averages, and signals"""
    try:
        import matplotlib.pyplot as plt
        
        print("📊 Creating signal chart...")
        
        # Create the plot
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), height_ratios=[3, 1])
        
        # Main price chart
        ax1.plot(data.index, data['Close'], label=f'{symbol} Close Price', linewidth=2, color='blue')
        ax1.plot(data.index, data['SMA_20'], label='20-day MA', linewidth=1.5, color='orange', alpha=0.8)
        ax1.plot(data.index, data['SMA_50'], label='50-day MA', linewidth=1.5, color='red', alpha=0.8)
        
        # Add signal markers
        for signal in signals:
            if signal['type'] == 'BUY':
                ax1.scatter(signal['date'], signal['price'], color='green', marker='^', 
                           s=100, zorder=5, label='BUY Signal' if signal == signals[0] else "")
                # Add stop loss and take profit lines for latest BUY signal
                if signal == signals[-1] and signal['type'] == 'BUY':
                    ax1.axhline(y=signal['stop_loss'], color='red', linestyle='--', alpha=0.5, label='Stop Loss')
                    ax1.axhline(y=signal['take_profit'], color='green', linestyle='--', alpha=0.5, label='Take Profit')
            else:  # SELL
                ax1.scatter(signal['date'], signal['price'], color='red', marker='v', 
                           s=100, zorder=5, label='SELL Signal' if signal == signals[0] else "")
        
        ax1.set_title(f'{symbol} - Price Action with Trading Signals', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Price ($)', fontsize=12)
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)
        
        # Moving average difference subplot (helps visualize crossovers)
        ma_diff = data['SMA_20'] - data['SMA_50']
        ax2.plot(data.index, ma_diff, label='MA Difference (20-50)', color='purple', linewidth=2)
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax2.fill_between(data.index, ma_diff, 0, where=(ma_diff > 0), color='green', alpha=0.3, label='Bullish')
        ax2.fill_between(data.index, ma_diff, 0, where=(ma_diff <= 0), color='red', alpha=0.3, label='Bearish')
        
        # Mark crossover points
        for signal in signals:
            ax2.scatter(signal['date'], 0, color='black', marker='o', s=50, zorder=5)
        
        ax2.set_title('Moving Average Crossover Indicator', fontsize=12)
        ax2.set_xlabel('Date', fontsize=12)
        ax2.set_ylabel('MA Difference', fontsize=10)
        ax2.legend(fontsize=9)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.xticks(rotation=45)
        plt.show()
        
        print("✅ Signal chart displayed!")
        
        # Educational explanation
        print("\n🎓 Chart Reading Guide:")
        print("• 🟢 Green triangles = BUY signals (MA crossover up)")
        print("• 🔴 Red triangles = SELL signals (MA crossover down)")  
        print("• Dashed lines = Current stop loss & take profit levels")
        print("• Bottom chart = MA difference (above 0 = bullish)")
        
    except ImportError:
        print("📊 Install matplotlib to see charts: pip install matplotlib")
    except Exception as e:
        print(f"📊 Chart error: {e}")

if __name__ == "__main__":
    main()