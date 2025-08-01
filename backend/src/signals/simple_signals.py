"""
Simple Signal Generator
This is where we generate actual BUY/SELL signals based on moving average crossovers
"""
import pandas as pd
from datetime import datetime

class SimpleSignalGenerator:
    """Generate trading signals based on moving average crossovers"""
    
    def __init__(self, stop_loss_pct=0.05, take_profit_pct=0.10):
        """
        Initialize the signal generator
        
        Args:
            stop_loss_pct: Stop loss percentage (default 5%)
            take_profit_pct: Take profit percentage (default 10%)
        """
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct
        print(f"🚦 Signal Generator initialized (Stop: {stop_loss_pct*100}%, Target: {take_profit_pct*100}%)")
    
    def find_crossover_signals(self, data_with_indicators, symbol):
        """
        Find moving average crossover signals
        
        Trading Logic:
        - BUY Signal: When 20-day MA crosses ABOVE 50-day MA
        - SELL Signal: When 20-day MA crosses BELOW 50-day MA
        
        Args:
            data_with_indicators: DataFrame with moving averages
            symbol: Stock symbol for reference
            
        Returns:
            List of signal dictionaries
        """
        if data_with_indicators is None or len(data_with_indicators) < 51:
            print(f"❌ Not enough data for crossover analysis (need 51+ days)")
            return []
        
        print(f"🔍 Looking for crossover signals in {symbol}...")
        
        signals = []
        
        # We need both SMA columns
        if 'SMA_20' not in data_with_indicators.columns or 'SMA_50' not in data_with_indicators.columns:
            print("❌ Missing moving average data")
            return []
        
        # Look for crossovers by comparing each day to the previous day
        for i in range(1, len(data_with_indicators)):
            current_date = data_with_indicators.index[i]
            current_price = data_with_indicators['Close'].iloc[i]
            
            # Current day values
            sma_20_today = data_with_indicators['SMA_20'].iloc[i]
            sma_50_today = data_with_indicators['SMA_50'].iloc[i]
            
            # Previous day values
            sma_20_yesterday = data_with_indicators['SMA_20'].iloc[i-1]
            sma_50_yesterday = data_with_indicators['SMA_50'].iloc[i-1]
            
            # Skip if we don't have valid data for both days
            if (pd.isna(sma_20_today) or pd.isna(sma_50_today) or 
                pd.isna(sma_20_yesterday) or pd.isna(sma_50_yesterday)):
                continue
            
            # BUY SIGNAL: 20-day MA crosses ABOVE 50-day MA
            if (sma_20_yesterday <= sma_50_yesterday and sma_20_today > sma_50_today):
                signal = self._create_buy_signal(current_date, current_price, symbol)
                signals.append(signal)
                print(f"📈 BUY signal found: {current_date.strftime('%Y-%m-%d')} at ${current_price:.2f}")
            
            # SELL SIGNAL: 20-day MA crosses BELOW 50-day MA
            elif (sma_20_yesterday >= sma_50_yesterday and sma_20_today < sma_50_today):
                signal = self._create_sell_signal(current_date, current_price, symbol)
                signals.append(signal)
                print(f"📉 SELL signal found: {current_date.strftime('%Y-%m-%d')} at ${current_price:.2f}")
        
        print(f"✅ Found {len(signals)} crossover signals")
        return signals
    
    def _create_buy_signal(self, date, price, symbol):
        """Create a BUY signal with stop loss and take profit"""
        stop_loss = price * (1 - self.stop_loss_pct)
        take_profit = price * (1 + self.take_profit_pct)
        
        return {
            'date': date,
            'symbol': symbol,
            'type': 'BUY',
            'price': price,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'risk_reward_ratio': self.take_profit_pct / self.stop_loss_pct,
            'reason': 'SMA 20 crossed above SMA 50'
        }
    
    def _create_sell_signal(self, date, price, symbol):
        """Create a SELL signal"""
        return {
            'date': date,
            'symbol': symbol,
            'type': 'SELL',
            'price': price,
            'stop_loss': None,  # For sell signals, we might handle differently
            'take_profit': None,
            'risk_reward_ratio': None,
            'reason': 'SMA 20 crossed below SMA 50'
        }
    
    def get_latest_signal(self, signals):
        """Get the most recent signal"""
        if not signals:
            return None
        return signals[-1]
    
    def analyze_signal_performance(self, signal, current_price):
        """
        Analyze how a BUY signal is performing
        
        Args:
            signal: The signal dictionary
            current_price: Current stock price
            
        Returns:
            Performance analysis dictionary
        """
        if signal['type'] != 'BUY':
            return {'error': 'Performance analysis only for BUY signals'}
        
        entry_price = signal['price']
        stop_loss = signal['stop_loss']
        take_profit = signal['take_profit']
        
        # Calculate current return
        current_return_pct = ((current_price - entry_price) / entry_price) * 100
        
        # Determine status
        if current_price >= take_profit:
            status = '🎯 TARGET HIT'
            outcome = 'WIN'
        elif current_price <= stop_loss:
            status = '🛑 STOPPED OUT'
            outcome = 'LOSS'
        else:
            status = '⏳ ACTIVE'
            outcome = 'PENDING'
        
        # Days since signal
        days_since = (datetime.now().date() - signal['date'].date()).days
        
        return {
            'status': status,
            'outcome': outcome,
            'entry_price': entry_price,
            'current_price': current_price,
            'current_return_pct': current_return_pct,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'days_holding': days_since,
            'risk_reward_ratio': signal['risk_reward_ratio']
        }
    
    def display_signals_summary(self, signals, current_price=None):
        """Display a summary of all signals"""
        if not signals:
            print("📭 No signals found")
            return
        
        print(f"\n🚦 SIGNALS SUMMARY ({len(signals)} total)")
        print("=" * 50)
        
        buy_signals = [s for s in signals if s['type'] == 'BUY']
        sell_signals = [s for s in signals if s['type'] == 'SELL']
        
        print(f"📈 BUY signals: {len(buy_signals)}")
        print(f"📉 SELL signals: {len(sell_signals)}")
        
        # Show last 3 signals
        recent_signals = signals[-3:] if len(signals) > 3 else signals
        
        print(f"\n📋 Recent Signals:")
        for i, signal in enumerate(recent_signals, 1):
            date_str = signal['date'].strftime('%Y-%m-%d')
            print(f"{i}. {signal['type']} on {date_str} at ${signal['price']:.2f}")
            
            if signal['type'] == 'BUY':
                print(f"   🛑 Stop: ${signal['stop_loss']:.2f} | 🎯 Target: ${signal['take_profit']:.2f}")
                
                # Show performance if we have current price
                if current_price:
                    performance = self.analyze_signal_performance(signal, current_price)
                    print(f"   📊 {performance['status']} ({performance['current_return_pct']:+.1f}%)")
    
    def get_current_recommendation(self, signals, current_ma_status):
        """
        Get current trading recommendation based on signals and MA status
        
        Args:
            signals: List of all signals
            current_ma_status: Dict with current MA relationship
            
        Returns:
            Recommendation string
        """
        latest_signal = self.get_latest_signal(signals)
        
        if not latest_signal:
            # No signals yet, base on current MA relationship
            if current_ma_status.get('sma_20') > current_ma_status.get('sma_50', 0):
                return "🟢 WATCH FOR PULLBACK - Currently bullish, wait for better entry"
            else:
                return "🔴 STAY AWAY - Currently bearish trend"
        
        # We have signals
        days_since = (datetime.now().date() - latest_signal['date'].date()).days
        
        if latest_signal['type'] == 'BUY':
            if days_since <= 5:
                return "📈 RECENT BUY SIGNAL - Consider entry or monitor position"
            else:
                return "⏳ OLD BUY SIGNAL - Reassess current conditions"
        
        elif latest_signal['type'] == 'SELL':
            if days_since <= 5:
                return "📉 RECENT SELL SIGNAL - Avoid buying, consider exit"
            else:
                return "🔍 OLD SELL SIGNAL - Monitor for trend change"
        
        return "🤔 UNCLEAR - Review signals and current trend"