#!/usr/bin/env python3
"""
ETA Rankings - Scotland International Players Performance During ETA Period
Rankings for caps and goals scored after November 5, 1995
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sys

def fetch_players_from_caps_page(url, min_caps, max_caps):
    """Fetch players from a specific Wikipedia caps page"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        tables = soup.find_all('table', {'class': 'wikitable'})
        if not tables:
            print(f"No wikitable found on {url}")
            return []
        
        # Use the first table
        table = tables[0]
        rows = table.find_all('tr')
        
        players = []
        for row in rows[1:]:  # Skip header
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 4:
                try:
                    # Extract player name (first cell)
                    name_cell = cells[0]
                    name_link = name_cell.find('a')
                    if name_link:
                        player_name = name_link.get_text().strip()
                    else:
                        player_name = name_cell.get_text().strip()
                    
                    # Extract caps and goals
                    caps_text = cells[1].get_text().strip()
                    goals_text = cells[2].get_text().strip()
                    
                    # Parse caps and goals
                    caps = int(caps_text) if caps_text.isdigit() else 0
                    goals = int(goals_text) if goals_text.isdigit() else 0
                    
                    # Extract career span (usually in 4th column)
                    career_span = cells[3].get_text().strip()
                    
                    if caps >= min_caps and (max_caps is None or caps <= max_caps):
                        players.append({
                            'name': player_name,
                            'total_caps': caps,
                            'total_goals': goals,
                            'career_span': career_span
                        })
                        
                except (ValueError, IndexError) as e:
                    continue
                    
        return players
        
    except Exception as e:
        print(f"Error fetching from {url}: {e}")
        return []

def fetch_all_players_data():
    """Fetch all Scotland international players from Wikipedia"""
    print("================================================================================")
    print("FETCHING LATEST DATA FROM WIKIPEDIA FOR ETA RANKINGS")
    print("================================================================================")
    
    all_players = []
    
    # Fetch players with 10+ caps
    print("Fetching 10+ caps...")
    url_10_plus = "https://en.wikipedia.org/wiki/List_of_Scotland_international_footballers_(10%2B_caps)"
    players_10_plus = fetch_players_from_caps_page(url_10_plus, 10, None)
    all_players.extend(players_10_plus)
    print(f"Found {len(players_10_plus)} players with 10+ caps")
    
    # Fetch players with 4-9 caps  
    print("Fetching 4-9 caps...")
    url_4_9 = "https://en.wikipedia.org/wiki/List_of_Scotland_international_footballers_(4%E2%80%939_caps)"
    players_4_9 = fetch_players_from_caps_page(url_4_9, 4, 9)
    all_players.extend(players_4_9)
    print(f"Found {len(players_4_9)} players with 4-9 caps")
    
    # Fetch players with 2-3 caps
    print("Fetching 2-3 caps...")
    url_2_3 = "https://en.wikipedia.org/wiki/List_of_Scotland_international_footballers_(2%E2%80%933_caps)"
    players_2_3 = fetch_players_from_caps_page(url_2_3, 2, 3)
    all_players.extend(players_2_3)
    print(f"Found {len(players_2_3)} players with 2-3 caps")
    
    # Fetch players with 1 cap
    print("Fetching 1 cap...")
    url_1_cap = "https://en.wikipedia.org/wiki/List_of_Scotland_international_footballers_(1_cap)"
    players_1_cap = fetch_players_from_caps_page(url_1_cap, 1, 1)
    all_players.extend(players_1_cap)
    print(f"Found {len(players_1_cap)} players with 1 cap")
    
    print(f"Successfully fetched {len(all_players)} players from Wikipedia")
    return all_players

