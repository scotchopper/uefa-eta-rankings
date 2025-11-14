#!/usr/bin/env python3
"""
ETA 30th Anniversary Data Visualization

Creates comprehensive charts and graphs from the analyze_eta30th.py data:
- Pie charts for results distribution, venue types, competition types
- Bar charts for top opponents, goalscorers, managers, venues
- Line graphs for year-by-year performance trends
- Comparison charts for home vs away performance
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from eta.eta_statistics import ScotlandFootballAnalyzer

# Set style for better looking charts
try:
    plt.style.use('seaborn-v0_8')
except:
    plt.style.use('default')
sns.set_palette("husl")

def create_eta_visualizations():
    """Create comprehensive visualizations for ETA 30th anniversary data."""
    print("📊 CREATING ETA 30TH ANNIVERSARY VISUALIZATIONS")
    print("=" * 60)
    
    # Load ETA data
    analyzer = ScotlandFootballAnalyzer('scot_games_eta_source.xlsx', worksheet_name='ETA30th')
    analyzer.load_data()
    
    if analyzer.df is None:
        print("❌ Failed to load data!")
        return
    
    print(f"✅ Loaded {len(analyzer.df)} matches from ETA30th period")
    
    # Create output directory
    os.makedirs('data/visualizations', exist_ok=True)
    
    # Set up the figure layout
    fig = plt.figure(figsize=(20, 24))
    
    # 1. Overall Results Pie Chart
    plt.subplot(4, 3, 1)
    results = analyzer.df['Result'].value_counts()
    colors = ['#2E8B57', '#FFD700', '#DC143C', '#4169E1']  # Green, Gold, Red, Blue
    plt.pie(results.values, labels=[f'{k}\n({v} games)' for k, v in results.items()], 
            autopct='%1.1f%%', colors=colors[:len(results)])
    plt.title('ETA Period: Match Results Distribution\n(1995-2025)', fontsize=12, fontweight='bold')
    
    # 2. Home vs Away Performance
    plt.subplot(4, 3, 2)
    venue_stats = analyzer.df.groupby('Home\\Away').agg({
        'Result': ['count', lambda x: sum(x.isin(['Win', 'WP']))]
    }).round(1)
    venue_stats.columns = ['Total', 'Wins']
    venue_stats['Win_Rate'] = (venue_stats['Wins'] / venue_stats['Total'] * 100).round(1)
    
    venues = ['Home', 'Away', 'Neutral']
    win_rates = [venue_stats.loc[v, 'Win_Rate'] if v in venue_stats.index else 0 for v in venues]
    colors_venue = ['#228B22', '#FF6347', '#4682B4']
    
    bars = plt.bar(venues, win_rates, color=colors_venue)
    plt.title('Win Rate by Venue Type\n(ETA Period)', fontsize=12, fontweight='bold')
    plt.ylabel('Win Rate (%)')
    plt.ylim(0, 60)
    
    # Add value labels on bars
    for bar, rate in zip(bars, win_rates):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                f'{rate:.1f}%', ha='center', fontweight='bold')
    
    # 3. Top 10 Opponents (by frequency)
    plt.subplot(4, 3, 3)
    opposition_stats = analyzer.analyze_by_opposition()
    top_opponents = opposition_stats.head(10)
    
    y_pos = np.arange(len(top_opponents))
    plt.barh(y_pos, top_opponents['matches_played'], color='skyblue')
    plt.yticks(y_pos, [f"{opp}\n({int(top_opponents.loc[opp, 'wins'])}W)" 
                       for opp in top_opponents.index])
    plt.xlabel('Number of Matches')
    plt.title('Top 10 Most Frequent Opponents\n(ETA Period)', fontsize=12, fontweight='bold')
    plt.gca().invert_yaxis()
    
    # 4. Top Goalscorers
    plt.subplot(4, 3, 4)
    goalscorers = analyzer.analyze_goalscorers()
    # Filter out own goals for this chart
    goalscorers_filtered = goalscorers[~goalscorers.index.str.contains('og', case=False)]
    top_scorers = goalscorers_filtered.head(10)
    
    y_pos = np.arange(len(top_scorers))
    plt.barh(y_pos, top_scorers['goals'], color='lightcoral')
    plt.yticks(y_pos, [f"{scorer}\n({int(top_scorers.loc[scorer, 'games_scored_in'])} games)" 
                       for scorer in top_scorers.index])
    plt.xlabel('Goals Scored')
    plt.title('Top 10 Goalscorers\n(ETA Period)', fontsize=12, fontweight='bold')
    plt.gca().invert_yaxis()
    
    # 5. Manager Performance
    plt.subplot(4, 3, 5)
    manager_stats = analyzer.analyze_by_manager()
    # Filter managers with at least 10 games
    significant_managers = manager_stats[manager_stats['matches_played'] >= 10]
    
    if len(significant_managers) > 0:
        y_pos = np.arange(len(significant_managers))
        plt.barh(y_pos, significant_managers['win_percentage'], color='gold')
        plt.yticks(y_pos, [f"{mgr}\n({int(significant_managers.loc[mgr, 'matches_played'])} games)" 
                           for mgr in significant_managers.index])
        plt.xlabel('Win Percentage (%)')
        plt.title('Manager Performance\n(Min 10 games, ETA Period)', fontsize=12, fontweight='bold')
        plt.gca().invert_yaxis()
    
    # 6. Competition Types
    plt.subplot(4, 3, 6)
    competition_stats = analyzer.df['Competition'].value_counts().head(8)
    plt.pie(competition_stats.values, labels=[f'{k[:15]}{"..." if len(k) > 15 else ""}\n({v})' 
                                             for k, v in competition_stats.items()], 
            autopct='%1.1f%%')
    plt.title('Matches by Competition Type\n(ETA Period)', fontsize=12, fontweight='bold')
    
    # 7. Year-by-Year Goals Scored
    plt.subplot(4, 3, 7)
    yearly_stats = analyzer.get_year_by_year_analysis()
    years = yearly_stats.index
    goals_scored = yearly_stats['goals_scored']
    
    plt.plot(years, goals_scored, marker='o', linewidth=2, markersize=4, color='green')
    plt.title('Goals Scored by Year\n(ETA Period)', fontsize=12, fontweight='bold')
    plt.xlabel('Year')
    plt.ylabel('Goals Scored')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    
    # 8. Year-by-Year Win Percentage  
    plt.subplot(4, 3, 8)
    win_percentage = yearly_stats['win_percentage']
    
    plt.plot(years, win_percentage, marker='s', linewidth=2, markersize=4, color='blue')
    plt.title('Win Percentage by Year\n(ETA Period)', fontsize=12, fontweight='bold')
    plt.xlabel('Year')
    plt.ylabel('Win Percentage (%)')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    
    # 9. Top Venues by Frequency
    plt.subplot(4, 3, 9)
    venue_stats = analyzer.analyze_by_venue()
    # Filter venues with at least 3 games
    significant_venues = venue_stats[venue_stats['matches_played'] >= 3].head(10)
    
    y_pos = np.arange(len(significant_venues))
    plt.barh(y_pos, significant_venues['matches_played'], color='purple')
    plt.yticks(y_pos, [f"{venue}\n({significant_venues.loc[venue, 'win_percentage']:.1f}% wins)" 
                       for venue in significant_venues.index])
    plt.xlabel('Number of Matches')
    plt.title('Top Venues by Frequency\n(Min 3 games, ETA Period)', fontsize=12, fontweight='bold')
    plt.gca().invert_yaxis()
    
    # 10. Goals For vs Against by Year
    plt.subplot(4, 3, 10)
    goals_for = yearly_stats['goals_scored']
    goals_against = yearly_stats['goals_conceded']
    
    x = np.arange(len(years))
    width = 0.35
    
    plt.bar(x - width/2, goals_for, width, label='Goals For', color='green', alpha=0.7)
    plt.bar(x + width/2, goals_against, width, label='Goals Against', color='red', alpha=0.7)
    
    plt.xlabel('Year')
    plt.ylabel('Goals')
    plt.title('Goals For vs Against by Year\n(ETA Period)', fontsize=12, fontweight='bold')
    plt.xticks(x, years, rotation=45)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 11. Results Distribution by Decade
    plt.subplot(4, 3, 11)
    analyzer.df['Decade'] = (analyzer.df['Date'].dt.year // 10) * 10
    decade_results = pd.crosstab(analyzer.df['Decade'], analyzer.df['Result'])
    
    decade_results.plot(kind='bar', stacked=True, ax=plt.gca(), 
                       color=['green', 'gold', 'red', 'blue'])
    plt.title('Results by Decade\n(ETA Period)', fontsize=12, fontweight='bold')
    plt.xlabel('Decade')
    plt.ylabel('Number of Matches')
    plt.legend(title='Result')
    plt.xticks(rotation=0)
    
    # 12. Overall Statistics Summary
    plt.subplot(4, 3, 12)
    overall_stats = analyzer.get_overall_statistics()
    
    # Create a summary text
    summary_text = f"""ETA 30TH ANNIVERSARY SUMMARY
