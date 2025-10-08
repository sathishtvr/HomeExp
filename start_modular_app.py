#!/usr/bin/env python3
"""
Professional Finance Manager - Modular Version Launcher
Starts the backend server and opens the modular frontend
"""

import subprocess
import webbrowser
import time
import os
import sys
from pathlib import Path

def main():
    print("Starting Professional Finance Manager (Modular Version)")
    print("=" * 60)
    
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check if required files exist
    required_files = [
        'simple_backend.py',
        'index.html',
        'styles.css',
        'js/app.js',
        'js/templates.js',
        'js/investments.js'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nPlease ensure all files are present before running.")
        input("Press Enter to exit...")
        return
    print("All required files found")
    
    try:
        # Start the Flask backend server
        print("Starting backend server...")
        backend_process = subprocess.Popen([
            sys.executable, 'simple_backend.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for the server to start
        print("Waiting for server to start...")
        time.sleep(3)
        
        # Check if the backend is running
        if backend_process.poll() is None:
            print("Backend server started successfully")
            
            # Open the frontend in the default web browser
            frontend_url = f"file://{script_dir.absolute()}/index.html"
            print(f"Opening frontend: {frontend_url}")
            webbrowser.open(frontend_url)
            
            print("\n" + "=" * 60)
            print("Professional Finance Manager is now running!")
            print("=" * 60)
            print("Frontend: Opened in your default browser")
            print("Backend: http://localhost:5000")
            print("Database: finance_app.db (auto-created)")
            print("\nFeatures Available:")
            print("   Dashboard with charts")
            print("   Template Management (4 types)")
            print("   Investment Tracking (RD/Chit/Gold)")
            print("   Modular Component Architecture")
            print("\nTo refresh data, click the refresh button in the app")
            print("To stop the server, press Ctrl+C in this window")
            print("=" * 60)
            
            try:
                # Keep the script running and monitor the backend
                while True:
                    if backend_process.poll() is not None:
                        print("Backend server stopped unexpectedly")
                        break
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nShutting down...")
                backend_process.terminate()
                backend_process.wait()
                print("Backend server stopped")
                
        else:
            # Backend failed to start
            stdout, stderr = backend_process.communicate()
            print("Failed to start backend server")
            print("Error output:")
            print(stderr.decode())
            
    except FileNotFoundError:
        print("Python not found. Please ensure Python is installed and in your PATH.")
    except Exception as e:
        print(f"Error starting application: {e}")
    
    print("\nThank you for using Professional Finance Manager!")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
