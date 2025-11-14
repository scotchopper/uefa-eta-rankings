#!/usr/bin/env python3
"""
Scotland Football Statistics - Main Analysis Script

This script analyzes the actual Scotland national team results from the Excel file.
"""

from pathlib import Path
from src.eta.eta_statistics import ScotlandFootballAnalyzer


def main():
    """Run comprehensive analysis of Scotland football results."""
    
    excel_file = "scot_games_eta_source.xlsx"
    
    if not Path(excel_file).exists():
        print(f"Error: {excel_file} not found!")
        print("Please ensure the Scotland results Excel file is in the current directory.")
        return
    
    print("🏴󠁧󠁢󠁳󠁣󠁴󠁿 SCOTLAND NATIONAL TEAM STATISTICS ANALYSIS")
    print("=" * 55)
    
    try:
        # Initialize analyzer
        analyzer = ScotlandFootballAnalyzer(excel_file, 'Games')
        df = analyzer.load_data()
        
        print(f"📊 Loaded {len(df)} matches from {df['Date'].min().strftime('%Y')} to {df['Date'].max().strftime('%Y')}")
        print()
        
        # Overall Statistics
        print("🎯 OVERALL PERFORMANCE")
        print("-" * 25)
        overall = analyzer.get_overall_statistics()
        print(f"Total Matches: {overall['total_matches']}")
        print(f"Record: {overall['wins']}-{overall['draws']}-{overall['losses']} (W-D-L)")
        print(f"Win Rate: {overall['win_percentage']:.1f}%")
        print(f"Goals: {overall['total_goals_scored']} scored, {overall['total_goals_conceded']} conceded")
        print(f"Goal Difference: {overall['goal_difference']:+d}")
        print(f"Average Goals per Match: {overall['goals_per_match']:.2f}")
        print()
        
        # Home vs Away
        print("🏠 HOME vs AWAY PERFORMANCE")
        print("-" * 32)
        home_away = analyzer.analyze_by_home_away()
        for location, stats in home_away.iterrows():
            location_emoji = "🏠" if location == "H" else ("✈️" if location == "A" else "🏟️")
            location_name = "Home" if location == "H" else ("Away" if location == "A" else "Neutral")
            print(f"{location_emoji} {location_name}: {int(stats['wins'])}-{int(stats['draws'])}-{int(stats['losses'])} ({stats['win_percentage']:.1f}% win rate)")
        print()
        
        # Top Opponents
        print("⚽ TOP 10 MOST FREQUENT OPPONENTS")
        print("-" * 35)
        opponents = analyzer.analyze_by_opposition().head(10)
        for i, (opponent, stats) in enumerate(opponents.iterrows(), 1):
            print(f"{i:2}. {opponent:<15} {int(stats['matches_played'])} games ({stats['win_percentage']:5.1f}% wins)")
        print()
        
        # Best Managers
        print("👔 MANAGER PERFORMANCE (min 15 games)")
        print("-" * 37)
        managers = analyzer.analyze_by_manager()
        managers_filtered = managers[managers['matches_played'] >= 15]
        for i, (manager, stats) in enumerate(managers_filtered.iterrows(), 1):
            print(f"{i:2}. {manager:<20} {int(stats['matches_played'])} games ({stats['win_percentage']:5.1f}% wins)")
        print()
        
        # Top Goalscorers
        print("⚽ TOP 10 GOALSCORERS")
        print("-" * 22)
        scorers = analyzer.analyze_goalscorers().head(10)
        for i, (scorer, stats) in enumerate(scorers.iterrows(), 1):
            print(f"{i:2}. {scorer:<15} {int(stats['goals'])} goals in {int(stats['games_scored_in'])} games ({stats['goals_per_scoring_game']:.2f} per scoring game)")
        print()
        
        # Competition Performance
        print("🏆 PERFORMANCE BY COMPETITION")
        print("-" * 31)
        competitions = analyzer.analyze_by_competition()
        for comp, stats in competitions.iterrows():
            if stats['matches_played'] >= 10:  # Only show major competitions
                print(f"{comp:<30} {int(stats['matches_played'])} games ({stats['win_percentage']:5.1f}% wins)")
        print()
        
        # Best Venues
        print("🏟️  TOP VENUES (min 5 games)")
        print("-" * 28)
        venues = analyzer.analyze_by_venue()
        venues_filtered = venues[venues['matches_played'] >= 5].head(10)
        # venues_filtered = venues # this is an override only to show all venues for testing
        for i, (venue, stats) in enumerate(venues_filtered.iterrows(), 1):
            print(f"{i:2}. {venue:<20} {int(stats['matches_played'])} games ({stats['win_percentage']:5.1f}% wins)")
        print()
        
        # Toughest Opponents
        print("😤 TOUGHEST OPPONENTS (min 5 games)")
        print("-" * 34)
        toughest = analyzer.get_toughest_opponents(min_matches=5, top_n=5)
        for i, (opponent, stats) in enumerate(toughest.iterrows(), 1):
            print(f"{i}. {opponent:<15} {int(stats['matches_played'])} games ({stats['win_percentage']:5.1f}% wins)")
        print()
        
        # Recent Form (last 50 games)
        recent_df = df.tail(50)
        recent_wins = len(recent_df[recent_df['Result'] == 'Win'])
        recent_draws = len(recent_df[recent_df['Result'] == 'Draw'])
        recent_losses = len(recent_df[recent_df['Result'] == 'Loss'])
        recent_win_pct = (recent_wins / 50) * 100
        
        print("📈 RECENT FORM (Last 50 Games)")
        print("-" * 32)
        print(f"Record: {recent_wins}-{recent_draws}-{recent_losses} ({recent_win_pct:.1f}% win rate)")
        print(f"Goals: {recent_df['Scotland_Goals'].sum()} scored, {recent_df['Opposition_Goals'].sum()} conceded")
        print()
        
        print("✅ Analysis complete!")
        print(f"Full data available in: {excel_file}")
        
    except Exception as e:
        print(f"❌ Error analyzing data: {e}")


if __name__ == "__main__":
    main()