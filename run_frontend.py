#!/usr/bin/env python3
"""
Script to run the React frontend development server
"""

import os
import subprocess
import sys
from pathlib import Path

def run_frontend():
    """Run the React frontend development server"""
    frontend_dir = Path(__file__).parent / 'frontend'
    
    print("🚀 Starting Personal Finance Tracker Frontend...")
    print("📍 Frontend URL: http://localhost:3000")
    print("⚛️  Framework: React + TypeScript + Vite")
    print("🎨 Styling: Tailwind CSS")
    print("-" * 50)
    
    # Change to frontend directory
    os.chdir(frontend_dir)
    
    # Check if node_modules exists
    if not (frontend_dir / 'node_modules').exists():
        print("📦 Installing dependencies...")
        try:
            subprocess.run(['npm', 'install'], check=True)
            print("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            print("Please run 'npm install' in the frontend directory manually")
            return
        except FileNotFoundError:
            print("❌ npm not found. Please install Node.js and npm")
            return
    
    # Start the development server
    try:
        print("🔥 Starting Vite development server...")
        subprocess.run(['npm', 'run', 'dev'], check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to start development server")
    except FileNotFoundError:
        print("❌ npm not found. Please install Node.js and npm")
    except KeyboardInterrupt:
        print("\n👋 Frontend server stopped")

if __name__ == '__main__':
    run_frontend()
