#!/usr/bin/env python3
"""
Mobile JSON Processor - Automatically update rankings from mobile JSON exports
No copy/paste needed - just reads the JSON file directly!
"""

import json
import os
import glob
from datetime import datetime
import subprocess
import sys

def find_mobile_json_files():
    """Find all mobile results JSON files"""
    pattern = "uefa_mobile_results_*.json"
    
    # Check current directory first
    files = glob.glob(pattern)
    
    # Also check mobile subdirectory (OneDrive sync location)
    mobile_pattern = os.path.join("mobile", pattern)
    mobile_files = glob.glob(mobile_pattern)
    files.extend(mobile_files)
    
    if not files:
        print("❌ No mobile results JSON files found!")
        print(f"   Looking for: {pattern}")
        print(f"   Also checked: {mobile_pattern}")
        print("\n💡 Expected locations:")
        print("   • Root folder (manual copy)")
        print("   • mobile/ folder (OneDrive sync)")
        print("\n🔄 If using OneDrive sync:")
        print("   1. Check that OneDrive has synced the file")
        print("   2. File should appear in mobile/ folder")
        print("   3. Wait a moment for sync to complete")
        return []
    
    # Sort by modification time (newest first)
    files.sort(key=os.path.getmtime, reverse=True)
    return files

def load_mobile_results(json_file):
    """Load results from mobile JSON export"""
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        print(f"📊 Loaded {data['total_results']} results from {json_file}")
        print(f"📅 Export timestamp: {data['export_timestamp']}")
        
        return data['results']
        
    except Exception as e:
        print(f"❌ Error loading {json_file}: {e}")
        return []

