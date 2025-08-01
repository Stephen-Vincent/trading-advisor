#!/usr/bin/env python3
"""
Test Runner - Runs all component tests including API tests
"""
import sys
from pathlib import Path

# Import individual test modules
from test_data_fetcher import run_all_tests as test_data_fetcher
from test_simple_indicators import run_all_tests as test_indicators
from test_simple_signals import run_all_tests as test_signals
from test_api_endpoints import run_all_api_tests
from test_api_quick import quick_api_test

def run_component_tests():
    """Run all component tests (your existing Python modules)"""
    print("🧪 COMPONENT TESTS")
    print("=" * 50)
    
    test_modules = [
        ("DataFetcher", test_data_fetcher),
        ("SimpleIndicators", test_indicators),
        ("SimpleSignals", test_signals),
    ]
    
    passed_modules = 0
    
    for module_name, test_function in test_modules:
        print(f"\n📊 Testing {module_name}")
        print("-" * 30)
        
        try:
            if test_function():
                print(f"✅ {module_name} - All tests passed!")
                passed_modules += 1
            else:
                print(f"❌ {module_name} - Some tests failed")
        except Exception as e:
            print(f"❌ {module_name} - Test suite crashed: {e}")
    
    return passed_modules, len(test_modules)

def run_api_tests():
    """Run API endpoint tests"""
    print("\n🌐 API TESTS")
    print("=" * 50)
    
    try:
        api_passed = run_all_api_tests()
        return api_passed
    except Exception as e:
        print(f"❌ API tests crashed: {e}")
        return False

def run_all_tests():
    """Run all tests for the Trading Advisor"""
    print("🎯 Trading Advisor - Complete Test Suite")
    print("=" * 60)
    
    # Run component tests
    component_passed, component_total = run_component_tests()
    
    # Run API tests
    api_passed = run_api_tests()
    
    # Calculate overall results
    total_test_categories = component_total + 1  # +1 for API tests
    total_passed_categories = component_passed + (1 if api_passed else 0)
    
    # Final summary
    print("\n" + "=" * 60)
    print("🏁 COMPLETE TEST RESULTS")
    print("=" * 60)
    print(f"Component modules: {component_passed}/{component_total}")
    print(f"API tests: {'✅ PASSED' if api_passed else '❌ FAILED'}")
    print(f"Overall success: {total_passed_categories}/{total_test_categories} categories")
    print(f"Success rate: {(total_passed_categories/total_test_categories)*100:.1f}%")
    
    if total_passed_categories == total_test_categories:
        print("\n🎉 ALL TESTS PASSED! Your Trading Advisor backend is fully working.")
        print("🚀 Ready for frontend development!")
        return True
    else:
        print(f"\n⚠️  {total_test_categories - total_passed_categories} test category(ies) failed.")
        print("🔧 Fix failing tests before proceeding to frontend.")
        return False

def run_quick_tests():
    """Run quick smoke tests for development"""
    print("⚡ Trading Advisor - Quick Test Suite")
    print("=" * 50)
    
    # Quick component test (just data fetcher)
    print("🧪 Quick Component Test")
    print("-" * 30)
    try:
        component_ok = test_data_fetcher()
        if component_ok:
            print("✅ Core components working")
        else:
            print("❌ Core components failing")
    except Exception as e:
        print(f"❌ Component test failed: {e}")
        component_ok = False
    
    # Quick API test
    api_ok = quick_api_test()
    
    # Results
    tests_passed = (1 if component_ok else 0) + (1 if api_ok else 0)
    total_tests = 2
    
    print("\n" + "=" * 50)
    print(f"Quick Test Results: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 Quick tests passed! System is working.")
        return True
    else:
        print("⚠️  Quick tests show issues. Run full tests for details.")
        return False

def main():
    """Main test runner with options"""
    if len(sys.argv) > 1:
        if sys.argv[1] == '--quick':
            run_quick_tests()
        elif sys.argv[1] == '--api-only':
            run_api_tests()
        elif sys.argv[1] == '--components-only':
            run_component_tests()
        else:
            print("Usage: python run_all_tests.py [--quick|--api-only|--components-only]")
    else:
        run_all_tests()

if __name__ == "__main__":
    main()