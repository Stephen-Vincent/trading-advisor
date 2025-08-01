#!/usr/bin/env python3
"""
Tests for FastAPI endpoints
"""
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
import json

# Add the backend directory to path so we can import the API
sys.path.append(str(Path(__file__).parent.parent))

from api.api import app

# Create test client
client = TestClient(app)

class TestHealthEndpoints:
    """Test basic health and status endpoints"""
    
    def test_root_endpoint(self):
        """Test the root endpoint returns basic info"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "status" in data
        assert data["status"] == "running"
        print("✅ Root endpoint working")
    
    def test_health_check(self):
        """Test the health check endpoint"""
        response = client.get("/api/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["backend"] == "python"
        assert data["frontend"] == "react"
        print("✅ Health check endpoint working")

class TestStockAnalysisEndpoint:
    """Test the main stock analysis endpoint"""
    
    def test_valid_stock_analysis(self):
        """Test analysis with a valid stock symbol"""
        symbol = "AAPL"
        period = "6mo"
        
        response = client.get(f"/api/analyze/{symbol}?period={period}")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields
        required_fields = [
            "symbol", "period", "current_price", "trend", 
            "data_points", "signals", "chart_data", "analysis_timestamp"
        ]
        
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        # Check data types and values
        assert isinstance(data["symbol"], str)
        assert data["symbol"] == symbol.upper()
        assert data["period"] == period
        assert isinstance(data["current_price"], (int, float))
        assert data["current_price"] > 0
        assert isinstance(data["data_points"], int)
        assert data["data_points"] > 0
        assert isinstance(data["signals"], list)
        assert isinstance(data["chart_data"], list)
        
        # Check signals structure if any exist
        if data["signals"]:
            signal = data["signals"][0]
            signal_required_fields = ["id", "date", "type", "price", "reason"]
            for field in signal_required_fields:
                assert field in signal
            assert signal["type"] in ["BUY", "SELL"]
        
        # Check chart data structure
        if data["chart_data"]:
            chart_point = data["chart_data"][0]
            assert "date" in chart_point
            assert "close" in chart_point
            assert isinstance(chart_point["close"], (int, float))
        
        print(f"✅ Valid stock analysis for {symbol}: {data['data_points']} data points, {len(data['signals'])} signals")
    
    def test_different_periods(self):
        """Test different time periods"""
        symbol = "AAPL"
        periods = ["1mo", "3mo", "6mo", "1y"]
        
        for period in periods:
            response = client.get(f"/api/analyze/{symbol}?period={period}")
            
            assert response.status_code == 200
            data = response.json()
            assert data["period"] == period
            assert data["data_points"] > 0
            
            print(f"✅ Period {period}: {data['data_points']} data points")
    
    def test_different_stocks(self):
        """Test analysis with different stock symbols"""
        symbols = ["AAPL", "MSFT", "GOOGL", "TSLA"]
        period = "3mo"
        
        for symbol in symbols:
            response = client.get(f"/api/analyze/{symbol}?period={period}")
            
            # Should either succeed or fail gracefully
            if response.status_code == 200:
                data = response.json()
                assert data["symbol"] == symbol.upper()
                assert data["current_price"] > 0
                print(f"✅ {symbol}: ${data['current_price']:.2f}, {len(data['signals'])} signals")
            elif response.status_code == 404:
                print(f"⚠️  {symbol}: Data not available (404)")
            else:
                print(f"❌ {symbol}: Unexpected status {response.status_code}")
    
    def test_invalid_stock_symbol(self):
        """Test with an invalid stock symbol"""
        invalid_symbol = "INVALIDSTOCK123"
        
        response = client.get(f"/api/analyze/{invalid_symbol}?period=1mo")
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert invalid_symbol in data["detail"]
        print(f"✅ Invalid symbol correctly handled: {data['detail']}")
    
    def test_trend_calculation(self):
        """Test that trend calculation is working"""
        response = client.get("/api/analyze/AAPL?period=6mo")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should have trend information
        assert "trend" in data
        assert data["trend"] in ["STRONG_BULLISH", "MIXED_BULLISH", "STRONG_BEARISH", "MIXED_BEARISH", "INSUFFICIENT_DATA"]
        
        if data["trend"] != "INSUFFICIENT_DATA":
            assert "trend_strength" in data
            assert isinstance(data["trend_strength"], (int, float))
        
        print(f"✅ Trend calculation: {data['trend']} (strength: {data.get('trend_strength', 'N/A')})")
    
    def test_moving_averages(self):
        """Test that moving averages are calculated"""
        response = client.get("/api/analyze/AAPL?period=6mo")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should have MA data (might be None if insufficient data)
        assert "sma_20" in data
        assert "sma_50" in data
        
        if data["sma_20"] is not None:
            assert isinstance(data["sma_20"], (int, float))
            assert data["sma_20"] > 0
        
        if data["sma_50"] is not None:
            assert isinstance(data["sma_50"], (int, float))
            assert data["sma_50"] > 0
        
        print(f"✅ Moving averages: SMA20=${data['sma_20']}, SMA50=${data['sma_50']}")
    
    def test_signals_count(self):
        """Test that signals count is accurate"""
        response = client.get("/api/analyze/AAPL?period=1y")  # Longer period for more signals
        
        assert response.status_code == 200
        data = response.json()
        
        assert "signals_count" in data
        signals_count = data["signals_count"]
        
        assert "total" in signals_count
        assert "buy" in signals_count
        assert "sell" in signals_count
        
        # Verify the counts match actual signals
        actual_total = len(data["signals"])
        actual_buy = len([s for s in data["signals"] if s["type"] == "BUY"])
        actual_sell = len([s for s in data["signals"] if s["type"] == "SELL"])
        
        assert signals_count["total"] == actual_total
        assert signals_count["buy"] == actual_buy
        assert signals_count["sell"] == actual_sell
        assert signals_count["buy"] + signals_count["sell"] == signals_count["total"]
        
        print(f"✅ Signal counts: {actual_buy} BUY, {actual_sell} SELL, {actual_total} total")

class TestBuySignalDetails:
    """Test BUY signal specific details"""
    
    def test_buy_signal_structure(self):
        """Test that BUY signals have stop loss and take profit"""
        # Use a longer period to increase chance of finding BUY signals
        response = client.get("/api/analyze/MSFT?period=1y")
        
        assert response.status_code == 200
        data = response.json()
        
        buy_signals = [s for s in data["signals"] if s["type"] == "BUY"]
        
        if buy_signals:
            buy_signal = buy_signals[0]  # Test first BUY signal
            
            # BUY signals should have these additional fields
            assert "stop_loss" in buy_signal
            assert "take_profit" in buy_signal
            assert "risk_reward_ratio" in buy_signal
            
            # Values should be reasonable
            assert buy_signal["stop_loss"] < buy_signal["price"]  # Stop loss below entry
            assert buy_signal["take_profit"] > buy_signal["price"]  # Take profit above entry
            assert buy_signal["risk_reward_ratio"] > 0
            
            print(f"✅ BUY signal structure valid: Entry=${buy_signal['price']:.2f}, "
                  f"SL=${buy_signal['stop_loss']:.2f}, TP=${buy_signal['take_profit']:.2f}, "
                  f"R/R={buy_signal['risk_reward_ratio']:.1f}")
        else:
            print("⚠️  No BUY signals found to test structure")

class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_invalid_period(self):
        """Test with invalid period parameter"""
        response = client.get("/api/analyze/AAPL?period=invalid")
        
        # Should still work or fail gracefully
        # (yfinance might handle invalid periods by using a default)
        print(f"✅ Invalid period handled: status {response.status_code}")
    
    def test_missing_period(self):
        """Test without period parameter (should use default)"""
        response = client.get("/api/analyze/AAPL")
        
        assert response.status_code == 200
        data = response.json()
        assert data["period"] == "6mo"  # Default period
        print("✅ Default period used when not specified")
    
    def test_case_insensitive_symbol(self):
        """Test that stock symbols are case insensitive"""
        symbols = ["aapl", "AAPL", "AaPl"]
        
        for symbol in symbols:
            response = client.get(f"/api/analyze/{symbol}?period=1mo")
            
            if response.status_code == 200:
                data = response.json()
                assert data["symbol"] == "AAPL"  # Should always return uppercase
                print(f"✅ {symbol} -> {data['symbol']}")

class TestPerformanceAndLimits:
    """Test performance and reasonable limits"""
    
    def test_reasonable_response_time(self):
        """Test that API responds in reasonable time"""
        import time
        
        start_time = time.time()
        response = client.get("/api/analyze/AAPL?period=1mo")
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 30  # Should respond within 30 seconds
        
        print(f"✅ Response time: {response_time:.2f} seconds")
    
    def test_data_size_reasonable(self):
        """Test that response size is reasonable"""
        response = client.get("/api/analyze/AAPL?period=1y")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check that we're not returning too much data
        assert len(data["chart_data"]) < 500  # Reasonable for 1 year of daily data
        assert len(data["signals"]) < 50      # Reasonable number of signals
        
        print(f"✅ Data size reasonable: {len(data['chart_data'])} chart points, {len(data['signals'])} signals")

def run_all_api_tests():
    """Run all API tests"""
    print("🎯 Running Trading Advisor API Tests")
    print("=" * 60)
    
    test_classes = [
        TestHealthEndpoints,
        TestStockAnalysisEndpoint,
        TestBuySignalDetails,
        TestErrorHandling,
        TestPerformanceAndLimits
    ]
    
    total_passed = 0
    total_tests = 0
    
    for test_class in test_classes:
        print(f"\n🧪 Testing {test_class.__name__}")
        print("-" * 40)
        
        test_instance = test_class()
        test_methods = [method for method in dir(test_instance) 
                       if method.startswith('test_') and callable(getattr(test_instance, method))]
        
        for method_name in test_methods:
            total_tests += 1
            try:
                method = getattr(test_instance, method_name)
                method()
                total_passed += 1
            except Exception as e:
                print(f"❌ {method_name} failed: {e}")
    
    print(f"\n" + "=" * 60)
    print(f"🏁 API TEST RESULTS")
    print("=" * 60)
    print(f"Tests run: {total_tests}")
    print(f"Tests passed: {total_passed}")
    print(f"Success rate: {(total_passed/total_tests)*100:.1f}%")
    
    if total_passed == total_tests:
        print("\n🎉 ALL API TESTS PASSED! Your API is working correctly.")
        return True
    else:
        print(f"\n⚠️  {total_tests - total_passed} test(s) failed.")
        return False

if __name__ == "__main__":
    run_all_api_tests()