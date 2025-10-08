#!/usr/bin/env python3
"""
Start the Complete Personal Finance Tracker with Admin Panel
This launches the backend and opens both user and admin interfaces
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def main():
    print("🚀 Personal Finance Tracker - Complete Version with Admin Panel")
    print("=" * 70)
    print("📍 Backend:      http://localhost:5000")
    print("📍 User App:     simple_frontend.html")
    print("📍 Admin Panel:  admin_frontend.html")
    print("=" * 70)
    
    # Start the backend server
    print("🐍 Starting enhanced backend server...")
    backend_process = subprocess.Popen([
        sys.executable, 'simple_backend.py'
    ], cwd=Path(__file__).parent)
    
    # Wait for backend to start
    print("⏳ Waiting for backend to initialize...")
    time.sleep(3)
    
    # Open both interfaces
    user_frontend = Path(__file__).parent / 'simple_frontend.html'
    admin_frontend = Path(__file__).parent / 'admin_frontend.html'
    
    print(f"🌐 Opening User Interface: {user_frontend}")
    print(f"🛠️  Opening Admin Panel: {admin_frontend}")
    
    try:
        # Open user interface
        webbrowser.open(f'file://{user_frontend.absolute()}')
        time.sleep(1)
        
        # Open admin panel in new tab
        webbrowser.open(f'file://{admin_frontend.absolute()}')
        
        print("✅ Both interfaces opened in your browser")
    except Exception as e:
        print(f"⚠️  Could not auto-open browser: {e}")
        print(f"Please manually open:")
        print(f"  User App: {user_frontend.absolute()}")
        print(f"  Admin Panel: {admin_frontend.absolute()}")
    
    print("\n🎉 Complete Application is now running!")
    print("📋 What you can do:")
    print("👤 User Interface:")
    print("  - Add and track expenses, assets, liabilities")
    print("  - View financial dashboard and net worth")
    print("  - Create and manage financial data")
    print()
    print("🛠️  Admin Panel:")
    print("  - View all users and their data")
    print("  - Manage expenses, assets, liabilities")
    print("  - Generate comprehensive reports")
    print("  - Delete and moderate content")
    print("  - View system statistics")
    print()
    print("3. Press Ctrl+C here to stop the backend server")
    print("-" * 70)
    
    try:
        # Keep the script running
        backend_process.wait()
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
        backend_process.terminate()
        backend_process.wait()
        print("✅ Backend server stopped")

if __name__ == '__main__':
    main()
