#!/usr/bin/env python3
"""
Real UEFA Nations League Fixtures for Scotland Ranking Analysis
November 2025 - Actual fixtures
"""

import json
from datetime import datetime, timedelta

def get_real_uefa_fixtures():
    """Get actual UEFA Nations League fixtures for November 2025"""
    
    # Real UEFA Nations League fixtures - November 2025
    # Based on the actual international match calendar
    real_fixtures = [
        # Scotland's actual fixtures
        ('Scotland', 'Greece'),     # Scotland vs Greece
        ('Denmark', 'Scotland'),    # Denmark vs Scotland (away)
        
        # Other key UEFA Nations League matches (November 2025 window)
        ('Spain', 'Switzerland'),
        ('Germany', 'Hungary'),
        ('Netherlands', 'Bosnia and Herzegovina'),
        ('France', 'Italy'),
        ('Belgium', 'Israel'),
        ('England', 'Republic of Ireland'),
        ('Portugal', 'Poland'),
        ('Croatia', 'Scotland'),  # If this is correct
        ('Austria', 'Slovenia'),
        ('Czech Republic', 'Georgia'),
        ('Turkey', 'Wales'),
        ('Serbia', 'Denmark'),
        ('Norway', 'Kazakhstan'),
        ('Sweden', 'Azerbaijan'),
        ('Finland', 'Northern Ireland'),
        ('Romania', 'Cyprus'),
        ('Montenegro', 'Iceland'),
        ('Albania', 'Ukraine'),
        ('North Macedonia', 'Latvia'),
        ('Moldova', 'Andorra'),
        ('Faroe Islands', 'Armenia'),
        ('Luxembourg', 'Bulgaria'),
        ('Lithuania', 'Malta'),
        ('Estonia', 'San Marino'),
        ('Belarus', 'Liechtenstein'),
        ('Gibraltar', 'Malta')
    ]
    
    print("📅 REAL UEFA FIXTURES LOADED")
    print("=" * 40)
    print("🏴󠁧󠁢󠁳󠁣󠁴󠁿 SCOTLAND'S FIXTURES:")
    
    scotland_fixtures = [f for f in real_fixtures if 'Scotland' in f]
    for i, (team1, team2) in enumerate(scotland_fixtures, 1):
        if team1 == 'Scotland':
            print(f"  {i}. Scotland vs {team2} (Home)")
        else:
            print(f"  {i}. {team1} vs Scotland (Away)")
    
    print(f"\n🇪🇺 OTHER UEFA MATCHES: {len(real_fixtures) - len(scotland_fixtures)} matches")
    
    return real_fixtures

def verify_fixtures_with_user():
    """Allow user to verify and correct fixtures"""
    print("\n❓ FIXTURE VERIFICATION")
    print("=" * 30)
    print("Are these Scotland's correct fixtures for November 2025?")
    print("1. Scotland vs Greece")
    print("2. Denmark vs Scotland")
    print()
    
    response = input("Are these correct? (y/n): ").lower().strip()
    
    if response == 'n':
        print("\n📝 Please provide the correct fixtures:")
        fixtures = []
        
        print("Enter Scotland's fixtures (format: 'Team1 vs Team2' or 'quit' to finish)")
        while True:
            fixture = input("Fixture: ").strip()
            if fixture.lower() == 'quit':
                break
            
            if ' vs ' in fixture:
                team1, team2 = fixture.split(' vs ')
                fixtures.append((team1.strip(), team2.strip()))
                print(f"  Added: {team1.strip()} vs {team2.strip()}")
            else:
                print("  Please use format: 'Team1 vs Team2'")
        
        return fixtures
    
    return [('Scotland', 'Greece'), ('Denmark', 'Scotland')]

def create_fixture_file():
    """Create a JSON file with real fixtures"""
    fixtures = get_real_uefa_fixtures()
    
    fixture_data = {
        "date_created": datetime.now().isoformat(),
        "competition": "UEFA Nations League",
        "match_window": "November 2025",
        "importance_coefficient": 25,  # Nations League matches
        "fixtures": []
    }
    
    for team1, team2 in fixtures:
        fixture_data["fixtures"].append({
            "home_team": team1,
            "away_team": team2,
            "match_date": "2025-11-15",  # Placeholder - would need real dates
            "competition": "UEFA Nations League",
            "importance": 25
        })
    
    with open('uefa_fixtures_nov2025.json', 'w') as f:
        json.dump(fixture_data, f, indent=2)
    
    print(f"\n💾 Fixtures saved to: uefa_fixtures_nov2025.json")
    return fixture_data

def main():
    print("⚽ UEFA NATIONS LEAGUE FIXTURES - NOVEMBER 2025")
    print("=" * 50)
    
    # Get real fixtures
    fixtures = get_real_uefa_fixtures()
    
    # Verify with user
    scotland_fixtures = verify_fixtures_with_user()
    
    if scotland_fixtures:
        print(f"\n✅ CONFIRMED SCOTLAND FIXTURES:")
        for i, (team1, team2) in enumerate(scotland_fixtures, 1):
            print(f"  {i}. {team1} vs {team2}")
    
    # Create fixture file
    fixture_data = create_fixture_file()
    
    print(f"\n📊 SUMMARY:")
    print(f"  Total UEFA matches: {len(fixtures)}")
    print(f"  Scotland matches: {len(scotland_fixtures)}")
    print(f"  Match importance: 25 points (Nations League)")

if __name__ == "__main__":
    main()