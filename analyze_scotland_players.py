#!/usr/bin/env python3
"""
Script to analyze Scotland international footballers (1+ caps) based on first and last cap dates
relative to November 5th, 1995.

Dynamically fetches data from Wikipedia pages to stay current with latest matches.
Includes players with 10+ caps, players with 4-9 caps, players with 2-3 caps, and players with 1 cap.
"""

import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import time
from spanning_players_template import spanning_players_data

def parse_date(date_str):
    """Parse date string from Wikipedia format to datetime object."""
    if not date_str or date_str.strip() == "":
        return None
    
    # Remove extra whitespace and clean up
    date_str = date_str.strip()
    
    try:
        # Format: "5 November 1995"
        return datetime.strptime(date_str, "%d %B %Y")
    except ValueError:
        try:
            # Format: "5 June 2015" - try different format
            return datetime.strptime(date_str, "%d %B %Y")
        except ValueError:
            print(f"Could not parse date: '{date_str}'")
            return None

def fetch_wikipedia_page(url, description):
    """Fetch a Wikipedia page with error handling and rate limiting."""
    print(f"Fetching {description}...")
    try:
        # Add a small delay to be respectful to Wikipedia servers
        time.sleep(1)
        
        headers = {
            'User-Agent': 'Scotland Football Analysis Script/1.0 (Educational Use)'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.RequestException as e:
        print(f"Error fetching {description}: {e}")
        return None

def extract_one_cap_players(soup):
    """Extract player data from the 1-cap Wikipedia page (different format)."""
    players_data = []
    
    if not soup:
        return players_data
    
    # Find the main table with 1-cap players
    tables = soup.find_all('table', class_='wikitable')
    
    for table in tables:
        rows = table.find_all('tr')
        
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) < 6:  # Need at least 6 cells for player data
                continue
                
            try:
                # For 1-cap players, the format is: Name | Reference | Caps | Goals | Date | Opponent
                name = cells[0].get_text().strip().rstrip('*')
                if not name or name in ['Player', 'Name', ''] or name.startswith('Key'):
                    continue
                
                # Skip header rows and empty rows
                if '|' not in str(cells[0]) and name:
                    # Extract caps (should be 1)
                    caps_text = cells[2].get_text().strip() if len(cells) > 2 else "1"
                    caps = 1  # All players on this page have 1 cap
                    
                    # Extract goals
                    goals_text = cells[3].get_text().strip() if len(cells) > 3 else "0"
                    goals_match = re.search(r'(\d+)', goals_text)
                    goals = int(goals_match.group(1)) if goals_match else 0
                    
                    # Extract date
                    date_text = cells[4].get_text().strip() if len(cells) > 4 else ""
                    
                    # Extract opponent
                    opponent_text = cells[5].get_text().strip() if len(cells) > 5 else ""
                    
                    # Create a position number from the date for consistency with other formats
                    try:
                        date_obj = parse_date(date_text)
                        if date_obj:
                            position = (date_obj.year - 1870) * 365 + date_obj.timetuple().tm_yday
                        else:
                            position = 50000
                    except:
                        position = 50000
                    
                    # Create player data string in the same format as other functions
                    player_line = f"{name} | [{position}] | {caps} | {goals} | {date_text} | {opponent_text} | {date_text} | {opponent_text}"
                    players_data.append(player_line)
                
            except Exception as e:
                # Skip problematic rows
                continue
    
    return players_data

def extract_players_from_table(soup, min_caps, max_caps=None):
    """Extract player data from Wikipedia table."""
    players_data = []
    
    if not soup:
        return players_data
    
    # Special handling for 1-cap players (different format)
    if min_caps == 1 and max_caps == 1:
        return extract_one_cap_players(soup)
    
    # Find all tables on the page
    tables = soup.find_all('table', class_='wikitable')
    
    for table in tables:
        rows = table.find_all('tr')
        
        # Skip the first 2 rows (headers) and process player data
        for row in rows[2:]:  # Skip header rows
            cells = row.find_all(['td', 'th'])
            if len(cells) < 8:  # Need 8 cells for full player data
                continue
                
            try:
                # Extract player name (first cell, remove asterisks and clean up)
                name = cells[0].get_text().strip().rstrip('*')
                if not name or name in ['Player', 'Name', '']:
                    continue
                
                # Extract caps (third cell - index 2)
                caps_text = cells[2].get_text().strip()
                caps_match = re.search(r'(\d+)', caps_text)
                if not caps_match:
                    continue
                caps = int(caps_match.group(1))
                
                # Filter by cap range
                if caps < min_caps:
                    continue
                if max_caps and caps > max_caps:
                    continue
                
                # Extract goals (fourth cell - index 3)
                goals_text = cells[3].get_text().strip()
                goals_match = re.search(r'(\d+)', goals_text)
                goals = int(goals_match.group(1)) if goals_match else 0
                
                # Extract first cap date (fifth cell - index 4)
                first_cap_date = cells[4].get_text().strip()
                
                # Extract first cap opponent (sixth cell - index 5)
                first_cap_opponent = cells[5].get_text().strip()
                
                # Extract last cap date (seventh cell - index 6)
                last_cap_date = cells[6].get_text().strip()
                
                # Extract last cap opponent (eighth cell - index 7)
                last_cap_opponent = cells[7].get_text().strip()
                
                # Create player data entry
                player_data = f"{name} | [{len(players_data)+1}] | {caps} | {goals} | {first_cap_date} | {first_cap_opponent} | {last_cap_date} | {last_cap_opponent}"
                players_data.append(player_data)
                
            except (ValueError, IndexError) as e:
                continue
    
    return players_data

