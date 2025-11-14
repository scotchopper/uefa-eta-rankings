#!/usr/bin/env python3
"""
Analyze top goalscorers specifically at Hampden Park during the ETA period.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
from collections import defaultdict
import re

def analyze_hampden_goalscorers():
    """Analyze goalscorers specifically at Hampden Park."""
    
    print("⚽ HAMPDEN PARK GOALSCORERS ANALYSIS - ETA PERIOD")
    print("="*55)
    
    # Load ETA data
    df = pd.read_excel("scot_games_eta_source.xlsx", sheet_name='ETA30th')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    # Filter for Hampden matches only
    hampden_matches = df[df['Venue'] == 'Hampden'].copy()
    
    print(f"✅ Loaded {len(df)} total matches, {len(hampden_matches)} at Hampden")
    
    if len(hampden_matches) == 0:
        print("❌ No Hampden matches found")
        return
    
    # Dictionary to store goalscorer data
    goalscorer_stats = defaultdict(lambda: {'goals': 0, 'games': set(), 'goal_details': []})
    
    # Process Scotland Scorers column for Hampden matches
    for _, match in hampden_matches.iterrows():
        date = match['Date'].strftime('%Y-%m-%d') if pd.notna(match['Date']) else 'N/A'
        opponent = match['Opposition']
        scorers = match.get('Scotland Scorers', '')
        
        if pd.isna(scorers) or scorers == '':
            continue
            
        # Parse the scorers string
        # Handle various formats like "McGinn(2), Adams", "Fraser", "Dykes, Christie"
        if isinstance(scorers, str):
            # Split by comma first
            scorer_parts = [part.strip() for part in scorers.split(',')]
            
            for part in scorer_parts:
                if not part:
                    continue
                    
                # Extract goals count if in brackets like "McGinn(2)"
                goal_count = 1  # default
                scorer_name = part
                
                # Check for goal count in brackets
                bracket_match = re.search(r'([^(]+)\((\d+)\)', part)
                if bracket_match:
                    scorer_name = bracket_match.group(1).strip()
                    goal_count = int(bracket_match.group(2))
                
                # Clean up scorer name (remove extra spaces, handle "og" etc.)
                scorer_name = scorer_name.strip()
                if scorer_name.lower() == 'og':
                    continue  # Skip own goals
                
                # Add to stats
                goalscorer_stats[scorer_name]['goals'] += goal_count
                goalscorer_stats[scorer_name]['games'].add(date)
                goalscorer_stats[scorer_name]['goal_details'].append({
                    'date': date,
                    'opponent': opponent,
                    'goals': goal_count
                })
    
    # Convert to list and sort by goals
    goalscorers_list = []
    for name, stats in goalscorer_stats.items():
        goalscorers_list.append({
            'name': name,
            'goals': stats['goals'],
            'games_scored': len(stats['games']),
            'avg_per_scoring_game': stats['goals'] / len(stats['games']) if stats['games'] else 0,
            'details': stats['goal_details']
        })
    
    # Sort by goals scored (descending)
    goalscorers_list.sort(key=lambda x: x['goals'], reverse=True)
    
    print(f"\n🎯 TOP HAMPDEN GOALSCORERS (ETA PERIOD)")
    print("="*45)
    print(f"{'Rank':<4} {'Player':<15} {'Goals':<6} {'Games':<6} {'Avg':<5}")
    print("-" * 45)
    
    for i, scorer in enumerate(goalscorers_list[:15], 1):  # Top 15
        avg = scorer['avg_per_scoring_game']
        print(f"{i:<4} {scorer['name']:<15} {scorer['goals']:<6} {scorer['games_scored']:<6} {avg:.2f}")
    
    # Show detailed breakdown for top 5
    print(f"\n📊 DETAILED BREAKDOWN - TOP 5 HAMPDEN GOALSCORERS:")
    print("="*55)
    
    for i, scorer in enumerate(goalscorers_list[:5], 1):
        print(f"\n{i}. {scorer['name']} - {scorer['goals']} goals in {scorer['games_scored']} games")
        print("   Recent goals:")
        
        # Sort details by date (most recent first)
        details_sorted = sorted(scorer['details'], key=lambda x: x['date'], reverse=True)
        
        for detail in details_sorted[:5]:  # Show last 5 goal-scoring games
            goals_text = f"{detail['goals']} goal{'s' if detail['goals'] > 1 else ''}"
            print(f"   • {detail['date']} vs {detail['opponent']:15} ({goals_text})")
    
    # Summary statistics
    print(f"\n📈 HAMPDEN GOALSCORING SUMMARY:")
    print("="*35)
    
    total_goalscorers = len(goalscorers_list)
    total_goals = sum(scorer['goals'] for scorer in goalscorers_list)
    
    print(f"Total different goalscorers: {total_goalscorers}")
    print(f"Total goals by named scorers: {total_goals}")
    print(f"Average goals per scorer: {total_goals/total_goalscorers:.2f}")
    
    # Goals by era (rough groupings)
    print(f"\n🕒 GOALS BY ERA:")
    print("-" * 20)
    
    era_goals = {'1995-2005': 0, '2006-2015': 0, '2016-2025': 0}
    
    for scorer in goalscorers_list:
        for detail in scorer['details']:
            year = int(detail['date'][:4])
            if 1995 <= year <= 2005:
                era_goals['1995-2005'] += detail['goals']
            elif 2006 <= year <= 2015:
                era_goals['2006-2015'] += detail['goals']
            elif 2016 <= year <= 2025:
                era_goals['2016-2025'] += detail['goals']
    
    for era, goals in era_goals.items():
        print(f"{era}: {goals} goals")
    
    # Return top scorer for article use
    if goalscorers_list:
        top_scorer = goalscorers_list[0]
        print(f"\n🏆 TOP HAMPDEN GOALSCORER: {top_scorer['name']} ({top_scorer['goals']} goals)")
        return goalscorers_list[:10]  # Return top 10
    
    return []

if __name__ == "__main__":
    top_scorers = analyze_hampden_goalscorers()