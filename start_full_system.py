#!/usr/bin/env python3
"""
Start the Complete Personal Finance System
- User Dashboard (View Only) with Rich Charts
- Admin Panel with Login, Edit, Delete functionality
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def main():
    print("🚀 Personal Finance Tracker - Complete System")
    print("=" * 70)
    print("📍 Backend:        http://localhost:5000")
    print("📊 User Dashboard: user_view.html (Rich charts & reports)")
    print("🛠️  Admin Panel:    admin_frontend.html (Login: admin/admin123)")
    print("=" * 70)
    
    # Start the backend server
    print("🐍 Starting enhanced backend server...")
    backend_process = subprocess.Popen([
        sys.executable, 'simple_backend.py'
    ], cwd=Path(__file__).parent)
    
    # Wait for backend to start
    print("⏳ Waiting for backend to initialize...")
    time.sleep(4)
    
    # Open both interfaces
    user_dashboard = Path(__file__).parent / 'user_view.html'
    admin_panel = Path(__file__).parent / 'admin_frontend.html'
    
    print(f"📊 Opening User Dashboard: {user_dashboard}")
    print(f"🛠️  Opening Admin Panel: {admin_panel}")
    
    try:
        # Open user dashboard (view-only with rich charts)
        webbrowser.open(f'file://{user_dashboard.absolute()}')
        time.sleep(1)
        
        # Open admin panel (login required)
        webbrowser.open(f'file://{admin_panel.absolute()}')
        
        print("✅ Both interfaces opened in your browser")
    except Exception as e:
        print(f"⚠️  Could not auto-open browser: {e}")
        print(f"Please manually open:")
        print(f"  📊 User Dashboard: {user_dashboard.absolute()}")
        print(f"  🛠️  Admin Panel: {admin_panel.absolute()}")
    
    print("\n🎉 Complete Finance System is now running!")
    print("📋 What you can do:")
    print()
    print("📊 User Dashboard (View-Only):")
    print("  ✅ Rich interactive charts (Chart.js)")
    print("  ✅ Net worth trends and asset distribution")
    print("  ✅ Monthly comparisons and expense categories")
    print("  ✅ Professional data tables")
    print("  ✅ Real-time financial analytics")
    print()
    print("🛠️  Admin Panel (Full Management):")
    print("  🔐 Secure login (admin/admin123)")
    print("  ✏️  Edit expenses, assets, liabilities")
    print("  🗑️  Delete any data entries")
    print("  👥 User management")
    print("  📈 System reports and analytics")
    print("  📊 Complete data oversight")
    print()
    print("🔧 Backend Features:")
    print("  ✅ RESTful API with all CRUD operations")
    print("  ✅ Admin authentication system")
    print("  ✅ Edit endpoints for all data types")
    print("  ✅ Advanced reporting and analytics")
    print()
    print("Press Ctrl+C here to stop the backend server")
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
