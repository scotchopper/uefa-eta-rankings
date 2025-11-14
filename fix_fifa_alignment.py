#!/usr/bin/env python3
"""
Fix team names and codes to match FIFA spreadsheet exactly
"""

import json
from datetime import datetime

def fix_names_and_codes():
    """Fix team names and codes to match FIFA spreadsheet"""
    
    # Load current fixture data
    with open('uefa_fixtures_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    fixtures = data.get('fixtures', {})
    
    # Define exact mappings from FIFA spreadsheet
    fifa_corrections = {
        # Team name corrections (fixtures → FIFA spreadsheet names)
        'Czech Republic': 'Czechia',
        'Turkey': 'Türkiye',
        
        # Code corrections (current → FIFA spreadsheet codes)
        # Keep teams with names that need to change
        'Czechia': 'CZE',           # Czech Republic → Czechia
        'Türkiye': 'TUR',           # Turkey → Türkiye (but use TUR code)
        
        # Fix codes to match FIFA spreadsheet exactly
        'Austria': 'AUS',           # Currently AUT → AUS
        'Belarus': 'BEL',           # Currently BLR → BEL (conflicts with Belgium!)
        'Belgium': 'BEL',           # This will create a conflict!
        'Bosnia and Herzegovina': 'BOS',   # Currently BIH → BOS
        'Malta': 'MAL',             # Currently MLT → MAL  
        'Moldova': 'MOL',           # Currently MDA → MOL
        'Montenegro': 'MON',        # Currently MNE → MON
        'Netherlands': 'NET',       # Currently NED → NET
        'North Macedonia': 'NOR',   # Currently MKD → NOR (conflicts!)
        'Northern Ireland': 'NOR',  # Currently NIR → NOR (conflicts!)  
        'Norway': 'NOR',            # All three use NOR!
        'Republic of Ireland': 'REP', # Currently IRL → REP
        'Romania': 'ROM',           # Currently ROU → ROM
        'San Marino': 'SAN',        # Currently SMR → SAN
        'Serbia': 'SER',            # Currently SRB → SER
        'Slovakia': 'SLO',          # Currently SVK → SLO (conflicts with Slovenia!)
        'Slovenia': 'SLO',          # Both Slovakia and Slovenia use SLO!
        'Spain': 'SPA',             # Currently ESP → SPA  
        'Switzerland': 'SWI'        # Currently SUI → SWI
    }
    
    print("🔧 FIXING TEAM NAMES AND CODES TO MATCH FIFA SPREADSHEET")
    print("=" * 60)
    
    changes_made = []
    
    # First pass: Fix team names
    for fixture_id, fixture in fixtures.items():
        home_team = fixture.get('home_team', '')
        away_team = fixture.get('away_team', '')
        
        # Fix home team name
        if home_team in fifa_corrections:
            if home_team != fifa_corrections[home_team]:  # Name change
                new_name = fifa_corrections[home_team]
                fixture['home_team'] = new_name
                changes_made.append(f"{fixture_id}: {home_team} → {new_name} (home team name)")
        
        # Fix away team name  
        if away_team in fifa_corrections:
            if away_team != fifa_corrections[away_team]:  # Name change
                new_name = fifa_corrections[away_team]
                fixture['away_team'] = new_name
                changes_made.append(f"{fixture_id}: {away_team} → {new_name} (away team name)")
    
    # Second pass: Fix codes based on current team names
    for fixture_id, fixture in fixtures.items():
        home_team = fixture.get('home_team', '')
        away_team = fixture.get('away_team', '')
        home_code = fixture.get('home_code')
        away_code = fixture.get('away_code')
        
        # Fix home team code
        if home_team in fifa_corrections:
            correct_code = fifa_corrections[home_team]
            if home_code != correct_code:
                old_code = home_code if home_code else 'null'
                fixture['home_code'] = correct_code
                changes_made.append(f"{fixture_id}: {home_team} code: {old_code} → {correct_code}")
        
        # Fix away team code
        if away_team in fifa_corrections:
            correct_code = fifa_corrections[away_team]
            if away_code != correct_code:
                old_code = away_code if away_code else 'null'
                fixture['away_code'] = correct_code
                changes_made.append(f"{fixture_id}: {away_team} code: {old_code} → {correct_code}")
    
    # Update timestamp
    data['last_updated'] = datetime.now().isoformat()
    
    # Save updated data
    with open('uefa_fixtures_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ MADE {len(changes_made)} CORRECTIONS:")
    print("-" * 40)
    
    for change in changes_made:
        print(f"   {change}")
    
    # Check for conflicts
    print(f"\n⚠️  CHECKING FOR CODE CONFLICTS:")
    print("-" * 35)
    
    code_conflicts = {
        'BEL': ['Belarus', 'Belgium'],
        'NOR': ['North Macedonia', 'Northern Ireland', 'Norway'], 
        'SLO': ['Slovakia', 'Slovenia']
    }
    
    for code, teams in code_conflicts.items():
        print(f"   {code}: {', '.join(teams)} ⚠️ CONFLICT!")
    
    print(f"\n📝 Note: Your FIFA spreadsheet has code conflicts that need resolution!")
    
    return len(changes_made)

if __name__ == "__main__":
    changes = fix_names_and_codes()
    print(f"\nTotal corrections made: {changes}")