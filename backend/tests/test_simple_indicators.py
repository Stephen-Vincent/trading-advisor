#!/usr/bin/env python3
"""
Tests for SimpleIndicators module
"""
import sys
from pathlib import Path
import pandas as pd

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from data.data_fetcher import DataFetcher
from indicators.simple_indicators import SimpleIndicators

def test_moving_average_calculation():
    """Test that moving averages are calculated correctly"""
    print("🧪 Test: Moving Average Calculation")
    print("-" * 40)
    
    # Create simple test data
    test_data = pd.DataFrame({
        'Close': [10, 12, 14, 16, 18, 20, 22, 24, 26, 28]
    })
    
    indicators = SimpleIndicators()
    result = indicators.add_moving_averages(test_data, short_window=3, long_window=5)
    
    # Check if columns were added
    if 'SMA_3' in result.columns and 'SMA_5' in result.columns:
        print("✅ Moving average columns added")
        
        # Check a specific calculation
        # For 3-day MA at index 4 (value 18): should be (14+16+18)/3 = 16
        expected_3day = (14 + 16 + 18) / 3
        actual_3day = result['SMA_3'].iloc[4]
        
        if abs(actual_3day - expected_3day) < 0.01:
            print(f"✅ 3-day MA calculation correct: {actual_3day:.2f}")
            return True
        else:
            print(f"❌ 3-day MA calculation wrong. Expected: {expected_3day}, Got: {actual_3day}")
            return False
    else:
        print("❌ Moving average columns not added")
        return False

def test_with_real_data():
    """Test indicators with real stock data"""
    print("\n🧪 Test: Real Stock Data Integration")
    print("-" * 40)
    
    # Get real data
    fetcher = DataFetcher()
    data = fetcher.get_stock_data("AAPL", "3mo")
    
    if data is None:
        print("❌ Could not fetch test data")
        return False
    
    # Calculate indicators
    indicators = SimpleIndicators()
    result = indicators.add_moving_averages(data, short_window=20, long_window=50)
    
    # Check results
    if result is not None and 'SMA_20' in result.columns and 'SMA_50' in result.columns:
        print("✅ Indicators calculated on real data")
        
        # Check that we have some non-NaN values
        sma_20_count = result['SMA_20'].notna().sum()
        sma_50_count = result['SMA_50'].notna().sum()
        
        print(f"✅ SMA_20 has {sma_20_count} valid values")
        print(f"✅ SMA_50 has {sma_50_count} valid values")
        
        # SMA_50 should have fewer valid values than SMA_20 (needs more days)
        if sma_50_count <= sma_20_count:
            print("✅ Longer MA has fewer valid values (as expected)")
            return True
        else:
            print("❌ MA value counts don't make sense")
            return False
    else:
        print("❌ Failed to calculate indicators on real data")
        return False

def test_latest_values_display():
    """Test the latest values display function"""
    print("\n🧪 Test: Latest Values Display")
    print("-" * 40)
    
    # Get data and calculate indicators
    fetcher = DataFetcher()
    data = fetcher.get_stock_data("AAPL", "3mo")
    
    if data is None:
        print("❌ Could not fetch test data")
        return False
    
    indicators = SimpleIndicators()
    data_with_indicators = indicators.add_moving_averages(data)
    
    # Test the display function (should not crash)
    try:
        print("Testing show_latest_values:")
        indicators.show_latest_values(data_with_indicators, "AAPL")
        print("✅ Latest values displayed without errors")
        return True
    except Exception as e:
        print(f"❌ Latest values display failed: {e}")
        return False

def test_trend_analysis():
    """Test the trend analysis function"""
    print("\n🧪 Test: Trend Analysis")
    print("-" * 40)
    
    # Get data with enough history for trend analysis
    fetcher = DataFetcher()
    data = fetcher.get_stock_data("AAPL", "6mo")  # 6 months for good MA calculation
    
    if data is None:
        print("❌ Could not fetch test data")
        return False
    
    indicators = SimpleIndicators()
    data_with_indicators = indicators.add_moving_averages(data)
    
    # Test trend analysis
    try:
        print("Testing analyze_trend:")
        indicators.analyze_trend(data_with_indicators, "AAPL")
        print("✅ Trend analysis completed without errors")
        return True
    except Exception as e:
        print(f"❌ Trend analysis failed: {e}")
        return False

def test_edge_cases():
    """Test edge cases like empty data"""
    print("\n🧪 Test: Edge Cases")
    print("-" * 40)
    
    indicators = SimpleIndicators()
    
    # Test with None data
    result1 = indicators.add_moving_averages(None)
    if result1 is None:
        print("✅ Correctly handled None data")
    else:
        print("❌ Should return None for None input")
        return False
    
    # Test with empty DataFrame
    empty_df = pd.DataFrame()
    result2 = indicators.add_moving_averages(empty_df)
    if result2 is None:
        print("✅ Correctly handled empty DataFrame")
    else:
        print("❌ Should return None for empty DataFrame")
        return False
    
    # Test display functions with None data
    try:
        indicators.show_latest_values(None, "TEST")
        indicators.analyze_trend(None, "TEST")
        print("✅ Display functions handle None data gracefully")
        return True
    except Exception as e:
        print(f"❌ Display functions should handle None data: {e}")
        return False

def run_all_tests():
    """Run all indicator tests"""
    print("🎯 Running SimpleIndicators Tests")
    print("=" * 50)
    
    tests = [
        test_moving_average_calculation,
        test_with_real_data,
        test_latest_values_display,
        test_trend_analysis,
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
        print("🎉 All SimpleIndicators tests passed!")
        return True
    else:
        print("⚠️  Some tests failed")
        return False

if __name__ == "__main__":
    run_all_tests()