#!/usr/bin/env python3
"""
Tests for DataFetcher module
"""
import sys
from pathlib import Path

# Add src to path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from data.data_fetcher import DataFetcher

def test_basic_data_fetch():
    """Test basic data fetching functionality"""
    print("🧪 Test: Basic Data Fetch")
    print("-" * 40)
    
    fetcher = DataFetcher()
    
    # Test with Apple stock
    symbol = "AAPL"
    data = fetcher.get_stock_data(symbol, "1mo")
    
    if data is not None and not data.empty:
        print(f"✅ Successfully fetched {len(data)} days of {symbol} data")
        print(f"✅ Data has required columns: {list(data.columns)}")
        print(f"✅ Latest close price: ${data['Close'].iloc[-1]:.2f}")
        return True
    else:
        print(f"❌ Failed to fetch data for {symbol}")
        return False

def test_invalid_symbol():
    """Test what happens with invalid stock symbol"""
    print("\n🧪 Test: Invalid Symbol")
    print("-" * 40)
    
    fetcher = DataFetcher()
    
    # Test with obviously invalid symbol
    invalid_symbol = "INVALIDSTOCK123"
    data = fetcher.get_stock_data(invalid_symbol, "1mo")
    
    if data is None:
        print(f"✅ Correctly handled invalid symbol: {invalid_symbol}")
        return True
    else:
        print(f"❌ Should have returned None for invalid symbol")
        return False

def test_different_periods():
    """Test different time periods"""
    print("\n🧪 Test: Different Time Periods")
    print("-" * 40)
    
    fetcher = DataFetcher()
    symbol = "AAPL"
    
    periods = ["1mo", "3mo", "6mo"]
    results = {}
    
    for period in periods:
        data = fetcher.get_stock_data(symbol, period)
        if data is not None:
            results[period] = len(data)
            print(f"✅ {period}: {len(data)} days")
        else:
            results[period] = 0
            print(f"❌ {period}: Failed")
    
    # Check that longer periods have more data
    if results["6mo"] > results["3mo"] > results["1mo"]:
        print("✅ Longer periods return more data as expected")
        return True
    else:
        print("❌ Period data counts don't make sense")
        return False

def test_show_basic_info():
    """Test the basic info display function"""
    print("\n🧪 Test: Basic Info Display")
    print("-" * 40)
    
    fetcher = DataFetcher()
    data = fetcher.get_stock_data("AAPL", "1mo")
    
    if data is not None:
        print("Testing show_basic_info function:")
        fetcher.show_basic_info(data, "AAPL")
        print("✅ Basic info displayed without errors")
        return True
    else:
        print("❌ No data to test basic info display")
        return False

def run_all_tests():
    """Run all data fetcher tests"""
    print("🎯 Running DataFetcher Tests")
    print("=" * 50)
    
    tests = [
        test_basic_data_fetch,
        test_invalid_symbol,
        test_different_periods,
        test_show_basic_info
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
        print("🎉 All DataFetcher tests passed!")
        return True
    else:
        print("⚠️  Some tests failed")
        return False

if __name__ == "__main__":
    run_all_tests()