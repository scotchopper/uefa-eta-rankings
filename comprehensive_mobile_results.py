#!/usr/bin/env python3
"""
Complete Mobile Results Form - All UEFA Fixtures
Creates a comprehensive mobile form for updating all UEFA match results
"""

import json
from datetime import datetime

def load_fixtures():
    """Load all UEFA fixtures"""
    try:
        with open('uefa_fixtures_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('fixtures', {})
    except FileNotFoundError:
        return {}

def get_fixtures_by_status():
    """Organize fixtures by completion status"""
    fixtures = load_fixtures()
    scheduled = []
    completed = []
    
    for fixture_id, fixture in fixtures.items():
        result = fixture.get('result', {})
        has_result = result and (result.get('home_goals') is not None or result.get('away_goals') is not None)
        
        fixture_data = {
            'id': fixture_id,
            'date': fixture.get('date', ''),
            'home': fixture.get('home_team', ''),
            'away': fixture.get('away_team', ''),
            'competition': fixture.get('competition', ''),
            'venue': fixture.get('venue', ''),
            'importance': fixture.get('importance', 25)
        }
        
        if has_result:
            fixture_data['result'] = result
            completed.append(fixture_data)
        else:
            scheduled.append(fixture_data)
    
    # Sort by date
    scheduled.sort(key=lambda x: x['date'])
    completed.sort(key=lambda x: x['date'])
    
    return scheduled, completed

def create_comprehensive_mobile_form():
    """Create mobile form for all UEFA fixtures"""
    
    scheduled, completed = get_fixtures_by_status()
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UEFA Results Mobile - All Fixtures</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, sans-serif; 
            margin: 0; padding: 10px; background: #f0f0f0; 
        }}
        .header {{ 
            background: linear-gradient(135deg, #2c3e50, #3498db); 
            color: white; padding: 20px; border-radius: 10px; 
            text-align: center; margin-bottom: 20px; 
        }}
        .stats {{ 
            display: grid; grid-template-columns: 1fr 1fr; gap: 15px; 
            margin-bottom: 20px; 
        }}
        .stat-card {{ 
            background: white; padding: 15px; border-radius: 8px; 
            text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); 
        }}
        .stat-number {{ font-size: 24px; font-weight: bold; color: #2c3e50; }}
        .stat-label {{ font-size: 12px; color: #666; margin-top: 5px; }}
        .tabs {{ 
            display: flex; background: white; border-radius: 10px; 
            margin-bottom: 20px; overflow: hidden; 
        }}
        .tab {{ 
            flex: 1; padding: 15px; text-align: center; background: white; 
            border: none; cursor: pointer; font-weight: 600; color: #666; 
        }}
        .tab.active {{ background: #3498db; color: white; }}
        .tab-content {{ display: none; }}
        .tab-content.active {{ display: block; }}
        .fixture {{ 
            background: white; margin: 10px 0; padding: 15px; 
            border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
            border-left: 4px solid #ddd;
        }}
        .fixture.scotland {{ border-left-color: #005EB8; }}
        .fixture.completed {{ border-left-color: #27ae60; }}
        .match-header {{ 
            display: flex; justify-content: space-between; align-items: center; 
            margin-bottom: 10px; 
        }}
        .match-title {{ font-size: 16px; font-weight: bold; color: #2c3e50; }}
        .match-date {{ font-size: 12px; color: #666; }}
        .match-details {{ 
            font-size: 13px; color: #666; margin-bottom: 15px; 
            text-align: center; 
        }}
        .score-row {{ 
            display: flex; justify-content: center; align-items: center; 
            gap: 15px; margin: 15px 0; 
        }}
        .team {{ text-align: center; flex: 1; }}
        .team-name {{ font-weight: bold; margin-bottom: 8px; font-size: 14px; }}
        .score-input {{ 
            width: 45px; height: 45px; font-size: 20px; font-weight: bold; 
            text-align: center; border: 2px solid #ddd; border-radius: 6px; 
        }}
        .vs {{ font-size: 18px; font-weight: bold; color: #888; }}
        .save-btn {{ 
            background: #27ae60; color: white; border: none; padding: 12px; 
            border-radius: 6px; font-size: 14px; font-weight: bold; 
            width: 100%; cursor: pointer; margin-top: 10px; 
        }}
        .result-display {{ 
            background: #f8f9fa; padding: 10px; border-radius: 6px; 
            text-align: center; font-weight: bold; 
        }}
        .controls {{ 
            background: white; padding: 20px; border-radius: 10px; 
            margin: 20px 0; text-align: center; 
        }}
        .control-btn {{ 
            background: #3498db; color: white; border: none; 
            padding: 12px 20px; border-radius: 6px; margin: 5px; 
            cursor: pointer; font-weight: bold; 
        }}
        .control-btn.danger {{ background: #e74c3c; }}
        .control-btn.success {{ background: #27ae60; }}
        .search-box {{ 
            width: 100%; padding: 10px; border: 1px solid #ddd; 
            border-radius: 6px; margin-bottom: 15px; 
        }}
        .hidden {{ display: none; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>UEFA Results Mobile</h1>
        <p>All 54 UEFA Fixtures - November 2025</p>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <div class="stat-number">{len(scheduled)}</div>
            <div class="stat-label">Scheduled</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{len(completed)}</div>
            <div class="stat-label">Completed</div>
        </div>
    </div>
    
    <div class="tabs">
        <button class="tab active" onclick="showTab('scheduled')">Scheduled</button>
        <button class="tab" onclick="showTab('completed')">Completed</button>
        <button class="tab" onclick="showTab('saved')">Saved</button>
    </div>
    
    <div id="scheduled" class="tab-content active">
        <input type="text" class="search-box" placeholder="Search teams..." onkeyup="filterFixtures('scheduled')">
        <div id="scheduled-fixtures">
'''

    # Add scheduled fixtures
    for fixture in scheduled:
        is_scotland = 'Scotland' in [fixture['home'], fixture['away']]
        fixture_class = 'fixture scotland' if is_scotland else 'fixture'
        comp_short = 'WCQ' if 'World Cup' in fixture['competition'] else 'F' if 'Friendly' in fixture['competition'] else 'NL'
        
        html += f'''
            <div class="{fixture_class}" data-teams="{fixture['home'].lower()} {fixture['away'].lower()}">
                <div class="match-header">
                    <div class="match-title">{fixture['home']} vs {fixture['away']}</div>
                    <div class="match-date">{fixture['date']}</div>
                </div>
                <div class="match-details">
                    {comp_short} (×{fixture['importance']}) • {fixture.get('venue', 'TBD')}
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
                
                <button class="save-btn" onclick="saveResult('{fixture['id']}', '{fixture['home']}', '{fixture['away']}')">
                    Save Result
                </button>
            </div>
        '''

    html += '''
        </div>
    </div>
    
    <div id="completed" class="tab-content">
        <input type="text" class="search-box" placeholder="Search teams..." onkeyup="filterFixtures('completed')">
        <div id="completed-fixtures">
'''

    # Add completed fixtures
    for fixture in completed:
        is_scotland = 'Scotland' in [fixture['home'], fixture['away']]
        fixture_class = 'fixture completed scotland' if is_scotland else 'fixture completed'
        result = fixture.get('result', {})
        home_goals = result.get('home_goals', 0)
        away_goals = result.get('away_goals', 0)
        
        html += f'''
            <div class="{fixture_class}" data-teams="{fixture['home'].lower()} {fixture['away'].lower()}">
                <div class="match-header">
                    <div class="match-title">{fixture['home']} vs {fixture['away']}</div>
                    <div class="match-date">{fixture['date']}</div>
                </div>
                <div class="match-details">
                    {fixture['competition']} • {fixture.get('venue', 'TBD')}
                </div>
                
                <div class="result-display">
                    Final Score: {fixture['home']} {home_goals}-{away_goals} {fixture['away']}
                </div>
            </div>
        '''

    html += f'''
        </div>
    </div>
    
    <div id="saved" class="tab-content">
        <div id="saved-results">No results saved yet</div>
    </div>
    
    <div class="controls">
        <button class="control-btn success" onclick="exportResults()">Export All Results</button>
        <button class="control-btn" onclick="exportScotlandOnly()">Export Scotland Only</button>
        <button class="control-btn danger" onclick="clearResults()">Clear All Saved</button>
    </div>
    
    <div style="background: white; padding: 20px; border-radius: 10px; margin-top: 20px; font-size: 13px;">
        <h3>PC Processing Instructions:</h3>
        <ol>
            <li>Export results using buttons above</li>
            <li>On PC: <code>python update_results.py</code></li>
            <li>Choose option 2 (Add result interactively) for each result</li>
            <li>Generate new rankings: <code>python enhanced_team_range_analysis.py</code></li>
            <li>Update mobile report: <code>python simple_mobile_analyzer.py</code></li>
        </ol>
        <p><strong>Tip:</strong> You can update just Scotland results for quick analysis, or all results for complete UEFA rankings.</p>
    </div>

    <script>
        let savedResults = JSON.parse(localStorage.getItem('uefa_mobile_results') || '[]');
        
        function showTab(tabName) {{
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(content => {{
                content.classList.remove('active');
            }});
            document.querySelectorAll('.tab').forEach(tab => {{
                tab.classList.remove('active');
            }});
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
            
            if (tabName === 'saved') {{
                updateSavedDisplay();
            }}
        }}
        
        function filterFixtures(tabName) {{
            const searchTerm = event.target.value.toLowerCase();
            const fixtures = document.querySelectorAll(`#${{tabName}}-fixtures .fixture`);
            
            fixtures.forEach(fixture => {{
                const teams = fixture.getAttribute('data-teams');
                if (teams.includes(searchTerm)) {{
                    fixture.classList.remove('hidden');
                }} else {{
                    fixture.classList.add('hidden');
                }}
            }});
        }}
        
        function saveResult(fixtureId, homeTeam, awayTeam) {{
            const homeGoals = document.getElementById('home_' + fixtureId).value;
            const awayGoals = document.getElementById('away_' + fixtureId).value;
            
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
                result_text: homeTeam + ' ' + homeGoals + '-' + awayGoals + ' ' + awayTeam,
                timestamp: new Date().toISOString(),
                is_scotland: homeTeam === 'Scotland' || awayTeam === 'Scotland'
            }};
            
            // Remove existing result for this fixture
            savedResults = savedResults.filter(r => r.fixture_id !== fixtureId);
            savedResults.push(result);
            localStorage.setItem('uefa_mobile_results', JSON.stringify(savedResults));
            
            // Visual feedback
            event.target.innerHTML = 'Saved!';
            event.target.style.background = '#2ecc71';
            setTimeout(() => {{
                event.target.innerHTML = 'Save Result';
                event.target.style.background = '#27ae60';
            }}, 2000);
        }}
        
        function updateSavedDisplay() {{
            const display = document.getElementById('saved-results');
            
            if (savedResults.length === 0) {{
                display.innerHTML = '<p style="text-align: center; color: #666;">No results saved yet</p>';
                return;
            }}
            
            // Group by Scotland vs Others
            const scotlandResults = savedResults.filter(r => r.is_scotland);
            const otherResults = savedResults.filter(r => !r.is_scotland);
            
            let html = '';
            
            if (scotlandResults.length > 0) {{
                html += '<h4 style="color: #005EB8;">Scotland Results (' + scotlandResults.length + ')</h4>';
                scotlandResults.forEach(result => {{
                    html += `<div style="margin: 5px 0; padding: 8px; background: #e3f2fd; border-radius: 4px; border-left: 3px solid #005EB8;">
                        <strong>${{result.result_text}}</strong><br>
                        <small>Saved: ${{new Date(result.timestamp).toLocaleString()}}</small>
                    </div>`;
                }});
            }}
            
            if (otherResults.length > 0) {{
                html += '<h4 style="color: #2c3e50;">Other Results (' + otherResults.length + ')</h4>';
                otherResults.forEach(result => {{
                    html += `<div style="margin: 5px 0; padding: 8px; background: #f8f9fa; border-radius: 4px; border-left: 3px solid #27ae60;">
                        <strong>${{result.result_text}}</strong><br>
                        <small>Saved: ${{new Date(result.timestamp).toLocaleString()}}</small>
                    </div>`;
                }});
            }}
            
            display.innerHTML = html;
        }}
        
        function exportResults() {{
            if (savedResults.length === 0) {{
                alert('No results to export');
                return;
            }}
            
            let text = 'UEFA Mobile Results - All Fixtures:\\n\\n';
            savedResults.forEach(result => {{
                text += result.fixture_id + ': ' + result.result_text + '\\n';
            }});
            text += '\\nTotal results: ' + savedResults.length + '\\n';
            text += 'Generated: ' + new Date().toLocaleString() + '\\n';
            
            copyToClipboard(text, 'All results exported!');
        }}
        
        function exportScotlandOnly() {{
            const scotlandResults = savedResults.filter(r => r.is_scotland);
            
            if (scotlandResults.length === 0) {{
                alert('No Scotland results to export');
                return;
            }}
            
            let text = 'Scotland Results Only:\\n\\n';
            scotlandResults.forEach(result => {{
                text += result.fixture_id + ': ' + result.result_text + '\\n';
            }});
            text += '\\nScotland results: ' + scotlandResults.length + '\\n';
            
            copyToClipboard(text, 'Scotland results exported!');
        }}
        
        function copyToClipboard(text, successMessage) {{
            if (navigator.clipboard) {{
                navigator.clipboard.writeText(text).then(() => {{
                    alert(successMessage);
                }});
            }} else {{
                alert('Copy this text:\\n\\n' + text);
            }}
        }}
        
        function clearResults() {{
            if (confirm('Clear all saved results?')) {{
                localStorage.removeItem('uefa_mobile_results');
                savedResults = [];
                updateSavedDisplay();
                
                // Reset all form inputs
                document.querySelectorAll('.score-input').forEach(input => {{
                    input.value = '';
                }});
                
                alert('All results cleared!');
            }}
        }}
        
        // Load saved results on page load
        window.onload = function() {{
            // Restore form values from saved results
            savedResults.forEach(result => {{
                const homeInput = document.getElementById('home_' + result.fixture_id);
                const awayInput = document.getElementById('away_' + result.fixture_id);
                if (homeInput) {{
                    homeInput.value = result.home_goals;
                    awayInput.value = result.away_goals;
                }}
            }});
        }};
    </script>
</body>
</html>'''
    
    return html

def main():
    """Generate comprehensive mobile results form"""
    print("🌍 CREATING COMPREHENSIVE UEFA MOBILE RESULTS FORM")
    print("=" * 55)
    
    html_content = create_comprehensive_mobile_form()
    
    output_file = 'uefa_mobile_results_all.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    scheduled, completed = get_fixtures_by_status()
    
    print(f"✅ Complete mobile form created: {output_file}")
    print(f"📱 File size: {len(html_content) / 1024:.1f}KB")
    print(f"⚽ Total fixtures: {len(scheduled) + len(completed)}")
    print(f"📅 Scheduled: {len(scheduled)}")
    print(f"✅ Completed: {len(completed)}")
    
    scotland_scheduled = [f for f in scheduled if 'Scotland' in [f['home'], f['away']]]
    print(f"🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland fixtures pending: {len(scotland_scheduled)}")
    
    print(f"\\n🔄 MOBILE WORKFLOW:")
    print(f"1. Open {output_file} on mobile (via OneDrive)")
    print(f"2. Use tabs: Scheduled → Enter results → Saved")
    print(f"3. Search function to find specific teams")
    print(f"4. Export all results OR just Scotland results")
    print(f"5. Process on PC with update_results.py")
    print(f"6. Generate new rankings for entire UEFA")
    
    return True

if __name__ == "__main__":
    main()