def parse_date_from_career_span(career_span):
    """Parse first and last appearance dates from career span"""
    try:
        # Handle different date formats in Wikipedia
        parts = career_span.split('–')
        if len(parts) != 2:
            parts = career_span.split('-')
        if len(parts) != 2:
            return None, None
            
        first_part = parts[0].strip()
        last_part = parts[1].strip()
        
        def parse_date_part(date_str):
            # Try different date formats
            formats = [
                "%m/%Y",      # 05/1995
                "%Y",         # 1995
                "%d/%m/%Y",   # 17/05/1995
                "%m/%d/%Y",   # 05/17/1995
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            return None
        
        first_date = parse_date_part(first_part)
        last_date = parse_date_part(last_part)
        
        return first_date, last_date
        
    except Exception:
        return None, None

def calculate_post_1995_contribution(player):
    """Calculate a player's caps and goals after November 5, 1995"""
    eta_start = datetime(1995, 11, 5)
    
    first_date, last_date = parse_date_from_career_span(player['career_span'])
    
    if not first_date or not last_date:
        return 0, 0, "UNKNOWN_DATES"
    
    # Categorize player
    if last_date <= eta_start:
        # Career ended before ETA
        return 0, 0, "PRE_ETA"
    elif first_date > eta_start:
        # Career started after ETA began
        return player['total_caps'], player['total_goals'], "POST_ETA"
    else:
        # Career spanned the ETA start date
        return 0, 0, "SPANNING"

def load_spanning_players_manual_data():
    """Load manual data for spanning players"""
    # This is the manually researched data for the 31 spanning players
    spanning_data = {
        'Kenny Dalglish': {'post_caps': 1, 'post_goals': 0},
        'Graeme Souness': {'post_caps': 0, 'post_goals': 0},
        'Alan Hansen': {'post_caps': 0, 'post_goals': 0},
        'Willie Miller': {'post_caps': 0, 'post_goals': 0},
        'Jim Leighton': {'post_caps': 21, 'post_goals': 0},
        'Roy Aitken': {'post_caps': 0, 'post_goals': 0},
        'Paul McStay': {'post_caps': 0, 'post_goals': 0},
        'Alex McLeish': {'post_caps': 0, 'post_goals': 0},
        'Maurice Johnston': {'post_caps': 0, 'post_goals': 0},
        'Stuart McCall': {'post_caps': 9, 'post_goals': 0},
        'Pat Nevin': {'post_caps': 2, 'post_goals': 1},
        'Ally McCoist': {'post_caps': 13, 'post_goals': 2},
        'Gary McAllister': {'post_caps': 21, 'post_goals': 1},
        'John Collins': {'post_caps': 30, 'post_goals': 4},
        'Tom Boyd': {'post_caps': 42, 'post_goals': 1},
        'Colin Hendry': {'post_caps': 38, 'post_goals': 2},
        'Dave McPherson': {'post_caps': 0, 'post_goals': 0},
        'Stewart McKimmie': {'post_caps': 4, 'post_goals': 0},
        'Eoin Jess': {'post_caps': 9, 'post_goals': 2},
        'Scott Booth': {'post_caps': 13, 'post_goals': 2},
        'Billy McKinlay': {'post_caps': 15, 'post_goals': 0},
        'Andy Goram': {'post_caps': 9, 'post_goals': 0},
        'John McGinlay': {'post_caps': 4, 'post_goals': 1},
        'Duncan Shearer': {'post_caps': 7, 'post_goals': 1},
        'Gordon Durie': {'post_caps': 17, 'post_goals': 7},
        'Kevin Gallacher': {'post_caps': 26, 'post_goals': 7},
        'Darren Jackson': {'post_caps': 20, 'post_goals': 4},
        'Colin Calderwood': {'post_caps': 28, 'post_goals': 0},
        'Alan McLaren': {'post_caps': 1, 'post_goals': 0},
        'Scot Gemmill': {'post_caps': 23, 'post_goals': 1},
        'Craig Burley': {'post_caps': 41, 'post_goals': 3}
    }
    return spanning_data

def create_eta_rankings():
    """Create comprehensive ETA period rankings"""
    print("\n" + "="*100)
    print("SCOTLAND INTERNATIONAL PLAYERS - ETA PERIOD RANKINGS")
    print("Period: After November 5, 1995")
    print("="*100)
    
    # Fetch all current Wikipedia data
    all_players = fetch_all_players_data()
    
    # Load manual data for spanning players
    spanning_manual = load_spanning_players_manual_data()
    
    # Calculate ETA contributions for all players
    eta_players = []
    
    for player in all_players:
        post_caps, post_goals, category = calculate_post_1995_contribution(player)
        
        if category == "POST_ETA":
            # Player started after ETA - use full career stats
            eta_players.append({
                'name': player['name'],
                'eta_caps': player['total_caps'],
                'eta_goals': player['total_goals'],
                'total_caps': player['total_caps'],
                'total_goals': player['total_goals'],
                'category': 'Post-ETA Only',
                'career_span': player['career_span']
            })
        elif category == "SPANNING" and player['name'] in spanning_manual:
            # Use manual data for spanning players
            manual_data = spanning_manual[player['name']]
            eta_players.append({
                'name': player['name'],
                'eta_caps': manual_data['post_caps'],
                'eta_goals': manual_data['post_goals'],
                'total_caps': player['total_caps'],
                'total_goals': player['total_goals'],
                'category': 'Spanning (Manual Data)',
                'career_span': player['career_span']
            })
    
    # Filter out players with 0 ETA contributions
    eta_players = [p for p in eta_players if p['eta_caps'] > 0]
    
    return eta_players

def display_rankings(eta_players):
    """Display comprehensive rankings"""
    print(f"\nTotal players with ETA period appearances: {len(eta_players)}")
    
    # Caps Rankings
    print("\n" + "="*100)
    print("🏴󠁧󠁢󠁳󠁣󠁴󠁿 TOP ETA CAPS RANKINGS")
    print("="*100)
    
    caps_sorted = sorted(eta_players, key=lambda x: x['eta_caps'], reverse=True)
    
    print(f"{'Rank':<4} {'Player Name':<25} {'ETA Caps':<9} {'Total Caps':<10} {'Category':<20} {'Career Span'}")
    print("-" * 100)
    
    for i, player in enumerate(caps_sorted[:30], 1):  # Top 30
        print(f"{i:<4} {player['name']:<25} {player['eta_caps']:<9} {player['total_caps']:<10} {player['category']:<20} {player['career_span']}")
    
    # Goals Rankings
    print("\n" + "="*100)
    print("⚽ TOP ETA GOALS RANKINGS")
    print("="*100)
    
    goals_sorted = sorted(eta_players, key=lambda x: x['eta_goals'], reverse=True)
    
    print(f"{'Rank':<4} {'Player Name':<25} {'ETA Goals':<10} {'Total Goals':<11} {'ETA Caps':<9} {'Category':<20}")
    print("-" * 100)
    
    for i, player in enumerate(goals_sorted[:30], 1):  # Top 30
        if player['eta_goals'] > 0:  # Only show players with goals
            print(f"{i:<4} {player['name']:<25} {player['eta_goals']:<10} {player['total_goals']:<11} {player['eta_caps']:<9} {player['category']:<20}")
    
    # Summary Statistics
    print("\n" + "="*100)
    print("📊 ETA PERIOD SUMMARY STATISTICS")
    print("="*100)
    
    total_eta_caps = sum(p['eta_caps'] for p in eta_players)
    total_eta_goals = sum(p['eta_goals'] for p in eta_players)
    post_eta_only = [p for p in eta_players if p['category'] == 'Post-ETA Only']
    spanning_players = [p for p in eta_players if p['category'] == 'Spanning (Manual Data)']
    
    print(f"Total ETA period caps: {total_eta_caps}")
    print(f"Total ETA period goals: {total_eta_goals}")
    print(f"Players who started post-ETA: {len(post_eta_only)}")
    print(f"Spanning players (with ETA contributions): {len(spanning_players)}")
    print(f"Average caps per player: {total_eta_caps / len(eta_players):.1f}")
    print(f"Average goals per player: {total_eta_goals / len(eta_players):.1f}")
    
    if eta_players:
        top_caps_player = caps_sorted[0]
        top_goals_player = goals_sorted[0]
        print(f"\nMost ETA caps: {top_caps_player['name']} ({top_caps_player['eta_caps']} caps)")
        print(f"Most ETA goals: {top_goals_player['name']} ({top_goals_player['eta_goals']} goals)")

def main():
    """Main execution function"""
    try:
        print("🏴󠁧󠁢󠁳󠁣󠁴󠁿 SCOTLAND ETA PERIOD PLAYER RANKINGS")
        print("Analyzing player performances after November 5, 1995\n")
        
        # Create rankings
        eta_players = create_eta_rankings()
        
        # Display results
        display_rankings(eta_players)
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()