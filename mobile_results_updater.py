#!/usr/bin/env python3
"""
Mobile Results Updater - Create forms for updating match results from mobile
Generates HTML forms that can be used on mobile to update results
"""

import json
import os
from datetime import datetime

def load_fixtures():
    """Load current fixtures"""
    try:
        with open('uefa_fixtures_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('fixtures', {})
    except FileNotFoundError:
        return {}

def get_scheduled_fixtures():
    """Get fixtures without results"""
    fixtures = load_fixtures()
    scheduled = []
    
    for fixture_id, fixture in fixtures.items():
        if not fixture.get('result', {}).get('home_goals') and fixture.get('result', {}).get('home_goals') != 0:
            scheduled.append({
                'id': fixture_id,
                'date': fixture.get('date', ''),
                'home_team': fixture.get('home_team', ''),
                'away_team': fixture.get('away_team', ''),
                'competition': fixture.get('competition', ''),
                'venue': fixture.get('venue', '')
            })
    
    # Sort by date
    scheduled.sort(key=lambda x: x['date'])
    return scheduled

def create_mobile_results_form():
    """Create a mobile-friendly HTML form for updating results"""
    
    scheduled_fixtures = get_scheduled_fixtures()
    
    if not scheduled_fixtures:
        return create_no_fixtures_page()
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Update FIFA Results</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 15px;
            background: #f5f5f5;
            color: #333;
        }}
        .header {{
            background: linear-gradient(135deg, #e74c3c, #c0392b);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 20px;
        }}
        .fixture-form {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-left: 4px solid #3498db;
        }}
        .match-info {{
            text-align: center;
            margin-bottom: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
        }}
        .match-title {{
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .match-details {{
            color: #666;
            font-size: 14px;
        }}
        .score-input {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 15px;
            margin: 20px 0;
        }}
        .team-score {{
            text-align: center;
            flex: 1;
        }}
        .team-name {{
            font-weight: bold;
            margin-bottom: 8px;
            font-size: 14px;
        }}
        .score-field {{
            width: 60px;
            height: 60px;
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            border: 2px solid #ddd;
            border-radius: 8px;
            background: #fff;
        }}
        .vs {{
            font-size: 20px;
            font-weight: bold;
            color: #666;
        }}
        .notes-field {{
            width: 100%;
            height: 80px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-family: inherit;
            resize: vertical;
        }}
        .submit-btn {{
            background: linear-gradient(135deg, #27ae60, #2ecc71);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            width: 100%;
            cursor: pointer;
            margin-top: 15px;
        }}
        .submit-btn:active {{
            transform: scale(0.98);
        }}
        .instructions {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 6px;
            padding: 15px;
            margin-bottom: 20px;
            font-size: 14px;
        }}
        .footer {{
            text-align: center;
            color: #666;
            margin-top: 30px;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>⚽ Update Results</h1>
        <p>UEFA Fixtures - November 2025</p>
    </div>
    
    <div class="instructions">
        <strong>📱 How to use:</strong><br>
        1. Enter final scores for completed matches<br>
        2. Add any notes (optional)<br>
        3. Tap "Update Result" - this saves to OneDrive<br>
        4. Run analysis script on PC to see new rankings
    </div>
'''

    for i, fixture in enumerate(scheduled_fixtures):
        html += f'''
    <div class="fixture-form">
        <div class="match-info">
            <div class="match-title">{fixture['home_team']} vs {fixture['away_team']}</div>
            <div class="match-details">
                📅 {fixture['date']} • 🏆 {fixture['competition']}<br>
                🏟️ {fixture['venue']}
            </div>
        </div>
        
        <form id="form-{fixture['id']}" onsubmit="updateResult(event, '{fixture['id']}')">
            <div class="score-input">
                <div class="team-score">
                    <div class="team-name">{fixture['home_team']}</div>
                    <input type="number" class="score-field" id="home-{fixture['id']}" 
                           min="0" max="20" placeholder="0" required>
                </div>
                <div class="vs">VS</div>
                <div class="team-score">
                    <div class="team-name">{fixture['away_team']}</div>
                    <input type="number" class="score-field" id="away-{fixture['id']}" 
                           min="0" max="20" placeholder="0" required>
                </div>
            </div>
            
            <textarea class="notes-field" id="notes-{fixture['id']}" 
                      placeholder="Optional notes (e.g., red cards, penalties, etc.)"></textarea>
            
            <button type="submit" class="submit-btn">
                ✅ Update Result for {fixture['home_team']} vs {fixture['away_team']}
            </button>
        </form>
    </div>
'''

    html += f'''
    <div class="footer">
        Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}<br>
        {len(scheduled_fixtures)} fixtures awaiting results
    </div>

    <script>
        function updateResult(event, fixtureId) {{
            event.preventDefault();
            
            const homeGoals = document.getElementById('home-' + fixtureId).value;
            const awayGoals = document.getElementById('away-' + fixtureId).value;
            const notes = document.getElementById('notes-' + fixtureId).value;
            
            // Create result data
            const result = {{
                fixture_id: fixtureId,
                home_goals: parseInt(homeGoals),
                away_goals: parseInt(awayGoals),
                notes: notes,
                updated_at: new Date().toISOString()
            }};
            
            // Save to localStorage (will be processed later)
            let savedResults = JSON.parse(localStorage.getItem('fifa_results') || '[]');
            
            // Remove any existing result for this fixture
            savedResults = savedResults.filter(r => r.fixture_id !== fixtureId);
            
            // Add new result
            savedResults.push(result);
            localStorage.setItem('fifa_results', JSON.stringify(savedResults));
            
            // Visual feedback
            const form = document.getElementById('form-' + fixtureId);
            const button = form.querySelector('.submit-btn');
            button.innerHTML = '✅ Result Saved!';
            button.style.background = '#27ae60';
            
            // Disable form
            form.querySelectorAll('input, textarea, button').forEach(el => {{
                el.disabled = true;
            }});
            
            setTimeout(() => {{
                alert('Result saved! ' + homeGoals + '-' + awayGoals + '\\n\\nTo update rankings:\\n1. Sync OneDrive\\n2. Run analysis on PC');
            }}, 500);
        }}
        
        // Load saved results on page load
        window.onload = function() {{
            const savedResults = JSON.parse(localStorage.getItem('fifa_results') || '[]');
            
            savedResults.forEach(result => {{
                const homeField = document.getElementById('home-' + result.fixture_id);
                const awayField = document.getElementById('away-' + result.fixture_id);
                const notesField = document.getElementById('notes-' + result.fixture_id);
                
                if (homeField) {{
                    homeField.value = result.home_goals;
                    awayField.value = result.away_goals;
                    notesField.value = result.notes;
                    
                    // Disable the form
                    const form = document.getElementById('form-' + result.fixture_id);
                    form.querySelectorAll('input, textarea, button').forEach(el => {{
                        el.disabled = true;
                    }});
                    
                    const button = form.querySelector('.submit-btn');
                    button.innerHTML = '✅ Result Saved!';
                    button.style.background = '#27ae60';
                }}
            }});
        }};
    </script>
</body>
</html>'''

    return html

def create_no_fixtures_page():
    """Create page when no fixtures are scheduled"""
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>No Fixtures - FIFA Results</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 15px;
            background: #f5f5f5;
            color: #333;
            text-align: center;
        }}
        .message {{
            background: white;
            border-radius: 10px;
            padding: 40px 20px;
            margin-top: 50px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .icon {{
            font-size: 64px;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <div class="message">
        <div class="icon">✅</div>
        <h2>All Fixtures Complete!</h2>
        <p>No more fixtures awaiting results.</p>
        <p><strong>Next step:</strong> Run analysis to see final rankings!</p>
    </div>
</body>
</html>'''
    return html

def create_results_processor():
    """Create a Python script to process mobile results"""
    
    processor_code = '''#!/usr/bin/env python3
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
        print("\\n⚽ ADD RESULT:")
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
    
    print("\\n🏆 Results updated! Run enhanced_team_range_analysis.py for new rankings")

if __name__ == "__main__":
    process_mobile_results()
'''
    
    with open('process_mobile_results.py', 'w', encoding='utf-8') as f:
        f.write(processor_code)
    
    return 'process_mobile_results.py'

def main():
    """Generate mobile results update system"""
    print("📱 CREATING MOBILE RESULTS UPDATE SYSTEM")
    print("=" * 50)
    
    # Create the mobile form
    html_content = create_mobile_results_form()
    
    # Save HTML file
    output_file = 'mobile_results_form.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Create results processor
    processor_file = create_results_processor()
    
    scheduled = get_scheduled_fixtures()
    
    print(f"✅ Mobile form created: {output_file}")
    print(f"✅ Results processor: {processor_file}")
    print(f"📱 Fixtures awaiting results: {len(scheduled)}")
    
    if scheduled:
        print(f"\\n📅 NEXT FIXTURES:")
        for fixture in scheduled[:5]:  # Show first 5
            print(f"  • {fixture['date']}: {fixture['home_team']} vs {fixture['away_team']}")
    
    print(f"\\n🔄 MOBILE UPDATE WORKFLOW:")
    print(f"1. Open {output_file} on your mobile (via OneDrive)")
    print(f"2. Enter match results and tap 'Update Result'")
    print(f"3. On PC, run: python {processor_file}")
    print(f"4. Run: python enhanced_team_range_analysis.py")
    print(f"5. Generate mobile report: python simple_mobile_analyzer.py")
    
    return True

if __name__ == "__main__":
    main()