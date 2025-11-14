#!/usr/bin/env python3
"""
Comprehensive UEFA Fixture Data Validation
Check for wrong codes, missing countries, and data inconsistencies
"""

import json
from collections import defaultdict, Counter

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

def get_complete_uefa_list():
    """Get complete list of 54 UEFA member associations (excluding Russia)"""
    # Complete UEFA member list (55 total, minus Russia = 54)
    uefa_countries = {
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
        # Note: Russia excluded due to suspension
    }
    
    return uefa_countries

def analyze_fixture_data(fixtures, fifa_rankings):
    """Comprehensive analysis of fixture data"""
    print("🔍 COMPREHENSIVE UEFA FIXTURE DATA VALIDATION")
    print("=" * 60)
    
    uefa_countries = get_complete_uefa_list()
    
    # Collect all teams and codes from fixtures
    teams_in_fixtures = set()
    codes_in_fixtures = set()
    null_codes = []
    wrong_codes = []
    team_to_code_mapping = {}
    
    print("🔍 ANALYZING FIXTURE DATA:")
    print("-" * 30)
    
    for fixture_id, fixture in fixtures.items():
        home_team = fixture.get('home_team', '')
        away_team = fixture.get('away_team', '')
        home_code = fixture.get('home_code')
        away_code = fixture.get('away_code')
        
        teams_in_fixtures.add(home_team)
        teams_in_fixtures.add(away_team)
        
        # Check for null codes
        if home_code is None:
            null_codes.append(f"{fixture_id}: {home_team} (home)")
        else:
            codes_in_fixtures.add(home_code)
            team_to_code_mapping[home_team] = home_code
            
        if away_code is None:
            null_codes.append(f"{fixture_id}: {away_team} (away)")
        else:
            codes_in_fixtures.add(away_code)
            team_to_code_mapping[away_team] = away_code
    
    print(f"📊 Teams found in fixtures: {len(teams_in_fixtures)}")
    print(f"📊 Codes found in fixtures: {len(codes_in_fixtures)}")
    print(f"⚠️  Null codes found: {len(null_codes)}")
    
    # Check for code conflicts
    print(f"\n❌ NULL CODES ({len(null_codes)} instances):")
    print("-" * 25)
    if null_codes:
        for null_code in null_codes[:10]:  # Show first 10
            print(f"   {null_code}")
        if len(null_codes) > 10:
            print(f"   ... and {len(null_codes) - 10} more")
    
    # Check for duplicate codes (same code for different teams)
    code_to_teams = defaultdict(set)
    for team, code in team_to_code_mapping.items():
        code_to_teams[code].add(team)
    
    duplicate_codes = {code: teams for code, teams in code_to_teams.items() if len(teams) > 1}
    
    print(f"\n🔄 DUPLICATE CODES ({len(duplicate_codes)} conflicts):")
    print("-" * 25)
    for code, teams in duplicate_codes.items():
        print(f"   {code}: {', '.join(teams)}")
    
    # Check for wrong codes (codes that don't match expected UEFA codes)
    expected_codes = set(uefa_countries.values())
    unexpected_codes = codes_in_fixtures - expected_codes
    
    print(f"\n❓ UNEXPECTED CODES ({len(unexpected_codes)} codes):")
    print("-" * 25)
    for code in sorted(unexpected_codes):
        teams_using_code = [team for team, team_code in team_to_code_mapping.items() if team_code == code]
        print(f"   {code}: {', '.join(teams_using_code)}")
    
    # Find missing UEFA countries
    teams_normalized = {team.lower().strip() for team in teams_in_fixtures}
    missing_countries = []
    
    for country, expected_code in uefa_countries.items():
        country_variations = [
            country.lower(),
            country.replace(' ', '').lower(),
            country.replace(' ', ' ').lower()
        ]
        
        found = False
        for variation in country_variations:
            if any(variation in team_name for team_name in teams_normalized):
                found = True
                break
        
        if not found:
            missing_countries.append(country)
    
    print(f"\n❌ MISSING UEFA COUNTRIES ({len(missing_countries)} missing):")
    print("-" * 35)
    for country in missing_countries:
        expected_code = uefa_countries[country]
        print(f"   {country} ({expected_code})")
    
    # Teams in fixtures that might not be UEFA
    non_uefa_teams = []
    for team in teams_in_fixtures:
        if team and not any(
            team.lower() in country.lower() or country.lower() in team.lower() 
            for country in uefa_countries.keys()
        ):
            non_uefa_teams.append(team)
    
    if non_uefa_teams:
        print(f"\n⚠️  POSSIBLY NON-UEFA TEAMS:")
        print("-" * 25)
        for team in sorted(non_uefa_teams):
            print(f"   {team}")
    
    # Suggest corrections
    print(f"\n🔧 SUGGESTED CORRECTIONS:")
    print("-" * 25)
    
    corrections = {
        'Greece': 'GRE',
        'Belarus': 'BLR',
        'Slovakia': 'SVK', 
        'Turkey': 'TUR',
        'Malta': 'MLT',
        'Austria': 'AUT',
        'Norway': 'NOR',  # Keep NOR for Norway
        'Northern Ireland': 'NIR',  # Change Northern Ireland to NIR
        'Belgium': 'BEL',
        'North Macedonia': 'MKD',
        'Montenegro': 'MNE',
        'Czech Republic': 'CZE',
        'Netherlands': 'NED',  # Change NET to NED
        'Switzerland': 'SUI',  # Change SWI to SUI
        'Spain': 'ESP',  # Change SPA to ESP
        'Republic of Ireland': 'IRL',  # Change REP to IRL
        'Romania': 'ROU',  # Change ROM to ROU
        'Moldova': 'MDA',  # Change MOL to MDA
        'Bosnia and Herzegovina': 'BIH',  # Change BOS to BIH
        'Serbia': 'SRB',  # Change SER to SRB
        'Slovenia': 'SVN',  # Change SLO to SVN
        'San Marino': 'SMR',  # Change SAN to SMR
        'Bulgaria': 'BUL'
    }
    
    for team in teams_in_fixtures:
        if team in corrections:
            current_code = team_to_code_mapping.get(team, 'None')
            suggested_code = corrections[team]
            if current_code != suggested_code:
                print(f"   {team}: {current_code} → {suggested_code}")
    
    # Count fixture summary
    print(f"\n📊 FIXTURE COUNT SUMMARY:")
    print("-" * 25)
    
    team_fixture_count = defaultdict(int)
    for fixture_id, fixture in fixtures.items():
        home_team = fixture.get('home_team', '')
        away_team = fixture.get('away_team', '')
        if home_team:
            team_fixture_count[home_team] += 1
        if away_team:
            team_fixture_count[away_team] += 1
    
    fixture_distribution = Counter(team_fixture_count.values())
    
    for count, num_teams in sorted(fixture_distribution.items()):
        print(f"   {num_teams} teams have {count} fixture(s)")
    
    # Show teams with != 2 fixtures
    irregular_teams = [team for team, count in team_fixture_count.items() if count != 2]
    if irregular_teams:
        print(f"\n⚠️  TEAMS WITHOUT EXACTLY 2 FIXTURES:")
        print("-" * 35)
        for team in sorted(irregular_teams):
            count = team_fixture_count[team]
            print(f"   {team}: {count} fixture(s)")
    
    return {
        'total_teams': len(teams_in_fixtures),
        'null_codes': len(null_codes),
        'duplicate_codes': len(duplicate_codes),
        'unexpected_codes': len(unexpected_codes),
        'missing_countries': len(missing_countries),
        'irregular_fixture_teams': len(irregular_teams)
    }

def main():
    fixtures, fifa_rankings = load_data()
    
    if not fixtures:
        return
    
    results = analyze_fixture_data(fixtures, fifa_rankings)
    
    print(f"\n🏆 VALIDATION SUMMARY:")
    print("-" * 25)
    print(f"Total teams in fixtures: {results['total_teams']}")
    print(f"Expected UEFA teams: 54")
    print(f"Missing countries: {results['missing_countries']}")
    print(f"Teams with null codes: {results['null_codes']}")
    print(f"Code conflicts: {results['duplicate_codes']}")
    print(f"Unexpected codes: {results['unexpected_codes']}")
    print(f"Teams with irregular fixtures: {results['irregular_fixture_teams']}")
    
    if (results['null_codes'] == 0 and results['duplicate_codes'] == 0 and 
        results['unexpected_codes'] == 0 and results['missing_countries'] == 0 and
        results['irregular_fixture_teams'] == 0):
        print("✅ All validation checks passed!")
    else:
        print("❌ Issues found that need correction")

if __name__ == "__main__":
    main()