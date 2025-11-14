#!/usr/bin/env python3
"""
Check if the discrepancy is related to own goal counting in the analyzer.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
from eta.eta_statistics import ScotlandFootballAnalyzer

def check_own_goal_handling():
    """Check how own goals are handled in the analysis vs manual count."""
    print("🎯 CHECKING OWN GOAL HANDLING")
    print("=" * 60)
    
    analyzer = ScotlandFootballAnalyzer('scot_games_eta_source.xlsx', worksheet_name='Games')
    analyzer.load_data()
    
    if analyzer.df is None:
        print("❌ Failed to load data!")
        return
    
    # Manual count of own goals from the Scotland Scorers column
    manual_og_count = 0
    manual_og_matches = []
    
    for idx, row in analyzer.df.iterrows():
        scorers_text = row.get('Scotland Scorers', '')
        if pd.isna(scorers_text) or scorers_text == '':
            continue
            
        scorers_text_lower = str(scorers_text).lower()
        og_count_in_row = scorers_text_lower.count('og')
        
        if og_count_in_row > 0:
            manual_og_count += og_count_in_row
            manual_og_matches.append({
                'row': idx + 2 if isinstance(idx, int) else 2,
                'date': row.get('Date', 'Unknown'),
                'opponent': row.get('Opposition', 'Unknown'),
                'scorers': scorers_text,
                'og_count': og_count_in_row
            })
    
    print(f"📊 Manual own goal count: {manual_og_count}")
    print(f"   From {len(manual_og_matches)} matches")
    
    # Now check what the analyzer produces
    goalscorers = analyzer.analyze_goalscorers()
    
    # Count own goals in the analyzer results
    analyzer_og_players = [name for name in goalscorers.index if '(og)' in name]
    analyzer_og_count = sum(goalscorers.loc[player, 'goals'] for player in analyzer_og_players)
    
    print(f"📈 Analyzer own goal count: {analyzer_og_count}")
    print(f"   From players: {analyzer_og_players}")
    
    # Check if there are standalone 'og' entries
    standalone_og_count = 0
    for idx, row in analyzer.df.iterrows():
        scorers_text = row.get('Scotland Scorers', '')
        if pd.isna(scorers_text) or scorers_text == '':
            continue
            
        # Look for standalone 'og' entries (not attached to player names)
        scorers_list = [s.strip() for s in str(scorers_text).split(',')]
        for scorer in scorers_list:
            if scorer.lower() == 'og':
                standalone_og_count += 1
    
    print(f"🔍 Standalone 'og' entries: {standalone_og_count}")
    
    # Total discrepancy check
    total_scotland_goals = int(analyzer.df['Scotland_Goals'].sum())
    total_from_analysis = int(goalscorers['goals'].sum())
    discrepancy = total_scotland_goals - total_from_analysis
    
    print(f"\n📋 SUMMARY:")
    print(f"   Total Scotland goals: {total_scotland_goals}")
    print(f"   Total from analysis: {total_from_analysis}")
    print(f"   Discrepancy: {discrepancy}")
    print(f"   Manual OG count: {manual_og_count}")
    print(f"   Analyzer OG count: {analyzer_og_count}")
    print(f"   Standalone OG count: {standalone_og_count}")
    print(f"   OG difference: {manual_og_count - analyzer_og_count}")
    
    # If the OG difference matches the discrepancy, we found the issue
    if (manual_og_count - analyzer_og_count) == discrepancy:
        print(f"\n✅ FOUND THE ISSUE: Own goals are not being properly counted!")
        print(f"   {standalone_og_count} standalone 'og' entries are being missed")
    else:
        print(f"\n❓ The own goal difference ({manual_og_count - analyzer_og_count}) doesn't fully explain the discrepancy ({discrepancy})")
    
    # Show some examples of problematic matches
    print(f"\n📋 Examples of matches with own goals:")
    for match in manual_og_matches[:5]:
        print(f"   Row {match['row']}: {match['date']} vs {match['opponent']}")
        print(f"      Scorers: '{match['scorers']}'")

def main():
    """Run the own goal handling check."""
    check_own_goal_handling()
    print("\n" + "=" * 60)
    print("🏁 Own goal handling check complete!")

if __name__ == "__main__":
    main()