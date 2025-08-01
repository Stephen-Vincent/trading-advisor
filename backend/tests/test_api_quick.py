#!/usr/bin/env python3
"""
Quick API tests - Fast smoke tests for development
"""
import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add the backend directory to path
sys.path.append(str(Path(__file__).parent.parent))

from api.api import app

client = TestClient(app)

def quick_health_test():
    """Quick health check"""
    print("🚀 Quick API Health Check")
    print("-" * 30)
    
    try:
        # Test basic endpoints
        response = client.get("/")
        assert response.status_code == 200
        print("✅ Root endpoint: OK")
        
        response = client.get("/api/health")
        assert response.status_code == 200
        print("✅ Health endpoint: OK")
        
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def quick_analysis_test():
    """Quick analysis test with AAPL"""
    print("\n🔍 Quick Analysis Test")
    print("-" * 30)
    
    try:
        response = client.get("/api/analyze/AAPL?period=1mo")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ AAPL Analysis: ${data['current_price']:.2f}")
            print(f"   • Data points: {data['data_points']}")
            print(f"   • Signals: {len(data['signals'])}")
            print(f"   • Trend: {data['trend']}")
            return True
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Analysis test failed: {e}")
        return False

def quick_api_test():
    """Run quick API tests"""
    print("⚡ Trading Advisor - Quick API Test")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 2
    
    if quick_health_test():
        tests_passed += 1
    
    if quick_analysis_test():
        tests_passed += 1
    
    print("\n" + "=" * 50)
    print(f"Quick Test Results: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 Quick tests passed! API is working.")
        return True
    else:
        print("⚠️  Some quick tests failed.")
        return False

if __name__ == "__main__":
    quick_api_test()