def fetch_all_players_data():
    """Fetch player data from all Wikipedia pages and return parsed player objects."""
    
    wikipedia_urls = {
        "10+ caps": "https://en.wikipedia.org/wiki/List_of_Scotland_international_footballers",
        "4-9 caps": "https://en.wikipedia.org/wiki/List_of_Scotland_international_footballers_(4%E2%80%939_caps)",
        "2-3 caps": "https://en.wikipedia.org/wiki/List_of_Scotland_international_footballers_(2%E2%80%933_caps)",
        "1 cap": "https://en.wikipedia.org/wiki/List_of_Scotland_international_footballers_with_one_cap"
    }
    
    all_players_data = []
    
    for description, url in wikipedia_urls.items():
        soup = fetch_wikipedia_page(url, description)
        
        if description == "10+ caps":
            raw_players = extract_players_from_table(soup, 10)
        elif description == "4-9 caps":
            raw_players = extract_players_from_table(soup, 4, 9)
        elif description == "2-3 caps":
            raw_players = extract_players_from_table(soup, 2, 3)
        else:  # 1 cap
            raw_players = extract_players_from_table(soup, 1, 1)
        
        print(f"Found {len(raw_players)} players with {description}")
        
        # Parse the raw string data into player objects
        for line in raw_players:
            if not line.strip() or line.strip() == "|":
                continue
                
            # Split by | and clean up
            parts = [part.strip() for part in line.split('|') if part.strip()]
            
            if len(parts) < 7:
                continue
                
            try:
                player_name = parts[0]
                caps = int(parts[2])
                goals = int(parts[3])
                first_cap_date_str = parts[4]
                first_cap_opponent = parts[5] if len(parts) > 5 else ""
                last_cap_date_str = parts[6] if len(parts) > 6 else ""
                last_cap_opponent = parts[7] if len(parts) > 7 else ""
                
                # Parse dates
                first_cap_date = parse_date(first_cap_date_str)
                last_cap_date = parse_date(last_cap_date_str)
                
                if first_cap_date and last_cap_date:
                    all_players_data.append({
                        'name': player_name,
                        'caps': caps,
                        'goals': goals,
                        'first_cap_date': first_cap_date,
                        'first_cap_opponent': first_cap_opponent,
                        'last_cap_date': last_cap_date,
                        'last_cap_opponent': last_cap_opponent
                    })
            except (ValueError, IndexError) as e:
                print(f"Error parsing line: {line[:50]}... - {e}")
                continue
    
    return all_players_data

def extract_player_data():
    """Extract player data dynamically from Wikipedia pages - includes 10+ caps, 4-9 caps, 2-3 caps, and 1 cap players."""
    
    print("=" * 80)
    print("FETCHING LATEST DATA FROM WIKIPEDIA")
    print("=" * 80)
    
    # Fetch current data from Wikipedia
    all_players_raw = fetch_all_players_data()
    
    if not all_players_raw:
        print("ERROR: Could not fetch any player data from Wikipedia")
        return [], datetime(1995, 11, 5)
    
    cutoff_date = datetime(1995, 11, 5)
    
    # Use the data we already fetched dynamically from Wikipedia
    print(f"Successfully fetched {len(all_players_raw)} players from Wikipedia")
    return all_players_raw, cutoff_date

