#!/usr/bin/env python3
"""
Analyze ETA30th data to identify COVID-19 behind closed doors matches.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import pandas as pd
from datetime import datetime

def main():
    """Identify COVID-19 behind closed doors matches."""
    print("🦠 COVID-19 BEHIND CLOSED DOORS ANALYSIS")
    print("="*50)
    
    # Load data directly
    df = pd.read_excel("scot_games_eta_source.xlsx", sheet_name='ETA30th')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    print(f"✅ Loaded {len(df)} records from ETA30th worksheet")
    
    # COVID period analysis (roughly March 2020 to late 2021/early 2022)
    covid_start = datetime(2020, 3, 1)
    covid_end = datetime(2022, 3, 1)  # Conservative end date
    
    # Filter matches during COVID period
    covid_period_matches = df[
        (df['Date'] >= covid_start) & 
        (df['Date'] <= covid_end)
    ].copy()
    
    print(f"\n📅 COVID PERIOD ANALYSIS (March 2020 - March 2022):")
    print(f"   Total matches in period: {len(covid_period_matches)}")
    
    if len(covid_period_matches) > 0:
        print(f"   Date range: {covid_period_matches['Date'].min().strftime('%Y-%m-%d')} to {covid_period_matches['Date'].max().strftime('%Y-%m-%d')}")
        
        # Sort by date
        covid_matches_sorted = covid_period_matches.sort_values('Date')
        
        print(f"\n🏟️  ALL MATCHES DURING COVID PERIOD:")
        print("   Date       Opponent              Venue                Competition                Result Score")
        print("   " + "-" * 90)
        
        for i, (_, match) in enumerate(covid_matches_sorted.iterrows(), 1):
            date = match['Date'].strftime('%Y-%m-%d')
            opponent = str(match['Opposition'])[:15]
            venue = str(match['Venue'])[:15]
            competition = str(match.get('Competition', 'N/A'))[:25]
            result = match['Result']
            score = f"{match['Scot']}-{match['Opp']}"
            home_away = match.get('Home\\Away', 'N/A')
            
            print(f"   {date} {opponent:15} {venue:15} {competition:25} {result} {score:5} ({home_away})")
    
    # Check Notes column for COVID-related information
    print(f"\n🔍 CHECKING NOTES COLUMN FOR COVID REFERENCES:")
    
    # Look for COVID-related keywords in Notes
    covid_keywords = ['covid', 'behind closed doors', 'no fans', 'no supporters', 'no spectators', 'pandemic', 'lockdown']
    
    covid_notes_matches = df[
        df['Notes'].notna() & 
        df['Notes'].str.lower().str.contains('|'.join(covid_keywords), na=False)
    ]
    
    if len(covid_notes_matches) > 0:
        print(f"   Found {len(covid_notes_matches)} matches with COVID-related notes:")
        for _, match in covid_notes_matches.iterrows():
            date = match['Date'].strftime('%Y-%m-%d') if pd.notna(match['Date']) else 'N/A'
            opponent = match['Opposition']
            venue = match['Venue']
            notes = match['Notes']
            print(f"   • {date} vs {opponent} ({venue}): {notes}")
    else:
        print("   No explicit COVID references found in Notes column")
    
    # Analyze 2020 matches specifically (when most restrictions started)
    year_2020_matches = df[df['Date'].dt.year == 2020].copy()
    year_2021_matches = df[df['Date'].dt.year == 2021].copy()
    
    print(f"\n📊 YEAR-BY-YEAR BREAKDOWN:")
    print(f"   2020: {len(year_2020_matches)} matches")
    if len(year_2020_matches) > 0:
        print("   2020 matches:")
        for _, match in year_2020_matches.sort_values('Date').iterrows():
            date = match['Date'].strftime('%Y-%m-%d')
            opponent = match['Opposition']
            venue = match['Venue']
            result = match['Result']
            score = f"{match['Scot']}-{match['Opp']}"
            print(f"      {date} vs {opponent:15} at {venue:15} ({result} {score})")
    
    print(f"   2021: {len(year_2021_matches)} matches")
    if len(year_2021_matches) > 0:
        print("   2021 matches:")
        for _, match in year_2021_matches.sort_values('Date').iterrows():
            date = match['Date'].strftime('%Y-%m-%d')
            opponent = match['Opposition']
            venue = match['Venue']
            result = match['Result']
            score = f"{match['Scot']}-{match['Opp']}"
            print(f"      {date} vs {opponent:15} at {venue:15} ({result} {score})")
    
    # Look for patterns that might indicate behind closed doors
    print(f"\n🔍 PATTERN ANALYSIS:")
    print("   Looking for potential behind closed doors indicators...")
    
    # Check all column names to see what data we have
    print(f"\n📋 AVAILABLE COLUMNS:")
    for i, col in enumerate(df.columns, 1):
        print(f"   {i:2}. {col}")
    
    # Sample some data to understand structure
    print(f"\n📄 SAMPLE DATA STRUCTURE:")
    sample_match = df.iloc[0]
    for col in df.columns:
        value = sample_match[col]
        if pd.notna(value):
            print(f"   {col}: {value}")
    
    print(f"\n💡 RECOMMENDATION:")
    print("   To definitively identify behind closed doors matches, we would need:")
    print("   • Attendance figures (if available)")
    print("   • Official match reports mentioning restrictions")
    print("   • Cross-reference with known COVID restriction dates")
    print("   • Check if any additional data sources contain this information")
    
    # Based on known COVID timeline, likely candidates
    print(f"\n🎯 LIKELY BEHIND CLOSED DOORS CANDIDATES:")
    print("   Based on COVID timeline (March 2020 - early 2022):")
    
    # Show matches from key COVID restriction periods
    key_periods = [
        (datetime(2020, 3, 1), datetime(2020, 12, 31), "Initial COVID restrictions"),
        (datetime(2021, 1, 1), datetime(2021, 6, 30), "Continued restrictions"),
        (datetime(2021, 7, 1), datetime(2021, 12, 31), "Gradual reopening")
    ]
    
    for start_date, end_date, period_name in key_periods:
        period_matches = df[
            (df['Date'] >= start_date) & 
            (df['Date'] <= end_date)
        ].copy()
        
        if len(period_matches) > 0:
            print(f"\n   {period_name} ({start_date.strftime('%Y-%m')} to {end_date.strftime('%Y-%m')}):")
            for _, match in period_matches.sort_values('Date').iterrows():
                date = match['Date'].strftime('%Y-%m-%d')
                opponent = match['Opposition']
                venue = match['Venue']
                home_away = match.get('Home\\Away', 'N/A')
                print(f"      {date} vs {opponent:15} at {venue:15} ({home_away})")

if __name__ == "__main__":
    main()