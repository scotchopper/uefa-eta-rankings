#!/usr/bin/env python3
"""
Create visualizations for ETA 30th Anniversary data.
Direct approach using the ScotlandFootballAnalyzer.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import matplotlib.pyplot as plt
import pandas as pd
from eta.eta_statistics import ScotlandFootballAnalyzer
import os
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
try:
    from PIL import Image
    FLAGS_AVAILABLE = True
except ImportError:
    FLAGS_AVAILABLE = False
    print("⚠️  PIL not available - flags will be skipped")

# Country name to flag file mapping
COUNTRY_FLAG_MAPPING = {
    'Lithuania': 'lt',
    'Czechia': 'cz', 
    'Denmark': 'dk',
    'Faroe Islands': 'fo',
    'Netherlands': 'nl',
    'Norway': 'no',
    'England': 'gb-eng',
    'Austria': 'at',
    'Croatia': 'hr',
    'Israel': 'il',
    'Belgium': 'be',
    'Republic of Ireland': 'ie',
    'Poland': 'pl',
    'France': 'fr',
    'Wales': 'gb-wls',
    'Germany': 'de',
    'Spain': 'es',
    'Italy': 'it',
    'Portugal': 'pt',
    'Switzerland': 'ch',
    'Sweden': 'se',
    'Finland': 'fi',
    'Iceland': 'is',
    'Latvia': 'lv',
    'Estonia': 'ee',
    'Slovenia': 'si',
    'Slovakia': 'sk',
    'Hungary': 'hu',
    'Romania': 'ro',
    'Bulgaria': 'bg',
    'Greece': 'gr',
    'Turkey': 'tr',
    'Cyprus': 'cy',
    'Malta': 'mt',
    'Luxembourg': 'lu',
    'Moldova': 'md',
    'North Macedonia': 'mk',
    'Montenegro': 'me',
    'Serbia': 'rs',
    'Bosnia and Herzegovina': 'ba',
    'Albania': 'al',
    'Kosovo': 'xk',
    'Andorra': 'ad',
    'San Marino': 'sm',
    'Liechtenstein': 'li',
    'Gibraltar': 'gi'
}

FLAGS_DIR = "flags"

def get_country_emoji(country_name):
    """Get flag emoji for country (as fallback if image flags not available)."""
    country_emojis = {
        'Lithuania': '🇱🇹',
        'Czechia': '🇨🇿', 
        'Denmark': '🇩🇰',
        'Faroe Islands': '🇫🇴',
        'Netherlands': '🇳🇱',
        'Norway': '🇳🇴',
        'England': '🏴󠁧󠁢󠁥󠁮󠁧󠁿',
        'Austria': '🇦🇹',
        'Croatia': '🇭🇷',
        'Israel': '🇮🇱',
        'Belgium': '🇧🇪',
        'Republic of Ireland': '🇮🇪',
        'Poland': '🇵🇱',
        'France': '🇫🇷',
        'Wales': '🏴󠁧󠁢󠁷󠁬󠁳󠁿',
        'Germany': '🇩🇪',
        'Spain': '🇪🇸',
        'Italy': '🇮🇹',
        'Portugal': '🇵🇹',
        'Switzerland': '🇨🇭',
        'Sweden': '🇸🇪',
        'Finland': '🇫🇮',
        'Iceland': '🇮🇸'
    }
    return country_emojis.get(country_name, '🏳️')

def load_flag_image(country_name, size=(50, 35)):
    """Load PNG flag image and resize for chart display."""
    if not FLAGS_AVAILABLE:
        return None
    
    flag_code = COUNTRY_FLAG_MAPPING.get(country_name)
    if not flag_code:
        return None
    
    png_path = os.path.join(FLAGS_DIR, f"{flag_code}.png")
    
    try:
        if os.path.exists(png_path):
            img = Image.open(png_path)
            # Resize to desired size while maintaining aspect ratio
            img = img.resize((size[0], size[1]), Image.Resampling.LANCZOS)
            img = img.convert('RGBA')
            return np.array(img)
        else:
            print(f"   ⚠️  Flag PNG not found for: {country_name}")
            return None
    except Exception as e:
        print(f"   ⚠️  Error loading flag for {country_name}: {e}")
        return None

def create_eta_charts():
    """Create charts from ETA data."""
    print("📊 Creating ETA 30th Anniversary Charts")
    print("=" * 50)
    
    try:
        # Load the data
        analyzer = ScotlandFootballAnalyzer('scot_games_eta_source.xlsx', worksheet_name='ETA30th')
        analyzer.load_data()
        
        if analyzer.df is None:
            print("❌ Failed to load data")
            return
        
        print(f"✅ Loaded {len(analyzer.df)} matches")
        
        # 1. Results Pie Chart
        print("📈 Creating Results Pie Chart...")
        result_counts = analyzer.df['Result'].value_counts()
        
        plt.figure(figsize=(10, 8))
        colors = ['#28a745', '#dc3545', '#ffc107', '#17a2b8']
        plt.pie(result_counts.values, labels=result_counts.index, 
               autopct='%1.1f%%', colors=colors[:len(result_counts)], startangle=90)
        plt.title('Scotland Results - ETA Period (1995-2025)', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig('eta_results.png', dpi=300, bbox_inches='tight')
        plt.close()  # Close instead of show to prevent blocking
        print("   ✅ Saved: eta_results.png")
        
        # 2. Top Opponents Bar Chart with Flags
        print("📈 Creating Opponents Chart...")
        opposition_stats = analyzer.analyze_by_opposition()
        # Include countries with 7+ matches instead of just top 10
        top_opponents = opposition_stats[opposition_stats['matches_played'] >= 7].copy()
        
        # Add penalty wins to each opponent for sorting
        for opponent in top_opponents.index:
            opponent_matches = analyzer.df[analyzer.df['Opposition'] == opponent]
            wp_count = len(opponent_matches[opponent_matches['Result'] == 'WinPens'])
            top_opponents.loc[opponent, 'penalty_wins'] = wp_count
            # The 'wins' column only includes 'Win' results, not 'WinPens', so add them
            regular_wins = int(top_opponents.loc[opponent, 'wins'])
            top_opponents.loc[opponent, 'total_wins'] = regular_wins + wp_count
        
        # Sort by: 1) matches_played (desc), 2) total_wins (desc), 3) draws (desc), 4) name (asc)
        # First sort alphabetically by index (country name), then by the main criteria
        top_opponents = top_opponents.sort_index()  # Sort by name first
        top_opponents = top_opponents.sort_values(
            ['matches_played', 'total_wins', 'draws'], 
            ascending=[False, False, False],
            kind='stable'  # Keep alphabetical order for ties
        )
        
        fig, ax = plt.subplots(figsize=(16, 10))
        
        # Calculate penalty wins and regular wins for each opponent
        pen_wins = []
        regular_wins = []
        draws = top_opponents['draws'].values
        losses = top_opponents['losses'].values
        
        for opponent in top_opponents.index:
            # Count WinPens results for this opponent
            opponent_matches = analyzer.df[analyzer.df['Opposition'] == opponent]
            wp_count = len(opponent_matches[opponent_matches['Result'] == 'WinPens'])
            pen_wins.append(wp_count)
            
            # Regular wins = only 'Win' results (not including 'WinPens')
            regular_win_count = int(top_opponents.loc[opponent, 'wins'])  # This is just 'Win' results
            regular_wins.append(regular_win_count)
        
        # Create stacked bars
        bar_width = 0.8
        x_positions = range(len(top_opponents))
        
        # Stack the bars: losses (red) at bottom, draws (yellow), regular wins (green), pen wins (blue) on top
        bars_losses = ax.bar(x_positions, losses, bar_width, color='#dc3545', alpha=0.8, label='Losses')
        bars_draws = ax.bar(x_positions, draws, bar_width, bottom=losses, color='#ffc107', alpha=0.8, label='Draws')
        bars_wins = ax.bar(x_positions, regular_wins, bar_width, bottom=[l+d for l,d in zip(losses, draws)], color='#28a745', alpha=0.8, label='Wins')
        
        # Add penalty wins if any exist
        if any(pen_wins):
            bars_pen_wins = ax.bar(x_positions, pen_wins, bar_width, 
                                 bottom=[l+d+w for l,d,w in zip(losses, draws, regular_wins)], 
                                 color='#007bff', alpha=0.8, label='Wins on Penalties')
        
        ax.set_xlabel('Opponents', fontweight='bold', fontsize=12)
        ax.set_ylabel('Matches', fontweight='bold', fontsize=12)
        ax.set_title(f'Top {len(top_opponents)} Opponents (7+ matches) - ETA Period', fontsize=16, fontweight='bold')
        ax.set_xticks(x_positions)
        ax.set_xticklabels(top_opponents.index.tolist(), rotation=45, ha='right')
        
        # Add legend in reverse order to match chart stacking (top to bottom)
        if any(pen_wins):
            legend_handles = [bars_pen_wins, bars_wins, bars_draws, bars_losses]
        else:
            legend_handles = [bars_wins, bars_draws, bars_losses]
        ax.legend(handles=legend_handles, loc='upper right')
        
        # Add match count labels on bars
        for i, total_matches in enumerate(top_opponents['matches_played']):
            ax.text(i, total_matches + 0.1, f'{int(total_matches)}', 
                   ha='center', va='bottom', fontweight='bold')
        
        # Set y-axis range from 0 to 11
        ax.set_ylim(0, 11)
        
        # Add flags inside bars
        print("   🏁 Adding country flags inside bars...")
        for i, country in enumerate(top_opponents.index):
            flag_img = None
            if FLAGS_AVAILABLE:
                # Load flag with larger size to span bar width
                flag_img = load_flag_image(country, size=(90, 60))
            
            if flag_img is not None:
                # Position flag at bottom of the stacked bar, centered
                flag_x = i  # x position matches bar position
                flag_y = 0.8  # Just above the bottom of the y-axis range
                
                # Create OffsetImage and AnnotationBbox - larger zoom to span bar width
                imagebox = OffsetImage(flag_img, zoom=0.35)
                ab = AnnotationBbox(imagebox, (flag_x, flag_y), frameon=False)
                ax.add_artist(ab)
            else:
                # Fallback to country codes with colored background
                flag_code = COUNTRY_FLAG_MAPPING.get(country, country[:3])
                if flag_code is None:
                    flag_code = country[:3]
                flag_x = i
                flag_y = 0.8
                
                # Create a colored box for the country code
                colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', 
                         '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9']
                color = colors[i % len(colors)]
                
                # Add a rectangular background
                bbox_props = dict(boxstyle="round,pad=0.3", facecolor=color, alpha=0.7)
                ax.text(flag_x, flag_y, flag_code.upper(), ha='center', va='center', 
                       fontsize=12, fontweight='bold', bbox=bbox_props, color='white')
        
        plt.tight_layout()
        plt.savefig('eta_opponents.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("   ✅ Saved: eta_opponents.png")
        
        # 3. Goalscorers Bar Chart
        print("📈 Creating Goalscorers Chart...")
        goalscorers = analyzer.analyze_goalscorers()
        top_scorers = goalscorers.head(10)
        
        plt.figure(figsize=(12, 8))
        bars = plt.bar(range(len(top_scorers)), top_scorers['goals'], color='#dc3545', alpha=0.7)
        plt.xlabel('Players', fontweight='bold')
        plt.ylabel('Goals', fontweight='bold')
        plt.title('Top 10 Goalscorers - ETA Period', fontsize=14, fontweight='bold')
        plt.xticks(range(len(top_scorers)), top_scorers.index.tolist(), rotation=45, ha='right')
        
        # Add labels
        for i, bar in enumerate(bars):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.2,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('eta_goalscorers.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("   ✅ Saved: eta_goalscorers.png")
        
        # 4. Goals by Year Line Chart
        print("📈 Creating Goals by Year Chart...")
        analyzer.df['Year'] = pd.to_datetime(analyzer.df['Date']).dt.year
        yearly_goals = analyzer.df.groupby('Year')['Scot'].sum().sort_index()
        
        plt.figure(figsize=(12, 8))
        plt.plot(yearly_goals.index, yearly_goals.values, marker='o', 
                linewidth=2, markersize=6, color='#28a745')
        plt.xlabel('Year', fontweight='bold')
        plt.ylabel('Goals', fontweight='bold')
        plt.title('Scotland Goals by Year - ETA Period', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('eta_goals_by_year.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("   ✅ Saved: eta_goals_by_year.png")
        
        # 5. Venue Distribution Pie Chart
        print("📈 Creating Venue Chart...")
        venue_stats = analyzer.df['Home\\Away'].value_counts()
        
        plt.figure(figsize=(10, 8))
        colors = ['#007bff', '#28a745', '#ffc107']
        labels = ['Home', 'Away', 'Neutral']
        plt.pie(venue_stats.values, labels=labels[:len(venue_stats)], 
               autopct='%1.1f%%', colors=colors[:len(venue_stats)], startangle=90)
        plt.title('Match Venues - ETA Period', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig('eta_venues.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("   ✅ Saved: eta_venues.png")
        
        print(f"\n🎉 All charts created successfully!")
        print(f"📁 Generated 5 chart files:")
        print(f"   • eta_results.png")
        print(f"   • eta_opponents.png") 
        print(f"   • eta_goalscorers.png")
        print(f"   • eta_goals_by_year.png")
        print(f"   • eta_venues.png")
        
    except Exception as e:
        print(f"❌ Error creating charts: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_eta_charts()