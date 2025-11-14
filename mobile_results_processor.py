#!/usr/bin/env python3
"""
Mobile Results Processor - Automatically update rankings from mobile exports
"""

import json
import re
from datetime import datetime
import subprocess
import sys

def parse_mobile_export(export_text):
    """Parse the mobile export text format"""
    results = []
    lines = export_text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if ':' in line and '-' in line:
            # Format: "GRE_SCO: Greece 2-1 Scotland"
            parts = line.split(': ', 1)
            if len(parts) == 2:
                fixture_id = parts[0].strip()
                match_text = parts[1].strip()
                
                # Parse team names and scores
                # Handle formats like "Greece 2-1 Scotland"
                pattern = r'(.+?)\s+(\d+)-(\d+)\s+(.+)'
                match = re.match(pattern, match_text)
                
                if match:
                    home_team = match.group(1).strip()
                    home_goals = int(match.group(2))
                    away_goals = int(match.group(3))
                    away_team = match.group(4).strip()
                    
                    results.append({
                        'fixture_id': fixture_id,
                        'home_team': home_team,
                        'away_team': away_team,
                        'home_goals': home_goals,
                        'away_goals': away_goals,
                        'match_text': match_text
                    })
    
    return results

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
        # Find matching fixture
        fixture_found = False
        for fixture_id, fixture_data in data['fixtures'].items():
            # Match by teams
            home_match = fixture_data['home_team'].lower() == result['home_team'].lower()
            away_match = fixture_data['away_team'].lower() == result['away_team'].lower()
            
            if home_match and away_match:
                # Update results
                if 'results' not in data:
                    data['results'] = {}
                
                # Determine result
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
                    'notes': f"Updated from mobile - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                    'completed_at': datetime.now().isoformat()
                }
                
                # Update fixture status
                data['fixtures'][fixture_id]['status'] = 'completed'
                
                updated_count += 1
                fixture_found = True
                print(f"✅ Updated: {result['match_text']}")
                break
        
        if not fixture_found:
            print(f"⚠️  Could not find fixture for: {result['match_text']}")
    
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

def main():
    print("📱 Mobile Results Processor")
    print("=" * 40)
    
    # Get mobile export text
    print("\n📋 Paste your mobile export text below.")
    print("   (The text that starts with 'UEFA Mobile Results:')")
    print("   Press Enter twice when done:\n")
    
    lines = []
    empty_count = 0
    
    while True:
        try:
            line = input()
            if line.strip() == "":
                empty_count += 1
                if empty_count >= 2:
                    break
            else:
                empty_count = 0
                lines.append(line)
        except KeyboardInterrupt:
            print("\n❌ Cancelled by user")
            return
    
    export_text = '\n'.join(lines)
    
    if not export_text.strip():
        print("❌ No results provided!")
        return
    
    # Parse results
    print("\n🔍 Parsing mobile results...")
    results = parse_mobile_export(export_text)
    
    if not results:
        print("❌ No valid results found in export text!")
        return
    
    print(f"📊 Found {len(results)} results to process:")
    for result in results:
        print(f"   • {result['match_text']}")
    
    # Confirm update
    confirm = input(f"\n❓ Update these {len(results)} results? (y/n): ").lower().strip()
    if confirm != 'y':
        print("❌ Update cancelled")
        return
    
    # Update fixtures
    print("\n💾 Updating fixtures data...")
    if update_fixtures_data(results):
        # Run analysis
        if run_analysis():
            print("\n🎉 SUCCESS! Rankings updated from mobile results!")
            print("\n📊 Next steps:")
            print("   1. Check the analysis output above")
            print("   2. View updated mobile report: python simple_mobile_analyzer.py")
            print("   3. Scotland's new ranking position is shown in the analysis")
        else:
            print("\n⚠️  Results updated but analysis failed")
            print("   Run manually: python enhanced_team_range_analysis.py")
    else:
        print("\n❌ Failed to update fixtures data")

if __name__ == "__main__":
    main()