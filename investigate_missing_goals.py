#!/usr/bin/env python3
"""
Investigate the missing goals in goalscorer parsing.
Find out why there's a 27-goal difference between total Scotland goals 
and parsed goalscorer totals.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
from eta.eta_statistics import ScotlandFootballAnalyzer

def parse_goalscorers_for_row(scorers_text):
    """Parse goalscorers for a single row and return count (same logic as analyzer)."""
    if pd.isna(scorers_text) or scorers_text == '':
        return 0
        
    import re
    scorers_text = str(scorers_text)
    total_goals = 0
    
    # Split by comma and clean up
    scorers_list = [s.strip() for s in scorers_text.split(',')]
    
    for scorer in scorers_list:
        if scorer and scorer.lower() not in ['', 'nan']:
            goals = 1  # default
            
            # Check for parenthetical format first
            if '(' in scorer and ')' in scorer:
                match = re.search(r'\((\s*\d+\s*)\)', scorer)
                if match:
                    goals = int(match.group(1).strip())
            else:
                # Check for space-separated format like "Player 2"
                parts = scorer.split()
                if len(parts) > 1 and parts[-1].isdigit():
                    goals = int(parts[-1])
            
            total_goals += goals
    
    return total_goals

def investigate_missing_goals():
    """Find matches where Scotland goals don't match parsed goalscorers."""
    print("🔍 INVESTIGATING MISSING GOALS")
    print("=" * 60)
    
    analyzer = ScotlandFootballAnalyzer('scot_games_eta_source.xlsx', worksheet_name='Games')
    analyzer.load_data()
    goalscorers = analyzer.analyze_goalscorers()
    
    total_goals_from_scorers = int(goalscorers['goals'].sum())
    total_scotland_goals = int(analyzer.df['Scotland_Goals'].sum())
    difference = total_scotland_goals - total_goals_from_scorers
    
    print(f"📊 Overall Summary:")
    print(f"   Total Scotland goals: {total_scotland_goals}")
    print(f"   Total from scorers: {total_goals_from_scorers}")
    print(f"   Missing goals: {difference}")
    print()
    
    # Find problematic rows
    problem_matches = []
    total_missing = 0
    
    for idx, row in analyzer.df.iterrows():
        scot_goals = row.get('Scot', 0)
        scorers_text = row.get('Scotland Scorers', '')
        
        if pd.isna(scot_goals) or scot_goals == 0:
            continue
            
        parsed_goals = parse_goalscorers_for_row(scorers_text)
        scot_goals = int(scot_goals)
        
        if scot_goals != parsed_goals:
            missing = scot_goals - parsed_goals
            total_missing += missing
            problem_matches.append({
                'row': int(idx) + 2,
                'date': row.get('Date', 'Unknown'),
                'opponent': row.get('Opposition', 'Unknown'),
                'venue': row.get('Venue', 'Unknown'),
                'scot_goals': scot_goals,
                'parsed_goals': parsed_goals,
                'missing': missing,
                'scorers_text': scorers_text
            })
    
    print(f"🎯 Found {len(problem_matches)} problematic matches")
    print(f"   Total missing from these matches: {total_missing}")
    print()
    
    if problem_matches:
        print("❌ PROBLEMATIC MATCHES:")
        print("=" * 80)
        for i, match in enumerate(problem_matches[:20]):  # Show first 20
            print(f"{i+1}. Row {match['row']}: {match['date']} vs {match['opponent']}")
            print(f"   Venue: {match['venue']}")
            print(f"   Scotland Goals: {match['scot_goals']} | Parsed: {match['parsed_goals']} | Missing: {match['missing']}")
            print(f"   Scorers: '{match['scorers_text']}'")
            print()
        
        if len(problem_matches) > 20:
            print(f"... and {len(problem_matches) - 20} more matches")
        
        # Analyze patterns
        print("\n📈 ANALYSIS OF MISSING GOALS:")
        print("-" * 40)
        
        # Count by missing amount
        missing_counts = {}
        for match in problem_matches:
            missing = match['missing']
            missing_counts[missing] = missing_counts.get(missing, 0) + 1
        
        print("Missing goals distribution:")
        for missing, count in sorted(missing_counts.items()):
            print(f"   {missing} goal(s) missing: {count} matches")
        
        # Look for common patterns in scorer text
        print(f"\nCommon patterns in problematic scorers text:")
        scorers_patterns = {}
        for match in problem_matches:
            text = match['scorers_text']
            if 'og' in text.lower():
                scorers_patterns['Contains og'] = scorers_patterns.get('Contains og', 0) + 1
            if '(' in text and ')' in text:
                scorers_patterns['Contains parentheses'] = scorers_patterns.get('Contains parentheses', 0) + 1
            if text == '' or pd.isna(text):
                scorers_patterns['Empty/NaN'] = scorers_patterns.get('Empty/NaN', 0) + 1
            if any(char.isdigit() for char in text):
                scorers_patterns['Contains numbers'] = scorers_patterns.get('Contains numbers', 0) + 1
        
        for pattern, count in scorers_patterns.items():
            print(f"   {pattern}: {count} matches")

def main():
    """Run the investigation."""
    investigate_missing_goals()
    print("\n" + "=" * 60)
    print("🏁 Investigation complete!")

if __name__ == "__main__":
    main()