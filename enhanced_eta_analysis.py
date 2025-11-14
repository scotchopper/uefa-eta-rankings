#!/usr/bin/env python3
"""
Enhanced ETA analysis script with venue categorization.
Adds opponent venue categorization to the existing analysis.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from eta.eta_statistics import ScotlandFootballAnalyzer

def main():
    """Enhanced ETA analysis with venue categorization."""
    print("🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland Football - Enhanced ETA Analysis")
    print("="*60)
    
    # Initialize analyzer
    excel_file = "scot_games_eta_source.xlsx"
    analyzer = ScotlandFootballAnalyzer(excel_file, worksheet_name='ETA30th')
    
    # Load data
    analyzer.load_data()
    if analyzer.df is None:
        print("❌ Failed to load data")
        return
        
    print(f"✅ Loaded {len(analyzer.df)} matches from ETA30th period")
    
    # 1. Venue categorization analysis
    print("\n" + "="*60)
    print("🏟️  VENUE CATEGORIZATION ANALYSIS")
    print("="*60)
    
    analyzer.print_opponent_venue_categories()
    
    # 2. Show some interesting insights
    print("\n" + "="*60)
    print("📊 ADDITIONAL INSIGHTS")
    print("="*60)
    
    categories = analyzer.categorize_opponents_by_venue_type()
    
    # Most common scenario
    print(f"\n🎯 Most common opponent relationship:")
    if len(categories['home_and_away']) > 0:
        print(f"   • {len(categories['home_and_away'])} opponents played both home and away")
        print(f"   • This represents {len(categories['home_and_away'])/68*100:.1f}% of all opponents")
    
    # Travel analysis
    if len(categories['away_only']) > 0:
        print(f"\n✈️  Scotland-only traveled to meet:")
        for opponent in categories['away_only']:
            print(f"   • {opponent}")
    
    # Home hosting
    if len(categories['home_only']) > 0:
        print(f"\n🏠 Scotland hosted but never visited:")
        print(f"   • {len(categories['home_only'])} opponents ({len(categories['home_only'])/68*100:.1f}%)")
    
    # Neutral venues
    if len(categories['neutral_only']) > 0:
        print(f"\n🌍 Only met at neutral venues:")
        for opponent in categories['neutral_only']:
            print(f"   • {opponent}")
    
    # 3. Quick venue analysis
    print(f"\n" + "="*60)
    print("🏟️  TOP VENUES ANALYSIS")
    print("="*60)
    
    venue_analysis = analyzer.analyze_by_venue()
    if venue_analysis is not None and not venue_analysis.empty:
        print("\nTop 10 venues by number of matches:")
        # Sort by matches_played descending
        top_venues = venue_analysis.sort_values('matches_played', ascending=False).head(10)
        for i, (venue, row) in enumerate(top_venues.iterrows(), 1):
            matches = int(row['matches_played'])
            wins = int(row['wins'])
            draws = int(row['draws'])
            losses = int(row['losses'])
            win_pct = row['win_percentage']
            print(f"   {i:2}. {venue:25} {matches:2} matches "
                  f"(W:{wins:2} D:{draws:2} L:{losses:2}) {win_pct:5.1f}%")

if __name__ == "__main__":
    main()