#!/usr/bin/env python3
"""
Complete Test Runner for Personal Finance Tracker
Tests both backend and frontend components
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def run_script(script_name, description):
    """Run a test script and return success status"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=False, 
                              text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running {script_name}: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is too old")
        print("Please upgrade to Python 3.8 or higher")
        return False

def install_backend_deps():
    """Install backend dependencies"""
    print("\n📦 Installing backend dependencies...")
    backend_dir = Path(__file__).parent / 'backend'
    
    try:
        os.chdir(backend_dir)
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Backend dependencies installed successfully")
            return True
        else:
            print(f"❌ Failed to install backend dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing backend dependencies: {e}")
        return False

def main():
    """Main test runner"""
    print("🚀 Personal Finance Tracker - Complete Test Suite")
    print("=" * 70)
    print("This will test both backend and frontend components")
    print("=" * 70)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install backend dependencies first
    if not install_backend_deps():
        print("⚠️  Backend dependency installation failed, but continuing with tests...")
    
    # Change back to project root
    os.chdir(Path(__file__).parent)
    
    # Run tests
    tests = [
        ("test_frontend.py", "Frontend Component Tests"),
        ("test_backend.py", "Backend API Tests"),
    ]
    
    results = {}
    
    for script, description in tests:
        if Path(script).exists():
            success = run_script(script, description)
            results[description] = success
        else:
            print(f"⚠️  Test script {script} not found, skipping...")
            results[description] = False
    
    # Summary
    print(f"\n{'='*70}")
    print("📊 TEST SUMMARY")
    print(f"{'='*70}")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:<40} {status}")
    
    print(f"\n📈 Overall Result: {passed_tests}/{total_tests} test suites passed")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED!")
        print("Your Personal Finance Tracker is ready to use!")
        print("\n🚀 Quick Start:")
        print("1. Run: python start_dev.py")
        print("2. Open: http://localhost:3000")
        print("3. Create an account and start tracking your finances!")
        
    elif passed_tests > 0:
        print("\n⚠️  PARTIAL SUCCESS")
        print("Some components are working. Check the failed tests above.")
        print("\n📋 Next Steps:")
        if not results.get("Frontend Component Tests", False):
            print("- Fix frontend issues (check Node.js installation)")
        if not results.get("Backend API Tests", False):
            print("- Fix backend issues (check Python dependencies)")
        
    else:
        print("\n❌ ALL TESTS FAILED")
        print("Please check the setup guide and fix the issues above.")
        print("\n📖 Help:")
        print("- Read SETUP_GUIDE.md for detailed instructions")
        print("- Check that Python 3.8+ and Node.js are installed")
        print("- Ensure all dependencies are installed correctly")
    
    print(f"\n{'='*70}")

if __name__ == "__main__":
    main()
