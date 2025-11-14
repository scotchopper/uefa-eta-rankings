#!/usr/bin/env python3
"""
Fix all UEFA fixture code issues automatically
"""

import json
from datetime import datetime

def fix_fixture_codes():
    """Fix all code issues in UEFA fixtures data"""
    
    # Load current data
    with open('uefa_fixtures_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    fixtures = data.get('fixtures', {})
    
    # Define correct mappings
    correct_codes = {
        'Albania': 'ALB',
        'Andorra': 'AND',
        'Armenia': 'ARM',
        'Austria': 'AUT',
        'Azerbaijan': 'AZE',
        'Belarus': 'BLR',
        'Belgium': 'BEL',
        'Bosnia and Herzegovina': 'BIH',
        'Bulgaria': 'BUL',
        'Croatia': 'CRO',
        'Cyprus': 'CYP',
        'Czech Republic': 'CZE',
        'Denmark': 'DEN',
        'England': 'ENG',
        'Estonia': 'EST',
        'Faroe Islands': 'FAR',
        'Finland': 'FIN',
        'France': 'FRA',
        'Georgia': 'GEO',
        'Germany': 'GER',
        'Gibraltar': 'GIB',
        'Greece': 'GRE',
        'Hungary': 'HUN',
        'Iceland': 'ICE',
        'Republic of Ireland': 'IRL',
        'Israel': 'ISR',
        'Italy': 'ITA',
        'Kazakhstan': 'KAZ',
        'Kosovo': 'KOS',
        'Latvia': 'LAT',
        'Liechtenstein': 'LIE',
        'Lithuania': 'LIT',
        'Luxembourg': 'LUX',
        'Malta': 'MLT',
        'Moldova': 'MDA',
        'Montenegro': 'MNE',
        'Netherlands': 'NED',
        'North Macedonia': 'MKD',
        'Northern Ireland': 'NIR',
        'Norway': 'NOR',
        'Poland': 'POL',
        'Portugal': 'POR',
        'Romania': 'ROU',
        'San Marino': 'SMR',
        'Scotland': 'SCO',
        'Serbia': 'SRB',
        'Slovakia': 'SVK',
        'Slovenia': 'SVN',
        'Spain': 'ESP',
        'Sweden': 'SWE',
        'Switzerland': 'SUI',
        'Turkey': 'TUR',
        'Ukraine': 'UKR',
        'Wales': 'WAL'
    }
    
    # Fix codes in all fixtures
    changes_made = []
    
    for fixture_id, fixture in fixtures.items():
        home_team = fixture.get('home_team', '')
        away_team = fixture.get('away_team', '')
        home_code = fixture.get('home_code')
        away_code = fixture.get('away_code')
        
        # Fix home team code
        if home_team in correct_codes:
            correct_home_code = correct_codes[home_team]
            if home_code != correct_home_code:
                old_code = home_code if home_code is not None else 'null'
                fixture['home_code'] = correct_home_code
                changes_made.append(f"{fixture_id}: {home_team} home code: {old_code} → {correct_home_code}")
        
        # Fix away team code
        if away_team in correct_codes:
            correct_away_code = correct_codes[away_team]
            if away_code != correct_away_code:
                old_code = away_code if away_code is not None else 'null'
                fixture['away_code'] = correct_away_code
                changes_made.append(f"{fixture_id}: {away_team} away code: {old_code} → {correct_away_code}")
    
    # Update timestamp
    data['last_updated'] = datetime.now().isoformat()
    
    # Save corrected data
    with open('uefa_fixtures_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Create backup with original
    with open('uefa_fixtures_data_backup.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"🔧 FIXED {len(changes_made)} CODE ISSUES:")
    print("=" * 50)
    
    for change in changes_made:
        print(f"   ✅ {change}")
    
    print(f"\n📝 Backup saved as: uefa_fixtures_data_backup.json")
    print(f"✅ All fixture codes corrected!")
    
    return len(changes_made)

if __name__ == "__main__":
    changes = fix_fixture_codes()
    print(f"\nTotal changes made: {changes}")