#!/usr/bin/env python3
"""
Analyze point ranges for teams playing friendlies vs World Cup Qualifiers
"""

import json
from collections import defaultdict

def load_data():
    """Load fixtures and FIFA rankings"""
    with open('uefa_fixtures_data.json', 'r', encoding='utf-8') as f:
        fixtures_data = json.load(f)
        fixtures = fixtures_data.get('fixtures', {})
    
    with open('fifa_rankings_from_excel.json', 'r', encoding='utf-8') as f:
        fifa_data = json.load(f)
        fifa_by_name = {team['team']: team for team in fifa_data['rankings']}
    
    return fixtures, fifa_by_name

def calculate_expected_result(home_points, away_points, home_advantage=100):
    """Calculate expected result using FIFA Elo formula"""
    rating_diff = (home_points + home_advantage) - away_points
    expected_home = 1 / (10**(-rating_diff/600) + 1)
    return expected_home

def calculate_rating_change(team_points, opponent_points, actual_result, is_home=True, importance=25):
    """Calculate rating change with specified importance coefficient"""
    home_advantage = 100 if is_home else 0
    expected = calculate_expected_result(
        team_points + home_advantage if is_home else opponent_points + (100 if not is_home else 0),
        opponent_points if is_home else team_points
    )
    
    if not is_home:
        expected = 1 - expected
    
    change = importance * (actual_result - expected)
    return change

def analyze_team_competition_types(fixtures, fifa_by_name):
    """Categorize teams by competition types they play"""
    
    # Find teams in friendlies vs WCQ
    teams_friendlies = set()
    teams_wcq = set()
    team_fixtures = defaultdict(list)
    
    for fixture_id, fixture in fixtures.items():
        competition = fixture.get('competition', '')
        importance = fixture.get('importance', 25)
        home_team = fixture.get('home_team')
        away_team = fixture.get('away_team')
        
        # Track team fixtures
        if home_team:
            team_fixtures[home_team].append({
                'fixture': fixture,
                'is_home': True,
                'opponent': away_team,
                'competition': competition,
                'importance': importance
            })
        
        if away_team:
            team_fixtures[away_team].append({
                'fixture': fixture,
                'is_home': False,
                'opponent': home_team,
                'competition': competition,
                'importance': importance
            })
        
        # Categorize teams
        if competition == 'Friendlies':
            teams_friendlies.add(home_team)
            teams_friendlies.add(away_team)
        else:
            teams_wcq.add(home_team)
            teams_wcq.add(away_team)
    
    return teams_friendlies, teams_wcq, team_fixtures

def calculate_team_range_with_importance(team_name, team_fixtures_list, fifa_by_name):
    """Calculate team range considering actual importance coefficients"""
    
    team_data = fifa_by_name.get(team_name)
    if not team_data or len(team_fixtures_list) != 2:
        return None
    
    initial_points = team_data['points']
    
    fixture1 = team_fixtures_list[0]
    fixture2 = team_fixtures_list[1]
    
    opp1_data = fifa_by_name.get(fixture1['opponent'])
    opp2_data = fifa_by_name.get(fixture2['opponent'])
    
    if not opp1_data or not opp2_data:
        return None
    
    importance1 = fixture1['importance']
    importance2 = fixture2['importance']
    
    opp1_initial_points = opp1_data['points']
    opp2_initial_points = opp2_data['points']
    
    # Best case - win both games
    best_change_1 = calculate_rating_change(
        initial_points, opp1_initial_points, 1.0, fixture1['is_home'], importance1
    )
    best_points_after_1 = initial_points + best_change_1
    
    # Opponent 1's change after losing
    opp1_change_1 = calculate_rating_change(
        opp1_initial_points, initial_points, 0.0, not fixture1['is_home'], importance1
    )
    opp1_points_after_1 = opp1_initial_points + opp1_change_1
    
    # Game 2 - consider if same opponent
    opp2_points_for_game2 = opp1_points_after_1 if fixture1['opponent'] == fixture2['opponent'] else opp2_initial_points
    
    best_change_2 = calculate_rating_change(
        best_points_after_1, opp2_points_for_game2, 1.0, fixture2['is_home'], importance2
    )
    best_final_points = best_points_after_1 + best_change_2
    
    # Worst case - lose both games
    worst_change_1 = calculate_rating_change(
        initial_points, opp1_initial_points, 0.0, fixture1['is_home'], importance1
    )
    worst_points_after_1 = initial_points + worst_change_1
    
    # Opponent 1's change after winning
    opp1_change_1_win = calculate_rating_change(
        opp1_initial_points, initial_points, 1.0, not fixture1['is_home'], importance1
    )
    opp1_points_after_1_win = opp1_initial_points + opp1_change_1_win
    
    # Game 2 worst case
    opp2_points_for_game2_worst = opp1_points_after_1_win if fixture1['opponent'] == fixture2['opponent'] else opp2_initial_points
    
    worst_change_2 = calculate_rating_change(
        worst_points_after_1, opp2_points_for_game2_worst, 0.0, fixture2['is_home'], importance2
    )
    worst_final_points = worst_points_after_1 + worst_change_2
    
    return {
        'team_name': team_name,
        'team_code': team_data['code'],
        'current_rank': team_data['rank'],
        'initial_points': initial_points,
        'best_points': best_final_points,
        'worst_points': worst_final_points,
        'range': best_final_points - worst_final_points,
        'best_change': best_final_points - initial_points,
        'worst_change': worst_final_points - initial_points,
        'competition1': fixture1['competition'],
        'competition2': fixture2['competition'],
        'importance1': importance1,
        'importance2': importance2,
        'both_friendlies': importance1 == 10 and importance2 == 10,
        'both_wcq': importance1 == 25 and importance2 == 25,
        'mixed': importance1 != importance2
    }

