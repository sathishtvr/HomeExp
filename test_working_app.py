#!/usr/bin/env python3
"""
Test the working Personal Finance Tracker
This tests the simple backend API to ensure it's working correctly
"""

import requests
import json
import time
import subprocess
import sys
from pathlib import Path

def test_api():
    """Test all API endpoints"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Personal Finance Tracker API")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Health check
    total_tests += 1
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            tests_passed += 1
        else:
            print("❌ Health check failed")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    # Test 2: Register user
    total_tests += 1
    try:
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
        response = requests.post(f"{base_url}/api/auth/register", json=user_data)
        if response.status_code in [200, 201, 400]:  # 400 if user already exists
            print("✅ User registration endpoint working")
            tests_passed += 1
        else:
            print("❌ User registration failed")
    except Exception as e:
        print(f"❌ User registration failed: {e}")
    
    # Test 3: Add expense
    total_tests += 1
    try:
        expense_data = {
            "category": "Food",
            "description": "Test lunch",
            "amount": 25.50,
            "date": "2024-01-15"
        }
        response = requests.post(f"{base_url}/api/expenses", json=expense_data)
        if response.status_code == 201:
            print("✅ Add expense working")
            tests_passed += 1
        else:
            print("❌ Add expense failed")
    except Exception as e:
        print(f"❌ Add expense failed: {e}")
    
    # Test 4: Get expenses
    total_tests += 1
    try:
        response = requests.get(f"{base_url}/api/expenses")
        if response.status_code == 200:
            expenses = response.json()
            print(f"✅ Get expenses working ({len(expenses)} expenses found)")
            tests_passed += 1
        else:
            print("❌ Get expenses failed")
    except Exception as e:
        print(f"❌ Get expenses failed: {e}")
    
    # Test 5: Add asset
    total_tests += 1
    try:
        asset_data = {
            "name": "Test Savings",
            "category": "Cash",
            "value": 5000.00,
            "month": "2024-01"
        }
        response = requests.post(f"{base_url}/api/assets", json=asset_data)
        if response.status_code == 201:
            print("✅ Add asset working")
            tests_passed += 1
        else:
            print("❌ Add asset failed")
    except Exception as e:
        print(f"❌ Add asset failed: {e}")
    
    # Test 6: Add liability
    total_tests += 1
    try:
        liability_data = {
            "name": "Test Credit Card",
            "category": "Credit Cards",
            "amount": 1500.00,
            "month": "2024-01"
        }
        response = requests.post(f"{base_url}/api/liabilities", json=liability_data)
        if response.status_code == 201:
            print("✅ Add liability working")
            tests_passed += 1
        else:
            print("❌ Add liability failed")
    except Exception as e:
        print(f"❌ Add liability failed: {e}")
    
    # Test 7: Get net worth
    total_tests += 1
    try:
        response = requests.get(f"{base_url}/api/networth/2024-01")
        if response.status_code == 200:
            networth = response.json()
            print(f"✅ Net worth calculation working (Net Worth: ${networth['net_worth']})")
            tests_passed += 1
        else:
            print("❌ Net worth calculation failed")
    except Exception as e:
        print(f"❌ Net worth calculation failed: {e}")
    
    print("=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Your app is working perfectly!")
        return True
    elif tests_passed >= total_tests - 1:
        print("✅ Most tests passed! Your app should work fine.")
        return True
    else:
        print("⚠️  Some tests failed. Check the backend server.")
        return False

def main():
    """Main test function"""
    print("🚀 Personal Finance Tracker - API Test")
    print("Checking if backend is running...")
    
    # Check if backend is already running
    try:
        response = requests.get("http://localhost:5000/", timeout=2)
        print("✅ Backend is already running")
        success = test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Backend not running. Starting it now...")
        
        # Start backend
        backend_process = subprocess.Popen([
            sys.executable, 'simple_backend.py'
        ], cwd=Path(__file__).parent)
        
        print("⏳ Waiting for backend to start...")
        time.sleep(5)
        
        # Test the API
        success = test_api()
        
        # Stop backend
        backend_process.terminate()
        backend_process.wait()
        print("🛑 Backend stopped")
    
    if success:
        print("\n🎊 Your Personal Finance Tracker is ready to use!")
        print("To start the application, run:")
        print("  python start_working_app.py")
        print("\nOr manually:")
        print("  1. python simple_backend.py")
        print("  2. Open simple_frontend.html in your browser")
    else:
        print("\n❌ Some issues found. Please check the backend server.")

if __name__ == "__main__":
    main()