def update_fixtures_data(results):
    """Update the fixtures data JSON file"""
    try:
        with open('uefa_fixtures_data.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ uefa_fixtures_data.json not found!")
        return False
    
    updated_count = 0
    
    for result in results:
        # Find matching fixture by searching all fixtures
        fixture_found = False
        for fixture_id, fixture_data in data['fixtures'].items():
            # Match by teams (case insensitive)
            home_match = fixture_data['home_team'].lower() == result['home_team'].lower()
            away_match = fixture_data['away_team'].lower() == result['away_team'].lower()
            
            if home_match and away_match:
                # Update results
                if 'results' not in data:
                    data['results'] = {}
                
                # Determine result code
                if result['home_goals'] > result['away_goals']:
                    result_code = 'H'
                elif result['away_goals'] > result['home_goals']:
                    result_code = 'A'
                else:
                    result_code = 'D'
                
                data['results'][fixture_id] = {
                    'home_goals': result['home_goals'],
                    'away_goals': result['away_goals'],
                    'result': result_code,
                    'notes': f"Mobile JSON import - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                    'completed_at': datetime.now().isoformat()
                }
                
                # Update fixture status
                data['fixtures'][fixture_id]['status'] = 'completed'
                
                updated_count += 1
                fixture_found = True
                print(f"✅ Updated: {result['result_text']}")
                break
        
        if not fixture_found:
            print(f"⚠️  Could not find fixture for: {result['result_text']}")
    
    # Save updated data
    data['last_updated'] = datetime.now().isoformat()
    
    with open('uefa_fixtures_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n📊 Updated {updated_count} fixtures in uefa_fixtures_data.json")
    return updated_count > 0

def run_analysis():
    """Run the enhanced team range analysis"""
    try:
        print("\n🔄 Running enhanced team range analysis...")
        result = subprocess.run([sys.executable, 'enhanced_team_range_analysis.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Analysis completed successfully!")
            print("📊 Updated rankings are now available")
            return True
        else:
            print(f"❌ Analysis failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error running analysis: {e}")
        return False

def update_mobile_reports():
    """Update mobile HTML reports"""
    try:
        print("\n📱 Updating mobile reports...")
        result = subprocess.run([sys.executable, 'simple_mobile_analyzer.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Mobile reports updated!")
            print("📊 Updated mobile analysis available in OneDrive")
            return True
        else:
            print(f"⚠️  Mobile report update failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"⚠️  Error updating mobile reports: {e}")
        return False

def archive_processed_file(json_file):
    """Move processed JSON file to archive"""
    try:
        archive_dir = "processed_mobile_results"
        if not os.path.exists(archive_dir):
            os.makedirs(archive_dir)
        
        # Create archived filename with timestamp
        base_name = os.path.splitext(os.path.basename(json_file))[0]
        archive_name = f"{base_name}_processed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        archive_path = os.path.join(archive_dir, archive_name)
        
        os.rename(json_file, archive_path)
        print(f"📁 Archived processed file: {archive_path}")
        
    except Exception as e:
        print(f"⚠️  Could not archive file: {e}")

def main():
    print("📱→💻 Mobile JSON Results Processor")
    print("=" * 45)
    
    # Find mobile JSON files
    json_files = find_mobile_json_files()
    if not json_files:
        print("\n💡 To use this processor:")
        print("   📱 ONEDRIVE SYNC METHOD (Recommended):")
        print("      1. Export results from mobile HTML (saves to OneDrive)")
        print("      2. Wait for OneDrive sync (check mobile/ folder)")
        print("      3. Run this script again")
        print("\n   📂 MANUAL COPY METHOD:")
        print("      1. Export results from mobile HTML (downloads JSON)")
        print("      2. Copy/move the JSON file to this folder")
        print("      3. Run this script again")
        
        # Check if we should wait for sync
        retry = input("\n❓ Wait 10 seconds for OneDrive sync and retry? (y/n): ").lower().strip()
        if retry == 'y':
            print("⏳ Waiting for OneDrive sync...")
            import time
            time.sleep(10)
            print("🔄 Checking for files again...")
            json_files = find_mobile_json_files()
            if not json_files:
                print("❌ Still no files found after waiting")
                return
        else:
            return
    
    # Show available files
    print(f"\n📂 Found {len(json_files)} mobile results file(s):")
    for i, file in enumerate(json_files, 1):
        mtime = datetime.fromtimestamp(os.path.getmtime(file))
        size = os.path.getsize(file)
        print(f"   {i}. {file} ({size} bytes, {mtime.strftime('%Y-%m-%d %H:%M')})")
    
    # Select file to process
    if len(json_files) == 1:
        selected_file = json_files[0]
        print(f"\n🎯 Processing: {selected_file}")
    else:
        try:
            choice = input(f"\n❓ Select file to process (1-{len(json_files)}): ").strip()
            index = int(choice) - 1
            if 0 <= index < len(json_files):
                selected_file = json_files[index]
            else:
                print("❌ Invalid selection")
                return
        except (ValueError, KeyboardInterrupt):
            print("❌ Invalid input or cancelled")
            return
    
    # Load and process results
    print(f"\n🔍 Loading results from {selected_file}...")
    results = load_mobile_results(selected_file)
    
    if not results:
        print("❌ No valid results found!")
        return
    
    print(f"\n📊 Found {len(results)} results to process:")
    scotland_results = []
    other_results = []
    
    for result in results:
        if result['is_scotland']:
            scotland_results.append(result)
        else:
            other_results.append(result)
        print(f"   • {result['result_text']}")
    
    print(f"\n🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland results: {len(scotland_results)}")
    print(f"🌍 Other UEFA results: {len(other_results)}")
    
    # Confirm processing
    confirm = input(f"\n❓ Process these {len(results)} results? (y/n): ").lower().strip()
    if confirm != 'y':
        print("❌ Processing cancelled")
        return
    
    # Update fixtures
    print("\n💾 Updating fixtures data...")
    if update_fixtures_data(results):
        # Run analysis
        analysis_success = run_analysis()
        
        # Update mobile reports
        mobile_success = update_mobile_reports()
        
        if analysis_success:
            print("\n🎉 SUCCESS! Rankings updated from mobile JSON!")
            print("\n📊 What's been updated:")
            print("   ✅ UEFA fixtures data")
            print("   ✅ FIFA ranking analysis")
            if mobile_success:
                print("   ✅ Mobile HTML reports (synced to OneDrive)")
            print(f"   ✅ {len(scotland_results)} Scotland result(s) processed")
            print(f"   ✅ {len(other_results)} other UEFA result(s) processed")
            
            print("\n📱 Next steps:")
            print("   • Check mobile/fifa_mobile_simple.html for updated rankings")
            print("   • Scotland's new position is shown in the analysis above")
            print("   • Mobile reports will sync back to your device via OneDrive")
            
            # Archive the processed file
            archive_processed_file(selected_file)
            
        else:
            print("\n⚠️  Results updated but analysis failed")
            print("   Try running manually: python enhanced_team_range_analysis.py")
    else:
        print("\n❌ Failed to update fixtures data")

if __name__ == "__main__":
    main()