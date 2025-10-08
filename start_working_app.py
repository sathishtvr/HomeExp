#!/usr/bin/env python3
"""
Start the working Personal Finance Tracker
This launches the simple backend and opens the frontend in your browser
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def main():
    print("🚀 Personal Finance Tracker - Working Version")
    print("=" * 60)
    print("📍 Backend:  http://localhost:5000")
    print("📍 Frontend: simple_frontend.html (opens in browser)")
    print("=" * 60)
    
    # Start the backend server
    print("🐍 Starting backend server...")
    backend_process = subprocess.Popen([
        sys.executable, 'simple_backend.py'
    ], cwd=Path(__file__).parent)
    
    # Wait for backend to start
    print("⏳ Waiting for backend to initialize...")
    time.sleep(3)
    
    # Open the frontend in browser
    frontend_path = Path(__file__).parent / 'simple_frontend.html'
    print(f"🌐 Opening frontend: {frontend_path}")
    
    try:
        webbrowser.open(f'file://{frontend_path.absolute()}')
        print("✅ Frontend opened in your default browser")
    except Exception as e:
        print(f"⚠️  Could not auto-open browser: {e}")
        print(f"Please manually open: {frontend_path.absolute()}")
    
    print("\n🎉 Application is now running!")
    print("📋 Instructions:")
    print("1. Use the web interface to add expenses, assets, and liabilities")
    print("2. View your financial dashboard with net worth calculations")
    print("3. Press Ctrl+C here to stop the backend server")
    print("-" * 60)
    
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
