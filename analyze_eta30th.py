#!/usr/bin/env python3
"""
Scotland Football Statistics - ETA 30th Anniversary Analysis

This script analyzes the Scotland national team results from the ETA30th worksheet,
which contains the subset of results whilst ETA was formed.
"""

from pathlib import Path
from src.eta.eta_statistics import ScotlandFootballAnalyzer

def main():
    """Run comprehensive analysis of Scotland football results during ETA period."""
    
    excel_file = "scot_games_eta_source.xlsx"
    
    if not Path(excel_file).exists():
        print(f"Error: {excel_file} not found!")
        print("Please ensure the Scotland results Excel file is in the current directory.")
        return
    
    print("🏴󠁧󠁢󠁳󠁣󠁴󠁿 SCOTLAND NATIONAL TEAM STATISTICS - ETA 30TH ANNIVERSARY")
    print("=" * 65)
    
    try:
        # Initialize analyzer with ETA30th worksheet
        analyzer = ScotlandFootballAnalyzer(excel_file, 'ETA30th')
        df = analyzer.load_data()
        
        print(f"📊 Loaded {len(df)} matches from ETA period ({df['Date'].min().strftime('%Y')} to {df['Date'].max().strftime('%Y')})")
        print()
        
        # Overall Statistics
        print("🎯 OVERALL PERFORMANCE (ETA PERIOD)")
        print("-" * 35)
        overall = analyzer.get_overall_statistics()
        print(f"Total Matches: {overall['total_matches']}")
        print(f"Record: {overall['wins']}-{overall['draws']}-{overall['losses']} (W-D-L)")
        print(f"Win Rate: {overall['win_percentage']:.1f}%")
        print(f"Goals: {overall['total_goals_scored']} scored, {overall['total_goals_conceded']} conceded")
        print(f"Goal Difference: {overall['goal_difference']:+d}")
        print(f"Average Goals per Match: {overall['goals_per_match']:.2f}")
        print()
        
        # Home vs Away
        print("🏠 HOME vs AWAY PERFORMANCE (ETA PERIOD)")
        print("-" * 40)
        home_away = analyzer.analyze_by_home_away()
        for location, stats in home_away.iterrows():
            location_emoji = "🏠" if location == "H" else ("✈️" if location == "A" else "🏟️")
            location_name = "Home" if location == "H" else ("Away" if location == "A" else "Neutral")
            print(f"{location_emoji} {location_name}: {int(stats['wins'])}-{int(stats['draws'])}-{int(stats['losses'])} ({stats['win_percentage']:.1f}% win rate)")
        print()
        
        # Top Opponents
        print("⚽ TOP 10 MOST FREQUENT OPPONENTS (ETA PERIOD)")
        print("-" * 45)
        opponents = analyzer.analyze_by_opposition().head(10)
        for i, (opponent, stats) in enumerate(opponents.iterrows(), 1):
            print(f"{i:2}. {opponent:<15} {int(stats['matches_played'])} games ({stats['win_percentage']:5.1f}% wins)")
        print()
        
        # Manager Performance during ETA period
        print("👔 MANAGER PERFORMANCE (ETA PERIOD)")
        print("-" * 35)
        managers = analyzer.analyze_by_manager()
        for i, (manager, stats) in enumerate(managers.iterrows(), 1):
            print(f"{i:2}. {manager:<20} {int(stats['matches_played'])} games ({stats['win_percentage']:5.1f}% wins)")
        print()
        
        # Top Goalscorers
        print("⚽ TOP GOALSCORERS (ETA PERIOD)")
        print("-" * 32)
        scorers = analyzer.analyze_goalscorers()
        if not scorers.empty:
            top_scorers = scorers.head(10)
            for i, (scorer, stats) in enumerate(top_scorers.iterrows(), 1):
                print(f"{i:2}. {scorer:<15} {int(stats['goals'])} goals in {int(stats['games_scored_in'])} games ({stats['goals_per_scoring_game']:.2f} per scoring game)")
        else:
            print("No goalscorer data available for this period.")
        print()
        
        # Competition Performance
        print("🏆 PERFORMANCE BY COMPETITION (ETA PERIOD)")
        print("-" * 41)
        competitions = analyzer.analyze_by_competition()
        for comp, stats in competitions.iterrows():
            print(f"{comp:<30} {int(stats['matches_played'])} games ({stats['win_percentage']:5.1f}% wins)")
        print()
        
        # Best Venues during ETA period
        print("🏟️  TOP VENUES (ETA PERIOD)")
        print("-" * 28)
        venues = analyzer.analyze_by_venue()
        venues_filtered = venues[venues['matches_played'] >= 2].head(10)  # Lower threshold for ETA period
        for i, (venue, stats) in enumerate(venues_filtered.iterrows(), 1):
            print(f"{i:2}. {venue:<20} {int(stats['matches_played'])} games ({stats['win_percentage']:5.1f}% wins)")
        print()
        
        # Toughest Opponents during ETA period
        print("😤 TOUGHEST OPPONENTS (ETA PERIOD, min 2 games)")
        print("-" * 44)
        toughest = analyzer.get_toughest_opponents(min_matches=2, top_n=5)
        if not toughest.empty:
            for i, (opponent, stats) in enumerate(toughest.iterrows(), 1):
                print(f"{i}. {opponent:<15} {int(stats['matches_played'])} games ({stats['win_percentage']:5.1f}% wins)")
        else:
            print("No opponents with minimum 2 games found.")
        print()
        
        # Best opponents during ETA period
        print("✅ BEST OPPONENTS (ETA PERIOD, min 2 games)")
        print("-" * 41)
        opposition_stats = analyzer.analyze_by_opposition()
        frequent_opponents = opposition_stats[opposition_stats['matches_played'] >= 2]
        if not frequent_opponents.empty:
            best_opponents = frequent_opponents.nlargest(5, 'win_percentage')
            for i, (opponent, stats) in enumerate(best_opponents.iterrows(), 1):
                print(f"{i}. {opponent:<15} {int(stats['matches_played'])} games ({stats['win_percentage']:5.1f}% wins)")
        else:
            print("No opponents with minimum 2 games found.")
        print()
        
        # Year-by-year performance during ETA period
        print("📊 YEAR-BY-YEAR PERFORMANCE (ETA PERIOD)")
        print("-" * 39)
        yearly = analyzer.get_year_by_year_analysis()
        for year, stats in yearly.iterrows():
            print(f"{year}: {int(stats['wins'])}-{int(stats['draws'])}-{int(stats['losses'])} ({stats['win_percentage']:5.1f}% wins, {int(stats['goals_scored'])} goals)")
        print()

        # All Venues during ETA period
        print("🏟️  All VENUES (ETA PERIOD)")
        print("-" * 28)
        venues = analyzer.analyze_by_city()        

        for i, (venue, stats) in enumerate(venues.iterrows(), 1):
            print(f"{i:2}. {venue:<20} {int(stats['matches_played'])} games ( {int(stats['wins'])}-{int(stats['draws'])}-{int(stats['losses'])}  {stats['win_percentage']:5.1f}% wins)")
    
        print()

        # All Opponents during ETA period
        print("🏟️  All OPPONENTS (ETA PERIOD)")
        print("-" * 28)
        opponents = analyzer.analyze_by_opposition()        

        for i, (opponent, stats) in enumerate(opponents.iterrows(), 1):
            print(f"{i:2}. {opponent:<20} {int(stats['matches_played'])} games ( {int(stats['wins'])}-{int(stats['draws'])}-{int(stats['losses'])}  {stats['win_percentage']:5.1f}% wins)")
    
        print()

        print(f"✅ ETA 30th Anniversary analysis complete!")
        print(f"This covers Scotland's performance during the ETA period from the ETA30th worksheet.")
        
    except Exception as e:
        print(f"❌ Error analyzing ETA data: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()