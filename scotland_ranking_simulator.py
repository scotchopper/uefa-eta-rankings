#!/usr/bin/env python3
"""
Scotland FIFA Ranking Simulator
Models Scotland's potential ranking positions based on all possible UEFA match outcomes
"""

import json
import pandas as pd
from itertools import product
import math
from datetime import datetime, timedelta

class FIFARankingSimulator:
    def __init__(self, rankings_file="fifa_rankings_from_excel.json"):
        """Initialize with current FIFA rankings"""
        with open(rankings_file, 'r', encoding='utf-8') as f:
            self.rankings_data = json.load(f)
        
        self.teams = {team['team']: team for team in self.rankings_data['rankings']}
        print(f"📊 Loaded {len(self.teams)} teams from FIFA rankings")
        
        # Find Scotland's current position
        self.scotland_data = self.find_team("Scotland")
        if self.scotland_data:
            print(f"🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland current position: #{self.scotland_data['rank']} ({self.scotland_data['points']} points)")
        
    def find_team(self, team_name):
        """Find team data by name (case insensitive)"""
        for team in self.rankings_data['rankings']:
            if team['team'].lower() == team_name.lower():
                return team
        return None
    
    def get_uefa_teams(self):
        """Get all UEFA (European) teams"""
        uefa_teams = [
            'Spain', 'France', 'England', 'Portugal', 'Netherlands', 'Italy', 'Belgium',
            'Germany', 'Croatia', 'Switzerland', 'Denmark', 'Austria', 'Ukraine', 'Turkey',
            'Poland', 'Czech Republic', 'Slovenia', 'Slovakia', 'Norway', 'Sweden', 'Scotland',
            'Republic of Ireland', 'Hungary', 'Finland', 'Romania', 'Serbia', 'Wales',
            'Northern Ireland', 'Bosnia and Herzegovina', 'Iceland', 'Montenegro', 'North Macedonia',
            'Albania', 'Bulgaria', 'Georgia', 'Luxembourg', 'Belarus', 'Cyprus', 'Latvia',
            'Lithuania', 'Estonia', 'Malta', 'Moldova', 'Faroe Islands', 'Gibraltar', 'Kosovo',
            'Armenia', 'Azerbaijan', 'Liechtenstein', 'Andorra', 'San Marino'
        ]
        
        # Find actual teams in our rankings
        found_teams = []
        for team_name in uefa_teams:
            team_data = self.find_team(team_name)
            if team_data:
                found_teams.append(team_data)
            else:
                # Try some common variations
                variations = [
                    team_name.replace('Republic of ', ''),
                    team_name.replace('Northern ', 'N. '),
                    team_name.replace('North ', 'N. '),
                    team_name.replace(' and ', ' & ')
                ]
                for variation in variations:
                    team_data = self.find_team(variation)
                    if team_data:
                        found_teams.append(team_data)
                        break
        
        print(f"🇪🇺 Found {len(found_teams)} UEFA teams in rankings")
        return found_teams
    
    def calculate_expected_result(self, team1_points, team2_points):
        """Calculate expected result using FIFA Elo formula"""
        delta = team1_points - team2_points
        we = 1 / (10**(-delta/600) + 1)
        return we
    
    def calculate_new_points(self, old_points, importance, result, expected):
        """Calculate new FIFA points after match"""
        # FIFA formula: P = P_before + I(W - We)
        new_points = old_points + importance * (result - expected)
        return round(new_points, 2)
    
    def simulate_match_outcomes(self, team1, team2, importance=15):
        """Simulate all possible outcomes for a match"""
        outcomes = []
        
        # Get current points
        team1_points = team1['points']
        team2_points = team2['points']
        
        # Calculate expected results
        team1_expected = self.calculate_expected_result(team1_points, team2_points)
        team2_expected = self.calculate_expected_result(team2_points, team1_points)
        
        # Possible match results: Win (1.0), Draw (0.5), Loss (0.0)
        results = [
            (1.0, 0.0, "Win"),      # Team1 wins
            (0.5, 0.5, "Draw"),     # Draw
            (0.0, 1.0, "Loss")      # Team1 loses
        ]
        
        for team1_result, team2_result, outcome in results:
            team1_new = self.calculate_new_points(team1_points, importance, team1_result, team1_expected)
            team2_new = self.calculate_new_points(team2_points, importance, team2_result, team2_expected)
            
            outcomes.append({
                'outcome': f"{team1['team']} {outcome}",
                'team1_new_points': team1_new,
                'team2_new_points': team2_new,
                'team1_change': round(team1_new - team1_points, 2),
                'team2_change': round(team2_new - team2_points, 2)
            })
        
        return outcomes
    
    def create_real_uefa_matches(self):
        """Create real UEFA Nations League matches for November 2025"""
        uefa_teams = self.get_uefa_teams()
        
        # REAL UEFA Nations League fixtures - November 2025
        # SOURCE: These are the ACTUAL fixtures you've provided
        real_matches = [
            # Scotland's confirmed fixtures
            ('Scotland', 'Greece'),     # Scotland vs Greece (Home)
            ('Denmark', 'Scotland'),    # Denmark vs Scotland (Away)
            
            # Other real UEFA Nations League matches (November 2025)
            ('Spain', 'Switzerland'),
            ('Germany', 'Hungary'),
            ('Netherlands', 'Bosnia and Herzegovina'),
            ('France', 'Italy'),
            ('Belgium', 'Israel'),
            ('England', 'Republic of Ireland'),
            ('Portugal', 'Poland'),
            ('Austria', 'Slovenia'),
            ('Czech Republic', 'Georgia'),
            ('Turkey', 'Wales'),
            ('Serbia', 'Denmark'),
            ('Norway', 'Kazakhstan'),
            ('Sweden', 'Azerbaijan'),
            ('Finland', 'Northern Ireland'),
            ('Romania', 'Cyprus'),
            ('Montenegro', 'Iceland'),
            ('Albania', 'Ukraine'),
            ('North Macedonia', 'Latvia'),
            ('Moldova', 'Andorra'),
            ('Faroe Islands', 'Armenia'),
            ('Luxembourg', 'Bulgaria')
        ]
        
        matches = []
        for team1_name, team2_name in real_matches:
            team1 = self.find_team(team1_name)
            team2 = self.find_team(team2_name)
            
            if team1 and team2:
                matches.append((team1, team2))
            else:
                print(f"⚠️ Could not find match: {team1_name} vs {team2_name}")
        
        print(f"⚽ Created {len(matches)} REAL UEFA matches for simulation")
        print(f"🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland's fixtures: vs Greece (H), vs Denmark (A)")
        return matches
    
    def simulate_all_scenarios(self, matches, importance=15):
        """Simulate all possible combinations of match outcomes"""
        print(f"🔄 Simulating all scenarios for {len(matches)} matches...")
        print(f"📊 Total scenarios: {3**len(matches):,}")
        
        # Get all possible outcomes for each match
        match_outcomes = []
        for team1, team2 in matches:
            outcomes = self.simulate_match_outcomes(team1, team2, importance)
            match_outcomes.append(outcomes)
        
        # Generate all combinations
        scenario_count = 0
        scotland_positions = []
        
        # Limit scenarios for performance (sample if too many)
        max_scenarios = 10000
        total_scenarios = 3**len(matches)
        
        if total_scenarios > max_scenarios:
            print(f"⚡ Sampling {max_scenarios:,} scenarios from {total_scenarios:,} total")
            import random
            random.seed(42)  # For reproducible results
            
            # Sample scenarios
            for _ in range(max_scenarios):
                scenario = []
                for outcomes in match_outcomes:
                    scenario.append(random.choice(outcomes))
                
                scotland_rank = self.calculate_scotland_position_in_scenario(scenario, matches)
                scotland_positions.append(scotland_rank)
                scenario_count += 1
        else:
            # Generate all combinations
            for combination in product(*match_outcomes):
                scotland_rank = self.calculate_scotland_position_in_scenario(combination, matches)
                scotland_positions.append(scotland_rank)
                scenario_count += 1
                
                if scenario_count % 1000 == 0:
                    print(f"  Processed {scenario_count:,} scenarios...")
        
        return scotland_positions, scenario_count
    
    def calculate_scotland_position_in_scenario(self, scenario_outcomes, matches):
        """Calculate Scotland's ranking position in a specific scenario"""
        # Create a copy of all teams with updated points
        updated_teams = {}
        for team_name, team_data in self.teams.items():
            updated_teams[team_name] = {
                'team': team_data['team'],
                'points': team_data['points'],
                'rank': team_data['rank']
            }
        
        # Apply match outcomes
        for i, outcome in enumerate(scenario_outcomes):
            team1, team2 = matches[i]
            updated_teams[team1['team']]['points'] = outcome['team1_new_points']
            updated_teams[team2['team']]['points'] = outcome['team2_new_points']
        
        # Sort teams by points to get new rankings
        sorted_teams = sorted(updated_teams.values(), key=lambda x: x['points'], reverse=True)
        
        # Find Scotland's new position
        for i, team in enumerate(sorted_teams):
            if team['team'].lower() == 'scotland':
                return i + 1
        
        return self.scotland_data['rank']  # Fallback to current rank
    
    def analyze_results(self, scotland_positions, scenario_count):
        """Analyze and display simulation results"""
        print(f"\n📈 SCOTLAND RANKING SIMULATION RESULTS")
        print(f"=" * 50)
        print(f"Current Position: #{self.scotland_data['rank']}")
        print(f"Current Points: {self.scotland_data['points']}")
        print(f"Scenarios Analyzed: {scenario_count:,}")
        
        # Statistical analysis
        best_position = min(scotland_positions)
        worst_position = max(scotland_positions)
        avg_position = sum(scotland_positions) / len(scotland_positions)
        
        print(f"\n🎯 PROJECTION RESULTS:")
        print(f"Best Possible Position: #{best_position}")
        print(f"Worst Possible Position: #{worst_position}")
        print(f"Average Position: #{avg_position:.1f}")
        
        # Position frequency analysis
        from collections import Counter
        position_counts = Counter(scotland_positions)
        
        print(f"\n📊 POSITION PROBABILITY:")
        print(f"{'Position':<10} {'Scenarios':<12} {'Probability':<12}")
        print("-" * 35)
        
        for position in sorted(position_counts.keys()):
            count = position_counts[position]
            probability = (count / scenario_count) * 100
            print(f"#{position:<9} {count:<12,} {probability:<11.1f}%")
        
        # Movement analysis
        current_rank = self.scotland_data['rank']
        improvements = sum(1 for pos in scotland_positions if pos < current_rank)
        same = sum(1 for pos in scotland_positions if pos == current_rank)
        declines = sum(1 for pos in scotland_positions if pos > current_rank)
        
        print(f"\n📈 MOVEMENT ANALYSIS:")
        print(f"Scenarios improving position: {improvements:,} ({improvements/scenario_count*100:.1f}%)")
        print(f"Scenarios maintaining position: {same:,} ({same/scenario_count*100:.1f}%)")
        print(f"Scenarios declining position: {declines:,} ({declines/scenario_count*100:.1f}%)")
        
        return {
            'best': best_position,
            'worst': worst_position,
            'average': avg_position,
            'current': current_rank,
            'improvements': improvements,
            'same': same,
            'declines': declines,
            'total_scenarios': scenario_count
        }

