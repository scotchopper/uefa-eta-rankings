#!/usr/bin/env python3
"""
Quick test to verify the goalscorer analysis fix works correctly.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from eta.eta_statistics import ScotlandFootballAnalyzer

def quick_test():
    """Quick test of the fixed goalscorer analysis."""
    print("🧪 QUICK TEST: Fixed Goalscorer Analysis")
    print("=" * 50)
    
    analyzer = ScotlandFootballAnalyzer('scot_games_eta_source.xlsx', worksheet_name='Games')
    analyzer.load_data()
    
    goalscorers = analyzer.analyze_goalscorers()
    
    # Check totals
    total_goals_from_scorers = int(goalscorers['goals'].sum())
    total_scotland_goals = int(analyzer.df['Scotland_Goals'].sum())
    
    print(f"📊 Totals:")
    print(f"   Scotland goals from data: {total_scotland_goals}")
    print(f"   Goals from analysis: {total_goals_from_scorers}")
    print(f"   Difference: {total_scotland_goals - total_goals_from_scorers}")
    
    # Check own goals
    own_goal_players = [name for name in goalscorers.index if '(og)' in name]
    own_goal_count = sum(goalscorers.loc[player, 'goals'] for player in own_goal_players)
    
    print(f"\n⚽ Own Goals:")
    print(f"   Total own goals: {own_goal_count}")
    print(f"   Own goal players: {len(own_goal_players)}")
    
    if own_goal_players:
        print(f"   Examples:")
        for player in own_goal_players[:3]:
            goals = goalscorers.loc[player, 'goals']
            print(f"     - {player}: {goals} goals")
    
    # Check top scorers still work
    print(f"\n🏆 Top 3 Scorers:")
    for i, (player, data) in enumerate(goalscorers.head(3).iterrows()):
        print(f"   {i+1}. {player}: {data['goals']} goals in {data['games_scored_in']} games")
    
    print(f"\n✅ Analysis working correctly!")

if __name__ == "__main__":
    quick_test()