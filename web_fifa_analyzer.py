#!/usr/bin/env python3
"""
Web Interface for Enhanced UEFA Teams Analysis
Simple Flask app to run FIFA ranking analysis from mobile
"""

from flask import Flask, render_template, jsonify, request
import json
import sys
import os
from enhanced_team_range_analysis import EnhancedTeamRangeAnalyzer
from update_results import ResultsUpdater

app = Flask(__name__)

@app.route('/')
def home():
    """Main page with analysis options"""
    return render_template('index.html')

@app.route('/api/analyze')
def analyze_teams():
    """API endpoint to run the full team analysis"""
    try:
        analyzer = EnhancedTeamRangeAnalyzer()
        all_results = analyzer.analyze_all_teams()
        scotland_summary = analyzer.scotland_detailed_analysis(all_results)
        
        # Format results for web display
        formatted_results = []
        for result in all_results:
            if result.get('valid_data', True):
                formatted_results.append({
                    'fifa_rank': result['current_rank'],
                    'uefa_rank': result.get('uefa_rank', 0),
                    'team_name': result['team_name'],
                    'team_code': result['team_code'],
                    'current_points': round(result['initial_points'], 2),
                    'best_points': round(result['best_points'], 2),
                    'worst_points': round(result['worst_points'], 2),
                    'range': round(result['range'], 2),
                    'best_change': round(result['best_change'], 2),
                    'worst_change': round(result['worst_change'], 2),
                    'fixtures': {
                        'opponent1': result.get('fixture1_opponent', ''),
                        'opponent2': result.get('fixture2_opponent', ''),
                        'home1': result.get('fixture1_home', False),
                        'home2': result.get('fixture2_home', False),
                        'comp1': result.get('fixture1_competition', ''),
                        'comp2': result.get('fixture2_competition', ''),
                        'importance1': result.get('importance1', 25),
                        'importance2': result.get('importance2', 25)
                    }
                })
        
        return jsonify({
            'success': True,
            'teams': formatted_results,
            'scotland_summary': scotland_summary,
            'total_teams': len(formatted_results)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/scotland')
def scotland_analysis():
    """Quick Scotland-only analysis"""
    try:
        analyzer = EnhancedTeamRangeAnalyzer()
        all_results = analyzer.analyze_all_teams()
        scotland_summary = analyzer.scotland_detailed_analysis(all_results)
        
        # Find Scotland's data
        scotland_data = None
        for result in all_results:
            if result['team_name'] == 'Scotland':
                scotland_data = result
                break
        
        if not scotland_data:
            return jsonify({'success': False, 'error': 'Scotland data not found'}), 404
        
        return jsonify({
            'success': True,
            'scotland': {
                'fifa_rank': scotland_data['current_rank'],
                'uefa_rank': scotland_data.get('uefa_rank', 0),
                'current_points': round(scotland_data['initial_points'], 2),
                'best_points': round(scotland_data['best_points'], 2),
                'worst_points': round(scotland_data['worst_points'], 2),
                'best_change': round(scotland_data['best_change'], 2),
                'worst_change': round(scotland_data['worst_change'], 2),
                'fixtures': [
                    {
                        'opponent': scotland_data.get('fixture1_opponent', ''),
                        'home': scotland_data.get('fixture1_home', False),
                        'competition': scotland_data.get('fixture1_competition', ''),
                        'importance': scotland_data.get('importance1', 25)
                    },
                    {
                        'opponent': scotland_data.get('fixture2_opponent', ''),
                        'home': scotland_data.get('fixture2_home', False),
                        'competition': scotland_data.get('fixture2_competition', ''),
                        'importance': scotland_data.get('importance2', 25)
                    }
                ]
            },
            'summary': scotland_summary
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/fixtures')
def get_fixtures():
    """Get all fixtures data"""
    try:
        with open('uefa_fixtures_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            fixtures = data.get('fixtures', {})
        
        formatted_fixtures = []
        for fixture_id, fixture in fixtures.items():
            formatted_fixtures.append({
                'id': fixture_id,
                'date': fixture.get('date', ''),
                'home_team': fixture.get('home_team', ''),
                'away_team': fixture.get('away_team', ''),
                'competition': fixture.get('competition', ''),
                'importance': fixture.get('importance', 25),
                'venue': fixture.get('venue', ''),
                'result': fixture.get('result', {})
            })
        
        return jsonify({
            'success': True,
            'fixtures': formatted_fixtures,
            'total': len(formatted_fixtures)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/update_result', methods=['POST'])
def update_result():
    """Add a match result"""
    try:
        data = request.get_json()
        fixture_id = data.get('fixture_id')
        home_goals = data.get('home_goals')
        away_goals = data.get('away_goals')
        notes = data.get('notes', '')
        
        if not all([fixture_id, home_goals is not None, away_goals is not None]):
            return jsonify({
                'success': False,
                'error': 'Missing required fields: fixture_id, home_goals, away_goals'
            }), 400
        
        updater = ResultsUpdater()
        success = updater.add_result(fixture_id, int(home_goals), int(away_goals), notes)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Result added for fixture {fixture_id}'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to add result'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Create templates directory and basic HTML
def create_templates():
    """Create the templates directory and HTML files"""
    templates_dir = 'templates'
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
    
    # Create index.html
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FIFA Ranking Analyzer</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 20px;
        }
        .header {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 30px;
        }
        .buttons {
            display: flex;
            gap: 15px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
            transition: transform 0.2s;
        }
        .btn:hover {
            transform: translateY(-2px);
        }
        .btn-scotland {
            background: linear-gradient(135deg, #005EB8 0%, #ffffff 100%);
            color: #005EB8;
        }
        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        .results {
            margin-top: 20px;
        }
        .scotland-summary {
            background: linear-gradient(135deg, #005EB8 0%, #ffffff 100%);
            color: #005EB8;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            border: 2px solid #005EB8;
        }
        .teams-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        .teams-table th,
        .teams-table td {
            padding: 8px 12px;
            text-align: left;
            border-bottom: 1px solid #eee;
            font-size: 14px;
        }
        .teams-table th {
            background-color: #f8f9fa;
            font-weight: 600;
            position: sticky;
            top: 0;
        }
        .teams-table tr:hover {
            background-color: #f8f9fa;
        }
        .scotland-row {
            background-color: #e3f2fd !important;
            font-weight: bold;
        }
        .mobile-card {
            display: none;
            border: 1px solid #ddd;
            border-radius: 8px;
            margin-bottom: 10px;
            padding: 15px;
        }
        .error {
            background: #fee;
            color: #c33;
            padding: 15px;
            border-radius: 6px;
            margin: 10px 0;
        }
        
        @media (max-width: 768px) {
            .teams-table {
                display: none;
            }
            .mobile-card {
                display: block;
            }
            .buttons {
                flex-direction: column;
            }
            .btn {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏆 FIFA Ranking Analyzer</h1>
            <p>UEFA Teams Best/Worst Case Analysis - November 2025</p>
        </div>
        
        <div class="buttons">
            <button class="btn btn-scotland" onclick="analyzeScotland()">🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland Analysis</button>
            <button class="btn" onclick="analyzeAllTeams()">🌍 All UEFA Teams</button>
            <button class="btn" onclick="showFixtures()">📅 View Fixtures</button>
        </div>
        
        <div id="results" class="results"></div>
    </div>

    <script>
        function showLoading() {
            document.getElementById('results').innerHTML = '<div class="loading">⏳ Calculating rankings...</div>';
        }
        
        function showError(message) {
            document.getElementById('results').innerHTML = `<div class="error">❌ Error: ${message}</div>`;
        }
        
        async function analyzeScotland() {
            showLoading();
            try {
                const response = await fetch('/api/scotland');
                const data = await response.json();
                
                if (data.success) {
                    displayScotlandResults(data);
                } else {
                    showError(data.error);
                }
            } catch (error) {
                showError('Network error: ' + error.message);
            }
        }
        
        async function analyzeAllTeams() {
            showLoading();
            try {
                const response = await fetch('/api/analyze');
                const data = await response.json();
                
                if (data.success) {
                    displayAllTeamsResults(data);
                } else {
                    showError(data.error);
                }
            } catch (error) {
                showError('Network error: ' + error.message);
            }
        }
        
        async function showFixtures() {
            showLoading();
            try {
                const response = await fetch('/api/fixtures');
                const data = await response.json();
                
                if (data.success) {
                    displayFixtures(data.fixtures);
                } else {
                    showError(data.error);
                }
            } catch (error) {
                showError('Network error: ' + error.message);
            }
        }
        
        function displayScotlandResults(data) {
            const scotland = data.scotland;
            const summary = data.summary;
            
            let html = `
                <div class="scotland-summary">
                    <h2>🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland Analysis</h2>
                    <p><strong>Current Position:</strong> FIFA #${scotland.fifa_rank} / UEFA #${scotland.uefa_rank} (${scotland.current_points} points)</p>
                    <p><strong>Best Case:</strong> ${scotland.best_points} points (${scotland.best_change >= 0 ? '+' : ''}${scotland.best_change})</p>
                    <p><strong>Worst Case:</strong> ${scotland.worst_points} points (${scotland.worst_change >= 0 ? '+' : ''}${scotland.worst_change})</p>
                    
                    <h3>Fixtures:</h3>
                    <ul>
                        ${scotland.fixtures.map(f => `
                            <li>vs ${f.opponent} (${f.home ? 'H' : 'A'}) - ${f.competition} (×${f.importance})</li>
                        `).join('')}
                    </ul>
                    
                    ${summary ? `
                        <h3>Ranking Movement Potential:</h3>
                        <p><strong>UEFA Ranking:</strong> Can move between #${summary.best_uefa_rank} and #${summary.worst_uefa_rank}</p>
                        <p><strong>Maximum gain:</strong> ${summary.max_uefa_gain} places up</p>
                        <p><strong>Maximum loss:</strong> ${summary.max_uefa_loss} places down</p>
                    ` : ''}
                </div>
            `;
            
            document.getElementById('results').innerHTML = html;
        }
        
        function displayAllTeamsResults(data) {
            let html = `
                <h2>📊 All UEFA Teams Analysis (${data.total_teams} teams)</h2>
                
                <table class="teams-table">
                    <thead>
                        <tr>
                            <th>FIFA</th>
                            <th>UEFA</th>
                            <th>Team</th>
                            <th>Current</th>
                            <th>Best</th>
                            <th>Worst</th>
                            <th>Range</th>
                            <th>Fixtures</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            
            data.teams.forEach(team => {
                const isScotland = team.team_name === 'Scotland';
                const rowClass = isScotland ? 'scotland-row' : '';
                
                html += `
                    <tr class="${rowClass}">
                        <td>#${team.fifa_rank}</td>
                        <td>#${team.uefa_rank}</td>
                        <td>${team.team_name}</td>
                        <td>${team.current_points}</td>
                        <td>${team.best_points}</td>
                        <td>${team.worst_points}</td>
                        <td>${team.range}</td>
                        <td>vs ${team.fixtures.opponent1} (${team.fixtures.home1 ? 'H' : 'A'}), ${team.fixtures.opponent2} (${team.fixtures.home2 ? 'H' : 'A'})</td>
                    </tr>
                `;
                
                // Mobile card version
                html += `
                    <div class="mobile-card ${rowClass}">
                        <h4>${team.team_name} (#${team.fifa_rank} FIFA / #${team.uefa_rank} UEFA)</h4>
                        <p><strong>Points:</strong> ${team.current_points} → ${team.best_points} / ${team.worst_points} (Range: ${team.range})</p>
                        <p><strong>Fixtures:</strong> vs ${team.fixtures.opponent1} (${team.fixtures.home1 ? 'H' : 'A'}), vs ${team.fixtures.opponent2} (${team.fixtures.home2 ? 'H' : 'A'})</p>
                    </div>
                `;
            });
            
            html += `
                    </tbody>
                </table>
            `;
            
            document.getElementById('results').innerHTML = html;
        }
        
        function displayFixtures(fixtures) {
            let html = `
                <h2>📅 All UEFA Fixtures (${fixtures.length} matches)</h2>
                <table class="teams-table">
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Match</th>
                            <th>Competition</th>
                            <th>Importance</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
            `;
            
            fixtures.sort((a, b) => new Date(a.date) - new Date(b.date));
            
            fixtures.forEach(fixture => {
                const hasResult = fixture.result && fixture.result.home_goals !== undefined;
                const status = hasResult ? 
                    `${fixture.result.home_goals}-${fixture.result.away_goals}` : 
                    'Scheduled';
                
                html += `
                    <tr>
                        <td>${fixture.date}</td>
                        <td>${fixture.home_team} vs ${fixture.away_team}</td>
                        <td>${fixture.competition}</td>
                        <td>×${fixture.importance}</td>
                        <td>${status}</td>
                    </tr>
                `;
            });
            
            html += `
                    </tbody>
                </table>
            `;
            
            document.getElementById('results').innerHTML = html;
        }
    </script>
</body>
</html>'''
    
    with open(os.path.join(templates_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)

def main():
    """Run the web server"""
    print("🌐 Starting FIFA Ranking Analyzer Web Server")
    print("=" * 50)
    
    # Create templates
    create_templates()
    print("✅ Templates created")
    
    # Get network info
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print(f"🖥️  Local access: http://localhost:5000")
    print(f"📱 Mobile access: http://{local_ip}:5000")
    print(f"🌍 Network access: http://{hostname}:5000")
    print("\n💡 Make sure your mobile is on the same WiFi network!")
    print("⚠️  For internet access, you'll need port forwarding or a service like ngrok")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    main()