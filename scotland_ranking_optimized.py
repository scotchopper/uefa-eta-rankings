#!/usr/bin/env python3
"""
Scotland UEFA Rankings Movement Analysis - Optimized Version
Focus on teams that can realistically affect Scotland's position
"""

import json
from collections import defaultdict
import itertools
from datetime import datetime

class ScotlandRankingAnalyzer:
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
    
    def identify_relevant_teams(self):
        """Identify teams that could realistically affect Scotland's ranking"""
        scotland_points = self.fifa_rankings.get('SCO', {}).get('points', 1504.2)
        scotland_rank = self.fifa_rankings.get('SCO', {}).get('rank', 38)
        
        # Teams within reasonable range that Scotland could catch or lose to
        relevant_teams = set(['SCO'])  # Always include Scotland
        
        # Add teams Scotland plays directly
        for fixture_id, fixture in self.fixtures.items():
            if fixture.get('home_code') == 'SCO' or fixture.get('away_code') == 'SCO':
                if fixture.get('home_code'):
                    relevant_teams.add(fixture['home_code'])
                if fixture.get('away_code'):
                    relevant_teams.add(fixture['away_code'])
        
        # Add teams within +/- 100 points of Scotland that are in fixtures
        participating_teams = set()
        for fixture_id, fixture in self.fixtures.items():
            if fixture.get('home_code'):
                participating_teams.add(fixture['home_code'])
            if fixture.get('away_code'):
                participating_teams.add(fixture['away_code'])
        
        for team_code in participating_teams:
            if team_code in self.fifa_rankings:
                team_points = self.fifa_rankings[team_code]['points']
                # Include teams within 100 points or within 10 ranks
                if (abs(team_points - scotland_points) <= 100 or 
                    abs(self.fifa_rankings[team_code]['rank'] - scotland_rank) <= 10):
                    relevant_teams.add(team_code)
        
        print(f"🎯 Focusing on {len(relevant_teams)} teams that could affect Scotland's ranking")
        
        # Show relevant teams
        relevant_rankings = []
        for team_code in relevant_teams:
            if team_code in self.fifa_rankings:
                team_data = self.fifa_rankings[team_code]
                relevant_rankings.append({
                    'code': team_code,
                    'rank': team_data['rank'],
                    'team': team_data['team'],
                    'points': team_data['points']
                })
        
        relevant_rankings.sort(key=lambda x: x['rank'])
        
        print("📊 Relevant Teams:")
        for team in relevant_rankings:
            marker = "👉" if team['code'] == 'SCO' else "  "
            print(f"{marker} #{team['rank']:2d} {team['team']:<20} ({team['points']:7.2f} pts)")
        
        return relevant_teams
    
    def get_relevant_fixtures(self, relevant_teams):
        """Get fixtures involving relevant teams"""
        relevant_fixtures = {}
        
        for fixture_id, fixture in self.fixtures.items():
            home_code = fixture.get('home_code')
            away_code = fixture.get('away_code')
            
            # Include fixture if either team is relevant
            if (home_code in relevant_teams or away_code in relevant_teams or
                home_code == 'SCO' or away_code == 'SCO'):
                relevant_fixtures[fixture_id] = fixture
        
        print(f"⚽ Analyzing {len(relevant_fixtures)} relevant fixtures")
        return relevant_fixtures
    
    def simulate_scotland_scenarios(self):
        """Simulate scenarios focusing on Scotland's ranking movement"""
        print("\n🎲 SCOTLAND RANKING SCENARIOS")
        print("=" * 40)
        
        # Get Scotland's current info
        scotland_current = self.fifa_rankings.get('SCO', {})
        current_rank = scotland_current.get('rank', 38)
        current_points = scotland_current.get('points', 1504.2)
        
        print(f"📍 Current: #{current_rank} ({current_points} points)")
        
        # Identify relevant teams and fixtures
        relevant_teams = self.identify_relevant_teams()
        relevant_fixtures = self.get_relevant_fixtures(relevant_teams)
        
        # Get Scotland's specific fixtures
        scotland_fixtures = []
        other_fixtures = []
        
        for fixture_id, fixture in relevant_fixtures.items():
            if fixture.get('home_code') == 'SCO' or fixture.get('away_code') == 'SCO':
                scotland_fixtures.append((fixture_id, fixture))
            else:
                other_fixtures.append((fixture_id, fixture))
        
        print(f"\n🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland's fixtures: {len(scotland_fixtures)}")
        for fixture_id, fixture in scotland_fixtures:
            opponent = fixture['home_team'] if fixture.get('away_code') == 'SCO' else fixture['away_team']
            venue = "H" if fixture.get('home_code') == 'SCO' else "A"
            print(f"   {fixture['date']}: vs {opponent} ({venue})")
        
        print(f"\n⚡ Key other fixtures affecting rankings: {len(other_fixtures)}")
        
        # Simulate all combinations for Scotland's matches + sample key others
        scotland_outcomes = 3 ** len(scotland_fixtures)  # W/D/L for each Scotland match
        
        if len(other_fixtures) > 15:
            # Sample other fixtures if too many
            import random
            random.seed(42)
            sampled_others = random.sample(other_fixtures, 15)
            print(f"   📊 Sampling {len(sampled_others)} most impactful other fixtures")
        else:
            sampled_others = other_fixtures
        
        total_scenarios = scotland_outcomes * (3 ** len(sampled_others))
        print(f"🎲 Total scenarios to analyze: {total_scenarios:,}")
        
        # Analyze scenarios
        outcomes = []
        
        for scotland_results in itertools.product([0, 0.5, 1], repeat=len(scotland_fixtures)):
            for other_results in itertools.product([0, 0.5, 1], repeat=len(sampled_others)):
                # Initialize points
                team_points = {}
                for team_code in relevant_teams:
                    if team_code in self.fifa_rankings:
                        team_points[team_code] = self.fifa_rankings[team_code]['points']
                
                # Process Scotland's matches first (chronologically)
                scotland_matches_sorted = sorted(scotland_fixtures, key=lambda x: x[1]['date'])
                
                for i, (fixture_id, fixture) in enumerate(scotland_matches_sorted):
                    home_code = fixture.get('home_code')
                    away_code = fixture.get('away_code')
                    
                    if not home_code or not away_code:
                        continue
                    
                    actual_result = scotland_results[i]
                    
                    # Calculate changes
                    home_change = self.calculate_rating_change(
                        team_points[home_code], team_points[away_code], actual_result, True
                    )
                    away_change = self.calculate_rating_change(
                        team_points[away_code], team_points[home_code], 1-actual_result, False
                    )
                    
                    team_points[home_code] += home_change
                    team_points[away_code] += away_change
                
                # Process other relevant matches
                for i, (fixture_id, fixture) in enumerate(sampled_others):
                    home_code = fixture.get('home_code')
                    away_code = fixture.get('away_code')
                    
                    if (not home_code or not away_code or 
                        home_code not in team_points or away_code not in team_points):
                        continue
                    
                    actual_result = other_results[i]
                    
                    home_change = self.calculate_rating_change(
                        team_points[home_code], team_points[away_code], actual_result, True
                    )
                    away_change = self.calculate_rating_change(
                        team_points[away_code], team_points[home_code], 1-actual_result, False
                    )
                    
                    team_points[home_code] += home_change
                    team_points[away_code] += away_change
                
                # Calculate Scotland's final ranking position
                scotland_final_points = team_points.get('SCO', current_points)
                
                # Count teams above Scotland (simplified - just count relevant teams)
                relevant_teams_above = 0
                for team_code, points in team_points.items():
                    if team_code != 'SCO' and points > scotland_final_points:
                        relevant_teams_above += 1
                
                # Estimate full ranking (rough approximation)
                estimated_rank = current_rank + relevant_teams_above - sum(
                    1 for team_code, points in team_points.items() 
                    if (team_code != 'SCO' and 
                        team_code in self.fifa_rankings and
                        self.fifa_rankings[team_code]['points'] > current_points and
                        points <= scotland_final_points)
                )
                
                scotland_change = scotland_final_points - current_points
                
                outcomes.append({
                    'rank': max(1, estimated_rank),
                    'points': scotland_final_points,
                    'change': scotland_change,
                    'scotland_results': scotland_results,
                    'other_results': other_results
                })
        
        print(f"✅ Analyzed {len(outcomes):,} scenarios")
        return outcomes
    
    def analyze_results(self, outcomes):
        """Analyze the simulation results"""
        if not outcomes:
            print("❌ No outcomes to analyze")
            return
        
        current_rank = self.fifa_rankings.get('SCO', {}).get('rank', 38)
        current_points = self.fifa_rankings.get('SCO', {}).get('points', 1504.2)
        
        # Calculate statistics
        best_rank = min(outcome['rank'] for outcome in outcomes)
        worst_rank = max(outcome['rank'] for outcome in outcomes)
        best_points = max(outcome['points'] for outcome in outcomes)
        worst_points = min(outcome['points'] for outcome in outcomes)
        best_change = max(outcome['change'] for outcome in outcomes)
        worst_change = min(outcome['change'] for outcome in outcomes)
        
        avg_rank = sum(outcome['rank'] for outcome in outcomes) / len(outcomes)
        avg_points = sum(outcome['points'] for outcome in outcomes) / len(outcomes)
        avg_change = sum(outcome['change'] for outcome in outcomes) / len(outcomes)
        
        # Count improvements/declines
        improvements = sum(1 for outcome in outcomes if outcome['rank'] < current_rank)
        declines = sum(1 for outcome in outcomes if outcome['rank'] > current_rank)
        unchanged = len(outcomes) - improvements - declines
        
        print(f"\n📈 SCOTLAND RANKING MOVEMENT ANALYSIS")
        print("=" * 45)
        
        print(f"🎯 RANK MOVEMENT POTENTIAL:")
        print(f"   Best possible: #{best_rank} (up {current_rank - best_rank} places)")
        print(f"   Worst possible: #{worst_rank} (down {worst_rank - current_rank} places)")
        print(f"   Average: #{avg_rank:.1f}")
        print(f"   Current: #{current_rank}")
        
        print(f"\n⚡ POINTS MOVEMENT:")
        print(f"   Best: {best_points:.2f} ({best_change:+.2f})")
        print(f"   Worst: {worst_points:.2f} ({worst_change:+.2f})")
        print(f"   Average: {avg_points:.2f} ({avg_change:+.2f})")
        print(f"   Current: {current_points:.2f}")
        
        print(f"\n📊 OUTCOME PROBABILITIES:")
        print(f"   Ranking improvement: {improvements/len(outcomes)*100:.1f}% ({improvements:,} scenarios)")
        print(f"   Ranking decline: {declines/len(outcomes)*100:.1f}% ({declines:,} scenarios)")
        print(f"   Ranking unchanged: {unchanged/len(outcomes)*100:.1f}% ({unchanged:,} scenarios)")
        
        # Find best and worst scenarios
        best_scenario = max(outcomes, key=lambda x: x['points'])
        worst_scenario = min(outcomes, key=lambda x: x['points'])
        
        print(f"\n🏆 BEST CASE SCENARIO:")
        print(f"   Rank: #{best_scenario['rank']} ({best_scenario['change']:+.2f} points)")
        print(f"   Scotland results: {self.format_results(best_scenario['scotland_results'])}")
        
        print(f"\n⚠️  WORST CASE SCENARIO:")
        print(f"   Rank: #{worst_scenario['rank']} ({worst_scenario['change']:+.2f} points)")
        print(f"   Scotland results: {self.format_results(worst_scenario['scotland_results'])}")
        
        return {
            'best_rank': best_rank,
            'worst_rank': worst_rank,
            'best_points': best_points,
            'worst_points': worst_points,
            'improvement_probability': improvements/len(outcomes),
            'decline_probability': declines/len(outcomes)
        }
    
    def format_results(self, results):
        """Format match results for display"""
        result_map = {0: 'L', 0.5: 'D', 1: 'W'}
        return ', '.join(result_map[r] for r in results)

def main():
    analyzer = ScotlandRankingAnalyzer()
    outcomes = analyzer.simulate_scotland_scenarios()
    results = analyzer.analyze_results(outcomes)

if __name__ == "__main__":
    main()