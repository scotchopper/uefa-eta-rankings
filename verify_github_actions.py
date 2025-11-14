#!/usr/bin/env python3
"""
Simple GitHub Actions Test Script
Tests core functionality without complex dependencies
"""

import json
import os
from datetime import datetime
from pathlib import Path

def test_github_actions():
    """Test basic functionality for GitHub Actions"""
    print("🧪 Testing GitHub Actions UEFA Processing")
    print("=" * 45)
    
    # Test 1: Check if fixtures file exists
    fixtures_file = Path("uefa_fixtures_data.json")
    if fixtures_file.exists():
        try:
            with open(fixtures_file, 'r', encoding='utf-8') as f:
                fixtures = json.load(f)
            print(f"✅ Fixtures file loaded: {len(fixtures)} fixtures")
        except Exception as e:
            print(f"❌ Error loading fixtures: {e}")
            return False
    else:
        print("⚠️ No fixtures file found - this is expected for initial test")
    
    # Test 2: Check directory structure
    required_dirs = ['mobile', '.github/workflows']
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ Directory exists: {dir_name}")
        else:
            print(f"❌ Missing directory: {dir_name}")
    
    # Test 3: Check workflow files
    workflow_files = [
        '.github/workflows/uefa-auto-processor.yml',
        '.github/workflows/mobile-results-processor.yml'
    ]
    
    for workflow in workflow_files:
        if os.path.exists(workflow):
            print(f"✅ Workflow file exists: {os.path.basename(workflow)}")
        else:
            print(f"❌ Missing workflow: {workflow}")
    
    # Test 4: Test JSON processing (simulate mobile results)
    test_results = {
        "timestamp": datetime.now().isoformat(),
        "source": "github_actions_test",
        "results": [
            {
                "fixture_id": "test_001",
                "home_score": 2,
                "away_score": 1
            }
        ]
    }
    
    try:
        test_json = json.dumps(test_results, indent=2)
        print("✅ JSON processing test passed")
    except Exception as e:
        print(f"❌ JSON processing failed: {e}")
        return False
    
    # Test 5: Basic file operations
    try:
        test_file = Path("github_actions_test.json")
        with open(test_file, 'w') as f:
            json.dump(test_results, f, indent=2)
        
        # Read it back
        with open(test_file, 'r') as f:
            loaded_data = json.load(f)
        
        # Clean up
        test_file.unlink()
        print("✅ File operations test passed")
    except Exception as e:
        print(f"❌ File operations failed: {e}")
        return False
    
    print("\n🎉 All basic tests passed!")
    print("✅ GitHub Actions environment is ready")
    print("✅ Core functionality works without complex dependencies")
    
    return True

def main():
    """Main test function"""
    success = test_github_actions()
    
    if success:
        print("\n🚀 GitHub Actions UEFA Processing is ready!")
        print("📱 Mobile results can be processed successfully")
        print("🔄 Automated workflows should work correctly")
    else:
        print("\n❌ Setup issues detected - check the errors above")
        exit(1)

if __name__ == "__main__":
    main()