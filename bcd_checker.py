#!/usr/bin/env python3
"""
Utility functions to check if Scotland matches were behind closed doors.
"""

import json
import pandas as pd
from datetime import datetime
from typing import Optional, Dict, Any

class BehindClosedDoorsChecker:
    """Class to check if Scotland matches were played behind closed doors."""
    
    def __init__(self, lookup_file: str = "data/behind_closed_doors_lookup.json"):
        """Initialize with the BCD lookup file."""
        self.lookup_file = lookup_file
        self.bcd_data = self._load_lookup_data()
        
    def _load_lookup_data(self) -> Dict[str, Any]:
        """Load the behind closed doors lookup data."""
        try:
            with open(self.lookup_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Lookup file {self.lookup_file} not found. Run create_bcd_lookup.py first.")
            return {'behind_closed_doors_matches': []}
    
    def is_behind_closed_doors(self, date: str, opposition: Optional[str] = None) -> bool:
        """
        Check if a match was played behind closed doors.
        
        Args:
            date: Match date in YYYY-MM-DD format
            opposition: Opposition team name (optional, for additional verification)
            
        Returns:
            True if match was behind closed doors, False otherwise
        """
        for match in self.bcd_data.get('behind_closed_doors_matches', []):
            if match['date'] == date:
                if opposition is None or match['opposition'] == opposition:
                    return True
        return False
    
    def get_bcd_match_details(self, date: str, opposition: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get details of a behind closed doors match.
        
        Args:
            date: Match date in YYYY-MM-DD format
            opposition: Opposition team name (optional)
            
        Returns:
            Match details dictionary if found, None otherwise
        """
        for match in self.bcd_data.get('behind_closed_doors_matches', []):
            if match['date'] == date:
                if opposition is None or match['opposition'] == opposition:
                    return match
        return None
    
    def get_all_bcd_matches(self) -> list:
        """Get all behind closed doors matches."""
        return self.bcd_data.get('behind_closed_doors_matches', [])
    
    def get_bcd_summary(self) -> Dict[str, Any]:
        """Get summary statistics of BCD matches."""
        matches = self.get_all_bcd_matches()
        
        if not matches:
            return {}
        
        # Count by year
        year_counts = {}
        venue_counts = {}
        result_counts = {}
        
        for match in matches:
            year = match['date'][:4]
            year_counts[year] = year_counts.get(year, 0) + 1
            
            venue_type = match['home_away']
            venue_counts[venue_type] = venue_counts.get(venue_type, 0) + 1
            
            result = match['result']
            result_counts[result] = result_counts.get(result, 0) + 1
        
        return {
            'total_matches': len(matches),
            'by_year': year_counts,
            'by_venue_type': venue_counts,
            'by_result': result_counts,
            'metadata': self.bcd_data.get('metadata', {})
        }
    
    def print_bcd_summary(self):
        """Print a formatted summary of BCD matches."""
        summary = self.get_bcd_summary()
        
        if not summary:
            print("❌ No behind closed doors data available.")
            return
        
        print("🔒 BEHIND CLOSED DOORS MATCHES SUMMARY")
        print("="*45)
        print(f"Total BCD matches: {summary['total_matches']}")
        
        print(f"\n📅 By Year:")
        for year, count in sorted(summary['by_year'].items()):
            print(f"  {year}: {count} matches")
        
        print(f"\n🏟️  By Venue Type:")
        venue_names = {'H': 'Home', 'A': 'Away', 'N': 'Neutral'}
        for venue_type, count in summary['by_venue_type'].items():
            venue_name = venue_names.get(venue_type, venue_type)
            print(f"  {venue_name}: {count} matches")
        
        print(f"\n📊 By Result:")
        result_names = {'W': 'Wins', 'D': 'Draws', 'L': 'Losses', 'WP': 'Wins (Penalties)'}
        for result, count in summary['by_result'].items():
            result_name = result_names.get(result, result)
            print(f"  {result_name}: {count} matches")

def demo_usage():
    """Demonstrate how to use the BCD checker."""
    print("🔒 BEHIND CLOSED DOORS CHECKER - DEMO")
    print("="*40)
    
    # Initialize checker
    checker = BehindClosedDoorsChecker()
    
    # Print summary
    checker.print_bcd_summary()
    
    print(f"\n🔍 EXAMPLE CHECKS:")
    print("="*20)
    
    # Test some specific matches
    test_matches = [
        ("2020-10-08", "Israel", "Euro 2020 Playoff"),
        ("2021-06-14", "Czechia", "First match with spectators"),
        ("2019-06-08", "England", "Pre-COVID match"),
        ("2021-03-31", "Faroe Islands", "Last BCD match")
    ]
    
    for date, opposition, description in test_matches:
        is_bcd = checker.is_behind_closed_doors(date, opposition)
        status = "🔒 Behind Closed Doors" if is_bcd else "👥 With Spectators"
        print(f"  {date} vs {opposition:12} - {status}")
        print(f"    {description}")
        
        if is_bcd:
            details = checker.get_bcd_match_details(date, opposition)
            if details:
                print(f"    Venue: {details['venue']} ({details['home_away']})")
                print(f"    Result: {details['result']} {details['score_scotland']}-{details['score_opposition']}")
        print()

if __name__ == "__main__":
    demo_usage()