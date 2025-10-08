#!/usr/bin/env python3
"""
🚀 Professional Personal Finance Application
Complete system with intelligent features, current date handling, and loan calculator
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def main():
    print("🎉 PROFESSIONAL PERSONAL FINANCE APPLICATION")
    print("=" * 80)
    print("🧠 INTELLIGENT FEATURES:")
    print("  ✅ Auto current date handling")
    print("  ✅ Smart loan calculator with closure tips")
    print("  ✅ Financial health scoring")
    print("  ✅ Rich interactive charts")
    print("  ✅ Professional UI/UX")
    print("=" * 80)
    print("📍 Backend:        http://localhost:5000")
    print("📊 User Dashboard: user_view.html (Rich analytics)")
    print("🛠️  Admin Panel:    admin_frontend.html (Full management)")
    print("📱 Simple App:     simple_frontend.html (Quick entry)")
    print("=" * 80)
    
    # Start the enhanced backend server
    print("🐍 Starting professional backend with AI features...")
    backend_process = subprocess.Popen([
        sys.executable, 'simple_backend.py'
    ], cwd=Path(__file__).parent)
    
    # Wait for backend to start
    print("⏳ Initializing intelligent systems...")
    time.sleep(4)
    
    # Define interface files
    professional_app = Path(__file__).parent / 'professional_finance_app.html'
    user_dashboard = Path(__file__).parent / 'user_view.html'
    admin_panel = Path(__file__).parent / 'admin_frontend.html'
    
    print(f"🚀 Opening Professional Finance Application...")
    
    try:
        # Open professional app first (main interface)
        webbrowser.open(f'file://{professional_app.absolute()}')
        time.sleep(1)
        
        print("✅ Professional Finance App opened successfully!")
    except Exception as e:
        print(f"⚠️  Could not auto-open browser: {e}")
        print(f"Please manually open these files:")
        print(f"  📊 Main Dashboard: {user_dashboard.absolute()}")
        print(f"  🛠️  Admin Panel: {admin_panel.absolute()}")
        print(f"  📱 Quick Entry: {simple_app.absolute()}")
    
    print("\n🎊 PROFESSIONAL FINANCE APPLICATION IS LIVE!")
    print("=" * 80)
    print("🎯 WHAT YOU CAN DO:")
    print()
    print("📊 USER DASHBOARD (Main Interface):")
    print("  🎨 Rich interactive charts with Chart.js")
    print("  📈 Net worth trends and financial analytics")
    print("  🏦 Smart loan calculator with closure tips")
    print("  📅 Auto current date handling")
    print("  💡 Intelligent financial recommendations")
    print("  📱 Responsive design for all devices")
    print()
    print("🛠️  ADMIN PANEL (Management Interface):")
    print("  🔐 Secure login system (admin/admin123)")
    print("  ✏️  Edit all financial data with modal forms")
    print("  🗑️  Delete operations with confirmation")
    print("  👥 Complete user management")
    print("  📊 System-wide analytics and reports")
    print("  🎯 Data oversight and moderation")
    print()
    print("📱 SIMPLE APP (Quick Entry Interface):")
    print("  ⚡ Fast data entry with auto-dates")
    print("  📋 Professional tables for viewing")
    print("  💰 Real-time net worth calculations")
    print("  📊 Monthly financial summaries")
    print()
    print("🧠 INTELLIGENT BACKEND FEATURES:")
    print("  🏦 Advanced loan calculator with smart tips")
    print("  📊 Financial health scoring algorithm")
    print("  💡 Personalized recommendations")
    print("  📅 Automatic date handling")
    print("  🔧 RESTful API with full CRUD operations")
    print("  🛡️  Admin authentication system")
    print()
    print("💡 SMART LOAN TIPS INCLUDE:")
    print("  📈 Extra payment impact calculations")
    print("  📅 Bi-weekly payment strategies")
    print("  🏦 Refinancing recommendations")
    print("  💰 Lump sum payment benefits")
    print("  ⏰ Time and interest savings projections")
    print()
    print("🎨 PROFESSIONAL UI FEATURES:")
    print("  🌈 Modern gradients and animations")
    print("  📱 Fully responsive design")
    print("  🎯 Intuitive user experience")
    print("  📊 Interactive data visualizations")
    print("  🎪 Professional color schemes")
    print("=" * 80)
    print("Press Ctrl+C here to stop the backend server")
    print("🎉 Enjoy your professional finance management system!")
    print("-" * 80)
    
    try:
        # Keep the script running
        backend_process.wait()
    except KeyboardInterrupt:
        print("\n👋 Shutting down professional finance system...")
        backend_process.terminate()
        backend_process.wait()
        print("✅ All systems stopped gracefully")
        print("💫 Thank you for using the Professional Finance App!")

if __name__ == '__main__':
    main()
