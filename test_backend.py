#!/usr/bin/env python3
"""
Backend API Test Script
Tests all major API endpoints to ensure they work correctly
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
TEST_USER = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
}

class APITester:
    def __init__(self):
        self.base_url = BASE_URL
        self.token = None
        self.user_id = None
        
    def log(self, message, status="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {status}: {message}")
    
    def test_connection(self):
        """Test if backend server is running"""
        try:
            response = requests.get(f"{self.base_url}/api/auth/login", timeout=5)
            self.log("✅ Backend server is running")
            return True
        except requests.exceptions.ConnectionError:
            self.log("❌ Backend server is not running", "ERROR")
            self.log("Please start the backend server first: python run_backend.py", "INFO")
            return False
        except Exception as e:
            self.log(f"❌ Connection error: {e}", "ERROR")
            return False
    
    def test_user_registration(self):
        """Test user registration"""
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/register",
                json=TEST_USER,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 201:
                data = response.json()
                self.token = data.get("access_token")
                self.user_id = data.get("user", {}).get("id")
                self.log("✅ User registration successful")
                return True
            elif response.status_code == 400:
                # User might already exist, try login
                self.log("⚠️  User already exists, trying login...")
                return self.test_user_login()
            else:
                self.log(f"❌ Registration failed: {response.text}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Registration error: {e}", "ERROR")
            return False
    
    def test_user_login(self):
        """Test user login"""
        try:
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                json={
                    "username": TEST_USER["username"],
                    "password": TEST_USER["password"]
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                self.user_id = data.get("user", {}).get("id")
                self.log("✅ User login successful")
                return True
            else:
                self.log(f"❌ Login failed: {response.text}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Login error: {e}", "ERROR")
            return False
    
    def get_headers(self):
        """Get headers with authentication token"""
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
    
    def test_expense_operations(self):
        """Test expense CRUD operations"""
        if not self.token:
            self.log("❌ No authentication token available", "ERROR")
            return False
        
        try:
            # Create expense
            expense_data = {
                "category": "Food",
                "description": "Test lunch",
                "amount": 25.50,
                "date": "2024-01-15"
            }
            
            response = requests.post(
                f"{self.base_url}/api/expenses",
                json=expense_data,
                headers=self.get_headers()
            )
            
            if response.status_code == 201:
                expense = response.json()
                expense_id = expense.get("id")
                self.log("✅ Expense creation successful")
                
                # Test getting expenses by month
                response = requests.get(
                    f"{self.base_url}/api/expenses/month/2024-01",
                    headers=self.get_headers()
                )
                
                if response.status_code == 200:
                    expenses = response.json()
                    self.log(f"✅ Retrieved {len(expenses)} expenses for January 2024")
                else:
                    self.log("❌ Failed to retrieve expenses", "ERROR")
                
                # Test expense deletion
                if expense_id:
                    response = requests.delete(
                        f"{self.base_url}/api/expenses/{expense_id}",
                        headers=self.get_headers()
                    )
                    
                    if response.status_code == 200:
                        self.log("✅ Expense deletion successful")
                    else:
                        self.log("❌ Failed to delete expense", "ERROR")
                
                return True
            else:
                self.log(f"❌ Expense creation failed: {response.text}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Expense operations error: {e}", "ERROR")
            return False
    
    def test_asset_operations(self):
        """Test asset CRUD operations"""
        if not self.token:
            return False
        
        try:
            asset_data = {
                "name": "Test Savings",
                "category": "Cash",
                "value": 5000.00,
                "month": "2024-01"
            }
            
            response = requests.post(
                f"{self.base_url}/api/assets",
                json=asset_data,
                headers=self.get_headers()
            )
            
            if response.status_code == 201:
                asset = response.json()
                asset_id = asset.get("id")
                self.log("✅ Asset creation successful")
                
                # Clean up
                if asset_id:
                    requests.delete(
                        f"{self.base_url}/api/assets/{asset_id}",
                        headers=self.get_headers()
                    )
                
                return True
            else:
                self.log(f"❌ Asset creation failed: {response.text}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Asset operations error: {e}", "ERROR")
            return False
    
    def test_liability_operations(self):
        """Test liability CRUD operations"""
        if not self.token:
            return False
        
        try:
            liability_data = {
                "name": "Test Credit Card",
                "category": "Credit Cards",
                "amount": 1500.00,
                "month": "2024-01"
            }
            
            response = requests.post(
                f"{self.base_url}/api/liabilities",
                json=liability_data,
                headers=self.get_headers()
            )
            
            if response.status_code == 201:
                liability = response.json()
                liability_id = liability.get("id")
                self.log("✅ Liability creation successful")
                
                # Clean up
                if liability_id:
                    requests.delete(
                        f"{self.base_url}/api/liabilities/{liability_id}",
                        headers=self.get_headers()
                    )
                
                return True
            else:
                self.log(f"❌ Liability creation failed: {response.text}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Liability operations error: {e}", "ERROR")
            return False
    
    def test_analytics_endpoints(self):
        """Test analytics and reporting endpoints"""
        if not self.token:
            return False
        
        try:
            # Test available months
            response = requests.get(
                f"{self.base_url}/api/available-months",
                headers=self.get_headers()
            )
            
            if response.status_code == 200:
                months = response.json()
                self.log(f"✅ Available months: {len(months)} months found")
            else:
                self.log("❌ Failed to get available months", "ERROR")
            
            # Test monthly comparison
            response = requests.get(
                f"{self.base_url}/api/monthly-comparison",
                headers=self.get_headers()
            )
            
            if response.status_code == 200:
                comparison = response.json()
                self.log(f"✅ Monthly comparison: {len(comparison)} months data")
                return True
            else:
                self.log("❌ Failed to get monthly comparison", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Analytics endpoints error: {e}", "ERROR")
            return False
    
    def run_all_tests(self):
        """Run all API tests"""
        self.log("🚀 Starting Backend API Tests")
        self.log("=" * 50)
        
        tests = [
            ("Connection Test", self.test_connection),
            ("User Registration", self.test_user_registration),
            ("Expense Operations", self.test_expense_operations),
            ("Asset Operations", self.test_asset_operations),
            ("Liability Operations", self.test_liability_operations),
            ("Analytics Endpoints", self.test_analytics_endpoints),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            self.log(f"Running: {test_name}")
            if test_func():
                passed += 1
            self.log("-" * 30)
        
        self.log("=" * 50)
        self.log(f"📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            self.log("🎉 All tests passed! Backend API is working correctly.")
            return True
        else:
            self.log("⚠️  Some tests failed. Please check the errors above.")
            return False

def main():
    """Main function"""
    print("🧪 Personal Finance Tracker - Backend API Test")
    print("=" * 60)
    
    tester = APITester()
    success = tester.run_all_tests()
    
    if success:
        print("\n✅ Backend is ready for use!")
        print("Next steps:")
        print("1. Start the frontend: python run_frontend.py")
        print("2. Open http://localhost:3000 in your browser")
        print("3. Create an account and start using the app")
    else:
        print("\n❌ Backend tests failed!")
        print("Please check the backend server and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
