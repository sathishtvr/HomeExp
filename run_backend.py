#!/usr/bin/env python3
"""
Script to run the Flask backend server
"""

import os
import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_dir))

# Change to backend directory
os.chdir(backend_dir)

# Import and run the Flask app
from app import app, db

if __name__ == '__main__':
    print("🚀 Starting Personal Finance Tracker Backend...")
    print("📍 Backend URL: http://localhost:5000")
    print("📊 API Documentation: http://localhost:5000/api")
    print("🔧 Environment: Development")
    print("-" * 50)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        print("✅ Database tables created/verified")
    
    # Run the Flask development server
    app.run(debug=True, host='0.0.0.0', port=5000)
