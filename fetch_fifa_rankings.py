#!/usr/bin/env python3
"""
Fetch FIFA Men's World Rankings from Excel file and save to JSON file.
"""
import pandas as pd
import json
from datetime import datetime
import os

def load_country_codes():
    """Load official FIFA country codes from lookup file"""
    try:
        with open('fifa_country_codes.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('country_codes', {})
    except FileNotFoundError:
        print("⚠️ FIFA country codes file not found. Using fallback method.")
        return {}
    except Exception as e:
        print(f"⚠️ Error loading country codes: {e}. Using fallback method.")
        return {}

def get_country_code(team_name, country_codes):
    """Get proper FIFA country code for team name"""
    # Direct lookup first
    if team_name in country_codes:
        return country_codes[team_name]
    
    # Try case-insensitive lookup
    team_lower = team_name.lower()
    for country, code in country_codes.items():
        if country.lower() == team_lower:
            return code
    
    # Fallback: generate from first 3 letters (old method)
    code = team_name[:3].upper().replace(" ", "").replace(".", "")
    if len(code) < 3:
        code = f"{code}XX"[:3]
    
    print(f"⚠️ No official code found for '{team_name}', using fallback: {code}")
    return code

def fetch_fifa_rankings_from_excel(excel_file_path="data/fifarankings20251016.xlsx"):
    """Fetch complete FIFA World Rankings from Excel file with special format handling"""
    
    try:
        # Load official FIFA country codes
        country_codes = load_country_codes()
        print(f"📊 Loaded {len(country_codes)} official FIFA country codes")
        
        # Read the Excel file without headers
        print(f"📊 Reading FIFA rankings from {excel_file_path}...")
        df = pd.read_excel(excel_file_path, header=None)
        
        print(f"📊 Total rows: {len(df)}")
        
        # Create rankings data structure
        rankings_data = {
            "date": "2025-10-16",  # Based on filename
            "last_updated": "16 October 2025",
            "next_update": "21 November 2025",
            "source": "FIFA Men's World Ranking Excel File",
            "methodology": "Elo-based system (since August 2018)",
            "total_teams": 0,
            "rankings": []
        }
        
        # The file has a specific format: alternating rows with rank/points and team names
        # Row pattern: rank data row, then team name row
        i = 0
        while i < len(df) - 1:
            try:
                # Look for rows that contain ranking data
                current_row = df.iloc[i]
                next_row = df.iloc[i + 1] if i + 1 < len(df) else None
                
                # Skip completely empty rows
                if current_row.isna().all():
                    i += 1
                    continue
                
                # Look for rank in first column
                rank_val = current_row.iloc[0]
                points_val = current_row.iloc[2] if len(current_row) > 2 else None
                change_val = current_row.iloc[4] if len(current_row) > 4 else None
                
                # Look for team name in next row if current row has rank
                team_name = None
                if next_row is not None and not next_row.isna().all():
                    # Team name is usually in column 1 of the next row
                    team_name = next_row.iloc[1] if len(next_row) > 1 and pd.notna(next_row.iloc[1]) else None
                
                # Process if we have rank and points
                if pd.notna(rank_val) and pd.notna(points_val):
                    try:
                        rank = int(float(rank_val))
                        points = float(points_val)
                        
                        # Extract team name
                        if team_name and pd.notna(team_name):
                            team = str(team_name).strip()
                        else:
                            team = f"Team_Rank_{rank}"
                        
                        # Get proper FIFA country code using lookup
                        code = get_country_code(team, country_codes)
                        
                        # Process change value
                        change = 0
                        if pd.notna(change_val):
                            try:
                                change_str = str(change_val).strip()
                                if change_str and change_str not in ['nan', 'NaN', '']:
                                    change = int(float(change_str))
                            except:
                                change = 0
                        
                        team_data = {
                            "rank": rank,
                            "team": team,
                            "code": code,
                            "points": round(points, 2),
                            "change": change
                        }
                        
                        rankings_data["rankings"].append(team_data)
                        
                        # Skip the team name row since we processed it
                        i += 2
                        continue
                        
                    except ValueError:
                        pass  # Skip rows that don't have valid rank/points data
                
                i += 1
                
            except Exception as e:
                print(f"⚠️ Error processing row {i}: {e}")
                i += 1
                continue
        
        # Remove duplicates and sort by rank
        seen_ranks = set()
        unique_rankings = []
        for team in rankings_data["rankings"]:
            if team["rank"] not in seen_ranks:
                unique_rankings.append(team)
                seen_ranks.add(team["rank"])
        
        rankings_data["rankings"] = sorted(unique_rankings, key=lambda x: x["rank"])
        rankings_data["total_teams"] = len(rankings_data["rankings"])
        
        print(f"✅ Successfully loaded {len(rankings_data['rankings'])} teams from Excel file")
        
        # Show first few teams for verification
        if rankings_data["rankings"]:
            print(f"📋 Sample teams loaded:")
            for team in rankings_data["rankings"][:5]:
                print(f"   {team['rank']}. {team['team']} - {team['points']} pts")
        
        return rankings_data
        
    except FileNotFoundError:
        print(f"❌ Excel file not found: {excel_file_path}")
        return None
    except PermissionError:
        print(f"❌ Permission denied accessing: {excel_file_path}")
        print(f"💡 Please close the Excel file if it's open and try again")
        return None
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")
        return None

def save_rankings_to_json(rankings_data, filename="fifa_rankings_oct_2025.json"):
    """Save rankings data to JSON file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(rankings_data, f, indent=2, ensure_ascii=False)
        print(f"✓ FIFA Rankings saved to {filename}")
        print(f"✓ Total teams: {len(rankings_data['rankings'])}")
        print(f"✓ Date: {rankings_data['date']}")
        return True
    except Exception as e:
        print(f"✗ Error saving to JSON: {e}")
        return False

def display_top_rankings(rankings_data, top_n=20):
    """Display top N rankings"""
    print(f"\n📊 FIFA Men's World Ranking - Top {top_n} (as of {rankings_data['date']})")
    print("=" * 60)
    print(f"{'Rank':<4} {'Team':<20} {'Code':<4} {'Points':<8} {'Change':<6}")
    print("-" * 60)
    
    for team in rankings_data['rankings'][:top_n]:
        change_str = f"+{team['change']}" if team['change'] > 0 else str(team['change'])
        if team['change'] == 0:
            change_str = "--"
        print(f"{team['rank']:<4} {team['team']:<20} {team['code']:<4} {team['points']:<8} {change_str:<6}")

if __name__ == "__main__":
    print("🌍 Fetching FIFA Men's World Rankings from Excel file...")
    
    # Fetch rankings from Excel
    rankings = fetch_fifa_rankings_from_excel()
    
    if rankings:
        # Display top 20
        display_top_rankings(rankings, 20)
        
        # Save to JSON
        save_rankings_to_json(rankings, "fifa_rankings_from_excel.json")
        
        print(f"\n📝 Complete rankings loaded from Excel file")
        print(f"📝 Data source: {rankings['source']}")
        print(f"📝 Last updated: {rankings['last_updated']}")
    else:
        print("❌ Failed to load rankings from Excel file")