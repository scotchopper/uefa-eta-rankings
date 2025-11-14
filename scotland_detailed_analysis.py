#!/usr/bin/env python3
"""
Enhanced Scotland FIFA Ranking Analysis
Detailed scenario analysis with specific outcome requirements
"""

import json
import pandas as pd
from collections import defaultdict, Counter
from datetime import datetime

class ScotlandRankingAnalyzer:
    def __init__(self, simulation_file="scotland_ranking_simulation.json", rankings_file="fifa_rankings_from_excel.json"):
        """Initialize with simulation results and current rankings"""
        
        # Load simulation results
        with open(simulation_file, 'r') as f:
            self.simulation_data = json.load(f)
        
        # Load current rankings
        with open(rankings_file, 'r') as f:
            self.rankings_data = json.load(f)
        
        self.teams = {team['team']: team for team in self.rankings_data['rankings']}
        self.scotland_data = self.find_team("Scotland")
        
        print(f"📊 Loaded simulation data: {self.simulation_data['scenarios_analyzed']:,} scenarios")
        print(f"🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland: #{self.scotland_data['rank']} ({self.scotland_data['points']} pts)")
    
    def find_team(self, team_name):
        """Find team data by name"""
        for team in self.rankings_data['rankings']:
            if team['team'].lower() == team_name.lower():
                return team
        return None
    
    def get_teams_around_scotland(self, range_positions=5):
        """Get teams around Scotland's current position"""
        current_rank = self.scotland_data['rank']
        
        teams_around = []
        for team in self.rankings_data['rankings']:
            if abs(team['rank'] - current_rank) <= range_positions:
                teams_around.append(team)
        
        return sorted(teams_around, key=lambda x: x['rank'])
    
    def analyze_position_changes(self):
        """Analyze what drives Scotland's position changes"""
        print(f"\n🔍 DETAILED RANKING ANALYSIS")
        print(f"=" * 50)
        
        # Current position context
        current_rank = self.scotland_data['rank']
        current_points = self.scotland_data['points']
        
        print(f"Current Situation:")
        print(f"  Position: #{current_rank}")
        print(f"  Points: {current_points}")
        
        # Teams around Scotland
        nearby_teams = self.get_teams_around_scotland(3)
        print(f"\n🎯 TEAMS AROUND SCOTLAND:")
        print(f"{'Rank':<6} {'Team':<25} {'Points':<10} {'Gap':<10}")
        print("-" * 55)
        
        for team in nearby_teams:
            gap = team['points'] - current_points
            gap_str = f"{gap:+.2f}" if gap != 0 else "0.00"
            marker = " 🏴󠁧󠁢󠁳󠁣󠁴󠁿" if team['team'] == 'Scotland' else ""
            print(f"#{team['rank']:<5} {team['team']:<25} {team['points']:<10.2f} {gap_str:<10}{marker}")
        
        # Points needed for position changes
        teams_above = [t for t in nearby_teams if t['rank'] < current_rank]
        teams_below = [t for t in nearby_teams if t['rank'] > current_rank]
        
        if teams_above:
            next_team_above = min(teams_above, key=lambda x: x['rank'])
            points_to_overtake = next_team_above['points'] - current_points + 0.01
            print(f"\n📈 TO IMPROVE POSITION:")
            print(f"  Need {points_to_overtake:.2f} points to overtake {next_team_above['team']} (#{next_team_above['rank']})")
        
        if teams_below:
            next_team_below = max(teams_below, key=lambda x: x['rank'])
            points_to_avoid_drop = current_points - next_team_below['points']
            print(f"\n📉 TO AVOID DROPPING:")
            print(f"  Must stay within {points_to_avoid_drop:.2f} points of {next_team_below['team']} (#{next_team_below['rank']})")
    
    def analyze_scotland_match_impact(self):
        """Analyze the impact of Scotland's specific match"""
        print(f"\n⚽ SCOTLAND'S MATCH IMPACT ANALYSIS")
        print(f"=" * 50)
        
        # Simulate Scotland vs Poland outcomes
        scotland = self.scotland_data
        poland = self.find_team("Poland")
        
        if not poland:
            print("❌ Could not find Poland in rankings")
            return
        
        print(f"Scotland vs Poland:")
        print(f"  Scotland: #{scotland['rank']} ({scotland['points']} pts)")
        print(f"  Poland: #{poland['rank']} ({poland['points']} pts)")
        
        # Calculate expected results and point changes
        delta = scotland['points'] - poland['points']
        scotland_expected = 1 / (10**(-delta/600) + 1)
        poland_expected = 1 - scotland_expected
        
        importance = 15  # Nations League matches
        
        outcomes = [
            (1.0, 0.0, "Scotland Win"),
            (0.5, 0.5, "Draw"),
            (0.0, 1.0, "Scotland Loss")
        ]
        
        print(f"\n📊 POSSIBLE OUTCOMES:")
        print(f"{'Outcome':<15} {'Scotland Points':<15} {'Change':<10} {'Impact'}")
        print("-" * 60)
        
        for scot_result, pol_result, outcome_name in outcomes:
            new_points = scotland['points'] + importance * (scot_result - scotland_expected)
            change = new_points - scotland['points']
            
            if change > 5:
                impact = "🚀 Major boost"
            elif change > 0:
                impact = "📈 Positive"
            elif change == 0:
                impact = "➡️ Neutral"
            elif change > -5:
                impact = "📉 Negative"
            else:
                impact = "💥 Major drop"
            
            print(f"{outcome_name:<15} {new_points:<15.2f} {change:+.2f}     {impact}")
    
    def find_best_case_scenarios(self, target_position=35):
        """Find what results would lead to target position"""
        print(f"\n🎯 BEST CASE SCENARIO ANALYSIS")
        print(f"=" * 50)
        
        positions = self.simulation_data['all_positions']
        best_positions = [pos for pos in positions if pos <= target_position]
        
        print(f"Target: Reach position #{target_position} or better")
        print(f"Scenarios achieving target: {len(best_positions):,} out of {len(positions):,}")
        print(f"Probability: {len(best_positions)/len(positions)*100:.1f}%")
        
        if len(best_positions) > 0:
            best_possible = min(positions)
            print(f"Best possible position: #{best_possible}")
            
            # Count how often each position occurs in best cases
            best_position_counts = Counter(best_positions)
            print(f"\n📊 DISTRIBUTION OF GOOD OUTCOMES:")
            for pos in sorted(best_position_counts.keys()):
                count = best_position_counts[pos]
                pct = count / len(best_positions) * 100
                print(f"  Position #{pos}: {count:,} scenarios ({pct:.1f}% of good outcomes)")
    
    def create_summary_report(self):
        """Create a comprehensive summary report"""
        print(f"\n📋 EXECUTIVE SUMMARY")
        print(f"=" * 50)
        
        current_rank = self.scotland_data['rank']
        results = self.simulation_data['results']
        
        # Key statistics
        improvement_chance = results['improvements'] / results['total_scenarios'] * 100
        decline_chance = results['declines'] / results['total_scenarios'] * 100
        
        print(f"🏴󠁧󠁢󠁳󠁣󠁴󠁿 SCOTLAND RANKING OUTLOOK:")
        print(f"  Current Position: #{current_rank}")
        print(f"  Best Case: #{results['best']}")
        print(f"  Worst Case: #{results['worst']}")
        print(f"  Most Likely: #{results['average']:.0f}")
        
        print(f"\n📊 PROBABILITY BREAKDOWN:")
        print(f"  Improve Position: {improvement_chance:.1f}%")
        print(f"  Stay Same: {results['same']/results['total_scenarios']*100:.1f}%")
        print(f"  Drop Position: {decline_chance:.1f}%")
        
        print(f"\n⚡ KEY INSIGHTS:")
        if improvement_chance > 50:
            print(f"  ✅ Scotland is likely to improve their ranking")
        elif improvement_chance > 30:
            print(f"  🟡 Scotland has a good chance to improve")
        else:
            print(f"  🔴 Scotland faces an uphill battle to improve")
        
        if decline_chance > 50:
            print(f"  ⚠️ High risk of dropping in rankings")
        elif decline_chance > 30:
            print(f"  🟡 Moderate risk of position loss")
        else:
            print(f"  ✅ Low risk of significant decline")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        print(f"  🎯 Target: Beat Poland to maximize improvement chances")
        print(f"  📈 Minimum: Draw with Poland to limit downside risk")
        print(f"  🤞 Hope for: Upsets by teams ranked above Scotland")

def main():
    print("🏴󠁧󠁢󠁳󠁣󠁴󠁿 SCOTLAND FIFA RANKING - DETAILED ANALYSIS")
    print("=" * 60)
    
    try:
        analyzer = ScotlandRankingAnalyzer()
        
        # Run all analyses
        analyzer.analyze_position_changes()
        analyzer.analyze_scotland_match_impact()
        analyzer.find_best_case_scenarios(35)
        analyzer.create_summary_report()
        
        print(f"\n✅ Analysis complete!")
        
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        print("💡 Make sure to run the simulator first: python scotland_ranking_simulator.py")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()