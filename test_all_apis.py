#!/usr/bin/env python3
"""
Comprehensive API Testing Script for Professional Finance Manager
Tests all backend endpoints and identifies issues.
"""

import requests
import json
import time
import sys
from pathlib import Path

# Configuration
API_BASE = "http://localhost:5000"
TIMEOUT = 5

def test_server_connection():
    """Test if the backend server is running."""
    print("Testing server connection...")
    try:
        response = requests.get(f"{API_BASE}/", timeout=TIMEOUT)
        print(f"   OK - Server responding (Status: {response.status_code})")
        return True
    except requests.exceptions.ConnectionError:
        print("   ERROR - Server not responding. Please start the backend first.")
        return False
    except Exception as e:
        print(f"   ERROR - Connection failed: {e}")
        return False

def test_template_endpoints():
    """Test all template-related endpoints."""
    print("\nTesting Template Endpoints:")
    
    endpoints = [
        "/api/templates/expense",
        "/api/templates/expense/categories",
        "/api/templates/asset", 
        "/api/templates/asset/categories",
        "/api/templates/liability",
        "/api/templates/liability/categories",
        "/api/templates/income",
        "/api/templates/income/categories"
    ]
    
    results = {}
    for endpoint in endpoints:
        try:
            response = requests.get(f"{API_BASE}{endpoint}", timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                results[endpoint] = {"status": "OK", "count": len(data), "data": data}
                print(f"   OK - {endpoint} ({len(data)} items)")
            else:
                results[endpoint] = {"status": "ERROR", "code": response.status_code}
                print(f"   ERROR - {endpoint} (Status: {response.status_code})")
        except Exception as e:
            results[endpoint] = {"status": "ERROR", "error": str(e)}
            print(f"   ERROR - {endpoint} ({e})")
    
    return results

def test_data_endpoints():
    """Test all data management endpoints."""
    print("\nTesting Data Endpoints:")
    
    endpoints = [
        "/api/expenses",
        "/api/assets", 
        "/api/liabilities",
        "/api/income"
    ]
    
    results = {}
    for endpoint in endpoints:
        try:
            response = requests.get(f"{API_BASE}{endpoint}", timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                results[endpoint] = {"status": "OK", "count": len(data)}
                print(f"   OK - {endpoint} ({len(data)} items)")
            else:
                results[endpoint] = {"status": "ERROR", "code": response.status_code}
                print(f"   ERROR - {endpoint} (Status: {response.status_code})")
        except Exception as e:
            results[endpoint] = {"status": "ERROR", "error": str(e)}
            print(f"   ERROR - {endpoint} ({e})")
    
    return results

def test_investment_endpoints():
    """Test investment-related endpoints."""
    print("\nTesting Investment Endpoints:")
    
    endpoints = [
        "/api/rd",
        "/api/chit",
        "/api/goldchit"
    ]
    
    results = {}
    for endpoint in endpoints:
        try:
            response = requests.get(f"{API_BASE}{endpoint}", timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                results[endpoint] = {"status": "OK", "count": len(data)}
                print(f"   OK - {endpoint} ({len(data)} items)")
            else:
                results[endpoint] = {"status": "ERROR", "code": response.status_code}
                print(f"   ERROR - {endpoint} (Status: {response.status_code})")
        except Exception as e:
            results[endpoint] = {"status": "ERROR", "error": str(e)}
            print(f"   ERROR - {endpoint} ({e})")
    
    return results

def test_post_endpoints():
    """Test POST endpoints with sample data."""
    print("\nTesting POST Endpoints:")
    
    # Test adding an expense template
    try:
        template_data = {
            "category": "Test Category",
            "subcategory": "Test Subcategory", 
            "description": "Test template",
            "default_amount": 100
        }
        response = requests.post(f"{API_BASE}/api/templates/expense", 
                               json=template_data, timeout=TIMEOUT)
        if response.status_code == 200:
            print("   OK - POST /api/templates/expense")
        else:
            print(f"   ERROR - POST /api/templates/expense (Status: {response.status_code})")
    except Exception as e:
        print(f"   ERROR - POST /api/templates/expense ({e})")
    
    # Test adding an expense
    try:
        expense_data = {
            "category": "Test Category",
            "description": "Test expense",
            "amount": 50.0,
            "date": "2025-01-08"
        }
        response = requests.post(f"{API_BASE}/api/expenses", 
                               json=expense_data, timeout=TIMEOUT)
        if response.status_code == 200:
            print("   OK - POST /api/expenses")
        else:
            print(f"   ERROR - POST /api/expenses (Status: {response.status_code})")
    except Exception as e:
        print(f"   ERROR - POST /api/expenses ({e})")

def check_database_file():
    """Check if database file exists and has data."""
    print("\nChecking Database:")
    
    db_files = ["finance_simple.db", "finance_app.db"]
    found_db = False
    
    for db_file in db_files:
        db_path = Path(db_file)
        if db_path.exists():
            size = db_path.stat().st_size
            print(f"   OK - {db_file} exists ({size:,} bytes)")
            found_db = True
        else:
            print(f"   INFO - {db_file} not found")
    
    if not found_db:
        print("   WARNING - No database file found")
    
    return found_db

def run_comprehensive_test():
    """Run all tests and provide summary."""
    print("=" * 60)
    print("COMPREHENSIVE API TEST - Professional Finance Manager")
    print("=" * 60)
    
    # Test server connection
    if not test_server_connection():
        print("\nFAILED: Backend server is not running!")
        print("Please run: python simple_backend.py")
        return False
    
    # Check database
    check_database_file()
    
    # Test all endpoints
    template_results = test_template_endpoints()
    data_results = test_data_endpoints()
    investment_results = test_investment_endpoints()
    
    # Test POST functionality
    test_post_endpoints()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    all_results = {**template_results, **data_results, **investment_results}
    
    success_count = sum(1 for r in all_results.values() if r["status"] == "OK")
    total_count = len(all_results)
    
    print(f"Total Endpoints Tested: {total_count}")
    print(f"Successful: {success_count}")
    print(f"Failed: {total_count - success_count}")
    
    if success_count == total_count:
        print("\nSTATUS: ALL TESTS PASSED!")
        return True
    else:
        print(f"\nSTATUS: {total_count - success_count} TESTS FAILED!")
        
        # Show failed endpoints
        print("\nFailed Endpoints:")
        for endpoint, result in all_results.items():
            if result["status"] != "OK":
                print(f"   {endpoint}: {result}")
        
        return False

def diagnose_template_issues():
    """Specific diagnosis for template loading issues."""
    print("\n" + "=" * 60)
    print("TEMPLATE LOADING DIAGNOSIS")
    print("=" * 60)
    
    # Check each template category endpoint
    categories = ["expense", "asset", "liability", "income"]
    
    for category in categories:
        print(f"\nTesting {category.title()} Templates:")
        
        # Test main template endpoint
        try:
            response = requests.get(f"{API_BASE}/api/templates/{category}", timeout=TIMEOUT)
            if response.status_code == 200:
                templates = response.json()
                print(f"   Templates: {len(templates)} found")
                if templates:
                    print(f"   Sample: {templates[0]}")
            else:
                print(f"   Templates: ERROR (Status {response.status_code})")
        except Exception as e:
            print(f"   Templates: ERROR ({e})")
        
        # Test categories endpoint
        try:
            response = requests.get(f"{API_BASE}/api/templates/{category}/categories", timeout=TIMEOUT)
            if response.status_code == 200:
                categories_data = response.json()
                print(f"   Categories: {len(categories_data)} found")
                if categories_data:
                    cats = [c.get('category', 'Unknown') for c in categories_data]
                    print(f"   List: {', '.join(cats[:5])}")
            else:
                print(f"   Categories: ERROR (Status {response.status_code})")
        except Exception as e:
            print(f"   Categories: ERROR ({e})")

if __name__ == "__main__":
    print("Starting comprehensive API tests...")
    print("Make sure the backend server is running first!")
    print("Run: python simple_backend.py")
    print()
    
    # Wait a moment for user to start server if needed
    time.sleep(2)
    
    # Run tests
    success = run_comprehensive_test()
    
    # Run specific template diagnosis
    diagnose_template_issues()
    
    print("\n" + "=" * 60)
    if success:
        print("RESULT: All APIs are working correctly!")
    else:
        print("RESULT: Some APIs have issues that need fixing.")
    print("=" * 60)
    
    sys.exit(0 if success else 1)
