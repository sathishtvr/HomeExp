#!/usr/bin/env python3
"""
Script to start both backend and frontend development servers
"""

import os
import subprocess
import sys
import time
import threading
from pathlib import Path

def check_dependencies():
    """Check if all dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python dependencies
    backend_dir = Path(__file__).parent / 'backend'
    requirements_file = backend_dir / 'requirements.txt'
    
    if requirements_file.exists():
        try:
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)
            ], capture_output=True, text=True, cwd=backend_dir)
            
            if result.returncode == 0:
                print("✅ Backend dependencies ready")
            else:
                print("⚠️  Installing backend dependencies...")
                
        except Exception as e:
            print(f"⚠️  Backend dependency check failed: {e}")
    
    # Check Node.js dependencies
    frontend_dir = Path(__file__).parent / 'frontend'
    if not (frontend_dir / 'node_modules').exists():
        print("📦 Installing frontend dependencies...")
        try:
            os.chdir(frontend_dir)
            subprocess.run(['npm', 'install'], check=True)
            print("✅ Frontend dependencies installed")
        except Exception as e:
            print(f"❌ Failed to install frontend dependencies: {e}")
            return False
    else:
        print("✅ Frontend dependencies ready")
    
    return True

def run_backend():
    """Run the Flask backend server"""
    backend_dir = Path(__file__).parent / 'backend'
    
    print("🐍 Starting Flask Backend...")
    print("📍 Backend URL: http://localhost:5000")
    
    try:
        os.chdir(backend_dir)
        # Add backend to Python path
        sys.path.insert(0, str(backend_dir))
        
        from app import app, db
        
        # Create database tables
        with app.app_context():
            db.create_all()
            print("✅ Database tables created/verified")
        
        print("🚀 Backend server starting...")
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
        
    except ImportError as e:
        print(f"❌ Backend import error: {e}")
        print("Please check that all backend dependencies are installed")
    except Exception as e:
        print(f"❌ Backend error: {e}")

def run_frontend():
    """Run the React frontend server"""
    frontend_dir = Path(__file__).parent / 'frontend'
    
    print("⚛️  Starting React Frontend...")
    print("📍 Frontend URL: http://localhost:3000")
    
    try:
        os.chdir(frontend_dir)
        
        # Check if package.json exists
        if not (frontend_dir / 'package.json').exists():
            print("❌ package.json not found in frontend directory")
            return
        
        print("🚀 Frontend server starting...")
        subprocess.run(['npm', 'run', 'dev'], check=True)
        
    except FileNotFoundError:
        print("❌ npm not found. Please install Node.js and npm")
        print("Download from: https://nodejs.org/")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start frontend server: {e}")
    except KeyboardInterrupt:
        print("\n👋 Frontend server stopped")

def main():
    """Start both servers concurrently"""
    print("🚀 Personal Finance Tracker - Development Environment")
    print("=" * 70)
    print("📍 Backend:  http://localhost:5000")
    print("📍 Frontend: http://localhost:3000")
    print("=" * 70)
    print("Press Ctrl+C to stop both servers")
    print()
    
    # Check and install dependencies
    if not check_dependencies():
        print("❌ Dependency check failed. Please fix the issues above.")
        return
    
    print("\n🔄 Starting servers...")
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Give backend time to start
    print("⏳ Waiting for backend to start...")
    time.sleep(5)
    
    try:
        # Start frontend in main thread
        run_frontend()
    except KeyboardInterrupt:
        print("\n👋 Shutting down development servers...")
        print("Thank you for using Personal Finance Tracker!")
        sys.exit(0)

if __name__ == '__main__':
    main()
