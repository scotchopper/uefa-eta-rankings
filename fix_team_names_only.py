#!/usr/bin/env python3
"""
Fix team names to match FIFA spreadsheet while keeping sensible codes
"""

import json
from datetime import datetime

def fix_team_names_only():
    """Fix only team names to match FIFA spreadsheet, keep sensible codes"""
    
    # Load current fixture data
    with open('uefa_fixtures_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    fixtures = data.get('fixtures', {})
    
    # Only fix team names - keep our sensible codes
    name_corrections = {
        'Czech Republic': 'Czechia',
        'Turkey': 'Türkiye'
    }
    
    # Note: We discovered your FIFA spreadsheet has code conflicts:
    # BEL: Belarus + Belgium  
    # NOR: North Macedonia + Northern Ireland + Norway
    # SLO: Slovakia + Slovenia
    
    print("🔧 FIXING TEAM NAMES TO MATCH FIFA SPREADSHEET")
    print("=" * 50)
    print("⚠️  Note: Keeping sensible codes due to FIFA spreadsheet conflicts")
    print()
    
    changes_made = []
    
    for fixture_id, fixture in fixtures.items():
        home_team = fixture.get('home_team', '')
        away_team = fixture.get('away_team', '')
        
        # Fix home team name
        if home_team in name_corrections:
            new_name = name_corrections[home_team]
            fixture['home_team'] = new_name
            changes_made.append(f"{fixture_id}: {home_team} → {new_name} (home)")
        
        # Fix away team name
        if away_team in name_corrections:
            new_name = name_corrections[away_team]
            fixture['away_team'] = new_name
            changes_made.append(f"{fixture_id}: {away_team} → {new_name} (away)")
    
    # Update timestamp
    data['last_updated'] = datetime.now().isoformat()
    
    # Save updated data
    with open('uefa_fixtures_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ MADE {len(changes_made)} NAME CORRECTIONS:")
    print("-" * 40)
    
    for change in changes_made:
        print(f"   {change}")
    
    print(f"\n📊 FIFA SPREADSHEET CODE CONFLICTS DETECTED:")
    print("-" * 45)
    print("   BEL: Belarus + Belgium")  
    print("   NOR: North Macedonia + Northern Ireland + Norway")
    print("   SLO: Slovakia + Slovenia")
    print()
    print("💡 RECOMMENDATION:")
    print("   Fix your FIFA spreadsheet to use unique codes:")
    print("   Belarus: BLR, Belgium: BEL")
    print("   North Macedonia: MKD, Northern Ireland: NIR, Norway: NOR") 
    print("   Slovakia: SVK, Slovenia: SVN")
    
    return len(changes_made)

if __name__ == "__main__":
    changes = fix_team_names_only()
    print(f"\nTeam name corrections made: {changes}")