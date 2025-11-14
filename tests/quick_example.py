"""
Quick example of using the Scotland Football Statistics Analyzer
with the actual scot_games_eta_source.xlsx file.
"""

from src.eta.eta_statistics import ScotlandFootballAnalyzer

def main():
    """Quick example usage."""
    
    # Initialize with your actual data file
    analyzer = ScotlandFootballAnalyzer('scot_games_eta_source.xlsx', 'Games')
    
    # Load the data
    print("Loading Scotland football data...")
    df = analyzer.load_data()
    print(f"Loaded {len(df)} matches")
    
    # Get basic stats
    stats = analyzer.get_overall_statistics()
    print(f"\nScotland's overall record:")
    print(f"Wins: {stats['wins']}, Draws: {stats['draws']}, Losses: {stats['losses']}")
    print(f"Win percentage: {stats['win_percentage']:.1f}%")
    
    # Home vs Away performance
    home_away = analyzer.analyze_by_home_away()
    print(f"\nHome vs Away:")
    for location, record in home_away.iterrows():
        loc_name = "Home" if location == "H" else ("Away" if location == "A" else "Neutral")
        print(f"{loc_name}: {record['win_percentage']:.1f}% win rate")
    
    # Top goalscorers
    scorers = analyzer.analyze_goalscorers().head(5)
    print(f"\nTop 5 goalscorers:")
    for i, (scorer, stats) in enumerate(scorers.iterrows(), 1):
        print(f"{i}. {scorer}: {stats['goals']} goals")
    
    # Best opponents to play against
    opposition = analyzer.analyze_by_opposition()
    # Filter for teams played at least 5 times
    frequent_opponents = opposition[opposition['matches_played'] >= 5]
    best_opponents = frequent_opponents.nlargest(5, 'win_percentage')
    
    print(f"\nBest opponents (min 5 games):")
    for i, (opponent, stats) in enumerate(best_opponents.iterrows(), 1):
        print(f"{i}. {opponent}: {stats['win_percentage']:.1f}% win rate ({stats['matches_played']} games)")

if __name__ == "__main__":
    main()