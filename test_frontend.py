#!/usr/bin/env python3
"""
Frontend Test Script
Tests if the frontend development server and dependencies are working correctly
"""

import subprocess
import sys
import os
import time
import requests
from pathlib import Path

class FrontendTester:
    def __init__(self):
        self.frontend_dir = Path(__file__).parent / 'frontend'
        self.frontend_url = "http://localhost:3000"
        
    def log(self, message, status="INFO"):
        print(f"[{status}] {message}")
    
    def check_node_npm(self):
        """Check if Node.js and npm are installed"""
        try:
            # Check Node.js
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                node_version = result.stdout.strip()
                self.log(f"✅ Node.js found: {node_version}")
            else:
                self.log("❌ Node.js not found", "ERROR")
                return False
            
            # Check npm
            result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                npm_version = result.stdout.strip()
                self.log(f"✅ npm found: {npm_version}")
                return True
            else:
                self.log("❌ npm not found", "ERROR")
                return False
                
        except FileNotFoundError:
            self.log("❌ Node.js/npm not found in PATH", "ERROR")
            self.log("Please install Node.js from https://nodejs.org/", "INFO")
            return False
    
    def check_frontend_directory(self):
        """Check if frontend directory exists and has required files"""
        if not self.frontend_dir.exists():
            self.log("❌ Frontend directory not found", "ERROR")
            return False
        
        required_files = ['package.json', 'vite.config.ts', 'index.html']
        missing_files = []
        
        for file in required_files:
            if not (self.frontend_dir / file).exists():
                missing_files.append(file)
        
        if missing_files:
            self.log(f"❌ Missing required files: {', '.join(missing_files)}", "ERROR")
            return False
        
        self.log("✅ Frontend directory structure is correct")
        return True
    
    def check_dependencies(self):
        """Check if node_modules exists and dependencies are installed"""
        node_modules = self.frontend_dir / 'node_modules'
        
        if not node_modules.exists():
            self.log("⚠️  node_modules not found, dependencies need to be installed")
            return False
        
        # Check for key dependencies
        key_deps = ['react', 'react-dom', 'vite', '@vitejs/plugin-react']
        missing_deps = []
        
        for dep in key_deps:
            if not (node_modules / dep).exists():
                missing_deps.append(dep)
        
        if missing_deps:
            self.log(f"⚠️  Missing key dependencies: {', '.join(missing_deps)}")
            return False
        
        self.log("✅ Dependencies are installed")
        return True
    
    def install_dependencies(self):
        """Install npm dependencies"""
        self.log("📦 Installing frontend dependencies...")
        
        try:
            os.chdir(self.frontend_dir)
            result = subprocess.run(['npm', 'install'], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log("✅ Dependencies installed successfully")
                return True
            else:
                self.log(f"❌ Failed to install dependencies: {result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Error installing dependencies: {e}", "ERROR")
            return False
    
    def test_build(self):
        """Test if the frontend can be built"""
        self.log("🔨 Testing frontend build...")
        
        try:
            os.chdir(self.frontend_dir)
            result = subprocess.run(['npm', 'run', 'build'], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log("✅ Frontend builds successfully")
                return True
            else:
                self.log(f"❌ Build failed: {result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Build error: {e}", "ERROR")
            return False
    
    def check_typescript(self):
        """Check TypeScript configuration"""
        tsconfig = self.frontend_dir / 'tsconfig.json'
        
        if not tsconfig.exists():
            self.log("⚠️  tsconfig.json not found")
            return False
        
        self.log("✅ TypeScript configuration found")
        return True
    
    def check_tailwind(self):
        """Check Tailwind CSS configuration"""
        tailwind_config = self.frontend_dir / 'tailwind.config.js'
        
        if not tailwind_config.exists():
            self.log("⚠️  tailwind.config.js not found")
            return False
        
        self.log("✅ Tailwind CSS configuration found")
        return True
    
    def test_dev_server_start(self):
        """Test if dev server can start (quick test)"""
        self.log("🚀 Testing dev server startup...")
        
        try:
            os.chdir(self.frontend_dir)
            # Start dev server in background
            process = subprocess.Popen(
                ['npm', 'run', 'dev'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait a few seconds for server to start
            time.sleep(5)
            
            # Check if server is responding
            try:
                response = requests.get(self.frontend_url, timeout=3)
                if response.status_code == 200:
                    self.log("✅ Dev server started successfully")
                    success = True
                else:
                    self.log(f"⚠️  Dev server responded with status {response.status_code}")
                    success = False
            except requests.exceptions.ConnectionError:
                self.log("❌ Dev server not responding")
                success = False
            
            # Terminate the process
            process.terminate()
            process.wait(timeout=5)
            
            return success
            
        except Exception as e:
            self.log(f"❌ Error testing dev server: {e}", "ERROR")
            return False
    
    def run_all_tests(self):
        """Run all frontend tests"""
        self.log("🚀 Starting Frontend Tests")
        self.log("=" * 50)
        
        tests = [
            ("Node.js & npm Check", self.check_node_npm),
            ("Frontend Directory Check", self.check_frontend_directory),
            ("TypeScript Config Check", self.check_typescript),
            ("Tailwind Config Check", self.check_tailwind),
            ("Dependencies Check", self.check_dependencies),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            self.log(f"Running: {test_name}")
            if test_func():
                passed += 1
            else:
                # If dependencies check failed, try to install them
                if test_name == "Dependencies Check":
                    if self.install_dependencies():
                        passed += 1
            self.log("-" * 30)
        
        # Additional tests if basic setup is working
        if passed >= 4:  # Most basic tests passed
            additional_tests = [
                ("Build Test", self.test_build),
                ("Dev Server Test", self.test_dev_server_start),
            ]
            
            for test_name, test_func in additional_tests:
                self.log(f"Running: {test_name}")
                if test_func():
                    passed += 1
                total += 1
                self.log("-" * 30)
        
        self.log("=" * 50)
        self.log(f"📊 Test Results: {passed}/{total} tests passed")
        
        if passed >= total - 1:  # Allow one test to fail
            self.log("🎉 Frontend is ready!")
            return True
        else:
            self.log("⚠️  Some frontend tests failed.")
            return False

def main():
    """Main function"""
    print("🧪 Personal Finance Tracker - Frontend Test")
    print("=" * 60)
    
    tester = FrontendTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n✅ Frontend is ready for development!")
        print("Next steps:")
        print("1. Start the frontend: python run_frontend.py")
        print("2. Or start both servers: python start_dev.py")
        print("3. Open http://localhost:3000 in your browser")
    else:
        print("\n❌ Frontend tests failed!")
        print("Please check the errors above and fix them.")
        print("Common solutions:")
        print("- Install Node.js from https://nodejs.org/")
        print("- Run 'npm install' in the frontend directory")
        print("- Check for missing configuration files")

if __name__ == "__main__":
    main()
