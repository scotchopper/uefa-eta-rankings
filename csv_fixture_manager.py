#!/usr/bin/env python3
"""
CSV Fixture Import/Export Utility
For bulk management of UEFA fixtures
"""

import csv
import json
from uefa_fixtures_template import UEFAFixturesManager

def create_csv_template():
    """Create a CSV template for fixture input"""
    headers = [
        'match_id',
        'date',
        'home_team',
        'away_team', 
        'competition',
        'importance',
        'venue',
        'home_goals',
        'away_goals',
        'notes',
        'status'
    ]
    
    # Sample data
    sample_fixtures = [
        ['WCQ001', '2025-11-14', 'Scotland', 'Greece', 'World Cup Qualifiers', '25', 'Hampden Park', '', '', 'Home advantage crucial', 'scheduled'],
        ['WCQ002', '2025-11-14', 'Denmark', 'Belarus', 'World Cup Qualifiers', '25', 'Copenhagen', '', '', 'Denmark heavily favored', 'scheduled'],
        ['WCQ003', '2025-11-17', 'Denmark', 'Scotland', 'World Cup Qualifiers', '25', 'Copenhagen', '', '', 'Away challenge for Scotland', 'scheduled'],
        ['NL004', '2025-11-15', 'England', 'Ireland', 'Nations League', '15', 'Wembley', '', '', 'Derby match', 'scheduled'],
        ['NL005', '2025-11-16', 'Spain', 'Germany', 'Nations League', '15', 'Seville', '', '', 'Top tier clash', 'scheduled'],
        ['FR006', '2025-11-16', 'France', 'Italy', 'International Friendly', '10', 'Paris', '', '', 'Friendly but important', 'scheduled'],
        ['WCQ007', '2025-11-15', 'Portugal', 'Poland', 'World Cup Qualifiers', '25', 'Lisbon', '', '', 'Group leaders clash', 'scheduled'],
        ['WCQ008', '2025-11-18', 'Netherlands', 'Hungary', 'World Cup Qualifiers', '25', 'Amsterdam', '', '', 'Must win for Netherlands', 'scheduled']
    ]
    
    filename = 'uefa_fixtures_template.csv'
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(sample_fixtures)
    
    print(f"📄 CSV template created: {filename}")
    print("\n📝 Instructions:")
    print("1. Fill in fixture details in the CSV file")
    print("2. Leave home_goals/away_goals empty for scheduled matches")
    print("3. Add results by filling in home_goals/away_goals columns")
    print("4. Use import_from_csv() to load fixtures into the system")
    
    return filename

def import_from_csv(csv_file='uefa_fixtures_template.csv'):
    """Import fixtures from CSV file"""
    manager = UEFAFixturesManager()
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            fixtures_added = 0
            results_added = 0
            
            for row in reader:
                # Skip empty rows
                if not row['match_id'].strip():
                    continue
                
                # Add fixture
                manager.add_fixture(
                    match_id=row['match_id'],
                    date=row['date'],
                    home_team=row['home_team'],
                    away_team=row['away_team'],
                    competition=row['competition'],
                    importance=int(row['importance']) if row['importance'] else 25,
                    venue=row['venue']
                )
                fixtures_added += 1
                
                # Add result if available
                if row['home_goals'] and row['away_goals']:
                    manager.add_result(
                        match_id=row['match_id'],
                        home_goals=int(row['home_goals']),
                        away_goals=int(row['away_goals']),
                        notes=row['notes']
                    )
                    results_added += 1
            
            print(f"✅ Imported {fixtures_added} fixtures and {results_added} results from {csv_file}")
            
            # Display imported data
            manager.display_fixtures()
            
            # Save to JSON
            manager.save_data()
            
            return manager
            
    except FileNotFoundError:
        print(f"❌ CSV file {csv_file} not found")
        return None
    except Exception as e:
        print(f"❌ Error importing from CSV: {e}")
        return None

def export_to_csv(json_file='uefa_fixtures_data.json', csv_file='uefa_fixtures_export.csv'):
    """Export fixtures and results to CSV"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        fixtures = data.get('fixtures', {})
        results = data.get('results', {})
        
        headers = [
            'match_id', 'date', 'home_team', 'away_team', 'competition', 
            'importance', 'venue', 'home_goals', 'away_goals', 'result', 
            'notes', 'status', 'home_points', 'away_points'
        ]
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            
            for match_id, fixture in fixtures.items():
                result_data = results.get(match_id, {})
                
                row = [
                    match_id,
                    fixture['date'],
                    fixture['home_team'],
                    fixture['away_team'],
                    fixture['competition'],
                    fixture['importance'],
                    fixture.get('venue', ''),
                    result_data.get('home_goals', ''),
                    result_data.get('away_goals', ''),
                    result_data.get('result', ''),
                    result_data.get('notes', ''),
                    fixture['status'],
                    fixture.get('home_points', ''),
                    fixture.get('away_points', '')
                ]
                writer.writerow(row)
        
        print(f"📤 Exported data to {csv_file}")
        
    except FileNotFoundError:
        print(f"❌ JSON file {json_file} not found")
    except Exception as e:
        print(f"❌ Error exporting to CSV: {e}")

def main():
    print("📄 CSV FIXTURE MANAGEMENT UTILITY")
    print("=" * 40)
    print("1. Create CSV template")
    print("2. Import fixtures from CSV")
    print("3. Export fixtures to CSV")
    print("4. Exit")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == '1':
        create_csv_template()
    elif choice == '2':
        csv_file = input("CSV filename (default: uefa_fixtures_template.csv): ").strip()
        if not csv_file:
            csv_file = 'uefa_fixtures_template.csv'
        import_from_csv(csv_file)
    elif choice == '3':
        export_to_csv()
    elif choice == '4':
        print("👋 Goodbye!")
    else:
        print("❌ Invalid option")

if __name__ == "__main__":
    main()