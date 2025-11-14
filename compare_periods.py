#!/usr/bin/env python3
"""
Scotland Football Statistics - Full History vs ETA Period Comparison

This script compares Scotland's performance across the full historical period
versus the ETA 30th anniversary period.
"""

from pathlib import Path
from src.eta.eta_statistics import ScotlandFootballAnalyzer


def main():
    """Compare Scotland's performance across different periods."""
    
    excel_file = "scot_games_eta_source.xlsx"
    
    if not Path(excel_file).exists():
        print(f"Error: {excel_file} not found!")
        return
    
    print("🏴󠁧󠁢󠁳󠁣󠁴󠁿 SCOTLAND FOOTBALL STATISTICS - HISTORICAL COMPARISON")
    print("=" * 65)
    
    try:
        # Load full historical data
        print("Loading full historical data...")
        full_analyzer = ScotlandFootballAnalyzer(excel_file, 'Games')
        full_df = full_analyzer.load_data()
        full_stats = full_analyzer.get_overall_statistics()
        
        # Load ETA period data
        print("Loading ETA 30th period data...")
        eta_analyzer = ScotlandFootballAnalyzer(excel_file, 'ETA30th')
        eta_df = eta_analyzer.load_data()
        eta_stats = eta_analyzer.get_overall_statistics()
        
        print()
        print("📊 COMPARISON SUMMARY")
        print("=" * 50)
        
        # Basic comparison
        print("FULL HISTORY (1872-2025):")
        print(f"  Total Matches: {full_stats['total_matches']}")
        print(f"  Win Rate: {full_stats['win_percentage']:.1f}%")
        print(f"  Goals per Match: {full_stats['goals_per_match']:.2f}")
        print(f"  Goals Against per Match: {full_stats['goals_conceded_per_match']:.2f}")
        print()
        
        print("ETA PERIOD (1995-2025):")
        print(f"  Total Matches: {eta_stats['total_matches']} ({eta_stats['total_matches']/full_stats['total_matches']*100:.1f}% of total)")
        print(f"  Win Rate: {eta_stats['win_percentage']:.1f}% ({eta_stats['win_percentage']-full_stats['win_percentage']:+.1f}% vs full history)")
        print(f"  Goals per Match: {eta_stats['goals_per_match']:.2f} ({eta_stats['goals_per_match']-full_stats['goals_per_match']:+.2f} vs full history)")
        print(f"  Goals Against per Match: {eta_stats['goals_conceded_per_match']:.2f} ({eta_stats['goals_conceded_per_match']-full_stats['goals_conceded_per_match']:+.2f} vs full history)")
        print()
        
        # Top opponents comparison
        print("⚽ TOP 5 OPPONENTS - FREQUENCY COMPARISON")
        print("-" * 44)
        full_opponents = full_analyzer.analyze_by_opposition().head(5)
        eta_opponents = eta_analyzer.analyze_by_opposition().head(5)
        
        print("FULL HISTORY:")
        for i, (opponent, stats) in enumerate(full_opponents.iterrows(), 1):
            print(f"{i}. {opponent:<15} {int(stats['matches_played'])} games ({stats['win_percentage']:5.1f}% wins)")
        
        print("\nETA PERIOD:")
        for i, (opponent, stats) in enumerate(eta_opponents.iterrows(), 1):
            print(f"{i}. {opponent:<15} {int(stats['matches_played'])} games ({stats['win_percentage']:5.1f}% wins)")
        print()
        
        # Top goalscorers comparison
        print("⚽ TOP GOALSCORERS COMPARISON")
        print("-" * 30)
        full_scorers = full_analyzer.analyze_goalscorers().head(5)
        eta_scorers = eta_analyzer.analyze_goalscorers().head(5)
        
        if not full_scorers.empty:
            print("FULL HISTORY:")
            for i, (scorer, stats) in enumerate(full_scorers.iterrows(), 1):
                print(f"{i}. {scorer:<15} {int(stats['goals'])} goals")
        
        if not eta_scorers.empty:
            print("\nETA PERIOD:")
            for i, (scorer, stats) in enumerate(eta_scorers.iterrows(), 1):
                print(f"{i}. {scorer:<15} {int(stats['goals'])} goals")
        print()
        
        # Goals and scoring trends
        print("⚽ SCORING TRENDS")
        print("-" * 17)
        print(f"Full History: {full_stats['total_goals_scored']} goals in {full_stats['total_matches']} games = {full_stats['goals_per_match']:.2f} per game")
        print(f"ETA Period:   {eta_stats['total_goals_scored']} goals in {eta_stats['total_matches']} games = {eta_stats['goals_per_match']:.2f} per game")
        print(f"Defensive:    Full {full_stats['goals_conceded_per_match']:.2f} vs ETA {eta_stats['goals_conceded_per_match']:.2f} goals conceded per game")
        print()
        
        # Key insights
        print("💡 KEY INSIGHTS")
        print("-" * 15)
        win_rate_change = eta_stats['win_percentage'] - full_stats['win_percentage']
        scoring_change = eta_stats['goals_per_match'] - full_stats['goals_per_match']
        
        if win_rate_change < 0:
            print(f"• Scotland's win rate has DECLINED by {abs(win_rate_change):.1f}% in the ETA period")
        else:
            print(f"• Scotland's win rate has IMPROVED by {win_rate_change:.1f}% in the ETA period")
            
        if scoring_change < 0:
            print(f"• Scotland scores {abs(scoring_change):.2f} FEWER goals per game in the ETA period")
        else:
            print(f"• Scotland scores {scoring_change:.2f} MORE goals per game in the ETA period")
            
        print(f"• The ETA period represents {eta_stats['total_matches']/full_stats['total_matches']*100:.1f}% of Scotland's total international matches")
        print(f"• ETA period covers the last {eta_df['Date'].max().year - eta_df['Date'].min().year + 1} years of Scotland football")
        
        print("\n✅ Historical comparison complete!")
        
    except Exception as e:
        print(f"❌ Error in comparison analysis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()