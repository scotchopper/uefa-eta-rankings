"""
Demo script to create sample Scotland football data and demonstrate the statistics analyzer.
"""

import pandas as pd
from datetime import datetime, timedelta
import random
from pathlib import Path

from src.eta.eta_statistics import ScotlandFootballAnalyzer


def create_sample_scotland_data():
    """Create sample Scotland football results data for demonstration."""
    
    # Sample opponents
    opponents = [
        'England', 'Wales', 'Ireland', 'France', 'Germany', 'Spain', 'Italy', 'Netherlands',
        'Belgium', 'Portugal', 'Denmark', 'Norway', 'Sweden', 'Czech Republic', 'Poland',
        'Switzerland', 'Austria', 'Croatia', 'Ukraine', 'Greece', 'Turkey', 'Russia',
        'Israel', 'Georgia', 'Armenia', 'Kazakhstan', 'Moldova', 'Faroe Islands',
        'Lithuania', 'Estonia', 'Latvia', 'Luxembourg', 'Andorra', 'San Marino', 'Malta'
    ]
    
    # Sample competitions
    competitions = [
        'World Cup Qualifier', 'Euro Qualifier', 'Nations League', 'Friendly',
        'World Cup', 'European Championship'
    ]
    
    # Sample managers (last 30 years)
    managers = [
        'Craig Brown', 'Berti Vogts', 'Walter Smith', 'George Burley', 
        'Craig Levein', 'Gordon Strachan', 'Alex McLeish', 'Steve Clarke'
    ]
    
    # Generate data for last 30 years (approximately 10-15 matches per year)
    start_date = datetime.now() - timedelta(days=30*365)
    end_date = datetime.now()
    
    data = []
    current_date = start_date
    
    while current_date < end_date:
        # Generate 10-15 matches per year
        matches_this_year = random.randint(10, 15)
        
        for _ in range(matches_this_year):
            # Random date within the year
            days_offset = random.randint(0, 365)
            match_date = current_date + timedelta(days=days_offset)
            
            if match_date > end_date:
                break
                
            opponent = random.choice(opponents)
            venue = random.choices(['Home', 'Away', 'Neutral'], weights=[0.4, 0.4, 0.2])[0]
            competition = random.choice(competitions)
            
            # Manager based on era (simplified)
            if match_date.year < 2000:
                manager = 'Craig Brown'
            elif match_date.year < 2005:
                manager = random.choice(['Craig Brown', 'Berti Vogts'])
            elif match_date.year < 2008:
                manager = random.choice(['Berti Vogts', 'Walter Smith'])
            elif match_date.year < 2010:
                manager = random.choice(['Walter Smith', 'George Burley'])
            elif match_date.year < 2013:
                manager = random.choice(['George Burley', 'Craig Levein'])
            elif match_date.year < 2018:
                manager = random.choice(['Craig Levein', 'Gordon Strachan'])
            elif match_date.year < 2020:
                manager = random.choice(['Gordon Strachan', 'Alex McLeish'])
            else:
                manager = 'Steve Clarke'
            
            # Generate realistic scores
            # Scotland performance varies by opponent strength and venue
            opponent_strength = 0.5  # Default
            if opponent in ['England', 'France', 'Germany', 'Spain', 'Italy', 'Netherlands', 'Belgium', 'Portugal']:
                opponent_strength = 0.8  # Strong teams
            elif opponent in ['Denmark', 'Norway', 'Sweden', 'Czech Republic', 'Poland', 'Switzerland', 'Austria']:
                opponent_strength = 0.6  # Medium teams
            else:
                opponent_strength = 0.4  # Weaker teams
            
            # Venue advantage
            home_advantage = 0.2 if venue == 'Home' else (-0.1 if venue == 'Away' else 0)
            
            # Scotland's expected performance
            scotland_performance = 0.45 + home_advantage - (opponent_strength - 0.5) * 0.3
            
            # Generate goals (simplified Poisson-like distribution)
            scotland_goals = max(0, int(random.gauss(scotland_performance * 4, 1.2)))
            opposition_goals = max(0, int(random.gauss(opponent_strength * 3, 1.1)))
            
            # Cap at reasonable values
            scotland_goals = min(scotland_goals, 6)
            opposition_goals = min(opposition_goals, 5)
            
            data.append({
                'Date': match_date.strftime('%Y-%m-%d'),
                'Opposition': opponent,
                'Venue': venue,
                'Competition': competition,
                'Manager': manager,
                'Scotland_Goals': scotland_goals,
                'Opposition_Goals': opposition_goals
            })
        
        current_date = datetime(current_date.year + 1, 1, 1)
    
    # Sort by date
    data.sort(key=lambda x: x['Date'])
    
    return pd.DataFrame(data)