def analyze_players():
    """Analyze players based on the cutoff date."""
    players, cutoff_date = extract_player_data()
    
    print(f"Total players parsed: {len(players)}")
    print(f"Cutoff date: {cutoff_date.strftime('%B %d, %Y')}")
    print("=" * 80)
    
    # Category 1: First cap after November 5, 1995
    after_cutoff = []
    
    # Category 2: First cap before November 5, 1995 AND last cap after November 5, 1995
    spanning_cutoff = []
    
    # Category 3: Both first and last cap before November 5, 1995
    before_cutoff = []
    
    for player in players:
        first_cap = player['first_cap_date']
        last_cap = player['last_cap_date']
        
        if first_cap > cutoff_date:
            after_cutoff.append(player)
        elif first_cap <= cutoff_date and last_cap > cutoff_date:
            spanning_cutoff.append(player)
        else:
            before_cutoff.append(player)
    
    # Sort by first cap date
    after_cutoff.sort(key=lambda x: x['first_cap_date'])
    spanning_cutoff.sort(key=lambda x: x['first_cap_date'])
    before_cutoff.sort(key=lambda x: x['first_cap_date'])
    
    print(f"\n1. PLAYERS WHO MADE THEIR FIRST CAP AFTER NOVEMBER 5, 1995")
    print(f"   Total: {len(after_cutoff)} players")
    print("-" * 80)
    
    for i, player in enumerate(after_cutoff, 1):
        first_date = player['first_cap_date'].strftime('%B %d, %Y')
        last_date = player['last_cap_date'].strftime('%B %d, %Y')
        print(f"{i:3d}. {player['name']:<25} | {player['caps']:3d} caps | {player['goals']:2d} goals | "
              f"First: {first_date:<15} vs {player['first_cap_opponent']:<15} | "
              f"Last: {last_date:<15} vs {player['last_cap_opponent']}")
    
    print(f"\n\n2. PLAYERS WHO MADE THEIR FIRST CAP BEFORE NOVEMBER 5, 1995 BUT LAST CAP AFTER")
    print(f"   Total: {len(spanning_cutoff)} players")
    print(f"   (Exact post-Nov 5, 1995 contributions from detailed research)")
    print("-" * 80)
    print(f"{'':3} {'Player Name':<25} | {'Total':<15} | {'Exact Post-1995':<17} | {'Career Span'}")
    print(f"{'':3} {'':25} | {'Caps':<4} {'Goals':<4} {'%Post':<5} | {'Caps':<4} {'Goals':<4} {'%Total':<6} | {'First → Last'}")
    print("-" * 80)
    
    # Calculate exact post-1995 contributions for spanning players using researched data
    def get_exact_post_1995_stats(player_name):
        """Look up exact post-1995 stats from researched data."""
        for spanning_player in spanning_players_data:
            if spanning_player['name'] == player_name:
                return spanning_player['post_1995_caps'], spanning_player['post_1995_goals']
        # Fallback to estimation if not found (shouldn't happen with our complete data)
        return None, None
    
    total_post_caps = 0
    total_post_goals = 0
    
    for i, player in enumerate(spanning_cutoff, 1):
        first_date = player['first_cap_date']
        last_date = player['last_cap_date']
        
        # Get exact post-1995 stats from researched data
        exact_post_caps, exact_post_goals = get_exact_post_1995_stats(player['name'])
        
        if exact_post_caps is not None and exact_post_goals is not None:
            # Use exact researched data
            actual_post_caps = exact_post_caps
            actual_post_goals = exact_post_goals
        else:
            # Fallback to estimation if not found (shouldn't happen)
            print(f"Warning: No exact data found for {player['name']}, using estimation")
            total_career_days = (last_date - first_date).days
            post_cutoff_days = (last_date - cutoff_date).days
            if total_career_days > 0:
                post_cutoff_ratio = post_cutoff_days / total_career_days
            else:
                post_cutoff_ratio = 0
            actual_post_caps = round(player['caps'] * post_cutoff_ratio)
            actual_post_goals = round(player['goals'] * post_cutoff_ratio)
        
        # Calculate what percentage of total caps were post-cutoff
        post_cutoff_percentage = (actual_post_caps / player['caps'] * 100) if player['caps'] > 0 else 0
        
        total_post_caps += actual_post_caps
        total_post_goals += actual_post_goals
        
        first_date_str = first_date.strftime('%b %Y')
        last_date_str = last_date.strftime('%b %Y')
        
        print(f"{i:3d}. {player['name']:<25} | "
              f"{player['caps']:4d} {player['goals']:4d} {post_cutoff_percentage:5.1f}% | "
              f"{actual_post_caps:4d} {actual_post_goals:4d} {(actual_post_caps/player['caps']*100):5.1f}% | "
              f"{first_date_str} → {last_date_str}")
    
    print("-" * 80)
    print(f"{'TOTALS':<29} | {'':4} {'':4} {'':5} | {total_post_caps:4d} {total_post_goals:4d} {'':6} |")
    print(f"\nExact total post-Nov 5, 1995 contributions from spanning players:")
    print(f"  • Caps: {total_post_caps}")
    print(f"  • Goals: {total_post_goals}")
    
    print(f"\n\n3. PLAYERS WHO MADE BOTH FIRST AND LAST CAP BEFORE NOVEMBER 5, 1995")
    print(f"   Total: {len(before_cutoff)} players")
    print("-" * 80)
    
    # Show only last 20 for brevity, or all if less than 20
    display_before = before_cutoff[-20:] if len(before_cutoff) > 20 else before_cutoff
    start_num = len(before_cutoff) - len(display_before) + 1
    
    if len(before_cutoff) > 20:
        print(f"   (Showing last 20 of {len(before_cutoff)} players - most recent careers ending before cutoff)")
        print()
    
    for i, player in enumerate(display_before, start_num):
        first_date = player['first_cap_date'].strftime('%B %d, %Y')
        last_date = player['last_cap_date'].strftime('%B %d, %Y')
        print(f"{i:3d}. {player['name']:<25} | {player['caps']:3d} caps | {player['goals']:2d} goals | "
              f"First: {first_date:<15} vs {player['first_cap_opponent']:<15} | "
              f"Last: {last_date:<15} vs {player['last_cap_opponent']}")
    
    # Calculate total post-1995 contributions
    total_after_caps = sum(player['caps'] for player in after_cutoff)
    total_after_goals = sum(player['goals'] for player in after_cutoff)
    
    # Summary statistics
    print(f"\n\nSUMMARY")
    print("=" * 80)
    print(f"Players with first cap AFTER November 5, 1995:     {len(after_cutoff):3d}")
    print(f"Players spanning the cutoff date:                  {len(spanning_cutoff):3d}")
    print(f"Players with both caps BEFORE November 5, 1995:    {len(before_cutoff):3d}")
    print(f"Total players analyzed:                            {len(players):3d}")
    print()
    print("POST-NOVEMBER 5, 1995 CONTRIBUTIONS:")
    print(f"  Fully post-1995 players:    {total_after_caps:4d} caps, {total_after_goals:3d} goals")
    print(f"  Spanning players (exact):   {total_post_caps:4d} caps, {total_post_goals:3d} goals")
    print(f"  TOTAL POST-1995:           {total_after_caps + total_post_caps:4d} caps, {total_after_goals + total_post_goals:3d} goals")
    
    # Save results to files
    with open('players_after_1995.txt', 'w') as f:
        f.write(f"SCOTLAND INTERNATIONAL FOOTBALLERS (1+ CAPS) WITH FIRST CAP AFTER NOVEMBER 5, 1995\n")
        f.write(f"Total: {len(after_cutoff)} players\n")https://en.wikipedia.org/wiki/FIFA_Men%27s_World_Ranking
        f.write("=" * 80 + "\n\n")
        
        for i, player in enumerate(after_cutoff, 1):
            first_date = player['first_cap_date'].strftime('%B %d, %Y')
            last_date = player['last_cap_date'].strftime('%B %d, %Y')
            f.write(f"{i:3d}. {player['name']:<25} | {player['caps']:3d} caps | {player['goals']:2d} goals | "
                    f"First: {first_date:<15} vs {player['first_cap_opponent']:<15} | "
                    f"Last: {last_date:<15} vs {player['last_cap_opponent']}\n")
    
    with open('players_spanning_1995.txt', 'w') as f:
        f.write(f"SCOTLAND INTERNATIONAL FOOTBALLERS (1+ CAPS) SPANNING NOVEMBER 5, 1995\n")
        f.write(f"(First cap before, last cap after November 5, 1995)\n")
        f.write(f"Total: {len(spanning_cutoff)} players\n")
        f.write("=" * 80 + "\n\n")
        
        for i, player in enumerate(spanning_cutoff, 1):
            first_date = player['first_cap_date'].strftime('%B %d, %Y')
            last_date = player['last_cap_date'].strftime('%B %d, %Y')
            f.write(f"{i:3d}. {player['name']:<25} | {player['caps']:3d} caps | {player['goals']:2d} goals | "
                    f"First: {first_date:<15} vs {player['first_cap_opponent']:<15} | "
                    f"Last: {last_date:<15} vs {player['last_cap_opponent']}\n")
    
    print(f"\nResults saved to:")
    print(f"- players_after_1995.txt ({len(after_cutoff)} players)")
    print(f"- players_spanning_1995.txt ({len(spanning_cutoff)} players)")

if __name__ == "__main__":
    analyze_players()