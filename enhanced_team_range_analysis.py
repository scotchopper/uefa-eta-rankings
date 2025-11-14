#!/usr/bin/env python3
"""
Enhanced UEFA Teams Best/Worst Case Analysis with Table Display
Calculate highest and lowest possible points for each team after their 2 games
"""

import json
from collections import defaultdict

class EnhancedTeamRangeAnalyzer:
    def __init__(self):
        self.fixtures = {}
        self.fifa_rankings = {}
        self.load_data()
        self.importance_coefficient = 25
        
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
        
        # Load FIFA rankings (now with corrected codes)
        try:
            with open('fifa_rankings_from_excel.json', 'r', encoding='utf-8') as f:
                rankings_data = json.load(f)
                if 'rankings' in rankings_data:
                    rankings_list = rankings_data['rankings']
                    # Create lookup by both code and name
                    self.fifa_rankings_by_code = {team['code']: team for team in rankings_list}
                    self.fifa_rankings_by_name = {team['team']: team for team in rankings_list}
            print(f"✅ Loaded {len(self.fifa_rankings_by_code)} FIFA team rankings")
        except FileNotFoundError:
            print("❌ FIFA rankings file not found")
            return False
        
        return True
    
    def get_team_data_by_name(self, team_name):
        """Get team data by name from FIFA rankings"""
        return self.fifa_rankings_by_name.get(team_name)
    
    def get_team_data_by_code(self, team_code):
        """Get team data by code from FIFA rankings"""
        return self.fifa_rankings_by_code.get(team_code)
    
    def calculate_expected_result(self, home_points, away_points, home_advantage=100):
        """Calculate expected result using FIFA Elo formula"""
        rating_diff = (home_points + home_advantage) - away_points
        expected_home = 1 / (10**(-rating_diff/600) + 1)
        return expected_home
    
    def calculate_rating_change(self, team_points, opponent_points, actual_result, is_home=True, importance=25):
        """Calculate rating change for a team with specified importance coefficient"""
        home_advantage = 100 if is_home else 0
        expected = self.calculate_expected_result(
            team_points + home_advantage if is_home else opponent_points + (100 if not is_home else 0),
            opponent_points if is_home else team_points
        )
        
        if not is_home:
            expected = 1 - expected
        
        change = importance * (actual_result - expected)
        return change
    
    def get_team_fixtures(self):
        """Organize fixtures by team using name-based lookup"""
        team_fixtures = defaultdict(list)
        
        for fixture_id, fixture in self.fixtures.items():
            home_team = fixture.get('home_team')
            away_team = fixture.get('away_team')
            
            # Get team data using names (which are now perfectly aligned)
            home_data = self.get_team_data_by_name(home_team)
            away_data = self.get_team_data_by_name(away_team)
            
            if home_data:
                team_fixtures[home_team].append({
                    'fixture_id': fixture_id,
                    'fixture': fixture,
                    'is_home': True,
                    'opponent_name': away_team,
                    'opponent_data': away_data,
                    'importance': fixture.get('importance', 25)
                })
            
            if away_data:
                team_fixtures[away_team].append({
                    'fixture_id': fixture_id,
                    'fixture': fixture,
                    'is_home': False,
                    'opponent_name': home_team,
                    'opponent_data': home_data,
                    'importance': fixture.get('importance', 25)
                })
        
        # Sort fixtures by date for each team
        for team_name in team_fixtures:
            team_fixtures[team_name].sort(key=lambda x: x['fixture']['date'])
        
        return team_fixtures
    
    def calculate_team_range(self, team_name, team_fixtures_list):
        """Calculate best and worst case points for a team"""
        team_data = self.get_team_data_by_name(team_name)
        if not team_data:
            return None
        
        initial_points = team_data['points']
        
        if len(team_fixtures_list) != 2:
            return {
                'team_name': team_name,
                'team_code': team_data['code'],
                'initial_points': initial_points,
                'current_rank': team_data['rank'],
                'fixtures_count': len(team_fixtures_list),
                'best_points': initial_points,
                'worst_points': initial_points,
                'best_change': 0,
                'worst_change': 0,
                'range': 0,
                'valid_data': False
            }
        
        # Get the two fixtures
        fixture1 = team_fixtures_list[0]
        fixture2 = team_fixtures_list[1]
        
        opp1_data = fixture1['opponent_data']
        opp2_data = fixture2['opponent_data']
        
        if not opp1_data or not opp2_data:
            return None
        
        opp1_initial_points = opp1_data['points']
        opp2_initial_points = opp2_data['points']
        
        # Get importance coefficients for each game
        importance1 = fixture1['importance']
        importance2 = fixture2['importance']
        
        # Calculate best case scenario (team wins both games)
        # Game 1: Team wins
        best_change_1 = self.calculate_rating_change(
            initial_points, opp1_initial_points, 1.0, fixture1['is_home'], importance1
        )
        best_points_after_1 = initial_points + best_change_1
        
        # Opponent 1's points after losing to team
        opp1_change_1 = self.calculate_rating_change(
            opp1_initial_points, initial_points, 0.0, not fixture1['is_home'], importance1
        )
        opp1_points_after_1 = opp1_initial_points + opp1_change_1
        
        # Game 2: Team wins (with updated points)
        # Use opponent's updated points if same opponent
        opp2_points_for_game2 = opp1_points_after_1 if fixture1['opponent_name'] == fixture2['opponent_name'] else opp2_initial_points
        
        best_change_2 = self.calculate_rating_change(
            best_points_after_1, opp2_points_for_game2, 1.0, fixture2['is_home'], importance2
        )
        best_final_points = best_points_after_1 + best_change_2
        
        # Calculate worst case scenario (team loses both games)
        # Game 1: Team loses
        worst_change_1 = self.calculate_rating_change(
            initial_points, opp1_initial_points, 0.0, fixture1['is_home'], importance1
        )
        worst_points_after_1 = initial_points + worst_change_1
        
        # Opponent 1's points after beating team
        opp1_change_1_win = self.calculate_rating_change(
            opp1_initial_points, initial_points, 1.0, not fixture1['is_home'], importance1
        )
        opp1_points_after_1_win = opp1_initial_points + opp1_change_1_win
        
        # Game 2: Team loses (with updated points)
        opp2_points_for_game2_worst = opp1_points_after_1_win if fixture1['opponent_name'] == fixture2['opponent_name'] else opp2_initial_points
        
        worst_change_2 = self.calculate_rating_change(
            worst_points_after_1, opp2_points_for_game2_worst, 0.0, fixture2['is_home'], importance2
        )
        worst_final_points = worst_points_after_1 + worst_change_2
        
        return {
            'team_name': team_name,
            'team_code': team_data['code'],
            'initial_points': initial_points,
            'current_rank': team_data['rank'],
            'best_points': best_final_points,
            'worst_points': worst_final_points,
            'best_change': best_final_points - initial_points,
            'worst_change': worst_final_points - initial_points,
            'range': best_final_points - worst_final_points,
            'fixture1_opponent': fixture1['opponent_name'],
            'fixture2_opponent': fixture2['opponent_name'],
            'fixture1_home': fixture1['is_home'],
            'fixture2_home': fixture2['is_home'],
            'fixture1_date': fixture1['fixture']['date'],
            'fixture2_date': fixture2['fixture']['date'],
            'fixture1_competition': fixture1['fixture']['competition'],
            'fixture2_competition': fixture2['fixture']['competition'],
            'importance1': importance1,
            'importance2': importance2,
            'valid_data': True
        }
    
    def display_results_table(self, results):
        """Display results in a formatted table"""
        print(f"\n📊 UEFA TEAMS BEST/WORST CASE ANALYSIS - ALL {len(results)} TEAMS")
        print("=" * 140)
        
        # Table header
        print(f"{'FIFA':<4} {'UEFA':<4} {'Team':<20} {'Code':<4} {'Current':<8} {'Best':<8} {'Worst':<8} {'Range':<8} {'Competitions':<15} {'Fixtures':<20}")
        print("-" * 140)
        
        # Add UEFA ranking (1-54)
        for i, result in enumerate(results):
            result['uefa_rank'] = i + 1
        
        for result in results:
            if not result.get('valid_data', True):
                continue
                
            fifa_rank = result['current_rank']
            uefa_rank = result['uefa_rank']
            team = result['team_name'][:19]  # Truncate if too long
            code = result['team_code']
            current = result['initial_points']
            best = result['best_points']
            worst = result['worst_points']
            range_val = result['range']
            
            # Format competitions and fixtures info
            if 'fixture1_opponent' in result:
                h1 = "H" if result['fixture1_home'] else "A"
                h2 = "H" if result['fixture2_home'] else "A"
                opp1 = result['fixture1_opponent'][:12]
                opp2 = result['fixture2_opponent'][:12]
                
                # Show competition types
                comp1 = "F" if result.get('importance1', 25) == 10 else "W"
                comp2 = "F" if result.get('importance2', 25) == 10 else "W"
                comp_info = f"{comp1}{result.get('importance1', 25)}/{comp2}{result.get('importance2', 25)}"
                
                fixtures_info = f"vs {opp1}({h1}), {opp2}({h2})"
            else:
                comp_info = f"({result.get('fixtures_count', 0)} fixtures)"
                fixtures_info = ""
            
            print(f"{fifa_rank:<4} {uefa_rank:<4} {team:<20} {code:<4} {current:<8.2f} {best:<8.2f} {worst:<8.2f} {range_val:<8.2f} {comp_info:<15} {fixtures_info:<20}")
        
        return True
    
    def analyze_all_teams(self):
        """Analyze all teams with fixtures"""
        print("🎯 CALCULATING BEST/WORST CASE FOR ALL UEFA TEAMS")
        print("=" * 60)
        
        team_fixtures = self.get_team_fixtures()
        results = []
        
        print(f"📋 Found {len(team_fixtures)} teams with fixtures")
        
        # Analyze each team
        for team_name, fixtures_list in team_fixtures.items():
            if team_name == 'Scotland':
                print(f"🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland has {len(fixtures_list)} fixtures:")
                for i, fixture_info in enumerate(fixtures_list):
                    fixture = fixture_info['fixture']
                    opp = fixture_info['opponent_name']
                    home = "H" if fixture_info['is_home'] else "A"
                    print(f"   Game {i+1}: vs {opp} ({home}) on {fixture['date']}")
            
            result = self.calculate_team_range(team_name, fixtures_list)
            if result:
                results.append(result)
        
        # Sort by current ranking
        results.sort(key=lambda x: x['current_rank'])
        
        print(f"✅ Successfully analyzed {len(results)} teams")
        
        # Display in table format
        self.display_results_table(results)
        
        return results
    
    def scotland_detailed_analysis(self, all_results):
        """Detailed Scotland ranking analysis"""
        print(f"\n🏴󠁧󠁢󠁳󠁣󠁴󠁿 SCOTLAND DETAILED RANKING ANALYSIS")
        print("=" * 60)
        
        # Find Scotland's data
        scotland_data = None
        for result in all_results:
            if result['team_name'] == 'Scotland':
                scotland_data = result
                break
        
        if not scotland_data:
            print("❌ Scotland data not found")
            return
        
        fifa_rank = scotland_data['current_rank']
        uefa_rank = scotland_data['uefa_rank']
        current_points = scotland_data['initial_points']
        best_points = scotland_data['best_points']
        worst_points = scotland_data['worst_points']
        
        print(f"📍 Current Position: FIFA #{fifa_rank} / UEFA #{uefa_rank} ({current_points:.2f} points)")
        print(f"🎯 Best Case Scenario: {best_points:.2f} points ({scotland_data['best_change']:+.2f})")
        print(f"⚠️  Worst Case Scenario: {worst_points:.2f} points ({scotland_data['worst_change']:+.2f})")
        print(f"📊 Points Range: {scotland_data['range']:.2f} points")
        
        # Calculate ranking implications using UEFA rankings
        teams_scotland_could_catch = []
        teams_that_could_overtake = []
        
        for result in all_results:
            if result['team_name'] == 'Scotland':
                continue
            
            other_fifa_rank = result['current_rank']
            other_uefa_rank = result['uefa_rank'] 
            other_best = result['best_points']
            other_worst = result['worst_points']
            
            # Teams Scotland could catch (better UEFA rank)
            if other_uefa_rank < uefa_rank and other_worst < best_points:
                teams_scotland_could_catch.append({
                    'fifa_rank': other_fifa_rank,
                    'uefa_rank': other_uefa_rank,
                    'team': result['team_name'],
                    'current_points': result['initial_points'],
                    'worst_points': other_worst,
                    'gap': best_points - other_worst
                })
            
            # Teams that could overtake Scotland (worse UEFA rank)
            if other_uefa_rank > uefa_rank and other_best > worst_points:
                teams_that_could_overtake.append({
                    'fifa_rank': other_fifa_rank,
                    'uefa_rank': other_uefa_rank,
                    'team': result['team_name'],
                    'current_points': result['initial_points'],
                    'best_points': other_best,
                    'gap': other_best - worst_points
                })
        
        # Sort and analyze using UEFA rankings
        teams_scotland_could_catch.sort(key=lambda x: x['uefa_rank'])
        teams_that_could_overtake.sort(key=lambda x: x['uefa_rank'])
        
        best_possible_uefa_rank = min([t['uefa_rank'] for t in teams_scotland_could_catch], default=uefa_rank)
        worst_possible_uefa_rank = uefa_rank + len(teams_that_could_overtake)
        
        print(f"\n🎯 BEST CASE RANKING MOVEMENT (UEFA):")
        print("-" * 45)
        print(f"Best possible UEFA rank: #{best_possible_uefa_rank}")
        print(f"Upward movement: {uefa_rank - best_possible_uefa_rank} places")
        
        if teams_scotland_could_catch:
            print(f"UEFA teams Scotland could overtake:")
            for team in teams_scotland_could_catch[:5]:
                print(f"  UEFA #{team['uefa_rank']:2d} (FIFA #{team['fifa_rank']:2d}) {team['team']:<15} (gap: {team['gap']:+.2f})")
        
        print(f"\n⚠️  WORST CASE RANKING MOVEMENT (UEFA):")
        print("-" * 45)
        print(f"Worst possible UEFA rank: #{worst_possible_uefa_rank}")
        print(f"Downward movement: {worst_possible_uefa_rank - uefa_rank} places")
        
        if teams_that_could_overtake:
            print(f"UEFA teams that could overtake Scotland:")
            for team in teams_that_could_overtake[:5]:
                print(f"  UEFA #{team['uefa_rank']:2d} (FIFA #{team['fifa_rank']:2d}) {team['team']:<15} (gap: {team['gap']:+.2f})")
        
        print(f"\n🏆 FINAL SUMMARY:")
        print("-" * 25)
        print(f"FIFA Ranking: Can move between #{fifa_rank-len(teams_scotland_could_catch)} and #{fifa_rank+len(teams_that_could_overtake)}")
        print(f"UEFA Ranking: Can move between #{best_possible_uefa_rank} and #{worst_possible_uefa_rank}")
        print(f"Maximum UEFA gain: {uefa_rank - best_possible_uefa_rank} places up")
        print(f"Maximum UEFA loss: {worst_possible_uefa_rank - uefa_rank} places down")
        print(f"Points range: {worst_points:.2f} to {best_points:.2f}")
        
        return {
            'fifa_rank': fifa_rank,
            'uefa_rank': uefa_rank,
            'best_uefa_rank': best_possible_uefa_rank,
            'worst_uefa_rank': worst_possible_uefa_rank,
            'current_points': current_points,
            'best_points': best_points,
            'worst_points': worst_points,
            'max_uefa_gain': uefa_rank - best_possible_uefa_rank,
            'max_uefa_loss': worst_possible_uefa_rank - uefa_rank
        }

def main():
    analyzer = EnhancedTeamRangeAnalyzer()
    
    # Analyze all teams
    all_results = analyzer.analyze_all_teams()
    
    # Scotland-specific analysis
    scotland_summary = analyzer.scotland_detailed_analysis(all_results)
    
    return all_results, scotland_summary

if __name__ == "__main__":
    results, scotland_data = main()