#!/usr/bin/env python3
"""
UEFA Teams Best/Worst Case Analysis
Calculate highest and lowest possible points for each team after their 2 games
"""

import json
from collections import defaultdict

class TeamRangeAnalyzer:
    def __init__(self):
        self.fixtures = {}
        self.fifa_rankings = {}
        self.load_data()
        self.importance_coefficient = 25
        
        # Manual mapping for teams with missing codes
        self.team_name_to_code = {
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
            'Czech Republic': 'CZE'
        }
        
    def load_data(self):
        """Load fixtures and FIFA rankings"""
        # Load fixtures
        try:
            with open('uefa_fixtures_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.fixtures = data.get('fixtures', {})
            print(f"✅ Loaded {len(self.fixtures)} fixtures")
        except FileNotFoundError:
            print("❌ UEFA fixtures data not found")
            return False
        
        # Load FIFA rankings
        try:
            with open('fifa_rankings_from_excel.json', 'r', encoding='utf-8') as f:
                rankings_data = json.load(f)
                if 'rankings' in rankings_data:
                    rankings_list = rankings_data['rankings']
                    self.fifa_rankings = {team['code']: team for team in rankings_list}
                else:
                    self.fifa_rankings = rankings_data
            print(f"✅ Loaded {len(self.fifa_rankings)} FIFA team rankings")
        except FileNotFoundError:
            print("❌ FIFA rankings file not found")
            return False
        
        return True
    
    def calculate_expected_result(self, home_points, away_points, home_advantage=100):
        """Calculate expected result using FIFA Elo formula"""
        rating_diff = (home_points + home_advantage) - away_points
        expected_home = 1 / (10**(-rating_diff/600) + 1)
        return expected_home
    
    def calculate_rating_change(self, team_points, opponent_points, actual_result, is_home=True):
        """Calculate rating change for a team"""
        home_advantage = 100 if is_home else 0
        expected = self.calculate_expected_result(
            team_points + home_advantage if is_home else opponent_points + (100 if not is_home else 0),
            opponent_points if is_home else team_points
        )
        
        if not is_home:
            expected = 1 - expected
        
        change = self.importance_coefficient * (actual_result - expected)
        return change
    
    def get_team_code(self, team_name):
        """Get team code from name, using manual mapping if needed"""
        if team_name in self.team_name_to_code:
            return self.team_name_to_code[team_name]
        return None
    
    def get_team_fixtures(self):
        """Organize fixtures by team"""
        team_fixtures = defaultdict(list)
        
        for fixture_id, fixture in self.fixtures.items():
            home_code = fixture.get('home_code')
            away_code = fixture.get('away_code')
            home_team = fixture.get('home_team')
            away_team = fixture.get('away_team')
            
            # Use manual mapping if code is missing
            if not home_code and home_team:
                home_code = self.get_team_code(home_team)
            if not away_code and away_team:
                away_code = self.get_team_code(away_team)
            
            if home_code:
                team_fixtures[home_code].append({
                    'fixture_id': fixture_id,
                    'fixture': fixture,
                    'is_home': True,
                    'opponent_code': away_code
                })
            
            if away_code:
                team_fixtures[away_code].append({
                    'fixture_id': fixture_id,
                    'fixture': fixture,
                    'is_home': False,
                    'opponent_code': home_code
                })
        
        # Sort fixtures by date for each team
        for team_code in team_fixtures:
            team_fixtures[team_code].sort(key=lambda x: x['fixture']['date'])
        
        return team_fixtures
    
    def calculate_team_range(self, team_code, team_fixtures_list):
        """Calculate best and worst case points for a team"""
        if team_code not in self.fifa_rankings:
            return None
        
        initial_points = self.fifa_rankings[team_code]['points']
        
        if len(team_fixtures_list) != 2:
            print(f"⚠️  {team_code}: Expected 2 fixtures, found {len(team_fixtures_list)}")
            return {
                'team_code': team_code,
                'team_name': self.fifa_rankings[team_code]['team'],
                'initial_points': initial_points,
                'current_rank': self.fifa_rankings[team_code]['rank'],
                'fixtures_count': len(team_fixtures_list),
                'best_points': initial_points,
                'worst_points': initial_points,
                'best_change': 0,
                'worst_change': 0
            }
        
        # Get the two fixtures
        fixture1 = team_fixtures_list[0]
        fixture2 = team_fixtures_list[1]
        
        # Get opponent points
        opp1_code = fixture1['opponent_code']
        opp2_code = fixture2['opponent_code']
        
        if not opp1_code or not opp2_code:
            return None
        
        if opp1_code not in self.fifa_rankings or opp2_code not in self.fifa_rankings:
            return None
        
        opp1_initial_points = self.fifa_rankings[opp1_code]['points']
        opp2_initial_points = self.fifa_rankings[opp2_code]['points']
        
        # Calculate best case scenario (team wins both games)
        # Game 1: Team wins
        best_change_1 = self.calculate_rating_change(
            initial_points, opp1_initial_points, 1.0, fixture1['is_home']
        )
        best_points_after_1 = initial_points + best_change_1
        
        # Opponent 1's points after losing to team
        opp1_change_1 = self.calculate_rating_change(
            opp1_initial_points, initial_points, 0.0, not fixture1['is_home']
        )
        opp1_points_after_1 = opp1_initial_points + opp1_change_1
        
        # Game 2: Team wins (with updated points)
        # Use opponent's updated points if opponent 1 == opponent 2
        opp2_points_for_game2 = opp1_points_after_1 if opp1_code == opp2_code else opp2_initial_points
        
        best_change_2 = self.calculate_rating_change(
            best_points_after_1, opp2_points_for_game2, 1.0, fixture2['is_home']
        )
        best_final_points = best_points_after_1 + best_change_2
        
        # Calculate worst case scenario (team loses both games)
        # Game 1: Team loses
        worst_change_1 = self.calculate_rating_change(
            initial_points, opp1_initial_points, 0.0, fixture1['is_home']
        )
        worst_points_after_1 = initial_points + worst_change_1
        
        # Opponent 1's points after beating team
        opp1_change_1_win = self.calculate_rating_change(
            opp1_initial_points, initial_points, 1.0, not fixture1['is_home']
        )
        opp1_points_after_1_win = opp1_initial_points + opp1_change_1_win
        
        # Game 2: Team loses (with updated points)
        opp2_points_for_game2_worst = opp1_points_after_1_win if opp1_code == opp2_code else opp2_initial_points
        
        worst_change_2 = self.calculate_rating_change(
            worst_points_after_1, opp2_points_for_game2_worst, 0.0, fixture2['is_home']
        )
        worst_final_points = worst_points_after_1 + worst_change_2
        
        return {
            'team_code': team_code,
            'team_name': self.fifa_rankings[team_code]['team'],
            'initial_points': initial_points,
            'current_rank': self.fifa_rankings[team_code]['rank'],
            'best_points': best_final_points,
            'worst_points': worst_final_points,
            'best_change': best_final_points - initial_points,
            'worst_change': worst_final_points - initial_points,
            'range': best_final_points - worst_final_points,
            'fixture1_opponent': self.fifa_rankings[opp1_code]['team'] if opp1_code in self.fifa_rankings else opp1_code,
            'fixture2_opponent': self.fifa_rankings[opp2_code]['team'] if opp2_code in self.fifa_rankings else opp2_code,
            'fixture1_home': fixture1['is_home'],
            'fixture2_home': fixture2['is_home']
        }
    
    def analyze_all_teams(self):
        """Analyze all teams with fixtures"""
        print("🎯 CALCULATING BEST/WORST CASE FOR ALL UEFA TEAMS")
        print("=" * 60)
        
        team_fixtures = self.get_team_fixtures()
        results = []
        
        # Analyze each team
        for team_code, fixtures_list in team_fixtures.items():
            if team_code == 'SCO':
                print(f"🏴󠁧󠁢󠁳󠁣󠁴󠁿 Found Scotland with {len(fixtures_list)} fixtures")
                for i, fixture_info in enumerate(fixtures_list):
                    fixture = fixture_info['fixture']
                    opp = fixture_info['opponent_code']
                    home = "H" if fixture_info['is_home'] else "A"
                    print(f"   Game {i+1}: vs {opp} ({home}) on {fixture['date']}")
            
            if team_code in self.fifa_rankings:
                result = self.calculate_team_range(team_code, fixtures_list)
                if result:
                    results.append(result)
        
        # Sort by current ranking
        results.sort(key=lambda x: x['current_rank'])
        
        print(f"📊 Analyzed {len(results)} teams with fixtures")
        print("\nFormat: Rank Team (Current→Best/Worst) Range Opponents")
        print("-" * 80)
        
        for result in results:
            team_name = result['team_name'][:18]  # Truncate long names
            current_pts = result['initial_points']
            best_pts = result['best_points']
            worst_pts = result['worst_points']
            
            # Handle teams with incomplete fixture data
            if 'fixture1_home' in result and 'fixture2_home' in result:
                h1 = "H" if result['fixture1_home'] else "A"
                h2 = "H" if result['fixture2_home'] else "A"
                
                opp1 = result['fixture1_opponent'][:12]  # Truncate
                opp2 = result['fixture2_opponent'][:12]
                
                opponents_info = f"vs {opp1}({h1}), {opp2}({h2})"
                range_info = f"±{result.get('range', 0):5.1f}"
            else:
                opponents_info = f"({result.get('fixtures_count', 0)} fixtures)"
                range_info = "  N/A"
            
            print(f"#{result['current_rank']:2d} {team_name:<18} "
                  f"({current_pts:6.1f}→{best_pts:6.1f}/{worst_pts:6.1f}) "
                  f"{range_info} "
                  f"{opponents_info}")
        
        return results
    
    def scotland_ranking_analysis(self, all_results):
        """Analyze Scotland's potential ranking movement"""
        print(f"\n🏴󠁧󠁢󠁳󠁣󠁴󠁿 SCOTLAND RANKING MOVEMENT ANALYSIS")
        print("=" * 50)
        
        # Find Scotland's data
        scotland_data = None
        for result in all_results:
            if result['team_code'] == 'SCO':
                scotland_data = result
                break
        
        if not scotland_data:
            print("❌ Scotland data not found")
            return
        
        scotland_current_rank = scotland_data['current_rank']
        scotland_best_points = scotland_data['best_points']
        scotland_worst_points = scotland_data['worst_points']
        
        print(f"📍 Current Position: #{scotland_current_rank} ({scotland_data['initial_points']:.1f} pts)")
        print(f"🎯 Best Case: {scotland_best_points:.1f} pts ({scotland_data['best_change']:+.1f})")
        print(f"⚠️  Worst Case: {scotland_worst_points:.1f} pts ({scotland_data['worst_change']:+.1f})")
        
        # Calculate potential ranking changes
        teams_scotland_could_catch = []
        teams_that_could_overtake_scotland = []
        
        for result in all_results:
            if result['team_code'] == 'SCO':
                continue
            
            current_rank = result['current_rank']
            team_best = result['best_points']
            team_worst = result['worst_points']
            
            # Teams Scotland could potentially overtake
            if (current_rank < scotland_current_rank and 
                team_worst < scotland_best_points):
                teams_scotland_could_catch.append({
                    'rank': current_rank,
                    'team': result['team_name'],
                    'current_points': result['initial_points'],
                    'worst_points': team_worst,
                    'gap_if_scotland_best': scotland_best_points - team_worst
                })
            
            # Teams that could potentially overtake Scotland
            if (current_rank > scotland_current_rank and 
                team_best > scotland_worst_points):
                teams_that_could_overtake_scotland.append({
                    'rank': current_rank,
                    'team': result['team_name'],
                    'current_points': result['initial_points'],
                    'best_points': team_best,
                    'gap_if_scotland_worst': team_best - scotland_worst_points
                })
        
        # Sort and display
        teams_scotland_could_catch.sort(key=lambda x: x['rank'])
        teams_that_could_overtake_scotland.sort(key=lambda x: x['rank'])
        
        print(f"\n🎯 TEAMS SCOTLAND COULD CATCH (if Scotland gets best & they get worst):")
        print("-" * 65)
        if teams_scotland_could_catch:
            best_possible_rank = min(team['rank'] for team in teams_scotland_could_catch)
            print(f"   Best possible rank: #{best_possible_rank}")
            for team in teams_scotland_could_catch[:10]:  # Top 10
                print(f"   #{team['rank']:2d} {team['team']:<20} "
                      f"({team['current_points']:6.1f}→{team['worst_points']:6.1f}) "
                      f"Gap: {team['gap_if_scotland_best']:+.1f}")
        else:
            print("   No teams Scotland can realistically catch")
            best_possible_rank = scotland_current_rank
        
        print(f"\n⚠️  TEAMS THAT COULD OVERTAKE SCOTLAND (if they get best & Scotland gets worst):")
        print("-" * 75)
        if teams_that_could_overtake_scotland:
            worst_possible_rank = scotland_current_rank + len(teams_that_could_overtake_scotland)
            print(f"   Worst possible rank: #{worst_possible_rank}")
            for team in teams_that_could_overtake_scotland[:10]:  # Top 10
                print(f"   #{team['rank']:2d} {team['team']:<20} "
                      f"({team['current_points']:6.1f}→{team['best_points']:6.1f}) "
                      f"Gap: {team['gap_if_scotland_worst']:+.1f}")
        else:
            print("   No teams can realistically overtake Scotland")
            worst_possible_rank = scotland_current_rank
        
        print(f"\n🏆 SUMMARY:")
        print("-" * 20)
        print(f"Scotland can move between ranks #{best_possible_rank} and #{worst_possible_rank}")
        print(f"Maximum upward movement: {scotland_current_rank - best_possible_rank} places")
        print(f"Maximum downward movement: {worst_possible_rank - scotland_current_rank} places")
        print(f"Points range: {scotland_worst_points:.1f} to {scotland_best_points:.1f}")
        
        return {
            'current_rank': scotland_current_rank,
            'best_possible_rank': best_possible_rank,
            'worst_possible_rank': worst_possible_rank,
            'current_points': scotland_data['initial_points'],
            'best_points': scotland_best_points,
            'worst_points': scotland_worst_points
        }

def main():
    analyzer = TeamRangeAnalyzer()
    
    # Analyze all teams
    all_results = analyzer.analyze_all_teams()
    
    # Focus on Scotland's ranking movement
    scotland_analysis = analyzer.scotland_ranking_analysis(all_results)
    
    return all_results, scotland_analysis

if __name__ == "__main__":
    results, scotland_summary = main()