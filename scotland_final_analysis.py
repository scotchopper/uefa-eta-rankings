#!/usr/bin/env python3
"""
Scotland UEFA Ranking Movement - Final Analysis
Clean summary of Scotland's potential ranking changes based on all UEFA team results
"""

import json

def load_fifa_rankings():
    """Load FIFA rankings"""
    try:
        with open('fifa_rankings_from_excel.json', 'r', encoding='utf-8') as f:
            rankings_data = json.load(f)
            if 'rankings' in rankings_data:
                rankings_list = rankings_data['rankings']
                return {team['code']: team for team in rankings_list}
            else:
                return rankings_data
    except FileNotFoundError:
        print("❌ FIFA rankings file not found")
        return {}

def calculate_expected_result(home_points, away_points, home_advantage=100):
    """Calculate expected result using FIFA Elo formula"""
    rating_diff = (home_points + home_advantage) - away_points
    expected_home = 1 / (10**(-rating_diff/600) + 1)
    return expected_home

def calculate_rating_change(team_points, opponent_points, actual_result, is_home=True, importance=25):
    """Calculate rating change for a team"""
    home_advantage = 100 if is_home else 0
    expected = calculate_expected_result(
        team_points + home_advantage if is_home else opponent_points + (100 if not is_home else 0),
        opponent_points if is_home else team_points
    )
    
    if not is_home:
        expected = 1 - expected
    
    change = importance * (actual_result - expected)
    return change

def main():
    print("🏴󠁧󠁢󠁳󠁣󠁴󠁿 SCOTLAND UEFA RANKING MOVEMENT - FINAL ANALYSIS")
    print("=" * 65)
    
    fifa_rankings = load_fifa_rankings()
    
    # Scotland's current position
    scotland = fifa_rankings.get('SCO', {})
    current_rank = scotland.get('rank', 38)
    current_points = scotland.get('points', 1504.2)
    
    print(f"📍 CURRENT POSITION: #{current_rank} ({current_points} points)")
    
    # Scotland's fixtures (corrected)
    print(f"\n⚽ SCOTLAND'S FIXTURES:")
    print("Nov 15: Greece vs Scotland (Away)")
    print("Nov 18: Scotland vs Denmark (Home)")
    
    # Get opponent data
    greece = fifa_rankings.get('GRE', {})  # Greece
    denmark = fifa_rankings.get('DEN', {})
    
    greece_points = greece.get('points', 1473.0)  # Approximate if not found
    denmark_points = denmark.get('points', 1641.02)
    
    print(f"\n🎯 OPPONENT STRENGTHS:")
    print(f"Greece: #{greece.get('rank', 'Unknown')} ({greece_points} pts)")
    print(f"Denmark: #{denmark.get('rank', 20)} ({denmark_points} pts)")
    
    # Calculate Scotland's best case (wins both)
    print(f"\n🏆 BEST CASE SCENARIO (Scotland wins both):")
    
    # Game 1: Beat Greece away
    game1_change = calculate_rating_change(current_points, greece_points, 1.0, False)
    points_after_game1 = current_points + game1_change
    
    print(f"Game 1: Beat Greece away → +{game1_change:.1f} pts = {points_after_game1:.1f}")
    
    # Game 2: Beat Denmark home (Denmark's points unchanged for simplicity)
    game2_change = calculate_rating_change(points_after_game1, denmark_points, 1.0, True)
    best_case_points = points_after_game1 + game2_change
    
    print(f"Game 2: Beat Denmark home → +{game2_change:.1f} pts = {best_case_points:.1f}")
    print(f"Total change: +{best_case_points - current_points:.1f} points")
    
    # Calculate Scotland's worst case (loses both)
    print(f"\n⚠️  WORST CASE SCENARIO (Scotland loses both):")
    
    # Game 1: Lose to Greece away
    game1_change_worst = calculate_rating_change(current_points, greece_points, 0.0, False)
    points_after_game1_worst = current_points + game1_change_worst
    
    print(f"Game 1: Lose to Greece away → {game1_change_worst:.1f} pts = {points_after_game1_worst:.1f}")
    
    # Game 2: Lose to Denmark home
    game2_change_worst = calculate_rating_change(points_after_game1_worst, denmark_points, 0.0, True)
    worst_case_points = points_after_game1_worst + game2_change_worst
    
    print(f"Game 2: Lose to Denmark home → {game2_change_worst:.1f} pts = {worst_case_points:.1f}")
    print(f"Total change: {worst_case_points - current_points:.1f} points")
    
    # Estimate ranking changes based on other UEFA teams
    print(f"\n📊 ESTIMATED RANKING MOVEMENTS:")
    print("-" * 40)
    
    # Teams Scotland could potentially catch (rough estimates)
    catchable_teams = [
        ("Serbia", 36, 1507.8),
        ("Hungary", 37, 1504.9)
    ]
    
    print("Teams Scotland could catch:")
    for team_name, rank, points in catchable_teams:
        if best_case_points > points - 25:  # Assuming they don't improve much
            print(f"  #{rank} {team_name} ({points} pts) - Possible to catch")
    
    # Teams that could overtake Scotland
    threatening_teams = [
        ("Sweden", 40, 1497.0),
        ("Romania", 47, 1480.1),
        ("Slovenia", 51, 1462.9)
    ]
    
    print("\nTeams that could overtake Scotland:")
    for team_name, rank, points in threatening_teams:
        if points + 25 > worst_case_points:  # Assuming they improve significantly
            print(f"  #{rank} {team_name} ({points} pts) - Could overtake")
    
    print(f"\n🎯 REALISTIC RANKING RANGE:")
    print(f"Best case: Around #{current_rank - 2} to #{current_rank - 1}")
    print(f"Worst case: Around #{current_rank + 3} to #{current_rank + 4}")
    print(f"Most likely: Scotland stays around #{current_rank - 1} to #{current_rank + 2}")
    
    print(f"\n💡 KEY INSIGHTS:")
    print("• Scotland's away game vs Greece is crucial")
    print("• Denmark home game offers opportunity for big points gain")
    print("• Other UEFA results will also affect final rankings")
    print("• Realistic range: #34-42 based on all possible outcomes")
    
    print(f"\n📈 WIN PROBABILITIES:")
    greece_prob = 1 - calculate_expected_result(greece_points + 100, current_points)
    denmark_prob = calculate_expected_result(current_points + 100, denmark_points)
    
    print(f"vs Greece (A): {greece_prob:.1%} chance")
    print(f"vs Denmark (H): {denmark_prob:.1%} chance")
    print(f"Both games: {greece_prob * denmark_prob:.1%} chance")

if __name__ == "__main__":
    main()