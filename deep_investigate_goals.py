#!/usr/bin/env python3
"""
Deep investigation into the 27-goal discrepancy.
Check for empty scorers, own goals handling, and aggregation issues.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
from eta.eta_statistics import ScotlandFootballAnalyzer

def deep_investigate():
    """Perform deep investigation into the goal discrepancy."""
    print("🔬 DEEP INVESTIGATION: 27-GOAL DISCREPANCY")
    print("=" * 60)
    
    analyzer = ScotlandFootballAnalyzer('scot_games_eta_source.xlsx', worksheet_name='Games')
    analyzer.load_data()
    
    if analyzer.df is None:
        print("❌ Failed to load data!")
        return
    
    total_scotland_goals = int(analyzer.df['Scotland_Goals'].sum())
    print(f"📊 Total Scotland goals from data: {total_scotland_goals}")
    
    # Check matches with goals but no scorers
    empty_scorers_with_goals = []
    goals_without_scorers = 0
    
    for idx, row in analyzer.df.iterrows():
        scot_goals = row.get('Scot', 0)
        scorers_text = row.get('Scotland Scorers', '')
        
        if (pd.isna(scot_goals) or scot_goals == 0):
            continue
            
        if pd.isna(scorers_text) or str(scorers_text).strip() == '' or str(scorers_text).lower() == 'nan':
            empty_scorers_with_goals.append({
                'row': idx + 2 if isinstance(idx, int) else 2,
                'date': row.get('Date', 'Unknown'),
                'opponent': row.get('Opposition', 'Unknown'),
                'scot_goals': int(scot_goals),
                'scorers_text': repr(scorers_text)
            })
            goals_without_scorers += int(scot_goals)
    
    print(f"\n🚫 Matches with goals but no/empty scorers:")
    print(f"   Count: {len(empty_scorers_with_goals)}")
    print(f"   Total goals: {goals_without_scorers}")
    
    if empty_scorers_with_goals:
        print("\n   Details:")
        for match in empty_scorers_with_goals[:10]:
            print(f"   Row {match['row']}: {match['date']} vs {match['opponent']} - {match['scot_goals']} goals, scorers: {match['scorers_text']}")
    
    # Now run the goalscorer analysis and see what it produces
    print(f"\n📈 Running goalscorer analysis...")
    goalscorers = analyzer.analyze_goalscorers()
    total_from_analysis = int(goalscorers['goals'].sum())
    print(f"   Total from analysis: {total_from_analysis}")
    
    # Manual count using the same parsing logic as the analyzer
    print(f"\n🔍 Manual parsing of all matches...")
    manual_total = 0
    all_scorers = []
    
    for idx, row in analyzer.df.iterrows():
        scorers_text = row.get('Scotland Scorers', '')
        if pd.isna(scorers_text) or scorers_text == '':
            continue
            
        # Use the exact same parsing logic as the analyzer
        scorers_text = str(scorers_text)
        scorers_list = [s.strip() for s in scorers_text.split(',')]
        
        for scorer in scorers_list:
            if scorer and scorer.lower() not in ['', 'nan']:
                # Handle cases like "Smith 2", "Smith(2)", etc.
                import re
                name = scorer
                goals = 1  # default
                
                # Check for parenthetical format first
                if '(' in scorer and ')' in scorer:
                    match = re.search(r'\((\s*\d+\s*)\)', scorer)
                    if match:
                        goals = int(match.group(1).strip())
                        name = re.sub(r'\(\s*\d+\s*\)', '', scorer).strip()
                    else:
                        # Check if it's a penalty notation
                        penalty_match = re.search(r'\(\s*p\s*\)', scorer, re.IGNORECASE)
                        if penalty_match:
                            name = re.sub(r'\(\s*p\s*\)', '', scorer, flags=re.IGNORECASE).strip() 
                        else:
                            name = scorer.strip()
                elif '[' in scorer and ']' in scorer:
                    name = scorer.strip()
                else:
                    # Check for space-separated format like "Player 2"
                    parts = scorer.split()
                    if len(parts) > 1 and parts[-1].isdigit():
                        name = ' '.join(parts[:-1])
                        goals = int(parts[-1])
                    else:
                        name = scorer.strip()
                
                # Handle own goals
                if 'og' in name.lower():
                    name = name.replace('og', '').replace('OG', '').strip()
                    if name:
                        name += ' (og)'
                
                if name:
                    all_scorers.extend([name] * goals)
                    manual_total += goals
    
    print(f"   Manual total: {manual_total}")
    print(f"   Difference from analysis: {manual_total - total_from_analysis}")
    
    # Count own goals specifically
    own_goal_count = sum(1 for scorer in all_scorers if '(og)' in scorer)
    print(f"   Own goals in manual count: {own_goal_count}")
    
    # Final discrepancy breakdown
    print(f"\n📋 DISCREPANCY BREAKDOWN:")
    print(f"   Scotland goals total: {total_scotland_goals}")
    print(f"   Goals from empty scorers: {goals_without_scorers}")
    print(f"   Goals from analysis: {total_from_analysis}")
    print(f"   Manual parsing total: {manual_total}")
    print(f"   Own goals: {own_goal_count}")
    print(f"   Remaining discrepancy: {total_scotland_goals - total_from_analysis}")

def main():
    """Run the deep investigation."""
    deep_investigate()
    print("\n" + "=" * 60)
    print("🏁 Deep investigation complete!")

if __name__ == "__main__":
    main()