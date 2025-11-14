#!/usr/bin/env python3
"""
Final UEFA Fixture Count Verification
Verify that all 54 UEFA teams have exactly 2 games
"""

import json
from collections import defaultdict

def main():
    """Verify UEFA fixture counts"""
    
    # Load fixtures
    try:
        with open('uefa_fixtures_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            fixtures = data.get('fixtures', {})
        print(f"✅ Loaded {len(fixtures)} fixtures")
    except FileNotFoundError:
        print("❌ UEFA fixtures file not found")
        return
    
    print("\n🔍 FINAL UEFA FIXTURE VERIFICATION")
    print("=" * 50)
    
    # Count fixtures per team
    team_fixture_count = defaultdict(int)
    teams_in_fixtures = set()
    
    for fixture_id, fixture in fixtures.items():
        home_team = fixture.get('home_team', '')
        away_team = fixture.get('away_team', '')
        
        if home_team:
            teams_in_fixtures.add(home_team)
            team_fixture_count[home_team] += 1
        if away_team:
            teams_in_fixtures.add(away_team)
            team_fixture_count[away_team] += 1
    
    # Categorize teams by fixture count
    teams_with_2_games = []
    teams_with_other_counts = []
    
    for team, count in team_fixture_count.items():
        if count == 2:
            teams_with_2_games.append(team)
        else:
            teams_with_other_counts.append((team, count))
    
    # Results
    print(f"📊 Total unique teams found: {len(teams_in_fixtures)}")
    print(f"✅ Teams with exactly 2 games: {len(teams_with_2_games)}")
    print(f"⚠️  Teams with other counts: {len(teams_with_other_counts)}")
    
    if teams_with_other_counts:
        print(f"\n❌ TEAMS WITH INCORRECT FIXTURE COUNT:")
        print("-" * 40)
        for team, count in teams_with_other_counts:
            print(f"   {team}: {count} games")
    
    # Verify codes
    teams_without_codes = []
    for fixture_id, fixture in fixtures.items():
        home_team = fixture.get('home_team', '')
        away_team = fixture.get('away_team', '')
        home_code = fixture.get('home_code')
        away_code = fixture.get('away_code')
        
        if home_team and not home_code:
            teams_without_codes.append(f"{fixture_id}: {home_team} (home)")
        if away_team and not away_code:
            teams_without_codes.append(f"{fixture_id}: {away_team} (away)")
    
    print(f"\n🔍 CODE VERIFICATION:")
    print("-" * 25)
    print(f"Teams without codes: {len(teams_without_codes)}")
    
    if teams_without_codes:
        print("Missing codes:")
        for missing in teams_without_codes[:5]:  # Show first 5
            print(f"   {missing}")
        if len(teams_without_codes) > 5:
            print(f"   ... and {len(teams_without_codes) - 5} more")
    
    # List all teams with 2 games
    print(f"\n✅ ALL TEAMS WITH EXACTLY 2 GAMES ({len(teams_with_2_games)} teams):")
    print("-" * 55)
    for i, team in enumerate(sorted(teams_with_2_games), 1):
        print(f"{i:2d}. {team}")
    
    # Final verification
    print(f"\n🏆 FINAL VERIFICATION RESULT:")
    print("-" * 35)
    if len(teams_in_fixtures) == 54 and len(teams_with_2_games) == 54 and len(teams_without_codes) == 0:
        print("✅ PERFECT: All 54 UEFA teams have exactly 2 games with proper codes!")
    elif len(teams_in_fixtures) == 54 and len(teams_with_2_games) == 54:
        print("✅ EXCELLENT: All 54 UEFA teams have exactly 2 games!")
        if len(teams_without_codes) > 0:
            print(f"⚠️  Minor issue: {len(teams_without_codes)} missing codes")
    else:
        print(f"❌ Issues found:")
        print(f"   Total teams: {len(teams_in_fixtures)} (expected: 54)")
        print(f"   Teams with 2 games: {len(teams_with_2_games)} (expected: 54)")
        print(f"   Missing codes: {len(teams_without_codes)}")

if __name__ == "__main__":
    main()