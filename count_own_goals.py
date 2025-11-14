#!/usr/bin/env python3
"""
Count own goals (og) in the Scotland Scorers column.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
import re
from eta.eta_statistics import ScotlandFootballAnalyzer

def count_own_goals():
    """Count own goals in both worksheets."""
    print("⚽ COUNTING OWN GOALS (og) IN SCOTLAND SCORERS")
    print("=" * 60)
    
    worksheets = ['Games', 'ETA30th']
    
    for worksheet in worksheets:
        print(f"\n📊 Analyzing {worksheet} worksheet...")
        print("-" * 40)
        
        try:
            analyzer = ScotlandFootballAnalyzer('scot_games_eta_source.xlsx', worksheet_name=worksheet)
            analyzer.load_data()
            
            if analyzer.df is None:
                print(f"❌ Could not load {worksheet} worksheet")
                continue
                
            if 'Scotland Scorers' not in analyzer.df.columns:
                print(f"❌ No Scotland Scorers column in {worksheet}")
                continue
            
            print(f"✅ Loaded {len(analyzer.df)} matches from {worksheet}")
            
            own_goals_found = []
            total_own_goals = 0
            
            for idx, row in analyzer.df.iterrows():
                scorers_text = row.get('Scotland Scorers', '')
                if pd.isna(scorers_text) or scorers_text == '':
                    continue
                    
                scorers_text = str(scorers_text).lower()
                row_num = idx + 2 if isinstance(idx, int) else 2  # Excel row number
                
                # Count 'og' occurrences in this row
                og_count = scorers_text.count('og')
                
                if og_count > 0:
                    own_goals_found.append({
                        'row': row_num,
                        'date': row.get('Date', 'Unknown'),
                        'opponent': row.get('Opposition', 'Unknown'),
                        'venue': row.get('Venue', 'Unknown'),
                        'original_text': row.get('Scotland Scorers', ''),
                        'og_count': og_count
                    })
                    total_own_goals += og_count
            
            print(f"🎯 Own Goals Summary for {worksheet}:")
            print(f"   Total matches with own goals: {len(own_goals_found)}")
            print(f"   Total own goals: {total_own_goals}")
            
            if own_goals_found:
                print(f"\n📋 Matches with own goals:")
                print("=" * 80)
                for og in own_goals_found:
                    print(f"Row {og['row']}: {og['date']} vs {og['opponent']}")
                    print(f"   Venue: {og['venue']}")
                    print(f"   Scorers: '{og['original_text']}'")
                    print(f"   Own goals: {og['og_count']}")
                    print()
            
        except Exception as e:
            print(f"❌ Error analyzing {worksheet}: {e}")
            continue

def main():
    """Run the own goals count."""
    count_own_goals()
    print("\n" + "=" * 60)
    print("🏁 Own goals count complete!")

if __name__ == "__main__":
    main()