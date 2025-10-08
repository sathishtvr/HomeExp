#!/usr/bin/env python3
"""
Simple startup script for Personal Finance Tracker
This script starts only the backend server for testing
"""

import os
import sys
from pathlib import Path

def start_backend():
    """Start the Flask backend server"""
    print("🚀 Starting Personal Finance Tracker Backend")
    print("=" * 50)
    
    # Change to backend directory
    backend_dir = Path(__file__).parent / 'backend'
    os.chdir(backend_dir)
    
    # Add backend to Python path
    sys.path.insert(0, str(backend_dir))
    
    try:
        # Import and run the Flask app
        from app import app, db
        
        print("📍 Backend URL: http://localhost:5000")
        print("🔧 Environment: Development")
        print("💾 Database: SQLite (auto-created)")
        print("-" * 50)
        
        # Create database tables
        with app.app_context():
            db.create_all()
            print("✅ Database tables created/verified")
        
        print("🚀 Starting Flask server...")
        print("Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Run the Flask development server
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install backend dependencies:")
        print("cd backend && pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")

if __name__ == '__main__':
    start_backend()
