#!/usr/bin/env python3
"""
Simple Mobile Results Interface
Creates a mobile-friendly way to update match results
"""

import json
from datetime import datetime

def create_simple_results_form():
    """Create a simple mobile form for match results"""
    
    # Load current fixtures
    try:
        with open('uefa_fixtures_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            fixtures = data.get('fixtures', {})
    except:
        fixtures = {}
    
    # Get scheduled fixtures (no results yet)
    scheduled = []
    for fixture_id, fixture in fixtures.items():
        result = fixture.get('result', {})
        if not result or (result.get('home_goals') is None and result.get('away_goals') is None):
            scheduled.append({
                'id': fixture_id,
                'date': fixture.get('date', ''),
                'home': fixture.get('home_team', ''),
                'away': fixture.get('away_team', ''),
                'competition': fixture.get('competition', ''),
                'venue': fixture.get('venue', '')
            })
    
    # Sort by date
    scheduled.sort(key=lambda x: x['date'])
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📱 FIFA Results Mobile</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, sans-serif; 
            margin: 0; padding: 10px; background: #f0f0f0; 
        }}
        .header {{ 
            background: #2c3e50; color: white; padding: 20px; 
            border-radius: 10px; text-align: center; margin-bottom: 20px; 
        }}
        .fixture {{ 
            background: white; margin: 10px 0; padding: 20px; 
            border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
        }}
        .match {{ 
            text-align: center; font-size: 18px; font-weight: bold; 
            margin-bottom: 15px; color: #2c3e50; 
        }}
        .details {{ 
            text-align: center; color: #666; font-size: 14px; 
            margin-bottom: 20px; 
        }}
        .score-row {{ 
            display: flex; justify-content: center; align-items: center; 
            gap: 20px; margin: 20px 0; 
        }}
        .team {{ text-align: center; }}
        .team-name {{ font-weight: bold; margin-bottom: 10px; }}
        .score-input {{ 
            width: 50px; height: 50px; font-size: 24px; font-weight: bold; 
            text-align: center; border: 2px solid #ddd; border-radius: 8px; 
        }}
        .vs {{ font-size: 24px; font-weight: bold; color: #888; }}
        .notes {{ 
            width: 100%; height: 60px; padding: 10px; border: 1px solid #ddd; 
            border-radius: 6px; margin: 15px 0; 
        }}
        .save-btn {{ 
            background: #27ae60; color: white; border: none; padding: 15px; 
            border-radius: 8px; font-size: 16px; font-weight: bold; 
            width: 100%; cursor: pointer; 
        }}
        .instructions {{ 
            background: #fff3cd; padding: 15px; border-radius: 6px; 
            margin-bottom: 20px; font-size: 14px; 
        }}
        .saved {{ background: #27ae60 !important; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>⚽ Update Results</h1>
        <p>UEFA Fixtures Mobile Form</p>
    </div>
    
    <div class="instructions">
        <strong>📱 How to use:</strong><br>
        1. Enter final match scores<br>
        2. Tap "Save Result" - data stored locally<br>
        3. Copy results to PC for processing
    </div>
'''

    if not scheduled:
        html += '''
    <div class="fixture">
        <div class="match">✅ All fixtures have results!</div>
        <div class="details">No more matches to update</div>
    </div>
'''
    else:
        for fixture in scheduled:
            html += f'''
    <div class="fixture">
        <div class="match">{fixture['home']} vs {fixture['away']}</div>
        <div class="details">
            📅 {fixture['date']} • 🏆 {fixture['competition']}<br>
            🏟️ {fixture.get('venue', 'TBD')}
        </div>
        
        <div class="score-row">
            <div class="team">
                <div class="team-name">{fixture['home']}</div>
                <input type="number" class="score-input" id="home_{fixture['id']}" 
                       min="0" max="15" placeholder="0">
            </div>
            <div class="vs">-</div>
            <div class="team">
                <div class="team-name">{fixture['away']}</div>
                <input type="number" class="score-input" id="away_{fixture['id']}" 
                       min="0" max="15" placeholder="0">
            </div>
        </div>
        
        <textarea class="notes" id="notes_{fixture['id']}" 
                  placeholder="Optional notes..."></textarea>
        
        <button class="save-btn" onclick="saveResult('{fixture['id']}', '{fixture['home']}', '{fixture['away']}')">
            💾 Save Result
        </button>
    </div>
'''

    html += f'''
    <div style="background: white; padding: 20px; border-radius: 10px; margin-top: 20px; text-align: center;">
        <h3>📊 Saved Results</h3>
        <div id="saved-results">No results saved yet</div>
        <button onclick="exportResults()" style="background: #3498db; color: white; border: none; padding: 10px 20px; border-radius: 6px; margin-top: 10px;">
            📋 Copy All Results
        </button>
    </div>

    <script>
        let savedResults = JSON.parse(localStorage.getItem('fifa_mobile_results') || '[]');
        
        function saveResult(fixtureId, homeTeam, awayTeam) {{
            const homeGoals = document.getElementById('home_' + fixtureId).value;
            const awayGoals = document.getElementById('away_' + fixtureId).value;
            const notes = document.getElementById('notes_' + fixtureId).value;
            
            if (homeGoals === '' || awayGoals === '') {{
                alert('Please enter both scores');
                return;
            }}
            
            const result = {{
                fixture_id: fixtureId,
                home_team: homeTeam,
                away_team: awayTeam,
                home_goals: parseInt(homeGoals),
                away_goals: parseInt(awayGoals),
                notes: notes,
                timestamp: new Date().toISOString()
            }};
            
            // Remove existing result for this fixture
            savedResults = savedResults.filter(r => r.fixture_id !== fixtureId);
            savedResults.push(result);
            
            localStorage.setItem('fifa_mobile_results', JSON.stringify(savedResults));
            
            // Visual feedback
            const button = event.target;
            button.innerHTML = '✅ Saved!';
            button.classList.add('saved');
            
            updateSavedResultsDisplay();
            
            setTimeout(() => {{
                button.innerHTML = '💾 Save Result';
                button.classList.remove('saved');
            }}, 2000);
        }}
        
        function updateSavedResultsDisplay() {{
            const display = document.getElementById('saved-results');
            
            if (savedResults.length === 0) {{
                display.innerHTML = 'No results saved yet';
                return;
            }}
            
            let html = '';
            savedResults.forEach(result => {{
                html += `<div style="margin: 5px 0; padding: 5px; background: #f8f9fa; border-radius: 4px;">
                    ${{result.home_team}} ${{result.home_goals}}-${{result.away_goals}} ${{result.away_team}}
                </div>`;
            }});
            display.innerHTML = html;
        }}
        
        function exportResults() {{
            if (savedResults.length === 0) {{
                alert('No results to export');
                return;
            }}
            
            let text = 'FIFA Mobile Results:\\n\\n';
            savedResults.forEach(result => {{
                text += `${{result.fixture_id}}: ${{result.home_team}} ${{result.home_goals}}-${{result.away_goals}} ${{result.away_team}}\\n`;
                if (result.notes) text += `Notes: ${{result.notes}}\\n`;
                text += '\\n';
            }});
            
            // Copy to clipboard if possible
            if (navigator.clipboard) {{
                navigator.clipboard.writeText(text).then(() => {{
                    alert('Results copied to clipboard!');
                }});
            }} else {{
                // Fallback - show in alert
                alert(text);
            }}
        }}
        
        // Load saved results on page load
        window.onload = function() {{
            updateSavedResultsDisplay();
            
            // Restore form values
            savedResults.forEach(result => {{
                const homeInput = document.getElementById('home_' + result.fixture_id);
                const awayInput = document.getElementById('away_' + result.fixture_id);
                const notesInput = document.getElementById('notes_' + result.fixture_id);
                
                if (homeInput) {{
                    homeInput.value = result.home_goals;
                    awayInput.value = result.away_goals;
                    notesInput.value = result.notes || '';
                }}
            }});
        }};
    </script>
</body>
</html>'''
    
    return html

def main():
    """Generate the mobile results form"""
    print("📱 CREATING SIMPLE MOBILE RESULTS FORM")
    print("=" * 45)
    
    html_content = create_simple_results_form()
    
    output_file = 'mobile_results_simple.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Mobile form created: {output_file}")
    print(f"📱 File size: {len(html_content) / 1024:.1f}KB")
    
    print(f"\\n🔄 MOBILE UPDATE WORKFLOW:")
    print(f"1. Open {output_file} on mobile (via OneDrive)")
    print(f"2. Enter match results and tap 'Save Result'")
    print(f"3. Tap 'Copy All Results' to get formatted text")
    print(f"4. Share/email results to your PC")
    print(f"5. Use update_results.py to add to system")
    print(f"6. Run enhanced_team_range_analysis.py for new rankings")
    
    return True

if __name__ == "__main__":
    main()