def main():
    """Demonstrate the analyzer with real or sample data."""
    
    # Check if real data file exists
    real_data_file = Path("scot_games_eta_source.xlsx")
    
    if real_data_file.exists():
        print("Found real Scotland data file - using scot_games_eta_source.xlsx")
        excel_file = real_data_file
        worksheet_name = 'Games'  # Main data sheet
    else:
        # Create sample data
        print("Creating sample Scotland football results data...")
        df = create_sample_scotland_data()
        
        # Save to Excel  
        excel_file = Path("sample_scotland_results.xlsx")
        df.to_excel(excel_file, sheet_name='Results', index=False)
        print(f"Sample data saved to {excel_file}")
        print(f"Generated {len(df)} match results over {df['Date'].min()} to {df['Date'].max()}")
        worksheet_name = 'Results'
    
    # Demonstrate the analyzer
    print("\n" + "="*60)
    print("DEMONSTRATING SCOTLAND FOOTBALL STATISTICS ANALYZER")
    print("="*60)
    
    try:
        analyzer = ScotlandFootballAnalyzer(str(excel_file), worksheet_name)
        analyzer.load_data()
        
        # Overall statistics
        print("\nOVERALL STATISTICS:")
        print("-" * 40)
        overall_stats = analyzer.get_overall_statistics()
        for key, value in overall_stats.items():
            if isinstance(value, float):
                print(f"{key.replace('_', ' ').title()}: {value:.2f}")
            else:
                print(f"{key.replace('_', ' ').title()}: {value}")
        
        # Top 10 opponents
        print("\nTOP 10 MOST FREQUENT OPPONENTS:")
        print("-" * 40)
        opposition_stats = analyzer.analyze_by_opposition().head(10)
        print(opposition_stats[['matches_played', 'wins', 'draws', 'losses', 'win_percentage']].to_string())
        
        # Home/Away performance (new)
        home_away_stats = analyzer.analyze_by_home_away()
        if not home_away_stats.empty:
            print("\nPERFORMANCE BY HOME/AWAY/NEUTRAL:")
            print("-" * 40)
            print(home_away_stats[['matches_played', 'wins', 'draws', 'losses', 'win_percentage']].to_string())
        
        # Top venues
        print("\nTOP 10 MOST PLAYED VENUES:")
        print("-" * 40)
        venue_stats = analyzer.analyze_by_venue().head(10)
        print(venue_stats[['matches_played', 'wins', 'draws', 'losses', 'win_percentage']].to_string())
        
        # Manager performance
        print("\nPERFORMANCE BY MANAGER:")
        print("-" * 40)
        manager_stats = analyzer.analyze_by_manager()
        print(manager_stats[['matches_played', 'wins', 'draws', 'losses', 'win_percentage']].to_string())
        
        # Competition performance
        print("\nPERFORMANCE BY COMPETITION:")  
        print("-" * 40)
        competition_stats = analyzer.analyze_by_competition()
        print(competition_stats[['matches_played', 'wins', 'draws', 'losses', 'win_percentage']].to_string())
        
        # Goalscorers analysis (new)
        goalscorers = analyzer.analyze_goalscorers()
        if not goalscorers.empty:
            print("\nTOP 10 GOALSCORERS:")
            print("-" * 40)
            top_goalscorers = goalscorers.head(10)
            print(top_goalscorers.to_string())
        
        # Top scoring opponents
        print("\nTOP 5 OPPONENTS SCOTLAND SCORES MOST AGAINST:")
        print("-" * 40)
        top_scorers = analyzer.get_top_scorers_against_opposition(5)
        print(top_scorers.to_string())
        
        # Toughest opponents
        print("\nTOUGHEST OPPONENTS (min 3 matches):")
        print("-" * 40)
        toughest = analyzer.get_toughest_opponents(min_matches=3, top_n=5)
        print(toughest.to_string())
        
        # Summary report
        print("\n" + "="*60)
        print("SUMMARY REPORT")
        print("="*60)
        print(analyzer.generate_summary_report())
        
    except Exception as e:
        print(f"Error analyzing data: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()