#!/usr/bin/env python3
"""
Mobile Results Processor
Processes results saved from mobile and updates the main fixtures file
"""

import json
import os
from datetime import datetime

def process_mobile_results():
    """Process results from mobile form (saved in localStorage)"""
    print("🔄 MOBILE RESULTS PROCESSOR")
    print("=" * 40)
    
    # This would typically read from a shared file or database
    # For now, we'll create a manual input system
    
    print("📱 To process mobile results:")
    print("1. Mobile saves results to localStorage")
    print("2. Export localStorage data or manually input here")
    print("3. Results get added to uefa_fixtures_data.json")
    
    # Manual input system
    while True:
        print("\n⚽ ADD RESULT:")
        fixture_id = input("Fixture ID (or 'done' to finish): ").strip()
        
        if fixture_id.lower() == 'done':
            break
            
        try:
            home_goals = int(input("Home team goals: "))
            away_goals = int(input("Away team goals: "))
            notes = input("Notes (optional): ").strip()
            
            # Load current fixtures
            with open('uefa_fixtures_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if fixture_id in data['fixtures']:
                # Add result
                data['fixtures'][fixture_id]['result'] = {
                    'home_goals': home_goals,
                    'away_goals': away_goals,
                    'notes': notes,
                    'updated_at': datetime.now().isoformat(),
                    'source': 'mobile'
                }
                
                # Save back
                with open('uefa_fixtures_data.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                print(f"✅ Result added: {home_goals}-{away_goals}")
                
            else:
                print(f"❌ Fixture {fixture_id} not found")
                
        except ValueError:
            print("❌ Invalid input, please try again")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n🏆 Results updated! Run enhanced_team_range_analysis.py for new rankings")

if __name__ == "__main__":
    process_mobile_results()
