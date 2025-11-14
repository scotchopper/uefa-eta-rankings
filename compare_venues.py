#!/usr/bin/env python3
"""
Venue Comparison Script

This script compares venues from the Stewart venue check file with venues
in the Scotland football results database and reports exceptions/differences.
"""

import pandas as pd
from pathlib import Path
import sys
sys.path.append('src')
from eta.eta_statistics import ScotlandFootballAnalyzer


def load_stewart_venues():
    """Load venues from Stewart's venue check text file."""
    stewart_file = Path('stewart_venue_check.txt')
    
    if not stewart_file.exists():
        raise FileNotFoundError(f"Stewart venue file not found: {stewart_file}")
    
    # Read the text file - venues are separated by newlines
    with open(stewart_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Clean up the venue names - strip whitespace and remove empty lines
    stewart_venues = set()
    for line in lines:
        venue = line.strip()
        if venue:  # Only add non-empty lines
            stewart_venues.add(venue)
    
    return stewart_venues


def create_venue_mapping():
    """Create a mapping for known spelling variations between Stewart's list and database."""
    return {
        # Stewart format -> Database format (case-insensitive matching)
        "Ta'qali": "Valletta",  # Malta venue mapping
        "Serravalle": "San Marino",
        "Zalaegerszeg": "Zalaegerszeg, Hungary", 
        "Kyiv": "Kiev",
        "Kraków": "Krakow",
        "Saint-Étienne": "St. Etienne",
        "Reykjavík": "Reykjavik", 
        "Shkodër": "Shkoder",
        "Tórshavn": "Torshavn"
    }


def create_city_venue_mapping():
    """Create mappings for city names to specific stadium names in database."""
    return {
        # City name -> List of stadium names in that city
        "Glasgow": ["Celtic Park", "Ibrox", "Hampden","Hampden I","Hampden II","Ibrox I","Hamilton Crescent"],
        "Edinburgh": ["Easter Road", "Tynecastle","Hibernian Park"],
        "London": ["Wembley", "Emirates", "London", "Craven Cottage", "The Oval", "Crystal Palace", "Stamford Bridge"],
        "Dundee": ["Dens Park", "Dundee"]
    }


def normalize_venue_sets(stewart_venues, database_venues):
    """
    Normalize venue sets to account for spelling variations and city-to-stadium mappings.
    Returns updated sets with consistent spelling for comparison.
    """
    venue_mapping = create_venue_mapping()
    city_venue_mapping = create_city_venue_mapping()
    
    # Create normalized copies
    stewart_normalized = stewart_venues.copy()
    database_normalized = database_venues.copy()
    
    # Apply direct spelling mappings from Stewart format to Database format (case-insensitive)
    for stewart_name, database_name in venue_mapping.items():
        # Find the actual venue name in Stewart's list (case-insensitive)
        stewart_actual = None
        for venue in stewart_normalized:
            if venue.lower() == stewart_name.lower():
                stewart_actual = venue
                break
        
        # Find the actual venue name in database (case-insensitive) 
        database_actual = None
        for venue in database_normalized:
            if venue.lower() == database_name.lower():
                database_actual = venue
                break
        
        if stewart_actual and database_actual:
            # Replace Stewart's version with database version for consistency
            stewart_normalized.remove(stewart_actual)
            stewart_normalized.add(database_actual)
            print(f"   🔄 Mapped: '{stewart_actual}' ↔ '{database_actual}'")
    
    # Handle city-to-stadium mappings
    for city_name, stadium_names in city_venue_mapping.items():
        if city_name in stewart_normalized:
            # Check which stadiums from this city exist in the database
            matching_stadiums = [stadium for stadium in stadium_names if stadium in database_normalized]
            
            if matching_stadiums:
                # Remove the city name from Stewart's list
                stewart_normalized.remove(city_name)
                
                # Add all matching stadiums to Stewart's normalized list
                for stadium in matching_stadiums:
                    stewart_normalized.add(stadium)
                
                print(f"   🏟️  Mapped city '{city_name}' to stadiums: {matching_stadiums}")
    
    return stewart_normalized, database_normalized


def load_database_venues():
    """Load venues from the Scotland football results database."""
    try:
        analyzer = ScotlandFootballAnalyzer('scot_games_eta_source.xlsx', 'ETA30th')
        df = analyzer.load_data()
        
        if 'Venue' not in df.columns:
            raise ValueError("Venue column not found in database")
        
        # Get unique venues, cleaning up any whitespace
        database_venues = set(df['Venue'].dropna().str.strip())
        
        # Remove any empty strings that might have slipped through
        database_venues.discard('')
        
        return database_venues, df
        
    except Exception as e:
        raise Exception(f"Error loading database venues: {e}")


def compare_venues():
    """Compare Stewart's venue list with database venues and report differences."""
    
    print("🏟️  VENUE COMPARISON ANALYSIS")
    print("=" * 50)
    
    try:
        # Load Stewart's venues
        print("📝 Loading Stewart's venue list...")
        stewart_venues = load_stewart_venues()
        print(f"   Found {len(stewart_venues)} venues in Stewart's list")
        
        # Load database venues
        print("💾 Loading database venues...")
        database_venues, df = load_database_venues()
        print(f"   Found {len(database_venues)} venues in database")
        
        # Normalize venue names to account for spelling variations
        print("\n🔄 NORMALIZING SPELLING VARIATIONS:")
        print("-" * 38)
        stewart_normalized, database_normalized = normalize_venue_sets(stewart_venues, database_venues)
        
        print("\n" + "=" * 50)
        print("COMPARISON RESULTS (AFTER NORMALIZATION)")
        print("=" * 50)
        
        # Find venues in Stewart's list but NOT in database
        stewart_only = stewart_normalized - database_normalized
        print(f"\n🔍 VENUES IN STEWART'S LIST BUT NOT IN DATABASE ({len(stewart_only)}):")
        print("-" * 55)
        if stewart_only:
            for venue in sorted(stewart_only):
                print(f"   • {venue}")
        else:
            print("   ✅ None - all Stewart venues found in database!")
        
        # Find venues in database but NOT in Stewart's list
        database_only = database_normalized - stewart_normalized
        print(f"\n🔍 VENUES IN DATABASE BUT NOT IN STEWART'S LIST ({len(database_only)}):")
        print("-" * 55)
        if database_only:
            # Sort by frequency to show most common missing venues first
            venue_counts = df['Venue'].value_counts()
            database_only_sorted = sorted(database_only, 
                                        key=lambda x: venue_counts.get(x, 0), 
                                        reverse=True)
            
            for venue in database_only_sorted:
                count = venue_counts.get(venue, 0)
                print(f"   • {venue} ({count} games)")
        else:
            print("   ✅ None - all database venues found in Stewart's list!")
        
        # Find common venues
        common_venues = stewart_normalized & database_normalized
        print(f"\n✅ VENUES FOUND IN BOTH LISTS ({len(common_venues)}):")
        print("-" * 40)
        if common_venues:
            venue_counts = df['Venue'].value_counts()
            common_sorted = sorted(common_venues, 
                                 key=lambda x: venue_counts.get(x, 0), 
                                 reverse=True)
            
            # Show top 10 most frequent common venues
            print("   Top 10 most frequent:")
            for i, venue in enumerate(common_sorted[:10], 1):
                count = venue_counts.get(venue, 0)
                print(f"   {i:2}. {venue} ({count} games)")
            
            if len(common_sorted) > 10:
                print(f"   ... and {len(common_sorted) - 10} more")
        
        # Summary statistics
        print(f"\n📊 SUMMARY STATISTICS:")
        print("-" * 20)
        print(f"Stewart's venues (original): {len(stewart_venues)}")
        print(f"Stewart's venues (normalized): {len(stewart_normalized)}")
        print(f"Database venues: {len(database_venues)}")
        print(f"Common venues: {len(common_venues)}")
        print(f"Stewart-only venues: {len(stewart_only)}")
        print(f"Database-only venues: {len(database_only)}")
        
        # Calculate mapping changes
        mapping_expansion = len(stewart_normalized) - len(stewart_venues)
        if mapping_expansion > 0:
            print(f"Venue mappings expanded Stewart's list by: {mapping_expansion}")
        elif mapping_expansion < 0:
            print(f"Venue mappings consolidated Stewart's list by: {abs(mapping_expansion)}")
        else:
            print(f"Venue mappings: no net change in count")
        
        coverage_stewart = len(common_venues) / len(stewart_normalized) * 100
        coverage_database = len(common_venues) / len(database_venues) * 100
        
        print(f"Stewart list coverage: {coverage_stewart:.1f}%")
        print(f"Database coverage: {coverage_database:.1f}%")
        
        # Additional analysis - show venue usage patterns
        print(f"\n📈 VENUE USAGE IN DATABASE:")
        print("-" * 25)
        venue_counts = df['Venue'].value_counts()
        
        # Categorize venues by frequency
        high_frequency = len(venue_counts[venue_counts >= 10])
        medium_frequency = len(venue_counts[(venue_counts >= 5) & (venue_counts < 10)])
        low_frequency = len(venue_counts[(venue_counts >= 2) & (venue_counts < 5)])
        single_use = len(venue_counts[venue_counts == 1])
        
        print(f"High frequency venues (10+ games): {high_frequency}")
        print(f"Medium frequency venues (5-9 games): {medium_frequency}")
        print(f"Low frequency venues (2-4 games): {low_frequency}")
        print(f"Single-use venues (1 game): {single_use}")
        
        # Show the most frequently used venues not in Stewart's list
        missing_high_freq = [v for v in venue_counts.head(20).index if v in database_only]
        if missing_high_freq:
            print(f"\n⚠️  HIGH-FREQUENCY VENUES MISSING FROM STEWART'S LIST:")
            print("-" * 50)
            for venue in missing_high_freq:
                count = venue_counts[venue]
                print(f"   • {venue} ({count} games)")
        
        return {
            'stewart_venues': stewart_venues,
            'stewart_normalized': stewart_normalized,
            'database_venues': database_venues,
            'stewart_only': stewart_only,
            'database_only': database_only,
            'common_venues': common_venues,
            'spelling_variations_resolved': len(stewart_venues) - len(stewart_normalized)
        }
        
    except Exception as e:
        print(f"❌ Error during comparison: {e}")
        return None


def export_results(results):
    """Export comparison results to text files."""
    if not results:
        return
    
    print(f"\n💾 EXPORTING RESULTS TO FILES...")
    print("-" * 30)
    
    # Export Stewart-only venues
    with open('data/stewart_only_venues.txt', 'w', encoding='utf-8') as f:
        f.write("VENUES IN STEWART'S LIST BUT NOT IN DATABASE\n")
        f.write("=" * 45 + "\n\n")
        for venue in sorted(results['stewart_only']):
            f.write(f"{venue}\n")
    
    print(f"   ✅ data/stewart_only_venues.txt ({len(results['stewart_only'])} venues)")
    
    # Export database-only venues
    with open('data/database_only_venues.txt', 'w', encoding='utf-8') as f:
        f.write("VENUES IN DATABASE BUT NOT IN STEWART'S LIST\n")
        f.write("=" * 43 + "\n\n")
        for venue in sorted(results['database_only']):
            f.write(f"{venue}\n")
    
    print(f"   ✅ data/database_only_venues.txt ({len(results['database_only'])} venues)")
    
    # Export complete venue comparison
    with open('data/venue_comparison_report.txt', 'w', encoding='utf-8') as f:
        f.write("COMPLETE VENUE COMPARISON REPORT\n")
        f.write("=" * 35 + "\n\n")
        
        f.write(f"Stewart's venues: {len(results['stewart_venues'])}\n")
        f.write(f"Database venues: {len(results['database_venues'])}\n")
        f.write(f"Common venues: {len(results['common_venues'])}\n")
        f.write(f"Stewart-only: {len(results['stewart_only'])}\n")
        f.write(f"Database-only: {len(results['database_only'])}\n\n")
        
        f.write("VENUES IN STEWART'S LIST ONLY:\n")
        f.write("-" * 30 + "\n")
        for venue in sorted(results['stewart_only']):
            f.write(f"{venue}\n")
        
        f.write(f"\nVENUES IN DATABASE ONLY:\n")
        f.write("-" * 25 + "\n")
        for venue in sorted(results['database_only']):
            f.write(f"{venue}\n")
    
    print(f"   ✅ data/venue_comparison_report.txt (complete analysis)")


def main():
    """Main function to run the venue comparison."""
    results = compare_venues()
    
    if results:
        export_results(results)
        print(f"\n✅ Venue comparison complete!")
    else:
        print(f"\n❌ Venue comparison failed!")


if __name__ == "__main__":
    main()