def main():
    fixtures, fifa_by_name = load_data()
    
    teams_friendlies, teams_wcq, team_fixtures = analyze_team_competition_types(fixtures, fifa_by_name)
    
    print("🏆 COMPETITION TYPE ANALYSIS")
    print("=" * 50)
    print(f"Teams playing friendlies: {len(teams_friendlies)}")
    print(f"Teams playing WCQ only: {len(teams_wcq - teams_friendlies)}")
    print(f"Teams playing both: {len(teams_friendlies & teams_wcq)}")
    
    # Analyze ranges for different competition types
    friendly_results = []
    wcq_results = []
    mixed_results = []
    
    for team_name, fixtures_list in team_fixtures.items():
        if len(fixtures_list) == 2:
            result = calculate_team_range_with_importance(team_name, fixtures_list, fifa_by_name)
            if result:
                if result['both_friendlies']:
                    friendly_results.append(result)
                elif result['both_wcq']:
                    wcq_results.append(result)
                else:
                    mixed_results.append(result)
    
    # Display results
    print(f"\n📊 TEAMS PLAYING ONLY FRIENDLIES ({len(friendly_results)} teams)")
    print("=" * 70)
    print(f"{'Rank':<4} {'Team':<20} {'Current':<8} {'Range':<8} {'Competitions':<15}")
    print("-" * 70)
    
    friendly_results.sort(key=lambda x: x['current_rank'])
    for result in friendly_results:
        print(f"{result['current_rank']:<4} {result['team_name']:<20} "
              f"{result['initial_points']:<8.1f} {result['range']:<8.1f} "
              f"Friendlies (×{result['importance1']})")
    
    print(f"\n📊 TEAMS PLAYING ONLY WORLD CUP QUALIFIERS ({len(wcq_results)} teams)")
    print("=" * 70)
    print(f"{'Rank':<4} {'Team':<20} {'Current':<8} {'Range':<8} {'Competitions':<15}")
    print("-" * 70)
    
    wcq_results.sort(key=lambda x: x['current_rank'])
    for result in wcq_results[:10]:  # Show first 10
        print(f"{result['current_rank']:<4} {result['team_name']:<20} "
              f"{result['initial_points']:<8.1f} {result['range']:<8.1f} "
              f"WCQ (×{result['importance1']})")
    
    if len(wcq_results) > 10:
        print(f"... and {len(wcq_results) - 10} more WCQ teams")
    
    print(f"\n📊 TEAMS PLAYING MIXED COMPETITIONS ({len(mixed_results)} teams)")
    print("=" * 70)
    print(f"{'Rank':<4} {'Team':<20} {'Current':<8} {'Range':<8} {'Competitions':<15}")
    print("-" * 70)
    
    mixed_results.sort(key=lambda x: x['current_rank'])
    for result in mixed_results:
        comp_info = f"×{result['importance1']}/×{result['importance2']}"
        print(f"{result['current_rank']:<4} {result['team_name']:<20} "
              f"{result['initial_points']:<8.1f} {result['range']:<8.1f} "
              f"{comp_info}")
    
    # Statistics
    friendly_avg_range = sum(r['range'] for r in friendly_results) / len(friendly_results) if friendly_results else 0
    wcq_avg_range = sum(r['range'] for r in wcq_results) / len(wcq_results) if wcq_results else 0
    mixed_avg_range = sum(r['range'] for r in mixed_results) / len(mixed_results) if mixed_results else 0
    
    print(f"\n📈 RANGE STATISTICS COMPARISON")
    print("=" * 40)
    print(f"Friendlies only (×10): {friendly_avg_range:.1f} points average range")
    print(f"WCQ only (×25):        {wcq_avg_range:.1f} points average range")
    print(f"Mixed competitions:    {mixed_avg_range:.1f} points average range")
    print(f"\nRatio (WCQ/Friendlies): {wcq_avg_range/friendly_avg_range:.2f}x" if friendly_avg_range > 0 else "")
    print(f"Expected ratio (25/10): 2.50x")
    
    return friendly_results, wcq_results, mixed_results

if __name__ == "__main__":
    friendly_teams, wcq_teams, mixed_teams = main()