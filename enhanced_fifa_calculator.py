#!/usr/bin/env python3
"""
Enhanced FIFA Men's World Ranking Calculator
Advanced features for loading and processing real match data
"""

import csv
import requests
from datetime import datetime, date
import json
from typing import Dict
from fifa_ranking_calculator import FIFARankingCalculator, Match, CompetitionType, Team

class EnhancedFIFACalculator(FIFARankingCalculator):
    """Enhanced FIFA calculator with data loading capabilities"""
    
    def __init__(self):
        super().__init__()
        self.match_history = []
    
    def load_teams_from_csv(self, filename: str):
        """Load teams from a CSV file"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.add_team(
                        name=row['team_name'],
                        fifa_code=row['fifa_code'], 
                        initial_points=float(row['points']),
                        confederation=row['confederation']
                    )
            print(f"Loaded {len(self.teams)} teams from {filename}")
        except FileNotFoundError:
            print(f"File {filename} not found. Using default teams.")
            self.load_default_teams()
    
    def load_matches_from_csv(self, filename: str):
        """Load matches from a CSV file"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    match_date = datetime.strptime(row['date'], '%Y-%m-%d').date()
                    competition = self.parse_competition_type(row['competition'])
                    
                    match = Match(
                        date=match_date,
                        home_team=row['home_team'],
                        away_team=row['away_team'],
                        home_score=int(row['home_score']),
                        away_score=int(row['away_score']),
                        competition=competition,
                        penalty_winner=row.get('penalty_winner') or None,
                        is_knockout=row.get('is_knockout', 'False').lower() == 'true'
                    )
                    self.add_match(match)
            print(f"Loaded {len(self.matches)} matches from {filename}")
        except FileNotFoundError:
            print(f"File {filename} not found. Using sample matches.")
            self.load_sample_matches()
    
    def parse_competition_type(self, competition_str: str) -> CompetitionType:
        """Parse competition string to CompetitionType enum"""
        competition_map = {
            'friendly_outside': CompetitionType.FRIENDLY_OUTSIDE_WINDOW,
            'friendly_inside': CompetitionType.FRIENDLY_INSIDE_WINDOW,
            'nations_league_group': CompetitionType.NATIONS_LEAGUE_GROUP,
            'nations_league_finals': CompetitionType.NATIONS_LEAGUE_FINALS,
            'confederation_qualifiers': CompetitionType.CONFEDERATION_QUALIFIERS,
            'world_cup_qualifiers': CompetitionType.WORLD_CUP_QUALIFIERS,
            'confederation_finals_early': CompetitionType.CONFEDERATION_FINALS_EARLY,
            'confederation_finals_late': CompetitionType.CONFEDERATION_FINALS_LATE,
            'world_cup_early': CompetitionType.WORLD_CUP_EARLY,
            'world_cup_late': CompetitionType.WORLD_CUP_LATE,
        }
        return competition_map.get(competition_str.lower(), CompetitionType.FRIENDLY_INSIDE_WINDOW)
    
    def load_default_teams(self):
        """Load default team set with current FIFA rankings"""
        default_teams = [
            ("Spain", "ESP", 1880.76, "UEFA"),
            ("Argentina", "ARG", 1872.43, "CONMEBOL"),
            ("France", "FRA", 1862.71, "UEFA"),  
            ("England", "ENG", 1824.30, "UEFA"),
            ("Portugal", "POR", 1778.00, "UEFA"),
            ("Netherlands", "NED", 1759.96, "UEFA"),
            ("Brazil", "BRA", 1758.85, "CONMEBOL"),
            ("Belgium", "BEL", 1740.01, "UEFA"),
            ("Italy", "ITA", 1717.15, "UEFA"),
            ("Germany", "GER", 1713.30, "UEFA"),
            ("Croatia", "CRO", 1710.15, "UEFA"),
            ("Morocco", "MAR", 1710.11, "CAF"),
            ("Colombia", "COL", 1695.72, "CONMEBOL"),
            ("Mexico", "MEX", 1682.52, "CONCACAF"),
            ("Uruguay", "URU", 1677.57, "CONMEBOL"),
            ("United States", "USA", 1673.49, "CONCACAF"),
            ("Switzerland", "SUI", 1653.32, "UEFA"),
            ("Senegal", "SEN", 1650.61, "CAF"),
            ("Japan", "JPN", 1645.34, "AFC"),
            ("Denmark", "DEN", 1641.02, "UEFA"),
            ("Chile", "CHI", 1635.67, "CONMEBOL"),
            ("Iran", "IRN", 1629.11, "AFC"),
            ("Scotland", "SCO", 1628.21, "UEFA"),
            ("Peru", "PER", 1615.43, "CONMEBOL"),
            ("South Korea", "KOR", 1599.84, "AFC"),
        ]
        
        for name, code, points, conf in default_teams:
            self.add_team(name, code, points, conf)
    
    def load_sample_matches(self):
        """Load sample recent matches for demonstration"""
        sample_matches = [
            Match(date(2025, 11, 15), "Spain", "France", 2, 1, CompetitionType.NATIONS_LEAGUE_FINALS),
            Match(date(2025, 11, 15), "Germany", "Italy", 1, 1, CompetitionType.NATIONS_LEAGUE_FINALS),
            Match(date(2025, 11, 16), "Brazil", "Uruguay", 3, 0, CompetitionType.WORLD_CUP_QUALIFIERS),
            Match(date(2025, 11, 16), "Argentina", "Colombia", 2, 2, CompetitionType.WORLD_CUP_QUALIFIERS),
            Match(date(2025, 11, 17), "England", "Netherlands", 1, 2, CompetitionType.FRIENDLY_INSIDE_WINDOW),
            Match(date(2025, 11, 17), "Portugal", "Morocco", 2, 0, CompetitionType.FRIENDLY_INSIDE_WINDOW),
            Match(date(2025, 11, 18), "Belgium", "Switzerland", 3, 1, CompetitionType.FRIENDLY_INSIDE_WINDOW),
            Match(date(2025, 11, 18), "Chile", "Peru", 1, 0, CompetitionType.WORLD_CUP_QUALIFIERS),
        ]
        
        for match in sample_matches:
            self.add_match(match)
    
    def create_sample_csv_files(self):
        """Create sample CSV files for demonstration"""
        # Create teams CSV
        teams_data = [
            ["team_name", "fifa_code", "points", "confederation"],
            ["Spain", "ESP", "1880.76", "UEFA"],
            ["Argentina", "ARG", "1872.43", "CONMEBOL"],
            ["France", "FRA", "1862.71", "UEFA"],
            ["England", "ENG", "1824.30", "UEFA"],
            ["Portugal", "POR", "1778.00", "UEFA"],
            ["Netherlands", "NED", "1759.96", "UEFA"],
            ["Brazil", "BRA", "1758.85", "CONMEBOL"],
            ["Belgium", "BEL", "1740.01", "UEFA"],
            ["Italy", "ITA", "1717.15", "UEFA"],
            ["Germany", "GER", "1713.30", "UEFA"],
        ]
        
        with open('fifa_teams.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(teams_data)
        
        # Create matches CSV
        matches_data = [
            ["date", "home_team", "away_team", "home_score", "away_score", "competition", "penalty_winner", "is_knockout"],
            ["2025-11-15", "Spain", "France", "2", "1", "nations_league_finals", "", "false"],
            ["2025-11-15", "Germany", "Italy", "1", "1", "nations_league_finals", "", "false"],
            ["2025-11-16", "Brazil", "Uruguay", "3", "0", "world_cup_qualifiers", "", "false"],
            ["2025-11-16", "Argentina", "Colombia", "2", "2", "world_cup_qualifiers", "", "false"],
            ["2025-11-17", "England", "Netherlands", "1", "2", "friendly_inside", "", "false"],
        ]
        
        with open('fifa_matches.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(matches_data)
        
        print("Created sample CSV files: fifa_teams.csv and fifa_matches.csv")
    
    def analyze_ranking_changes(self) -> Dict:
        """Analyze ranking changes after processing matches"""
        initial_rankings = {team.name: (rank + 1, team.points) 
                          for rank, team in enumerate(self.get_rankings())}
        
        # Store initial state
        initial_state = {name: team.points for name, team in self.teams.items()}
        
        # Process matches
        self.process_all_matches()
        
        # Get final rankings
        final_rankings = {team.name: (rank + 1, team.points) 
                         for rank, team in enumerate(self.get_rankings())}
        
        # Analyze changes
        changes = {}
        for team_name in self.teams:
            initial_rank, initial_points = initial_rankings[team_name]
            final_rank, final_points = final_rankings[team_name]
            
            changes[team_name] = {
                'initial_rank': initial_rank,
                'final_rank': final_rank,
                'rank_change': initial_rank - final_rank,  # Positive = moved up
                'initial_points': initial_points,
                'final_points': final_points,
                'points_change': final_points - initial_points
            }
        
        return changes
    
    def display_ranking_changes(self, changes: Dict):
        """Display ranking changes in a formatted table"""
        print("=" * 100)
        print("FIFA RANKING CHANGES ANALYSIS")
        print("=" * 100)
        print(f"{'Team':<20} {'Initial':<8} {'Final':<8} {'Rank Δ':<8} {'Initial Pts':<12} {'Final Pts':<12} {'Points Δ':<10}")
        print("-" * 100)
        
        # Sort by rank change (biggest improvements first)
        sorted_changes = sorted(changes.items(), key=lambda x: x[1]['rank_change'], reverse=True)
        
        for team_name, change in sorted_changes:
            rank_change = change['rank_change']
            rank_symbol = "↑" if rank_change > 0 else "↓" if rank_change < 0 else "="
            points_change = change['points_change']
            points_symbol = "+" if points_change >= 0 else ""
            
            print(f"{team_name:<20} {change['initial_rank']:<8} {change['final_rank']:<8} "
                  f"{rank_symbol}{abs(rank_change):<7} {change['initial_points']:<12.2f} "
                  f"{change['final_points']:<12.2f} {points_symbol}{points_change:<9.2f}")

def main():
    """Enhanced main function with CSV loading capabilities"""
    print("🏆 ENHANCED FIFA MEN'S WORLD RANKING CALCULATOR")
    print("=" * 80)
    
    calculator = EnhancedFIFACalculator()
    
    # Ask user for data source preference
    print("Data loading options:")
    print("1. Use default teams and sample matches")
    print("2. Create sample CSV files and load from them")
    print("3. Load from existing CSV files (fifa_teams.csv, fifa_matches.csv)")
    
    choice = input("Choose option (1-3) [default: 1]: ").strip() or "1"
    
    if choice == "2":
        calculator.create_sample_csv_files()
        calculator.load_teams_from_csv('fifa_teams.csv')
        calculator.load_matches_from_csv('fifa_matches.csv')
    elif choice == "3":
        calculator.load_teams_from_csv('fifa_teams.csv')
        calculator.load_matches_from_csv('fifa_matches.csv')
    else:
        calculator.load_default_teams()
        calculator.load_sample_matches()
    
    print("\nInitial Rankings:")
    calculator.display_rankings(15)
    
    # Analyze changes
    print(f"\nProcessing {len(calculator.matches)} matches...")
    changes = calculator.analyze_ranking_changes()
    
    print("\nFinal Rankings:")
    calculator.display_rankings(15)
    
    # Display changes
    calculator.display_ranking_changes(changes)
    
    # Save results
    calculator.save_rankings_json("enhanced_fifa_rankings.json")
    
    print(f"\n✅ Processing complete!")
    print(f"📊 {len(calculator.teams)} teams processed")
    print(f"⚽ {len(calculator.matches)} matches calculated")

if __name__ == "__main__":
    main()