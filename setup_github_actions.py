#!/usr/bin/env python3
"""
GitHub Repository Setup Script
Prepares the UEFA ETA system for GitHub Actions deployment
"""

import os
import subprocess
import json
from pathlib import Path

def run_command(command, description):
    """Run a shell command and return the result"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=os.getcwd())
        if result.returncode == 0:
            print(f"✅ {description} completed")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} error: {e}")
        return False

def check_git_status():
    """Check current git repository status"""
    print("📊 Checking Git Status")
    print("=" * 30)
    
    # Check if we're in a git repo
    if not os.path.exists('.git'):
        print("❌ Not a git repository")
        return False
    
    # Check status
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    if result.returncode == 0:
        changes = result.stdout.strip().split('\n') if result.stdout.strip() else []
        print(f"📁 Working directory: {os.getcwd()}")
        print(f"📝 Uncommitted changes: {len(changes)}")
        
        if changes:
            print("📄 Modified files:")
            for change in changes[:10]:  # Show first 10
                print(f"   {change}")
            if len(changes) > 10:
                print(f"   ... and {len(changes) - 10} more")
        
        return True
    return False

def prepare_for_github():
    """Prepare repository for GitHub Actions"""
    print("\n🚀 Preparing for GitHub Actions")
    print("=" * 35)
    
    # Check required files
    required_files = [
        'uefa_fixtures_data.json',
        'requirements.txt', 
        '.github/workflows/uefa-auto-processor.yml',
        '.github/workflows/mobile-results-processor.yml',
        'github_mobile_processor.py',
        'mobile/github_uefa_mobile.html'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ Missing: {file}")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️ Missing {len(missing_files)} required files for GitHub Actions")
        return False
    
    print(f"✅ All {len(required_files)} required files present")
    return True

def create_gitignore():
    """Create or update .gitignore file"""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Data files (keep source data, ignore temp files)
*.tmp
*.temp
temp_*
debug_*

# Mobile exports (keep processed)
mobile_results_*.json
!processed_exports/

# Excel temp files
~$*.xlsx

# Cache
.pytest_cache/
.coverage
htmlcov/

# Local development
local_*
test_*
debug_*
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    print("✅ Updated .gitignore")

def validate_json_files():
    """Validate key JSON files"""
    print("\n🔍 Validating JSON Files")
    print("=" * 25)
    
    json_files = [
        'uefa_fixtures_data.json',
        'fifa_country_codes.json'
    ]
    
    for file in json_files:
        if os.path.exists(file):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"✅ {file} - Valid JSON ({len(data)} items)")
            except json.JSONDecodeError as e:
                print(f"❌ {file} - Invalid JSON: {e}")
                return False
        else:
            print(f"⚠️ {file} - Not found")
    
    return True

def show_next_steps():
    """Show the next steps for GitHub setup"""
    print("\n🎯 Next Steps for GitHub Actions")
    print("=" * 35)
    print("1. Create new GitHub repository:")
    print("   - Go to https://github.com/new")
    print("   - Name: uefa-eta-rankings")
    print("   - Public or Private")
    print("   - Don't initialize with README")
    print()
    print("2. Push to GitHub:")
    print("   git remote add origin https://github.com/YOUR_USERNAME/uefa-eta-rankings.git")
    print("   git branch -M main")
    print("   git add .")
    print("   git commit -m 'Initial commit: UEFA ETA with GitHub Actions'")
    print("   git push -u origin main")
    print()
    print("3. Configure GitHub repository:")
    print("   - Settings → Actions → General")
    print("   - ✅ Allow all actions")
    print("   - ✅ Read and write permissions")
    print()
    print("4. Test the workflows:")
    print("   - Actions tab → 'UEFA Mobile Results Auto-Processor'")
    print("   - Click 'Run workflow'")
    print()
    print("5. Access mobile interface:")
    print("   - https://YOUR_USERNAME.github.io/uefa-eta-rankings/mobile/github_uefa_mobile.html")
    print("   - Or download mobile/github_uefa_mobile.html locally")

def main():
    print("🚀 UEFA ETA GitHub Actions Setup")
    print("=" * 40)
    print("This script prepares your UEFA ETA system for GitHub Actions deployment")
    print()
    
    # Check git status
    if not check_git_status():
        print("❌ Git repository setup required first")
        return
    
    # Prepare for GitHub
    if not prepare_for_github():
        print("❌ Missing required files - setup incomplete")
        return
    
    # Create/update .gitignore
    create_gitignore()
    
    # Validate JSON files
    if not validate_json_files():
        print("❌ JSON validation failed")
        return
    
    print("\n🎉 GitHub Actions Setup Complete!")
    print("✅ All required files present")
    print("✅ Repository structure validated")
    print("✅ JSON files validated")
    
    # Show next steps
    show_next_steps()
    
    print("\n💡 Benefits of GitHub Actions:")
    print("   🌍 Process results from anywhere")
    print("   ⚡ Instant cloud processing")
    print("   🔄 Automatic hourly updates")  
    print("   📱 Mobile-optimized interface")
    print("   🛡️ Enterprise-grade reliability")

if __name__ == "__main__":
    main()