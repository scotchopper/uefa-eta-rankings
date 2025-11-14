#!/usr/bin/env python3
"""
Scotland vs Greece & Denmark - Specific Scenario Analysis
Real fixtures with detailed outcome predictions
"""

import json
from datetime import datetime

class ScotlandSpecificAnalysis:
    def __init__(self, rankings_file="fifa_rankings_from_excel.json"):
        with open(rankings_file, 'r', encoding='utf-8') as f:
            self.rankings_data = json.load(f)
        
        self.teams = {team['team']: team for team in self.rankings_data['rankings']}
        self.scotland = self.find_team("Scotland")
        self.greece = self.find_team("Greece")
        self.denmark = self.find_team("Denmark")
        
        print("🏴󠁧󠁢󠁳󠁣󠁴󠁿 SCOTLAND'S REAL FIXTURES ANALYSIS")
        print("=" * 50)
        print("📅 FIXTURE SOURCE: UEFA Nations League November 2025")
        print("🏆 Competition: UEFA Nations League (Importance: 25 points)")
        print("")
        
    def find_team(self, team_name):
        for team in self.rankings_data['rankings']:
            if team['team'].lower() == team_name.lower():
                return team
        return None
    
    def calculate_expected_result(self, team1_points, team2_points):
        delta = team1_points - team2_points
        we = 1 / (10**(-delta/600) + 1)
        return we
    
    def calculate_new_points(self, old_points, importance, result, expected):
        return round(old_points + importance * (result - expected), 2)
    
    def show_fixture_details(self):
        print("⚽ SCOTLAND'S CONFIRMED FIXTURES:")
        print("-" * 40)
        
        if self.scotland and self.greece:
            print(f"🏠 MATCH 1: Scotland vs Greece (HOME)")
            print(f"   Scotland: #{self.scotland['rank']} ({self.scotland['points']} pts)")
            print(f"   Greece: #{self.greece['rank']} ({self.greece['points']} pts)")
            print(f"   Points Gap: {self.scotland['points'] - self.greece['points']:+.2f}")
        
        if self.scotland and self.denmark:
            print(f"\n✈️ MATCH 2: Denmark vs Scotland (AWAY)")
            print(f"   Scotland: #{self.scotland['rank']} ({self.scotland['points']} pts)")
            print(f"   Denmark: #{self.denmark['rank']} ({self.denmark['points']} pts)")
            print(f"   Points Gap: {self.scotland['points'] - self.denmark['points']:+.2f}")
    
    def analyze_match_outcomes(self):
        print(f"\n📊 DETAILED MATCH ANALYSIS")
        print("=" * 50)
        
        # Match 1: Scotland vs Greece
        if self.scotland and self.greece:
            print(f"🏠 SCOTLAND vs GREECE (HOME)")
            self.analyze_single_match(self.scotland, self.greece, "Scotland", "Greece")
        
        # Match 2: Denmark vs Scotland
        if self.scotland and self.denmark:
            print(f"\n✈️ DENMARK vs SCOTLAND (AWAY)")
            self.analyze_single_match(self.denmark, self.scotland, "Denmark", "Scotland")
    
    def analyze_single_match(self, team1, team2, team1_name, team2_name):
        importance = 25  # Nations League
        
        # Calculate expected results
        team1_expected = self.calculate_expected_result(team1['points'], team2['points'])
        team2_expected = 1 - team1_expected
        
        print(f"Current Points: {team1_name} {team1['points']}, {team2_name} {team2['points']}")
        print(f"Expected Win Probability: {team1_name} {team1_expected:.1%}, {team2_name} {team2_expected:.1%}")
        
        outcomes = [
            (1.0, 0.0, f"{team1_name} Win"),
            (0.5, 0.5, "Draw"),
            (0.0, 1.0, f"{team2_name} Win")
        ]
        
        print(f"\n{'Outcome':<20} {'Scotland New':<12} {'Change':<8} {'Impact'}")
        print("-" * 55)
        
        for team1_result, team2_result, outcome_name in outcomes:
            team1_new = self.calculate_new_points(team1['points'], importance, team1_result, team1_expected)
            team2_new = self.calculate_new_points(team2['points'], importance, team2_result, team2_expected)
            
            # Find Scotland's change
            if team1_name == "Scotland":
                scotland_new = team1_new
                scotland_change = team1_new - team1['points']
            else:
                scotland_new = team2_new
                scotland_change = team2_new - team2['points']
            
            # Impact assessment
            if scotland_change >= 10:
                impact = "🚀 Massive boost"
            elif scotland_change >= 5:
                impact = "📈 Big gain"
            elif scotland_change > 0:
                impact = "✅ Positive"
            elif scotland_change == 0:
                impact = "➡️ Neutral"
            elif scotland_change >= -5:
                impact = "📉 Small loss"
            else:
                impact = "💥 Big drop"
            
            print(f"{outcome_name:<20} {scotland_new:<12.2f} {scotland_change:+.2f}     {impact}")
    
    def analyze_combined_scenarios(self):
        print(f"\n🎯 ALL POSSIBLE COMBINED OUTCOMES")
        print("=" * 60)
        
        if not (self.scotland and self.greece and self.denmark):
            print("❌ Missing team data for complete analysis")
            return
        
        importance = 25
        
        # Calculate expected results for both matches
        scot_greece_expected = self.calculate_expected_result(self.scotland['points'], self.greece['points'])
        den_scot_expected = self.calculate_expected_result(self.denmark['points'], self.scotland['points'])
        scot_den_expected = 1 - den_scot_expected
        
        # All possible outcomes
        match1_outcomes = [
            (1.0, 0.0, "W"),  # Scotland beats Greece
            (0.5, 0.5, "D"),  # Scotland draws with Greece
            (0.0, 1.0, "L")   # Scotland loses to Greece
        ]
        
        match2_outcomes = [
            (0.0, 1.0, "W"),  # Scotland beats Denmark (away)
            (0.5, 0.5, "D"),  # Scotland draws with Denmark
            (1.0, 0.0, "L")   # Scotland loses to Denmark
        ]
        
        print(f"{'Match 1':<8} {'Match 2':<8} {'Final Points':<12} {'Total Change':<12} {'Outlook'}")
        print("-" * 70)
        
        scenarios = []
        
        for m1_result, m1_opp_result, m1_code in match1_outcomes:
            for m2_home_result, m2_result, m2_code in match2_outcomes:
                # After Match 1 (vs Greece)
                points_after_m1 = self.calculate_new_points(
                    self.scotland['points'], importance, m1_result, scot_greece_expected
                )
                
                # After Match 2 (vs Denmark)
                final_points = self.calculate_new_points(
                    points_after_m1, importance, m2_result, scot_den_expected
                )
                
                total_change = final_points - self.scotland['points']
                
                # Create outlook
                if total_change >= 15:
                    outlook = "🚀 Excellent"
                elif total_change >= 8:
                    outlook = "📈 Very Good"
                elif total_change >= 3:
                    outlook = "✅ Good"
                elif total_change >= -3:
                    outlook = "➡️ Neutral"
                elif total_change >= -8:
                    outlook = "📉 Poor"
                else:
                    outlook = "💥 Very Poor"
                
                scenario_desc = f"vs GRE: {m1_code}  vs DEN: {m2_code}"
                scenarios.append((scenario_desc, final_points, total_change, outlook))
                
                print(f"{m1_code:<8} {m2_code:<8} {final_points:<12.2f} {total_change:+.2f}          {outlook}")
        
        # Find best and worst scenarios
        scenarios.sort(key=lambda x: x[2], reverse=True)  # Sort by change
        
        print(f"\n🏆 BEST CASE SCENARIO:")
        print(f"   {scenarios[0][0]}: {scenarios[0][1]:.2f} points ({scenarios[0][2]:+.2f})")
        
        print(f"\n💀 WORST CASE SCENARIO:")
        print(f"   {scenarios[-1][0]}: {scenarios[-1][1]:.2f} points ({scenarios[-1][2]:+.2f})")
        
        # Most likely scenarios
        realistic_scenarios = [s for s in scenarios if abs(s[2]) <= 15]  # Realistic range
        print(f"\n📊 REALISTIC RANGE:")
        print(f"   Best realistic: {realistic_scenarios[0][1]:.2f} pts ({realistic_scenarios[0][2]:+.2f})")
        print(f"   Worst realistic: {realistic_scenarios[-1][1]:.2f} pts ({realistic_scenarios[-1][2]:+.2f})")

def main():
    print("🏴󠁧󠁢󠁳󠁣󠁴󠁿 SCOTLAND SPECIFIC MATCH ANALYSIS")
    print("Real fixtures: Greece (H) & Denmark (A)")
    print("=" * 60)
    
    analyzer = ScotlandSpecificAnalysis()
    
    analyzer.show_fixture_details()
    analyzer.analyze_match_outcomes()
    analyzer.analyze_combined_scenarios()
    
    print(f"\n📋 FIXTURE SOURCE CONFIRMATION:")
    print(f"✅ Scotland vs Greece (HOME) - UEFA Nations League")
    print(f"✅ Denmark vs Scotland (AWAY) - UEFA Nations League")
    print(f"⚽ Competition: UEFA Nations League (25 points importance)")
    print(f"📅 Match Window: November 2025")

if __name__ == "__main__":
    main()