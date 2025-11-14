#!/usr/bin/env python3
"""
Scotland World Cup Qualifier Analysis - Sequential Match Effects
Factors in Denmark vs Belarus happening before Denmark vs Scotland
"""

import json
from datetime import datetime

class SequentialMatchAnalyzer:
    def __init__(self, rankings_file="fifa_rankings_from_excel.json"):
        with open(rankings_file, 'r', encoding='utf-8') as f:
            self.rankings_data = json.load(f)
        
        self.teams = {team['team']: team for team in self.rankings_data['rankings']}
        self.scotland = self.find_team("Scotland")
        self.greece = self.find_team("Greece")
        self.denmark = self.find_team("Denmark")
        self.belarus = self.find_team("Belarus")
        
        print("🏆 WORLD CUP QUALIFIER ANALYSIS - SEQUENTIAL MATCHES")
        print("=" * 60)
        print("📅 Competition: FIFA World Cup Qualifiers (Importance: 25 points)")
        print("⚽ Match Window: November 2025")
        print("")
        
    def find_team(self, team_name):
        for team in self.rankings_data['rankings']:
            if team['team'].lower() == team_name.lower():
                return team
        # Try variations
        variations = [team_name.replace('Republic of ', ''), team_name + ' Republic']
        for variation in variations:
            for team in self.rankings_data['rankings']:
                if team['team'].lower() == variation.lower():
                    return team
        return None
    
    def calculate_expected_result(self, team1_points, team2_points):
        delta = team1_points - team2_points
        we = 1 / (10**(-delta/600) + 1)
        return we
    
    def calculate_new_points(self, old_points, importance, result, expected):
        return round(old_points + importance * (result - expected), 2)
    
    def show_match_schedule(self):
        print("📅 MATCH SCHEDULE & SEQUENTIAL EFFECTS:")
        print("-" * 50)
        
        if self.scotland and self.greece:
            print(f"🏴󠁧󠁢󠁳󠁣󠁴󠁿 SIMULTANEOUS MATCHES (Round 1):")
            print(f"   Scotland vs Greece")
            print(f"   Denmark vs Belarus")
        
        print(f"\n⏭️ SUBSEQUENT MATCH (Round 2):")
        print(f"   Denmark vs Scotland (Denmark's points will be updated)")
        
        if not self.belarus:
            print(f"\n⚠️ Warning: Could not find Belarus in rankings")
            print(f"💡 Will use estimated Belarus data for Denmark calculation")
    
    def analyze_denmark_belarus_impact(self):
        print(f"\n🇩🇰 DENMARK vs BELARUS IMPACT ANALYSIS")
        print("=" * 50)
        
        if not self.belarus:
            # Estimate Belarus as a lower-ranked team
            belarus_estimated = {
                'team': 'Belarus (estimated)',
                'rank': 85,
                'points': 1300.0  # Typical for rank ~85
            }
            self.belarus = belarus_estimated
            print(f"📊 Using estimated Belarus data: #{belarus_estimated['rank']} ({belarus_estimated['points']} pts)")
        
        print(f"Denmark: #{self.denmark['rank']} ({self.denmark['points']} pts)")
        print(f"Belarus: #{self.belarus['rank']} ({self.belarus['points']} pts)")
        print(f"Points Gap: {self.denmark['points'] - self.belarus['points']:+.2f}")
        
        importance = 25  # World Cup Qualifiers
        den_expected = self.calculate_expected_result(self.denmark['points'], self.belarus['points'])
        
        print(f"Denmark Win Probability: {den_expected:.1%}")
        
        # Calculate Denmark's possible new points
        outcomes = [
            (1.0, "Denmark Win"),
            (0.5, "Draw"),
            (0.0, "Denmark Loss")
        ]
        
        denmark_scenarios = []
        
        print(f"\n{'Outcome':<15} {'Denmark New Points':<18} {'Change':<8}")
        print("-" * 45)
        
        for result, outcome_name in outcomes:
            new_points = self.calculate_new_points(
                self.denmark['points'], importance, result, den_expected
            )
            change = new_points - self.denmark['points']
            denmark_scenarios.append((outcome_name, new_points, change))
            print(f"{outcome_name:<15} {new_points:<18.2f} {change:+.2f}")
        
        return denmark_scenarios
    
    def analyze_scotland_greece(self):
        print(f"\n🏴󠁧󠁢󠁳󠁣󠁴󠁿 SCOTLAND vs GREECE ANALYSIS")
        print("=" * 50)
        
        print(f"Scotland: #{self.scotland['rank']} ({self.scotland['points']} pts)")
        print(f"Greece: #{self.greece['rank']} ({self.greece['points']} pts)")
        print(f"Points Gap: {self.scotland['points'] - self.greece['points']:+.2f}")
        
        importance = 25
        scot_expected = self.calculate_expected_result(self.scotland['points'], self.greece['points'])
        
        print(f"Scotland Win Probability: {scot_expected:.1%}")
        
        outcomes = [
            (1.0, "Scotland Win"),
            (0.5, "Draw"),
            (0.0, "Scotland Loss")
        ]
        
        scotland_scenarios = []
        
        print(f"\n{'Outcome':<15} {'Scotland New Points':<18} {'Change':<8}")
        print("-" * 45)
        
        for result, outcome_name in outcomes:
            new_points = self.calculate_new_points(
                self.scotland['points'], importance, result, scot_expected
            )
            change = new_points - self.scotland['points']
            scotland_scenarios.append((outcome_name, new_points, change))
            print(f"{outcome_name:<15} {new_points:<18.2f} {change:+.2f}")
        
        return scotland_scenarios
    
    def analyze_sequential_scenarios(self):
        print(f"\n🔄 COMPLETE SEQUENTIAL SCENARIO ANALYSIS")
        print("=" * 60)
        
        # Get scenarios from Round 1
        denmark_scenarios = self.analyze_denmark_belarus_impact()
        scotland_scenarios = self.analyze_scotland_greece()
        
        print(f"\n⚽ ALL POSSIBLE COMBINATIONS:")
        print(f"{'Scotland R1':<12} {'Denmark R1':<12} {'Denmark R2':<12} {'Scotland Final':<14} {'Total Change':<12} {'Outlook'}")
        print("-" * 90)
        
        importance = 25
        all_scenarios = []
        
        for scot_outcome, scot_points_r1, scot_change_r1 in scotland_scenarios:
            for den_outcome, den_points_r1, den_change_r1 in denmark_scenarios:
                
                # Round 2: Denmark (with updated points) vs Scotland (with updated points)
                den_expected_r2 = self.calculate_expected_result(den_points_r1, scot_points_r1)
                scot_expected_r2 = 1 - den_expected_r2
                
                # Possible Round 2 outcomes
                round2_outcomes = [
                    (1.0, 0.0, "Denmark Win"),
                    (0.5, 0.5, "Draw"),
                    (0.0, 1.0, "Scotland Win")
                ]
                
                for den_result_r2, scot_result_r2, r2_outcome in round2_outcomes:
                    # Calculate final Scotland points
                    scotland_final = self.calculate_new_points(
                        scot_points_r1, importance, scot_result_r2, scot_expected_r2
                    )
                    
                    total_change = scotland_final - self.scotland['points']
                    
                    # Create outlook
                    if total_change >= 20:
                        outlook = "🚀 Exceptional"
                    elif total_change >= 12:
                        outlook = "📈 Excellent"
                    elif total_change >= 5:
                        outlook = "✅ Very Good"
                    elif total_change >= 0:
                        outlook = "➡️ Good"
                    elif total_change >= -8:
                        outlook = "📉 Poor"
                    else:
                        outlook = "💥 Very Poor"
                    
                    # Simplified labels
                    scot_r1_code = scot_outcome.split()[1] if len(scot_outcome.split()) > 1 else scot_outcome[:4]
                    den_r1_code = den_outcome.split()[1] if len(den_outcome.split()) > 1 else den_outcome[:4]
                    
                    scenario_key = f"{scot_r1_code}+{den_r1_code}+{r2_outcome.split()[1] if len(r2_outcome.split()) > 1 else r2_outcome[:4]}"
                    
                    all_scenarios.append((
                        scot_outcome, den_outcome, r2_outcome, 
                        scotland_final, total_change, outlook
                    ))
                    
                    print(f"{scot_r1_code:<12} {den_r1_code:<12} {r2_outcome:<12} {scotland_final:<14.2f} {total_change:+.2f}          {outlook}")
        
        # Summary analysis
        all_scenarios.sort(key=lambda x: x[4], reverse=True)  # Sort by total change
        
        print(f"\n🏆 BEST CASE SCENARIO:")
        best = all_scenarios[0]
        print(f"   Scotland {best[0]}, Denmark {best[1]}, Round 2: {best[2]}")
        print(f"   Final Points: {best[3]:.2f} ({best[4]:+.2f}) - {best[5]}")
        
        print(f"\n💀 WORST CASE SCENARIO:")
        worst = all_scenarios[-1]
        print(f"   Scotland {worst[0]}, Denmark {worst[1]}, Round 2: {worst[2]}")
        print(f"   Final Points: {worst[3]:.2f} ({worst[4]:+.2f}) - {worst[5]}")
        
        # Probability analysis (assuming all outcomes equally likely for simplicity)
        positive_scenarios = [s for s in all_scenarios if s[4] > 0]
        neutral_scenarios = [s for s in all_scenarios if s[4] == 0]
        negative_scenarios = [s for s in all_scenarios if s[4] < 0]
        
        print(f"\n📊 SCENARIO DISTRIBUTION:")
        print(f"   Positive outcomes: {len(positive_scenarios)}/{len(all_scenarios)} ({len(positive_scenarios)/len(all_scenarios)*100:.1f}%)")
        print(f"   Neutral outcomes: {len(neutral_scenarios)}/{len(all_scenarios)} ({len(neutral_scenarios)/len(all_scenarios)*100:.1f}%)")
        print(f"   Negative outcomes: {len(negative_scenarios)}/{len(all_scenarios)} ({len(negative_scenarios)/len(all_scenarios)*100:.1f}%)")
        
        return all_scenarios

def main():
    print("🏆 FIFA WORLD CUP QUALIFIERS - SEQUENTIAL MATCH ANALYSIS")
    print("Factoring in Denmark vs Belarus before Denmark vs Scotland")
    print("=" * 70)
    
    analyzer = SequentialMatchAnalyzer()
    
    if not (analyzer.scotland and analyzer.greece and analyzer.denmark):
        print("❌ Missing required team data")
        return
    
    analyzer.show_match_schedule()
    scenarios = analyzer.analyze_sequential_scenarios()
    
    print(f"\n📋 COMPETITION CONFIRMATION:")
    print(f"✅ FIFA World Cup Qualifiers (25 points importance)")
    print(f"📅 November 2025 qualifying window")
    print(f"🔄 Sequential effects: Denmark's points update before facing Scotland")

if __name__ == "__main__":
    main()