#!/usr/bin/env python3
"""
Professional Finance Manager - Deployment Script
Creates a clean deployment package with only essential files.
"""

import os
import shutil
import sys
from pathlib import Path

def create_deployment():
    """Create deployment package with essential files only."""
    
    print("Creating Professional Finance Manager Deployment Package...")
    print("=" * 60)
    
    # Get current directory
    source_dir = Path(__file__).parent
    deploy_dir = source_dir / "finance-manager-deploy"
    
    # Remove existing deployment directory
    if deploy_dir.exists():
        print(f"Removing existing deployment directory...")
        shutil.rmtree(deploy_dir)
    
    # Create deployment directory
    deploy_dir.mkdir()
    print(f"Created deployment directory: {deploy_dir}")
    
    # Essential files to copy
    essential_files = [
        "index.html",
        "styles.css", 
        "simple_backend.py",
        "start_modular_app.py"
    ]
    
    # Copy essential files
    print("\nCopying essential files...")
    for file in essential_files:
        source_file = source_dir / file
        if source_file.exists():
            shutil.copy2(source_file, deploy_dir)
            print(f"   OK {file} ({source_file.stat().st_size:,} bytes)")
        else:
            print(f"   ERROR {file} (not found)")
    
    # Copy JavaScript directory
    js_source = source_dir / "js"
    js_deploy = deploy_dir / "js"
    if js_source.exists():
        shutil.copytree(js_source, js_deploy)
        print(f"\nCopied JavaScript directory:")
        for js_file in js_deploy.glob("*.js"):
            print(f"   OK js/{js_file.name} ({js_file.stat().st_size:,} bytes)")
    
    # Create requirements.txt
    requirements_content = """flask==2.3.3
flask-cors==4.0.0
"""
    requirements_file = deploy_dir / "requirements.txt"
    requirements_file.write_text(requirements_content)
    print(f"\nCreated requirements.txt")
    
    # Create deployment README
    readme_content = """# Professional Finance Manager - Deployment Package

## Quick Start

### 1. Install Python Dependencies:
```bash
pip install -r requirements.txt
```

### 2. Run Application:
```bash
python start_modular_app.py
```

### 3. Access Application:
- Backend: http://localhost:5000
- Frontend: Opens automatically in browser

## Features Included:
- Dashboard with Charts & Analytics
- Income & Expense Tracking  
- Asset & Liability Management
- Investment Tracking (RD, Chit Funds, Gold Chit)
- Template-based Categories
- Professional Reports
- AI Insights
- Loan Calculator
- Professional Table Interface
- Real-time Search & Filtering

## System Requirements:
- Python 3.7 or higher
- Modern web browser
- 50MB free disk space

## Package Contents:
- index.html (Main application interface)
- styles.css (Professional styling)
- simple_backend.py (Complete backend server)
- start_modular_app.py (Application launcher)
- js/ (JavaScript functionality)
  - app.js (Core features)
  - templates.js (Template management)
  - investments.js (Investment tracking)

## Troubleshooting:
1. Ensure Python 3.7+ is installed
2. Install dependencies: pip install flask flask-cors
3. Run: python start_modular_app.py
4. If port 5000 is busy, the app will find another port

## Support:
This is a complete, standalone finance management application.
All data is stored locally in SQLite database.
"""
    
    readme_file = deploy_dir / "README.md"
    readme_file.write_text(readme_content)
    print(f"Created deployment README.md")
    
    # Create run script for easy execution
    if sys.platform.startswith('win'):
        # Windows batch file
        run_script = deploy_dir / "run.bat"
        run_script.write_text("""@echo off
echo Starting Professional Finance Manager...
python start_modular_app.py
pause
""")
        print(f"Created run.bat (Windows launcher)")
    else:
        # Unix shell script
        run_script = deploy_dir / "run.sh"
        run_script.write_text("""#!/bin/bash
echo "Starting Professional Finance Manager..."
python3 start_modular_app.py
""")
        run_script.chmod(0o755)
        print(f"Created run.sh (Unix launcher)")
    
    # Calculate total size
    total_size = sum(f.stat().st_size for f in deploy_dir.rglob('*') if f.is_file())
    file_count = len(list(deploy_dir.rglob('*')))
    
    print("\n" + "=" * 60)
    print("DEPLOYMENT PACKAGE CREATED SUCCESSFULLY!")
    print("=" * 60)
    print(f"Location: {deploy_dir}")
    print(f"Total Size: {total_size:,} bytes ({total_size/1024:.1f} KB)")
    print(f"Files: {file_count} files")
    
    print(f"\nTo deploy:")
    print(f"1. Copy the entire '{deploy_dir.name}' folder to target location")
    print(f"2. Install dependencies: pip install -r requirements.txt")
    print(f"3. Run application: python start_modular_app.py")
    
    print(f"\nQuick test:")
    print(f"cd {deploy_dir.name}")
    print(f"python start_modular_app.py")
    
    return deploy_dir

if __name__ == "__main__":
    try:
        deployment_path = create_deployment()
        print(f"\nDeployment package ready at: {deployment_path}")
    except Exception as e:
        print(f"\nError creating deployment package: {e}")
        sys.exit(1)
