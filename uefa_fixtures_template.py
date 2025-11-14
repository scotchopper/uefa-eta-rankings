#!/usr/bin/env python3
"""
UEFA Fixtures Template - Week of November 11-18, 2025
Template for inputting all UEFA team fixtures and results
"""

import json
from datetime import datetime, timedelta
from collections import defaultdict

class UEFAFixturesManager:
    def __init__(self):
        self.fixtures = {}
        self.results = {}
        self.fifa_rankings = {}
        self.load_fifa_rankings()
    
    def load_fifa_rankings(self):
        """Load FIFA rankings from JSON file"""
        try:
            # Try the main filename first, then the Excel-generated one
            filenames = ['fifa_rankings.json', 'fifa_rankings_from_excel.json']
            for filename in filenames:
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Handle different JSON structures
                    if 'rankings' in data:
                        # Excel-generated format
                        rankings_list = data['rankings']
                        self.fifa_rankings = {team['code']: team for team in rankings_list}
                    else:
                        # Direct format
                        self.fifa_rankings = data
                    
                    print(f"✅ Loaded {len(self.fifa_rankings)} FIFA team rankings from {filename}")
                    return True
                except FileNotFoundError:
                    continue
            
            print("❌ FIFA rankings file not found. Please run fetch_fifa_rankings.py first")
            return False
        except Exception as e:
            print(f"❌ Error loading FIFA rankings: {e}")
            return False
    
    def get_team_info(self, team_name):
        """Get team ranking info by name (fuzzy matching)"""
        for team_code, team_data in self.fifa_rankings.items():
            if team_name.lower() in team_data['team'].lower() or team_data['team'].lower() in team_name.lower():
                return team_code, team_data
        return None, None
    
    def add_fixture(self, match_id, date, home_team, away_team, competition, importance=25, venue=""):
        """Add a fixture to the template"""
        # Get team info
        home_code, home_info = self.get_team_info(home_team)
        away_code, away_info = self.get_team_info(away_team)
        
        if not home_info or not away_info:
            print(f"⚠️  Warning: Could not find ranking data for {home_team} vs {away_team}")
        
        self.fixtures[match_id] = {
            'date': date,
            'home_team': home_team,
            'away_team': away_team,
            'home_code': home_code,
            'away_code': away_code,
            'home_points': home_info['points'] if home_info else 1500,
            'away_points': away_info['points'] if away_info else 1500,
            'competition': competition,
            'importance': importance,
            'venue': venue,
            'status': 'scheduled'
        }
        
        print(f"➕ Added fixture: {home_team} vs {away_team} on {date}")
    
    def add_result(self, match_id, home_goals, away_goals, notes=""):
        """Add result for a completed fixture"""
        if match_id not in self.fixtures:
            print(f"❌ Match ID {match_id} not found in fixtures")
            return False
        
        # Determine result
        if home_goals > away_goals:
            result = 'H'  # Home win
        elif away_goals > home_goals:
            result = 'A'  # Away win
        else:
            result = 'D'  # Draw
        
        self.results[match_id] = {
            'home_goals': home_goals,
            'away_goals': away_goals,
            'result': result,
            'notes': notes,
            'completed_at': datetime.now().isoformat()
        }
        
        # Update fixture status
        self.fixtures[match_id]['status'] = 'completed'
        
        print(f"✅ Result added: {self.fixtures[match_id]['home_team']} {home_goals}-{away_goals} {self.fixtures[match_id]['away_team']} ({result})")
        return True
    
    def calculate_expected_result(self, home_points, away_points, home_advantage=100):
        """Calculate expected result using FIFA Elo formula"""
        rating_diff = (home_points + home_advantage) - away_points
        expected_home = 1 / (10**(-rating_diff/600) + 1)
        return expected_home
    
    def calculate_rating_changes(self, match_id):
        """Calculate rating changes for a completed match"""
        if match_id not in self.results:
            print(f"❌ No result found for match {match_id}")
            return None
        
        fixture = self.fixtures[match_id]
        result = self.results[match_id]
        
        home_points = fixture['home_points']
        away_points = fixture['away_points']
        importance = fixture['importance']
        
        # Calculate expected result
        expected_home = self.calculate_expected_result(home_points, away_points)
        
        # Determine actual result value
        if result['result'] == 'H':
            actual_home = 1.0
        elif result['result'] == 'A':
            actual_home = 0.0
        else:  # Draw
            actual_home = 0.5
        
        # Calculate rating changes
        home_change = importance * (actual_home - expected_home)
        away_change = importance * ((1 - actual_home) - (1 - expected_home))
        
        return {
            'home_change': round(home_change, 2),
            'away_change': round(away_change, 2),
            'home_new_points': round(home_points + home_change, 2),
            'away_new_points': round(away_points + away_change, 2),
            'expected_home': round(expected_home, 3)
        }
    
    def display_fixtures(self, filter_status=None):
        """Display all fixtures with optional status filter"""
        print(f"\n📅 UEFA FIXTURES TEMPLATE - Week of November 11-18, 2025")
        print("=" * 80)
        
        for match_id, fixture in self.fixtures.items():
            if filter_status and fixture['status'] != filter_status:
                continue
            
            status_icon = "⏳" if fixture['status'] == 'scheduled' else "✅"
            
            print(f"\n{status_icon} MATCH {match_id}: {fixture['competition']}")
            print(f"   📍 {fixture['home_team']} vs {fixture['away_team']}")
            print(f"   📅 Date: {fixture['date']}")
            print(f"   🏆 Competition: {fixture['competition']} (Importance: {fixture['importance']})")
            
            if fixture['home_code'] and fixture['away_code']:
                expected = self.calculate_expected_result(fixture['home_points'], fixture['away_points'])
                print(f"   📊 Points: {fixture['home_team']} ({fixture['home_points']}) vs {fixture['away_team']} ({fixture['away_points']})")
                print(f"   🎯 Win Probability: {fixture['home_team']} {expected:.1%} - Draw ~15% - {fixture['away_team']} {1-expected:.1%}")
            
            if match_id in self.results:
                result = self.results[match_id]
                changes = self.calculate_rating_changes(match_id)
                print(f"   ⚽ RESULT: {result['home_goals']}-{result['away_goals']} ({result['result']})")
                if changes:
                    print(f"   📈 Rating Changes: {fixture['home_team']} {changes['home_change']:+.2f} → {changes['home_new_points']}")
                    print(f"                     {fixture['away_team']} {changes['away_change']:+.2f} → {changes['away_new_points']}")
    
    def save_data(self, filename="uefa_fixtures_data.json"):
        """Save fixtures and results to JSON file"""
        data = {
            'fixtures': self.fixtures,
            'results': self.results,
            'last_updated': datetime.now().isoformat()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Data saved to {filename}")
    
    def load_data(self, filename="uefa_fixtures_data.json"):
        """Load fixtures and results from JSON file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.fixtures = data.get('fixtures', {})
            self.results = data.get('results', {})
            
            print(f"📂 Loaded {len(self.fixtures)} fixtures and {len(self.results)} results from {filename}")
            return True
        except FileNotFoundError:
            print(f"📂 No existing data file found ({filename}). Starting fresh.")
            return False

def main():
    manager = UEFAFixturesManager()
    
    print("🏆 UEFA FIXTURES TEMPLATE SYSTEM")
    print("=" * 50)
    print("This template allows you to:")
    print("1. Add all UEFA fixtures for this week")
    print("2. Update with results after games complete")
    print("3. Calculate FIFA ranking changes automatically")
    print("4. Save/load data for persistence")
    
    # Try to load existing data
    manager.load_data()
    
    while True:
        print(f"\n📋 MENU OPTIONS:")
        print("1. Add new fixture")
        print("2. Add match result")
        print("3. View all fixtures")
        print("4. View scheduled fixtures only")
        print("5. View completed fixtures only")
        print("6. Save data")
        print("7. Load example fixtures")
        print("8. Exit")
        
        choice = input("\nSelect option (1-8): ").strip()
        
        if choice == '1':
            print("\n➕ ADD NEW FIXTURE")
            match_id = input("Match ID (e.g., WCQ001): ")
            date = input("Date (YYYY-MM-DD): ")
            home_team = input("Home team: ")
            away_team = input("Away team: ")
            competition = input("Competition (e.g., World Cup Qualifiers): ")
            importance = int(input("Importance coefficient (25 for WCQ, 15 for Nations League): ") or "25")
            venue = input("Venue (optional): ")
            
            manager.add_fixture(match_id, date, home_team, away_team, competition, importance, venue)
        
        elif choice == '2':
            print("\n⚽ ADD MATCH RESULT")
            match_id = input("Match ID: ")
            home_goals = int(input("Home team goals: "))
            away_goals = int(input("Away team goals: "))
            notes = input("Notes (optional): ")
            
            manager.add_result(match_id, home_goals, away_goals, notes)
        
        elif choice == '3':
            manager.display_fixtures()
        
        elif choice == '4':
            manager.display_fixtures('scheduled')
        
        elif choice == '5':
            manager.display_fixtures('completed')
        
        elif choice == '6':
            manager.save_data()
        
        elif choice == '7':
            print("\n📝 Loading example fixtures...")
            # Add some example fixtures
            manager.add_fixture("WCQ001", "2025-11-14", "Scotland", "Greece", "World Cup Qualifiers", 25)
            manager.add_fixture("WCQ002", "2025-11-14", "Denmark", "Belarus", "World Cup Qualifiers", 25)
            manager.add_fixture("WCQ003", "2025-11-17", "Denmark", "Scotland", "World Cup Qualifiers", 25)
            manager.add_fixture("NL004", "2025-11-15", "England", "Ireland", "Nations League", 15)
            manager.add_fixture("NL005", "2025-11-16", "Spain", "Germany", "Nations League", 15)
            print("✅ Example fixtures added!")
        
        elif choice == '8':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option. Please try again.")

if __name__ == "__main__":
    main()