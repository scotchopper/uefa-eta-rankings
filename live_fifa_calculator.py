#!/usr/bin/env python3
"""
FIFA World Ranking Calculator with Live Data Integration
This script can fetch real match data and calculate FIFA rankings
"""

import json
import requests
from datetime import datetime, date, timedelta
from enhanced_fifa_calculator import EnhancedFIFACalculator, CompetitionType, Match
import time

class LiveFIFACalculator(EnhancedFIFACalculator):
    """FIFA Calculator that can fetch live data from various sources"""
    
    def __init__(self, api_key: str = None):
        super().__init__()
        self.api_key = api_key
        self.api_calls_made = 0
        self.max_api_calls = 100  # Limit to prevent overuse
    
    def fetch_recent_international_matches(self, days_back: int = 30) -> list:
        """
        Fetch recent international matches
        This is a placeholder - in real implementation would connect to:
        - FIFA.com API
        - Football-Data.org API
        - RapidAPI Football APIs
        - ESPN APIs
        """
        # For demonstration, we'll create realistic recent matches
        end_date = date.today()
        start_date = end_date - timedelta(days=days_back)
        
        print(f"Fetching international matches from {start_date} to {end_date}")
        print("(Using simulated data - real implementation would fetch from FIFA/football APIs)")
        
        # Simulated recent international matches (realistic results)
        recent_matches = [
            # UEFA Nations League 2024-25 Finals
            {
                "date": "2025-11-14",
                "home_team": "Spain",
                "away_team": "Italy", 
                "home_score": 3,
                "away_score": 1,
                "competition": "nations_league_finals",
                "venue": "Seville, Spain"
            },
            {
                "date": "2025-11-14", 
                "home_team": "France",
                "away_team": "Netherlands",
                "home_score": 2,
                "away_score": 0,
                "competition": "nations_league_finals",
                "venue": "Paris, France"
            },
            # World Cup 2026 Qualifiers - CONMEBOL
            {
                "date": "2025-11-15",
                "home_team": "Brazil",
                "away_team": "Uruguay",
                "home_score": 4,
                "away_score": 2,
                "competition": "world_cup_qualifiers",
                "venue": "São Paulo, Brazil"
            },
            {
                "date": "2025-11-15",
                "home_team": "Argentina",
                "away_team": "Colombia",
                "home_score": 1,
                "away_score": 0,
                "competition": "world_cup_qualifiers", 
                "venue": "Buenos Aires, Argentina"
            },
            {
                "date": "2025-11-15",
                "home_team": "Chile",
                "away_team": "Peru",
                "home_score": 2,
                "away_score": 1,
                "competition": "world_cup_qualifiers",
                "venue": "Santiago, Chile"
            },
            # International Friendlies
            {
                "date": "2025-11-16",
                "home_team": "England",
                "away_team": "Germany",
                "home_score": 1,
                "away_score": 3,
                "competition": "friendly_inside",
                "venue": "London, England"
            },
            {
                "date": "2025-11-16",
                "home_team": "Portugal", 
                "away_team": "Belgium",
                "home_score": 2,
                "away_score": 2,
                "competition": "friendly_inside",
                "venue": "Lisbon, Portugal"
            },
            # AFC World Cup Qualifiers
            {
                "date": "2025-11-17",
                "home_team": "Japan",
                "away_team": "South Korea",
                "home_score": 3,
                "away_score": 0,
                "competition": "world_cup_qualifiers",
                "venue": "Tokyo, Japan"
            },
            # CAF Qualifiers
            {
                "date": "2025-11-17",
                "home_team": "Morocco",
                "away_team": "Senegal", 
                "home_score": 1,
                "away_score": 1,
                "competition": "world_cup_qualifiers",
                "venue": "Rabat, Morocco"
            },
            # CONCACAF Qualifiers
            {
                "date": "2025-11-18",
                "home_team": "United States",
                "away_team": "Mexico",
                "home_score": 2,
                "away_score": 0,
                "competition": "world_cup_qualifiers",
                "venue": "Austin, USA"
            }
        ]
        
        return recent_matches
    
    def convert_to_match_objects(self, match_data: list) -> list:
        """Convert raw match data to Match objects"""
        matches = []
        
        for match_info in match_data:
            try:
                match_date = datetime.strptime(match_info['date'], '%Y-%m-%d').date()
                competition = self.parse_competition_type(match_info['competition'])
                
                match = Match(
                    date=match_date,
                    home_team=match_info['home_team'],
                    away_team=match_info['away_team'],
                    home_score=int(match_info['home_score']),
                    away_score=int(match_info['away_score']),
                    competition=competition,
                    penalty_winner=match_info.get('penalty_winner'),
                    is_knockout=match_info.get('is_knockout', False)
                )
                matches.append(match)
                
            except (KeyError, ValueError) as e:
                print(f"Error processing match data: {e}")
                continue
        
        return matches
   
    def fetch_current_fifa_rankings(self) -> dict:
        """
        Fetch current FIFA rankings from official sources
        This is a placeholder - real implementation would fetch from FIFA.com
        """
        print("Fetching current FIFA rankings...")
        print("(Using simulated data - real implementation would fetch from FIFA.com)")
        
        # Current top FIFA rankings (as of November 2025)
        current_rankings = {
            "Spain": {"points": 1880.76, "fifa_code": "ESP", "confederation": "UEFA"},
            "Argentina": {"points": 1872.43, "fifa_code": "ARG", "confederation": "CONMEBOL"},
            "France": {"points": 1862.71, "fifa_code": "FRA", "confederation": "UEFA"},
            "England": {"points": 1824.30, "fifa_code": "ENG", "confederation": "UEFA"},
            "Portugal": {"points": 1778.00, "fifa_code": "POR", "confederation": "UEFA"},
            "Netherlands": {"points": 1759.96, "fifa_code": "NED", "confederation": "UEFA"},
            "Brazil": {"points": 1758.85, "fifa_code": "BRA", "confederation": "CONMEBOL"},
            "Belgium": {"points": 1740.01, "fifa_code": "BEL", "confederation": "UEFA"},
            "Italy": {"points": 1717.15, "fifa_code": "ITA", "confederation": "UEFA"},
            "Germany": {"points": 1713.30, "fifa_code": "GER", "confederation": "UEFA"},
            "Croatia": {"points": 1710.15, "fifa_code": "CRO", "confederation": "UEFA"},
            "Morocco": {"points": 1710.11, "fifa_code": "MAR", "confederation": "CAF"},
            "Colombia": {"points": 1695.72, "fifa_code": "COL", "confederation": "CONMEBOL"},
            "Mexico": {"points": 1682.52, "fifa_code": "MEX", "confederation": "CONCACAF"},
            "Uruguay": {"points": 1677.57, "fifa_code": "URU", "confederation": "CONMEBOL"},
            "United States": {"points": 1673.49, "fifa_code": "USA", "confederation": "CONCACAF"},
            "Switzerland": {"points": 1653.32, "fifa_code": "SUI", "confederation": "UEFA"},
            "Senegal": {"points": 1650.61, "fifa_code": "SEN", "confederation": "CAF"},
            "Japan": {"points": 1645.34, "fifa_code": "JPN", "confederation": "AFC"},
            "Denmark": {"points": 1641.02, "fifa_code": "DEN", "confederation": "UEFA"},
            "Chile": {"points": 1635.67, "fifa_code": "CHI", "confederation": "CONMEBOL"},
            "Iran": {"points": 1629.11, "fifa_code": "IRN", "confederation": "AFC"},
            "Scotland": {"points": 1628.21, "fifa_code": "SCO", "confederation": "UEFA"},
            "Peru": {"points": 1615.43, "fifa_code": "PER", "confederation": "CONMEBOL"},
            "South Korea": {"points": 1599.84, "fifa_code": "KOR", "confederation": "AFC"},
        }
        
        return current_rankings
    
    def load_current_rankings(self):
        """Load current FIFA rankings into the system"""
        rankings_data = self.fetch_current_fifa_rankings()
        
        for team_name, data in rankings_data.items():
            self.add_team(
                name=team_name,
                fifa_code=data['fifa_code'],
                initial_points=data['points'],
                confederation=data['confederation']
            )
    
    def run_live_calculation(self, days_back: int = 30):
        """Run a complete live FIFA ranking calculation"""
        print("🌍 LIVE FIFA WORLD RANKING CALCULATOR")
        print("=" * 80)
        
        # Load current rankings
        self.load_current_rankings()
        print(f"✅ Loaded {len(self.teams)} teams with current FIFA points")
        
        # Fetch recent matches
        recent_match_data = self.fetch_recent_international_matches(days_back)
        matches = self.convert_to_match_objects(recent_match_data)
        
        for match in matches:
            self.add_match(match)
        
        print(f"✅ Loaded {len(self.matches)} recent international matches")
        
        # Show initial rankings
        print(f"\n📊 CURRENT FIFA RANKINGS (Top 15):")
        self.display_rankings(15)
        
        # Process matches and show changes
        print(f"\n⚽ PROCESSING {len(self.matches)} RECENT MATCHES...")
        changes = self.analyze_ranking_changes()
        
        print(f"\n📊 UPDATED FIFA RANKINGS (Top 15):")
        self.display_rankings(15)
        
        # Show detailed changes
        self.display_ranking_changes(changes)
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"live_fifa_rankings_{timestamp}.json"
        self.save_rankings_json(filename)
        
        print(f"\n✅ Live calculation complete!")
        print(f"📊 {len(self.teams)} teams processed")
        print(f"⚽ {len(self.matches)} matches calculated")  
        print(f"💾 Results saved to {filename}")
        
        return changes
    
    def generate_analysis_report(self, changes: dict):
        """Generate a detailed analysis report"""
        print("\n" + "=" * 80)
        print("📈 FIFA RANKING ANALYSIS REPORT")
        print("=" * 80)
        
        # Biggest gainers
        gainers = [(team, data) for team, data in changes.items() 
                  if data['rank_change'] > 0]
        gainers.sort(key=lambda x: x[1]['rank_change'], reverse=True)
        
        print("🔥 BIGGEST RANK GAINERS:")
        for i, (team, data) in enumerate(gainers[:5], 1):
            print(f"{i}. {team}: Moved up {data['rank_change']} places "
                  f"({data['initial_rank']} → {data['final_rank']}) "
                  f"[{data['points_change']:+.2f} points]")
        
        # Biggest losers
        losers = [(team, data) for team, data in changes.items() 
                 if data['rank_change'] < 0]
        losers.sort(key=lambda x: x[1]['rank_change'])
        
        print(f"\n📉 BIGGEST RANK FALLERS:")
        for i, (team, data) in enumerate(losers[:5], 1):
            print(f"{i}. {team}: Dropped {abs(data['rank_change'])} places "
                  f"({data['initial_rank']} → {data['final_rank']}) "
                  f"[{data['points_change']:+.2f} points]")
        
        # Biggest point gains
        point_gainers = [(team, data) for team, data in changes.items() 
                        if data['points_change'] > 0]
        point_gainers.sort(key=lambda x: x[1]['points_change'], reverse=True)
        
        print(f"\n💪 BIGGEST POINT GAINERS:")
        for i, (team, data) in enumerate(point_gainers[:5], 1):
            print(f"{i}. {team}: +{data['points_change']:.2f} points "
                  f"({data['initial_points']:.2f} → {data['final_points']:.2f})")

def main():
    """Main function for live FIFA ranking calculation"""
    calculator = LiveFIFACalculator()
    
    print("Choose calculation mode:")
    print("1. Live calculation with recent matches (default)")
    print("2. Custom date range")
    print("3. Load from CSV files")
    
    choice = input("Enter choice (1-3) [default: 1]: ").strip() or "1"
    
    if choice == "1":
        days_back = int(input("Enter days back to fetch matches [default: 14]: ") or "14")
        changes = calculator.run_live_calculation(days_back)
        calculator.generate_analysis_report(changes)
        
    elif choice == "2":
        days_back = int(input("Enter days back to fetch matches: ") or "30")
        changes = calculator.run_live_calculation(days_back)
        calculator.generate_analysis_report(changes)
        
    elif choice == "3":
        calculator.load_teams_from_csv('fifa_teams.csv')
        calculator.load_matches_from_csv('fifa_matches.csv')
        changes = calculator.analyze_ranking_changes()
        calculator.display_rankings(20)
        calculator.display_ranking_changes(changes)
    
    print(f"\n🏆 FIFA Ranking calculation completed successfully!")

if __name__ == "__main__":
    main()