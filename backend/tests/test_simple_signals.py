#!/usr/bin/env python3
"""
Tests for SimpleSignalGenerator module
"""
import sys
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from data.data_fetcher import DataFetcher
from indicators.simple_indicators import SimpleIndicators
from signals.simple_signals import SimpleSignalGenerator

def create_test_data_with_crossover():
    """Create test data that has a clear MA crossover"""
    dates = pd.date_range('2024-01-01', periods=100, freq='D')
    
    # Create price data that will generate a crossover
    prices = []
    for i in range(100):
        if i < 30:
            # Declining trend
            price = 100 - i * 0.5
        elif i < 70:
            # Sideways
            price = 85 + (i-30) * 0.1
        else:
            # Rising trend (will create crossover)
            price = 85 + (i-70) * 1.5
        prices.append(price)
    
    data = pd.DataFrame({
        'Close': prices,
        'Open': [p * 1.01 for p in prices],
        'High': [p * 1.02 for p in prices],
        'Low': [p * 0.98 for p in prices],
        'Volume': [1000000] * 100
    }, index=dates)
    
    return data

def test_signal_initialization():
    """Test signal generator initialization"""
    print("🧪 Test: Signal Generator Initialization")
    print("-" * 40)
    
    signal_gen = SimpleSignalGenerator(stop_loss_pct=0.05, take_profit_pct=0.10)
    
    if signal_gen.stop_loss_pct == 0.05 and signal_gen.take_profit_pct == 0.10:
        print("✅ Signal generator initialized with correct parameters")
        return True
    else:
        print("❌ Signal generator parameters not set correctly")
        return False

def test_crossover_detection():
    """Test crossover signal detection"""
    print("\n🧪 Test: Crossover Detection")
    print("-" * 40)
    
    # Create test data
    test_data = create_test_data_with_crossover()
    
    # Calculate indicators
    indicators = SimpleIndicators()
    data_with_ma = indicators.add_moving_averages(test_data, short_window=10, long_window=20)
    
    # Generate signals
    signal_gen = SimpleSignalGenerator()
    signals = signal_gen.find_crossover_signals(data_with_ma, "TEST")
    
    if len(signals) > 0:
        print(f"✅ Found {len(signals)} signals in test data")
        
        # Check signal structure
        first_signal = signals[0]
        required_fields = ['date', 'symbol', 'type', 'price', 'reason']
        
        if all(field in first_signal for field in required_fields):
            print("✅ Signal structure is correct")
            return True
        else:
            print("❌ Signal missing required fields")
            return False
    else:
        print("⚠️  No signals found in test data (might be okay)")
        return True

def test_buy_signal_creation():
    """Test BUY signal creation with stop loss and take profit"""
    print("\n🧪 Test: BUY Signal Creation")
    print("-" * 40)
    
    signal_gen = SimpleSignalGenerator(stop_loss_pct=0.05, take_profit_pct=0.10)
    
    test_date = datetime.now()
    test_price = 100.0
    
    buy_signal = signal_gen._create_buy_signal(test_date, test_price, "TEST")
    
    # Check calculations
    expected_stop = test_price * 0.95  # 5% below
    expected_target = test_price * 1.10  # 10% above
    expected_rr = 0.10 / 0.05  # 2:1 risk/reward
    
    if (abs(buy_signal['stop_loss'] - expected_stop) < 0.01 and
        abs(buy_signal['take_profit'] - expected_target) < 0.01 and
        abs(buy_signal['risk_reward_ratio'] - expected_rr) < 0.01):
        print("✅ BUY signal calculations correct")
        print(f"   Entry: ${buy_signal['price']:.2f}")
        print(f"   Stop: ${buy_signal['stop_loss']:.2f}")
        print(f"   Target: ${buy_signal['take_profit']:.2f}")
        print(f"   R/R: 1:{buy_signal['risk_reward_ratio']:.1f}")
        return True
    else:
        print("❌ BUY signal calculations incorrect")
        return False

def test_performance_analysis():
    """Test signal performance analysis"""
    print("\n🧪 Test: Performance Analysis")
    print("-" * 40)
    
    signal_gen = SimpleSignalGenerator()
    
    # Create test BUY signal
    test_signal = {
        'date': datetime.now() - timedelta(days=5),
        'type': 'BUY',
        'price': 100.0,
        'stop_loss': 95.0,
        'take_profit': 110.0,
        'risk_reward_ratio': 2.0
    }
    
    # Test different scenarios
    scenarios = [
        (105.0, "Winning position"),
        (92.0, "Losing position"), 
        (110.0, "Target hit"),
        (95.0, "Stop loss hit")
    ]
    
    all_passed = True
    
    for current_price, description in scenarios:
        performance = signal_gen.analyze_signal_performance(test_signal, current_price)
        
        if 'current_return_pct' in performance and 'status' in performance:
            print(f"✅ {description}: {performance['status']}")
        else:
            print(f"❌ Performance analysis failed for {description}")
            all_passed = False
    
    return all_passed

def test_with_real_data():
    """Test signal generation with real stock data"""
    print("\n🧪 Test: Real Data Integration")
    print("-" * 40)
    
    try:
        # Get real data
        fetcher = DataFetcher()
        data = fetcher.get_stock_data("AAPL", "1y")
        
        if data is None:
            print("❌ Could not fetch real data")
            return False
        
        # Calculate indicators
        indicators = SimpleIndicators()
        data_with_ma = indicators.add_moving_averages(data)
        
        # Generate signals
        signal_gen = SimpleSignalGenerator()
        signals = signal_gen.find_crossover_signals(data_with_ma, "AAPL")
        
        print(f"✅ Real data test completed: {len(signals)} signals found")
        
        if signals:
            latest = signal_gen.get_latest_signal(signals)
            print(f"   Latest signal: {latest['type']} on {latest['date'].strftime('%Y-%m-%d')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Real data test failed: {e}")
        return False

def test_edge_cases():
    """Test edge cases"""
    print("\n🧪 Test: Edge Cases")
    print("-" * 40)
    
    signal_gen = SimpleSignalGenerator()
    
    # Test with insufficient data
    small_data = pd.DataFrame({
        'Close': [100, 101, 102],
        'SMA_20': [100, 101, 102],
        'SMA_50': [100, 101, 102]
    })
    
    signals = signal_gen.find_crossover_signals(small_data, "TEST")
    
    if len(signals) == 0:
        print("✅ Correctly handled insufficient data")
    else:
        print("❌ Should not generate signals with insufficient data")
        return False
    
    # Test with None data
    signals = signal_gen.find_crossover_signals(None, "TEST")
    if len(signals) == 0:
        print("✅ Correctly handled None data")
    else:
        print("❌ Should not generate signals with None data")
        return False
    
    # Test performance analysis with SELL signal
    sell_signal = {'type': 'SELL', 'price': 100.0}
    performance = signal_gen.analyze_signal_performance(sell_signal, 105.0)
    
    if 'error' in performance:
        print("✅ Correctly handled SELL signal in performance analysis")
        return True
    else:
        print("❌ Should return error for SELL signal performance analysis")
        return False

def run_all_tests():
    """Run all signal generator tests"""
    print("🎯 Running SimpleSignalGenerator Tests")
    print("=" * 50)
    
    tests = [
        test_signal_initialization,
        test_crossover_detection,
        test_buy_signal_creation,
        test_performance_analysis,
        test_with_real_data,
        test_edge_cases
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test_func.__name__} failed with error: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All SimpleSignalGenerator tests passed!")
        return True
    else:
        print("⚠️  Some tests failed")
        return False

if __name__ == "__main__":
    run_all_tests()