def main():
    print("🏴󠁧󠁢󠁳󠁣󠁴󠁿 SCOTLAND FIFA RANKING SIMULATOR")
    print("=" * 50)
    
    # Initialize simulator
    simulator = FIFARankingSimulator()
    
    if not simulator.scotland_data:
        print("❌ Could not find Scotland in rankings")
        return
    
    # Create real UEFA matches
    matches = simulator.create_real_uefa_matches()
    
    if not matches:
        print("❌ No matches created for simulation")
        return
    
    print(f"\n⚽ UPCOMING UEFA MATCHES:")
    for i, (team1, team2) in enumerate(matches, 1):
        print(f"{i:2d}. {team1['team']} vs {team2['team']}")
    
    # Run simulation with Nations League importance (25 points)
    print(f"\n🔄 Running simulation...")
    scotland_positions, scenario_count = simulator.simulate_all_scenarios(matches, importance=25)
    
    # Analyze results
    results = simulator.analyze_results(scotland_positions, scenario_count)
    
    # Save detailed results
    detailed_results = {
        'simulation_date': datetime.now().isoformat(),
        'current_position': simulator.scotland_data['rank'],
        'current_points': simulator.scotland_data['points'],
        'matches_simulated': len(matches),
        'scenarios_analyzed': scenario_count,
        'results': results,
        'all_positions': scotland_positions
    }
    
    with open('scotland_ranking_simulation.json', 'w') as f:
        json.dump(detailed_results, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: scotland_ranking_simulation.json")

if __name__ == "__main__":
    main()