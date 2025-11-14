#!/usr/bin/env python3
"""
UEFA Results Updater - Simple tool to update match results and recalculate rankings
"""

import json
from datetime import datetime
from enhanced_team_range_analysis import EnhancedTeamRangeAnalyzer

class ResultsUpdater:
    def __init__(self):
        self.fixtures_file = 'uefa_fixtures_data.json'
        self.load_data()
    
    def load_data(self):
        """Load current fixtures data"""
        try:
            with open(self.fixtures_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
                self.fixtures = self.data.get('fixtures', {})
                self.results = self.data.get('results', {})
            print(f"✅ Loaded {len(self.fixtures)} fixtures, {len(self.results)} results")
        except FileNotFoundError:
            print("❌ UEFA fixtures data not found")
            return False
        return True
    
    def show_scheduled_matches(self):
        """Display scheduled matches that need results"""
        scheduled = []
        for match_id, fixture in self.fixtures.items():
            if fixture.get('status') == 'scheduled':
                scheduled.append((match_id, fixture))
        
        if not scheduled:
            print("✅ All matches have results!")
            return []
        
        print(f"\n📅 SCHEDULED MATCHES ({len(scheduled)} remaining):")
        print("-" * 60)
        for i, (match_id, fixture) in enumerate(scheduled, 1):
            print(f"{i:2}. {match_id}: {fixture['home_team']} vs {fixture['away_team']}")
            print(f"     Date: {fixture['date']} | Competition: {fixture['competition']}")
        
        return scheduled
    
    def add_result(self, match_id, home_goals, away_goals, notes=""):
        """Add result for a match"""
        if match_id not in self.fixtures:
            print(f"❌ Match ID {match_id} not found")
            return False
        
        fixture = self.fixtures[match_id]
        
        # Determine result
        if home_goals > away_goals:
            result = 'H'  # Home win
        elif away_goals > home_goals:
            result = 'A'  # Away win
        else:
            result = 'D'  # Draw
        
        # Add result
        self.results[match_id] = {
            'home_goals': home_goals,
            'away_goals': away_goals,
            'result': result,
            'notes': notes,
            'completed_at': datetime.now().isoformat()
        }
        
        # Update fixture status
        self.fixtures[match_id]['status'] = 'completed'
        
        print(f"✅ Result added: {fixture['home_team']} {home_goals}-{away_goals} {fixture['away_team']} ({result})")
        return True
    
    def save_data(self):
        """Save updated fixtures and results"""
        self.data['fixtures'] = self.fixtures
        self.data['results'] = self.results
        self.data['last_updated'] = datetime.now().isoformat()
        
        with open(self.fixtures_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Data saved to {self.fixtures_file}")
    
    def interactive_update(self):
        """Interactive mode for adding results"""
        while True:
            scheduled = self.show_scheduled_matches()
            
            if not scheduled:
                break
            
            print("\nOptions:")
            print("1-{}: Add result for match number".format(len(scheduled)))
            print("0: Exit")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == '0':
                break
            
            try:
                match_num = int(choice)
                if 1 <= match_num <= len(scheduled):
                    match_id, fixture = scheduled[match_num - 1]
                    
                    print(f"\n⚽ Adding result for: {fixture['home_team']} vs {fixture['away_team']}")
                    print(f"Date: {fixture['date']} | Competition: {fixture['competition']}")
                    
                    home_goals = int(input(f"{fixture['home_team']} goals: "))
                    away_goals = int(input(f"{fixture['away_team']} goals: "))
                    notes = input("Notes (optional): ")
                    
                    if self.add_result(match_id, home_goals, away_goals, notes):
                        self.save_data()
                else:
                    print("❌ Invalid selection")
            except ValueError:
                print("❌ Please enter a valid number")
    
    def quick_add_results(self, results_list):
        """Quick method to add multiple results"""
        """
        results_list format: [(match_id, home_goals, away_goals, notes), ...]
        """
        added = 0
        for match_id, home_goals, away_goals, notes in results_list:
            if self.add_result(match_id, home_goals, away_goals, notes):
                added += 1
        
        if added > 0:
            self.save_data()
            print(f"✅ Added {added} results successfully!")
        
        return added
    
    def generate_new_rankings(self):
        """Generate updated rankings after adding results"""
        print("\n🔄 GENERATING UPDATED RANKINGS...")
        print("-" * 40)
        
        # Use the enhanced analyzer to recalculate with results
        analyzer = EnhancedTeamRangeAnalyzer()
        
        # Get all UEFA teams with fixtures
        teams_with_fixtures = []
        for match_id, fixture in self.fixtures.items():
            home_team = fixture['home_team']
            away_team = fixture['away_team']
            
            if home_team not in [t['team'] for t in teams_with_fixtures]:
                team_data = analyzer.get_team_data_by_name(home_team)
                if team_data:
                    teams_with_fixtures.append({
                        'team': home_team,
                        'current_points': team_data['points'],
                        'fifa_rank': team_data['rank']
                    })
            
            if away_team not in [t['team'] for t in teams_with_fixtures]:
                team_data = analyzer.get_team_data_by_name(away_team)
                if team_data:
                    teams_with_fixtures.append({
                        'team': away_team,
                        'current_points': team_data['points'],
                        'fifa_rank': team_data['rank']
                    })
        
        # Calculate updated points based on results
        updated_teams = []
        for team in teams_with_fixtures:
            team_name = team['team']
            current_points = team['current_points']
            new_points = current_points
            
            # Find all matches for this team and apply results
            for match_id, fixture in self.fixtures.items():
                if match_id in self.results:
                    result = self.results[match_id]
                    
                    if fixture['home_team'] == team_name:
                        # Team is home
                        opponent_data = analyzer.get_team_data_by_name(fixture['away_team'])
                        if opponent_data:
                            expected = analyzer.calculate_expected_result(current_points, opponent_data['points'])
                            if result['result'] == 'H':
                                actual = 1.0
                            elif result['result'] == 'A':
                                actual = 0.0
                            else:
                                actual = 0.5
                            change = fixture['importance'] * (actual - expected)
                            new_points += change
                    
                    elif fixture['away_team'] == team_name:
                        # Team is away
                        opponent_data = analyzer.get_team_data_by_name(fixture['home_team'])
                        if opponent_data:
                            expected = analyzer.calculate_expected_result(opponent_data['points'], current_points)
                            expected_away = 1 - expected
                            if result['result'] == 'A':
                                actual = 1.0
                            elif result['result'] == 'H':
                                actual = 0.0
                            else:
                                actual = 0.5
                            change = fixture['importance'] * (actual - expected_away)
                            new_points += change
            
            updated_teams.append({
                'team': team_name,
                'fifa_rank': team['fifa_rank'],
                'current_points': current_points,
                'new_points': new_points,
                'change': new_points - current_points
            })
        
        # Sort by new points and assign UEFA ranks
        updated_teams.sort(key=lambda x: x['new_points'], reverse=True)
        
        for i, team in enumerate(updated_teams):
            team['new_uefa_rank'] = i + 1
        
        # Display results
        print(f"\n📊 UPDATED UEFA RANKINGS WITH RESULTS ({len(self.results)} matches completed)")
        print("=" * 120)
        print(f"{'UEFA':<4} {'FIFA':<4} {'Team':<20} {'Old Points':<10} {'New Points':<10} {'Change':<8} {'Status'}")
        print("-" * 120)
        
        for team in updated_teams:
            change_str = f"{team['change']:+.2f}"
            status = "↗️" if team['change'] > 5 else "↘️" if team['change'] < -5 else "→"
            print(f"{team['new_uefa_rank']:2d}   {team['fifa_rank']:2d}   {team['team']:<20} {team['current_points']:8.2f}   {team['new_points']:8.2f}   {change_str:<8} {status}")
        
        # Show Scotland specifically if present
        scotland_team = next((t for t in updated_teams if 'Scotland' in t['team']), None)
        if scotland_team:
            print(f"\n🏴󠁧󠁢󠁳󠁣󠁴󠁿 SCOTLAND UPDATE:")
            print(f"   UEFA Rank: #{scotland_team['new_uefa_rank']}")
            print(f"   FIFA Rank: #{scotland_team['fifa_rank']}")
            print(f"   Points: {scotland_team['current_points']:.2f} → {scotland_team['new_points']:.2f} ({scotland_team['change']:+.2f})")
        
        return updated_teams

def main():
    """Main function with menu options"""
    updater = ResultsUpdater()
    
    print("🏆 UEFA RESULTS UPDATER")
    print("=" * 40)
    print("Update match results and generate new FIFA rankings")
    
    while True:
        print(f"\n📋 MENU OPTIONS:")
        print("1. Show scheduled matches")
        print("2. Add result interactively")
        print("3. Generate updated rankings")
        print("4. Quick example (add sample results)")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            updater.show_scheduled_matches()
        
        elif choice == '2':
            updater.interactive_update()
        
        elif choice == '3':
            updater.generate_new_rankings()
        
        elif choice == '4':
            print("\n📝 ADDING SAMPLE RESULTS...")
            # Example: Scotland beats Greece 2-1, Denmark beats Belarus 3-0
            sample_results = [
                ("WCQC09", 1, 2, "Scotland win away in Greece"),  # Greece 1-2 Scotland
                ("WCQC10", 3, 0, "Denmark dominate at home")      # Denmark 3-0 Belarus
            ]
            updater.quick_add_results(sample_results)
            print("🎯 Sample results added! Use option 3 to see updated rankings.")
        
        elif choice == '5':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option")

if __name__ == "__main__":
    main()