(1995-2025)

Total Matches: {len(analyzer.df)}
Win Rate: {overall_stats['win_percentage']:.1f}%
Goals Scored: {overall_stats['total_goals_scored']}
Goals Conceded: {overall_stats['total_goals_conceded']}
Goal Difference: {overall_stats['goal_difference']:+d}

Top Scorer: {goalscorers_filtered.index[0]}
({int(goalscorers_filtered.iloc[0]['goals'])} goals)

Most Played Opponent: {top_opponents.index[0]}
({int(top_opponents.iloc[0]['matches_played'])} games)

Most Used Venue: {significant_venues.index[0]}
({int(significant_venues.iloc[0]['matches_played'])} games)
"""
    
    plt.text(0.1, 0.9, summary_text, transform=plt.gca().transAxes, 
             fontsize=10, verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.5))
    plt.axis('off')
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig('data/visualizations/eta_30th_comprehensive_analysis.png', 
                dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"\n✅ Comprehensive visualization saved to: data/visualizations/eta_30th_comprehensive_analysis.png")
    
    # Create additional focused charts
    create_focused_charts(analyzer, goalscorers_filtered, yearly_stats)

def create_focused_charts(analyzer, goalscorers, yearly_stats):
    """Create focused individual charts for key metrics."""
    print(f"\n📈 Creating focused individual charts...")
    
    # 1. Detailed Goalscorers Chart
    plt.figure(figsize=(12, 8))
    top_15_scorers = goalscorers.head(15)
    
    bars = plt.bar(range(len(top_15_scorers)), top_15_scorers['goals'], 
                   color=plt.cm.Set3(np.linspace(0, 1, len(top_15_scorers))))
    
    plt.title('Top 15 Goalscorers - ETA Period (1995-2025)', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Players', fontsize=12)
    plt.ylabel('Goals Scored', fontsize=12)
    plt.xticks(range(len(top_15_scorers)), top_15_scorers.index, rotation=45, ha='right')
    
    # Add value labels on bars
    for bar, goals in zip(bars, top_15_scorers['goals']):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                f'{int(goals)}', ha='center', fontweight='bold')
    
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('data/visualizations/eta_top_goalscorers.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 2. Performance Trends Over Time
    plt.figure(figsize=(14, 8))
    years = yearly_stats.index
    
    plt.subplot(2, 1, 1)
    plt.plot(years, yearly_stats['win_percentage'], marker='o', linewidth=3, 
             markersize=6, color='blue', label='Win %')
    plt.axhline(y=yearly_stats['win_percentage'].mean(), color='red', linestyle='--', 
                label=f'Average ({yearly_stats["win_percentage"].mean():.1f}%)')
    plt.title('Scotland Performance Trends - ETA Period', fontsize=16, fontweight='bold')
    plt.ylabel('Win Percentage (%)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 1, 2)
    plt.plot(years, yearly_stats['goals_scored'], marker='s', linewidth=3, 
             markersize=6, color='green', label='Goals Scored')
    plt.plot(years, yearly_stats['goals_conceded'], marker='^', linewidth=3, 
             markersize=6, color='red', label='Goals Conceded')
    plt.axhline(y=yearly_stats['goals_scored'].mean(), color='green', linestyle='--', alpha=0.7)
    plt.axhline(y=yearly_stats['goals_conceded'].mean(), color='red', linestyle='--', alpha=0.7)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Goals', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('data/visualizations/eta_performance_trends.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 3. Opposition Analysis
    plt.figure(figsize=(12, 10))
    opposition_stats = analyzer.analyze_by_opposition().head(20)
    
    # Create a scatter plot: matches played vs win rate
    plt.scatter(opposition_stats['matches_played'], opposition_stats['win_percentage'], 
                s=opposition_stats['matches_played']*20, alpha=0.6, c=opposition_stats['win_percentage'],
                cmap='RdYlGn', edgecolors='black', linewidth=0.5)
    
    # Add labels for significant opponents
    for opponent in opposition_stats.head(10).index:
        plt.annotate(opponent, 
                    (opposition_stats.loc[opponent, 'matches_played'], 
                     opposition_stats.loc[opponent, 'win_percentage']),
                    xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    plt.colorbar(label='Win Percentage (%)')
    plt.title('Opposition Analysis - ETA Period\n(Bubble size = number of matches)', 
              fontsize=16, fontweight='bold')
    plt.xlabel('Matches Played', fontsize=12)
    plt.ylabel('Win Percentage (%)', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('data/visualizations/eta_opposition_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"✅ Individual charts saved:")
    print(f"   - data/visualizations/eta_top_goalscorers.png")
    print(f"   - data/visualizations/eta_performance_trends.png") 
    print(f"   - data/visualizations/eta_opposition_analysis.png")

def main():
    """Create all ETA visualizations."""
    try:
        create_eta_visualizations()
        print(f"\n🎉 All ETA 30th Anniversary visualizations created successfully!")
        print(f"📂 Check the data/visualizations/ folder for all charts and graphs.")
        
    except Exception as e:
        print(f"❌ Error creating visualizations: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()