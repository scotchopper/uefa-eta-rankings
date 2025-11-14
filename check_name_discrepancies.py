#!/usr/bin/env python3
"""
Check for discrepancies between fixture team names and FIFA ranking data
"""

import json
from difflib import get_close_matches

def load_data():
    """Load both fixtures and FIFA rankings"""
    
    # Load fixtures
    try:
        with open('uefa_fixtures_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            fixtures = data.get('fixtures', {})
        print(f"✅ Loaded {len(fixtures)} fixtures")
    except FileNotFoundError:
        print("❌ UEFA fixtures file not found")
        return {}, {}
    
    # Load FIFA rankings
    try:
        with open('fifa_rankings_from_excel.json', 'r', encoding='utf-8') as f:
            rankings_data = json.load(f)
            if 'rankings' in rankings_data:
                fifa_rankings = {team['team']: team for team in rankings_data['rankings']}
            else:
                fifa_rankings = rankings_data
        print(f"✅ Loaded {len(fifa_rankings)} FIFA team rankings")
    except FileNotFoundError:
        print("❌ FIFA rankings file not found")
        return fixtures, {}
    
    return fixtures, fifa_rankings

def check_team_name_discrepancies(fixtures, fifa_rankings):
    """Check for team name discrepancies between fixtures and rankings"""
    
    print("\n🔍 CHECKING TEAM NAME DISCREPANCIES")
    print("=" * 50)
    
    # Get all team names from fixtures
    fixture_teams = set()
    for fixture in fixtures.values():
        home_team = fixture.get('home_team', '').strip()
        away_team = fixture.get('away_team', '').strip()
        if home_team:
            fixture_teams.add(home_team)
        if away_team:
            fixture_teams.add(away_team)
    
    # Get all team names from FIFA rankings
    fifa_teams = set(fifa_rankings.keys())
    
    print(f"📊 Teams in fixtures: {len(fixture_teams)}")
    print(f"📊 Teams in FIFA rankings: {len(fifa_teams)}")
    
    # Find teams in fixtures but not in FIFA rankings (exact match)
    missing_from_fifa = fixture_teams - fifa_teams
    
    # Find teams in FIFA rankings but not in fixtures
    missing_from_fixtures = fifa_teams - fixture_teams
    
    print(f"\n❌ TEAMS IN FIXTURES BUT NOT IN FIFA RANKINGS ({len(missing_from_fifa)}):")
    print("-" * 55)
    
    discrepancies = []
    
    for team in sorted(missing_from_fifa):
        # Find closest match in FIFA rankings
        close_matches = get_close_matches(team, fifa_teams, n=3, cutoff=0.6)
        print(f"   {team}")
        if close_matches:
            print(f"      → Possible matches: {', '.join(close_matches)}")
            discrepancies.append({
                'fixture_name': team,
                'fifa_matches': close_matches
            })
        else:
            print(f"      → No close matches found")
            discrepancies.append({
                'fixture_name': team,
                'fifa_matches': []
            })
    
    print(f"\n❌ TEAMS IN FIFA RANKINGS BUT NOT IN FIXTURES ({len(missing_from_fixtures)}):")
    print("-" * 55)
    
    uefa_teams_in_fifa = []
    for team in sorted(missing_from_fixtures):
        # Check if this might be a UEFA team
        uefa_keywords = [
            'czech', 'czechia', 'republic', 'ireland', 'macedonia', 'bosnia',
            'herzegovina', 'san marino', 'north', 'northern', 'faroe'
        ]
        
        team_lower = team.lower()
        might_be_uefa = any(keyword in team_lower for keyword in uefa_keywords)
        
        if might_be_uefa:
            print(f"   {team} ⚠️  (might be UEFA)")
            uefa_teams_in_fifa.append(team)
        else:
            print(f"   {team}")
    
    # Check for exact code matches
    print(f"\n🔍 CHECKING CODES:")
    print("-" * 20)
    
    fixture_codes = set()
    fifa_codes = set()
    
    for fixture in fixtures.values():
        home_code = fixture.get('home_code')
        away_code = fixture.get('away_code')
        if home_code:
            fixture_codes.add(home_code)
        if away_code:
            fixture_codes.add(away_code)
    
    for team_data in fifa_rankings.values():
        if isinstance(team_data, dict) and 'code' in team_data:
            fifa_codes.add(team_data['code'])
    
    code_discrepancies = fixture_codes - fifa_codes
    
    print(f"Fixture codes not in FIFA: {len(code_discrepancies)}")
    if code_discrepancies:
        print(f"   {', '.join(sorted(code_discrepancies))}")
    
    # Suggest corrections
    print(f"\n🔧 SUGGESTED NAME CORRECTIONS:")
    print("-" * 35)
    
    corrections = {}
    for disc in discrepancies:
        fixture_name = disc['fixture_name']
        fifa_matches = disc['fifa_matches']
        
        if fifa_matches:
            # Pick the best match
            best_match = fifa_matches[0]
            corrections[fixture_name] = best_match
            print(f"   {fixture_name} → {best_match}")
    
    # Check specific known cases
    known_discrepancies = {
        'Czech Republic': 'Czechia',
        'Republic of Ireland': 'Republic of Ireland',
        'North Macedonia': 'North Macedonia',
        'Bosnia and Herzegovina': 'Bosnia and Herzegovina',
        'Northern Ireland': 'Northern Ireland'
    }
    
    print(f"\n🔍 CHECKING PREVIOUSLY PROBLEMATIC TEAMS:")
    print("-" * 45)
    
    actual_discrepancies = []
    for fixture_name, expected_fifa in known_discrepancies.items():
        if fixture_name in fixture_teams:
            if expected_fifa in fifa_teams:
                print(f"   ✅ Confirmed: {fixture_name} matches {expected_fifa}")
            else:
                actual_discrepancies.append((fixture_name, expected_fifa))
                print(f"   ❌ Problem: Expected '{expected_fifa}' not found in FIFA data")
        else:
            print(f"   ℹ️  Note: '{fixture_name}' not in current fixtures")
    
    return {
        'discrepancies': discrepancies,
        'corrections': corrections,
        'missing_from_fifa': len(missing_from_fifa),
        'missing_from_fixtures': len(missing_from_fixtures),
        'actual_discrepancies': actual_discrepancies
    }

def main():
    """Main analysis function"""
    fixtures, fifa_rankings = load_data()
    
    if not fixtures or not fifa_rankings:
        return
    
    results = check_team_name_discrepancies(fixtures, fifa_rankings)
    
    print(f"\n🏆 FINAL ALIGNMENT STATUS:")
    print("-" * 30)
    print(f"Teams in fixtures not in FIFA: {results['missing_from_fifa']}")
    print(f"Teams in FIFA not in fixtures: {results['missing_from_fixtures']}")
    print(f"Actual discrepancies found: {len(results['actual_discrepancies'])}")
    
    if results['missing_from_fifa'] == 0 and len(results['actual_discrepancies']) == 0:
        print("🎉✅ PERFECT ALIGNMENT! All fixture teams perfectly match FIFA rankings!")
    else:
        print("❌ Alignment issues found that need correction")

if __name__ == "__main__":
    main()