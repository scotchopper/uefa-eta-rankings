#!/usr/bin/env python3
"""
Update fixture codes to match the corrected FIFA country codes
"""

import json
from datetime import datetime

def update_fixture_codes():
    """Update fixture codes to match corrected FIFA country codes"""
    
    # Load FIFA rankings with corrected codes
    with open('fifa_rankings_from_excel.json', 'r', encoding='utf-8') as f:
        fifa_data = json.load(f)
    
    # Create name-to-code mapping from FIFA data
    fifa_codes = {team['team']: team['code'] for team in fifa_data['rankings']}
    
    # Load fixture data
    with open('uefa_fixtures_data.json', 'r', encoding='utf-8') as f:
        fixture_data = json.load(f)
    
    fixtures = fixture_data.get('fixtures', {})
    
    print("🔧 UPDATING FIXTURE CODES TO MATCH CORRECTED FIFA CODES")
    print("=" * 60)
    
    changes_made = []
    
    # Update codes in all fixtures
    for fixture_id, fixture in fixtures.items():
        home_team = fixture.get('home_team', '')
        away_team = fixture.get('away_team', '')
        home_code = fixture.get('home_code')
        away_code = fixture.get('away_code')
        
        # Update home team code
        if home_team in fifa_codes:
            correct_code = fifa_codes[home_team]
            if home_code != correct_code:
                old_code = home_code if home_code else 'null'
                fixture['home_code'] = correct_code
                changes_made.append(f"{fixture_id}: {home_team} code: {old_code} → {correct_code}")
        
        # Update away team code
        if away_team in fifa_codes:
            correct_code = fifa_codes[away_team]
            if away_code != correct_code:
                old_code = away_code if away_code else 'null'
                fixture['away_code'] = correct_code
                changes_made.append(f"{fixture_id}: {away_team} code: {old_code} → {correct_code}")
    
    # Update timestamp
    fixture_data['last_updated'] = datetime.now().isoformat()
    
    # Save updated fixture data
    with open('uefa_fixtures_data.json', 'w', encoding='utf-8') as f:
        json.dump(fixture_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ MADE {len(changes_made)} CODE UPDATES:")
    print("-" * 50)
    
    if changes_made:
        for change in changes_made:
            print(f"   {change}")
    else:
        print("   No changes needed - codes already correct!")
    
    # Verify alignment
    print(f"\n🔍 VERIFYING ALIGNMENT WITH FIFA CODES:")
    print("-" * 40)
    
    all_aligned = True
    mismatches = []
    
    for fixture in fixtures.values():
        home_team = fixture.get('home_team', '')
        away_team = fixture.get('away_team', '')
        home_code = fixture.get('home_code')
        away_code = fixture.get('away_code')
        
        if home_team in fifa_codes:
            expected_code = fifa_codes[home_team]
            if home_code != expected_code:
                mismatches.append(f"{home_team}: {home_code} (expected {expected_code})")
                all_aligned = False
        
        if away_team in fifa_codes:
            expected_code = fifa_codes[away_team]
            if away_code != expected_code:
                mismatches.append(f"{away_team}: {away_code} (expected {expected_code})")
                all_aligned = False
    
    if all_aligned:
        print("✅ Perfect alignment! All fixture codes match FIFA codes!")
    else:
        print(f"❌ Found {len(mismatches)} mismatches:")
        for mismatch in mismatches:
            print(f"   {mismatch}")
    
    return len(changes_made), all_aligned

if __name__ == "__main__":
    changes, aligned = update_fixture_codes()
    print(f"\nSummary:")
    print(f"  Code updates made: {changes}")
    print(f"  Fully aligned: {aligned}")