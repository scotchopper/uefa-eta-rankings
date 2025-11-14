#!/usr/bin/env python3
"""
Scotland UEFA Rankings Movement Analysis
Calculate Scotland's potential ranking movement considering all UEFA team interactions
"""

import json
from collections import defaultdict
import itertools
from datetime import datetime

class UEFARankingAnalyzer:
    def __init__(self):
        self.fixtures = {}
        self.fifa_rankings = {}
        self.uefa_teams = set()
        self.load_data()
        self.importance_coefficient = 25  # World Cup Qualifiers
        
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
    
    def identify_uefa_teams(self):
        """Identify all UEFA teams involved in fixtures"""
        uefa_codes = set()
        
        for fixture_id, fixture in self.fixtures.items():
            if fixture.get('home_code'):
                uefa_codes.add(fixture['home_code'])
            if fixture.get('away_code'):
                uefa_codes.add(fixture['away_code'])
        
        # Add known UEFA teams
        known_uefa = {
            'SCO', 'GRE', 'DEN', 'BLR', 'GER', 'LUX', 'NOR', 'SVK', 'SLO', 'KOS', 
            'SWI', 'SWE', 'AZE', 'ICE', 'FRA', 'UKR', 'GEO', 'SPA', 'TUR', 'BUL',
            'ARM', 'HUN', 'REP', 'POR', 'FIN', 'MLT', 'POL', 'NET', 'LIT', 'FAR',
            'KAZ', 'CYP', 'AUT', 'BOS', 'ROM', 'SAN', 'EST', 'MOL', 'ITA', 'ISR',
            'BEL', 'LIE', 'WAL', 'MKD', 'AND', 'ALB', 'ENG', 'SER', 'LAT', 'CRO',
            'GIB', 'MNE', 'CZE'
        }
        
        self.uefa_teams = uefa_codes.union(known_uefa)
        print(f"📍 Identified {len(self.uefa_teams)} UEFA teams in analysis")
        
        return self.uefa_teams
    
    def get_uefa_rankings(self):
        """Get current rankings for all UEFA teams"""
        uefa_rankings = {}
        
        for team_code in self.uefa_teams:
            if team_code in self.fifa_rankings:
                team_data = self.fifa_rankings[team_code]
                uefa_rankings[team_code] = {
                    'rank': team_data['rank'],
                    'team': team_data['team'],
                    'points': team_data['points'],
                    'code': team_code
                }
        
        # Sort by current rank
        sorted_uefa = sorted(uefa_rankings.values(), key=lambda x: x['rank'])
        return sorted_uefa
    
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
    
    def organize_fixtures_by_round(self):
        """Organize fixtures into rounds based on dates"""
        rounds = defaultdict(list)
        
        for fixture_id, fixture in self.fixtures.items():
            date = fixture['date']
            rounds[date].append((fixture_id, fixture))
        
        # Sort by date
        sorted_rounds = sorted(rounds.items())
        return sorted_rounds
    
    def simulate_all_scenarios(self):
        """Simulate all possible match outcomes"""
        rounds = self.organize_fixtures_by_round()
        
        # Get initial team points
        initial_points = {}
        for team_code in self.uefa_teams:
            if team_code in self.fifa_rankings:
                initial_points[team_code] = self.fifa_rankings[team_code]['points']
        
        # Generate all possible outcomes (W/D/L for each match)
        all_matches = []
        for date, fixtures in rounds:
            for fixture_id, fixture in fixtures:
                all_matches.append((fixture_id, fixture))
        
        total_scenarios = 3 ** len(all_matches)
        print(f"🎲 Analyzing {total_scenarios:,} total scenarios across {len(all_matches)} matches")
        
        scotland_outcomes = []
        
        # Sample scenarios if too many (for computational efficiency)
        if total_scenarios > 100000:
            print("⚡ Sampling 50,000 scenarios for analysis...")
            import random
            random.seed(42)  # Reproducible results
            scenario_count = 50000
        else:
            scenario_count = total_scenarios
        
        scenario_counter = 0
        sampled_scenarios = 0
        
        # Generate all combinations or sample them
        for outcomes in itertools.product([0, 0.5, 1], repeat=len(all_matches)):
            scenario_counter += 1
            
            # Skip scenarios if sampling
            if total_scenarios > 100000:
                if scenario_counter % (total_scenarios // 50000) != 0:
                    continue
            
            sampled_scenarios += 1
            
            # Simulate this scenario
            team_points = initial_points.copy()
            
            # Process matches chronologically
            for i, (match_id, fixture) in enumerate(all_matches):
                home_team = fixture.get('home_code')
                away_team = fixture.get('away_code')
                
                if not home_team or not away_team:
                    continue
                
                if home_team not in team_points or away_team not in team_points:
                    continue
                
                actual_result = outcomes[i]  # 0=away win, 0.5=draw, 1=home win
                
                # Calculate rating changes
                home_change = self.calculate_rating_change(
                    team_points[home_team], team_points[away_team], actual_result, True
                )
                away_change = self.calculate_rating_change(
                    team_points[away_team], team_points[home_team], 1-actual_result, False
                )
                
                # Update points
                team_points[home_team] += home_change
                team_points[away_team] += away_change
            
            # Calculate Scotland's final position
            if 'SCO' in team_points:
                scotland_final_points = team_points['SCO']
                
                # Count teams above Scotland
                teams_above = 0
                uefa_teams_above = 0
                
                for team_code, points in team_points.items():
                    if points > scotland_final_points:
                        teams_above += 1
                        if team_code in self.uefa_teams:
                            uefa_teams_above += 1
                
                # Add non-UEFA teams above Scotland (from original rankings)
                for team_code, team_data in self.fifa_rankings.items():
                    if team_code not in self.uefa_teams and team_data['points'] > scotland_final_points:
                        teams_above += 1
                
                scotland_rank = teams_above + 1
                scotland_change = scotland_final_points - initial_points['SCO']
                
                scotland_outcomes.append({
                    'rank': scotland_rank,
                    'points': scotland_final_points,
                    'change': scotland_change,
                    'uefa_teams_above': uefa_teams_above
                })
            
            if sampled_scenarios >= scenario_count:
                break
        
        print(f"✅ Analyzed {sampled_scenarios:,} scenarios")
        return scotland_outcomes
    
    def analyze_scotland_movement(self):
        """Analyze Scotland's potential ranking movement"""
        print("🏴󠁧󠁢󠁳󠁣󠁴󠁿 SCOTLAND UEFA RANKING MOVEMENT ANALYSIS")
        print("=" * 60)
        
        # Get current Scotland info
        scotland_current = self.fifa_rankings.get('SCO', {})
        current_rank = scotland_current.get('rank', 'Unknown')
        current_points = scotland_current.get('points', 0)
        
        print(f"📊 Current Position: #{current_rank} ({current_points} points)")
        
        # Identify UEFA teams
        self.identify_uefa_teams()
        
        # Get UEFA rankings around Scotland
        uefa_rankings = self.get_uefa_rankings()
        
        print(f"\n🌍 UEFA Teams Around Scotland:")
        print("-" * 40)
        
        scotland_uefa_rank = None
        for i, team in enumerate(uefa_rankings):
            if team['code'] == 'SCO':
                scotland_uefa_rank = i + 1
                start_idx = max(0, i - 5)
                end_idx = min(len(uefa_rankings), i + 6)
                
                for j in range(start_idx, end_idx):
                    marker = "👉" if j == i else "  "
                    team_info = uefa_rankings[j]
                    print(f"{marker} #{team_info['rank']:2d} {team_info['team']:<20} ({team_info['points']:7.2f} pts)")
                break
        
        print(f"\n🎯 Scotland's UEFA Position: #{scotland_uefa_rank} of {len(uefa_rankings)} UEFA teams")
        
        # Simulate all scenarios
        print(f"\n🎲 SCENARIO SIMULATION:")
        print("-" * 30)
        
        outcomes = self.simulate_all_scenarios()
        
        if not outcomes:
            print("❌ No scenarios generated")
            return
        
        # Analyze outcomes
        best_rank = min(outcome['rank'] for outcome in outcomes)
        worst_rank = max(outcome['rank'] for outcome in outcomes)
        best_points = max(outcome['points'] for outcome in outcomes)
        worst_points = min(outcome['points'] for outcome in outcomes)
        best_change = max(outcome['change'] for outcome in outcomes)
        worst_change = min(outcome['change'] for outcome in outcomes)
        
        avg_rank = sum(outcome['rank'] for outcome in outcomes) / len(outcomes)
        avg_points = sum(outcome['points'] for outcome in outcomes) / len(outcomes)
        avg_change = sum(outcome['change'] for outcome in outcomes) / len(outcomes)
        
        print(f"📈 RANKING MOVEMENT POTENTIAL:")
        print(f"   Best possible rank: #{best_rank} (up {current_rank - best_rank} places)")
        print(f"   Worst possible rank: #{worst_rank} (down {worst_rank - current_rank} places)")
        print(f"   Average rank: #{avg_rank:.1f}")
        
        print(f"\n⚡ POINTS MOVEMENT:")
        print(f"   Best points: {best_points:.2f} ({best_change:+.2f})")
        print(f"   Worst points: {worst_points:.2f} ({worst_change:+.2f})")
        print(f"   Average points: {avg_points:.2f} ({avg_change:+.2f})")
        
        # Analyze probability distribution
        rank_improvements = sum(1 for outcome in outcomes if outcome['rank'] < current_rank)
        rank_declines = sum(1 for outcome in outcomes if outcome['rank'] > current_rank)
        rank_same = len(outcomes) - rank_improvements - rank_declines
        
        print(f"\n📊 OUTCOME PROBABILITIES:")
        print(f"   Rank improvement: {rank_improvements/len(outcomes)*100:.1f}% ({rank_improvements:,} scenarios)")
        print(f"   Rank decline: {rank_declines/len(outcomes)*100:.1f}% ({rank_declines:,} scenarios)")
        print(f"   Rank unchanged: {rank_same/len(outcomes)*100:.1f}% ({rank_same:,} scenarios)")
        
        # Analyze UEFA-specific movements
        uefa_teams_catchable = []
        uefa_teams_threatening = []
        
        for team in uefa_rankings:
            if team['code'] == 'SCO':
                continue
            
            # Teams Scotland could potentially catch
            if team['rank'] < current_rank and team['points'] < best_points:
                uefa_teams_catchable.append(team)
            
            # Teams that could potentially overtake Scotland
            if team['rank'] > current_rank and team['points'] > worst_points:
                uefa_teams_threatening.append(team)
        
        print(f"\n🎯 UEFA TEAMS SCOTLAND COULD CATCH:")
        print("-" * 40)
        for team in uefa_teams_catchable[:10]:  # Show top 10
            gap = team['points'] - current_points
            print(f"   #{team['rank']:2d} {team['team']:<20} ({team['points']:7.2f} pts, gap: {gap:+.2f})")
        
        print(f"\n⚠️  UEFA TEAMS THAT COULD OVERTAKE SCOTLAND:")
        print("-" * 45)
        for team in uefa_teams_threatening[:10]:  # Show top 10
            gap = current_points - team['points']
            print(f"   #{team['rank']:2d} {team['team']:<20} ({team['points']:7.2f} pts, gap: {gap:+.2f})")
        
        return {
            'current_rank': current_rank,
            'current_points': current_points,
            'best_rank': best_rank,
            'worst_rank': worst_rank,
            'best_points': best_points,
            'worst_points': worst_points,
            'rank_improvement_probability': rank_improvements/len(outcomes),
            'rank_decline_probability': rank_declines/len(outcomes),
            'catchable_teams': len(uefa_teams_catchable),
            'threatening_teams': len(uefa_teams_threatening)
        }

def main():
    analyzer = UEFARankingAnalyzer()
    results = analyzer.analyze_scotland_movement()
    
    print(f"\n🏆 SUMMARY:")
    print("-" * 20)
    print(f"Scotland can move between ranks #{results['best_rank']}-#{results['worst_rank']}")
    print(f"Points range: {results['worst_points']:.2f} to {results['best_points']:.2f}")
    print(f"Most likely outcome: Rank improvement ({results['rank_improvement_probability']*100:.1f}% chance)")

if __name__ == "__main__":
    main()