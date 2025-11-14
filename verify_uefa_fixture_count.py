#!/usr/bin/env python3
"""
UEFA Teams Fixture Count Verification
Confirm that all UEFA teams (except Russia) have exactly 2 games
"""

import json
from collections import defaultdict

def load_data():
    """Load fixtures and FIFA rankings"""
    # Load fixtures
    try:
        with open('uefa_fixtures_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            fixtures = data.get('fixtures', {})
        print(f"✅ Loaded {len(fixtures)} fixtures")
    except FileNotFoundError:
        print("❌ UEFA fixtures data not found")
        return {}, {}
    
    # Load FIFA rankings
    try:
        with open('fifa_rankings_from_excel.json', 'r', encoding='utf-8') as f:
            rankings_data = json.load(f)
            if 'rankings' in rankings_data:
                rankings_list = rankings_data['rankings']
                fifa_rankings = {team['code']: team for team in rankings_list}
            else:
                fifa_rankings = rankings_data
        print(f"✅ Loaded {len(fifa_rankings)} FIFA team rankings")
    except FileNotFoundError:
        print("❌ FIFA rankings file not found")
        return fixtures, {}
    
    return fixtures, fifa_rankings

def get_uefa_teams():
    """Get list of all UEFA team codes"""
    # Comprehensive list of UEFA member associations (55 total, excluding Russia)
    uefa_teams = {
        'ALB', 'AND', 'ARM', 'AUT', 'AZE', 'BLR', 'BEL', 'BOS', 'BUL', 'CRO',
        'CYP', 'CZE', 'DEN', 'ENG', 'EST', 'FAR', 'FIN', 'FRA', 'GEO', 'GER',
        'GIB', 'GRE', 'HUN', 'ICE', 'IRL', 'ISR', 'ITA', 'KAZ', 'KOS', 'LAT',
        'LIE', 'LIT', 'LUX', 'MLT', 'MDA', 'MNE', 'NET', 'MKD', 'NOR', 'POL',
        'POR', 'ROU', 'SAN', 'SCO', 'SRB', 'SVK', 'SVN', 'ESP', 'SWE', 'SUI',
        'TUR', 'UKR', 'WAL', 'NIR', 'REP'
    }
    
    # Alternative codes that might be used
    alternative_codes = {
        'SPA': 'ESP', 'NET': 'NED', 'SWI': 'SUI', 'GRE': 'GRC', 'CZE': 'CZR',
        'SLO': 'SVN', 'SER': 'SRB', 'BOS': 'BIH', 'ROM': 'ROU', 'MOL': 'MDA',
        'REP': 'IRL', 'NOR': 'NIR'
    }
    
    return uefa_teams, alternative_codes

def get_team_code_mapping():
    """Create mapping from team names to codes for teams with missing codes"""
    return {
        'Greece': 'GRE',
        'Belarus': 'BLR', 
        'Slovakia': 'SVK',
        'Turkey': 'TUR',
        'Malta': 'MLT',
        'Austria': 'AUT',
        'Norway': 'NOR',
        'Belgium': 'BEL',
        'North Macedonia': 'MKD',
        'Montenegro': 'MNE',
        'Czech Republic': 'CZE',
        'Northern Ireland': 'NIR',
        'Republic of Ireland': 'REP',
        'Bosnia and Herzegovina': 'BOS',
        'San Marino': 'SAN',
        'Faroe Islands': 'FAR',
        'Liechtenstein': 'LIE'
    }

def analyze_team_fixtures(fixtures, fifa_rankings):
    """Analyze fixture count for each team"""
    team_fixtures = defaultdict(list)
    name_to_code = get_team_code_mapping()
    uefa_teams, alt_codes = get_uefa_teams()
    
    print("🔍 ANALYZING TEAM FIXTURE COUNTS")
    print("=" * 50)
    
    # Count fixtures for each team
    for fixture_id, fixture in fixtures.items():
        home_code = fixture.get('home_code')
        away_code = fixture.get('away_code')
        home_team = fixture.get('home_team', '')
        away_team = fixture.get('away_team', '')
        
        # Use manual mapping if code is missing
        if not home_code and home_team in name_to_code:
            home_code = name_to_code[home_team]
        if not away_code and away_team in name_to_code:
            away_code = name_to_code[away_team]
        
        # Add fixtures for each team
        if home_code:
            team_fixtures[home_code].append({
                'fixture_id': fixture_id,
                'opponent': away_team or away_code,
                'venue': 'H',
                'date': fixture['date']
            })
        
        if away_code:
            team_fixtures[away_code].append({
                'fixture_id': fixture_id,
                'opponent': home_team or home_code,
                'venue': 'A', 
                'date': fixture['date']
            })
    
    # Identify UEFA teams in the fixtures
    uefa_teams_in_fixtures = set()
    for team_code in team_fixtures.keys():
        # Check if team is UEFA (including alternative codes)
        if (team_code in uefa_teams or 
            team_code in alt_codes or
            team_code in fifa_rankings):
            uefa_teams_in_fixtures.add(team_code)
    
    print(f"📊 Found {len(uefa_teams_in_fixtures)} UEFA teams with fixtures")
    print(f"📋 Total UEFA teams expected: ~54 (excluding Russia)")
    
    # Analyze fixture counts
    teams_with_0_games = []
    teams_with_1_game = []
    teams_with_2_games = []
    teams_with_3plus_games = []
    
    # Check all possible UEFA teams
    all_possible_codes = uefa_teams.union(set(alt_codes.keys())).union(set(name_to_code.values()))
    
    for team_code in all_possible_codes:
        fixture_count = len(team_fixtures.get(team_code, []))
        
        if fixture_count == 0:
            teams_with_0_games.append(team_code)
        elif fixture_count == 1:
            teams_with_1_game.append(team_code)
        elif fixture_count == 2:
            teams_with_2_games.append(team_code)
        else:
            teams_with_3plus_games.append(team_code)
    
    # Display results
    print(f"\n📈 FIXTURE COUNT ANALYSIS:")
    print("-" * 30)
    print(f"✅ Teams with exactly 2 games: {len(teams_with_2_games)}")
    print(f"⚠️  Teams with 1 game: {len(teams_with_1_game)}")
    print(f"🔄 Teams with 3+ games: {len(teams_with_3plus_games)}")
    print(f"❌ Teams with 0 games: {len(teams_with_0_games)}")
    
    if teams_with_1_game:
        print(f"\n⚠️  TEAMS WITH ONLY 1 GAME:")
        for team_code in sorted(teams_with_1_game):
            team_name = fifa_rankings.get(team_code, {}).get('team', team_code)
            fixture = team_fixtures[team_code][0]
            print(f"   {team_code:<4} {team_name:<20} vs {fixture['opponent']} ({fixture['venue']}) on {fixture['date']}")
    
    if teams_with_3plus_games:
        print(f"\n🔄 TEAMS WITH 3+ GAMES:")
        for team_code in sorted(teams_with_3plus_games):
            team_name = fifa_rankings.get(team_code, {}).get('team', team_code)
            fixture_count = len(team_fixtures[team_code])
            print(f"   {team_code:<4} {team_name:<20} has {fixture_count} games")
            for i, fixture in enumerate(team_fixtures[team_code][:4]):  # Show first 4
                print(f"        Game {i+1}: vs {fixture['opponent']} ({fixture['venue']}) on {fixture['date']}")
    
    if teams_with_0_games:
        print(f"\n❌ TEAMS WITH NO GAMES (may not be in fixtures or use different codes):")
        missing_teams = []
        for team_code in sorted(teams_with_0_games):
            if team_code in fifa_rankings:
                team_name = fifa_rankings[team_code]['team']
                missing_teams.append(f"{team_code} ({team_name})")
            else:
                missing_teams.append(team_code)
        
        # Show in groups of 5
        for i in range(0, len(missing_teams), 5):
            group = missing_teams[i:i+5]
            print(f"   {', '.join(group)}")
    
    # Verify teams with exactly 2 games
    print(f"\n✅ TEAMS WITH EXACTLY 2 GAMES ({len(teams_with_2_games)} teams):")
    print("-" * 55)
    
    teams_with_2_sorted = []
    for team_code in teams_with_2_games:
        if team_code in fifa_rankings:
            team_data = fifa_rankings[team_code]
            teams_with_2_sorted.append({
                'code': team_code,
                'name': team_data['team'],
                'rank': team_data['rank']
            })
    
    teams_with_2_sorted.sort(key=lambda x: x['rank'])
    
    for team in teams_with_2_sorted[:20]:  # Show top 20
        fixtures = team_fixtures[team['code']]
        fixture1 = fixtures[0]
        fixture2 = fixtures[1]
        print(f"#{team['rank']:2d} {team['name']:<18} vs {fixture1['opponent'][:12]}({fixture1['venue']}), {fixture2['opponent'][:12]}({fixture2['venue']})")
    
    if len(teams_with_2_sorted) > 20:
        print(f"   ... and {len(teams_with_2_sorted) - 20} more teams")
    
    # Summary
    print(f"\n🏆 VERIFICATION SUMMARY:")
    print("-" * 25)
    print(f"UEFA teams with exactly 2 games: {len(teams_with_2_games)}")
    print(f"UEFA teams with incorrect count: {len(teams_with_1_game) + len(teams_with_3plus_games)}")
    
    if len(teams_with_1_game) + len(teams_with_3plus_games) == 0:
        print("✅ CONFIRMED: All UEFA teams in fixtures have exactly 2 games!")
    else:
        print("❌ ISSUE: Some UEFA teams do not have exactly 2 games")
    
    return {
        'teams_with_2_games': len(teams_with_2_games),
        'teams_with_1_game': len(teams_with_1_game),
        'teams_with_3plus_games': len(teams_with_3plus_games),
        'teams_with_0_games': len(teams_with_0_games),
        'all_correct': len(teams_with_1_game) + len(teams_with_3plus_games) == 0
    }

def main():
    fixtures, fifa_rankings = load_data()
    
    if not fixtures:
        return
    
    results = analyze_team_fixtures(fixtures, fifa_rankings)
    
    print(f"\n📋 FINAL ANSWER:")
    if results['all_correct']:
        print("✅ YES - All UEFA teams in the fixtures have exactly 2 games")
    else:
        print("❌ NO - Some UEFA teams do not have exactly 2 games")
        print(f"   Teams with 1 game: {results['teams_with_1_game']}")
        print(f"   Teams with 3+ games: {results['teams_with_3plus_games']}")

if __name__ == "__main__":
    main()