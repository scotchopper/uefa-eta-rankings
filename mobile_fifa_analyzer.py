#!/usr/bin/env python3
"""
Mobile-Friendly FIFA Analyzer - No Dependencies Required
Creates a standalone HTML file with embedded data
"""

import json
import os
from enhanced_team_range_analysis import EnhancedTeamRangeAnalyzer

def generate_mobile_report():
    """Generate a mobile-friendly HTML report"""
    print("📱 Generating mobile-friendly FIFA ranking report...")
    
    # Run the analysis
    analyzer = EnhancedTeamRangeAnalyzer()
    all_results = analyzer.analyze_all_teams()
    scotland_summary = analyzer.scotland_detailed_analysis(all_results)
    
    # Find Scotland data
    scotland_data = None
    for result in all_results:
        if result['team_name'] == 'Scotland':
            scotland_data = result
            break
    
    # Create HTML content
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FIFA Rankings - Mobile Report</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
        }}
        .header p {{
            margin: 5px 0 0 0;
            opacity: 0.9;
        }}
        .scotland-card {{
            background: linear-gradient(135deg, #005EB8 0%, #ffffff 100%);
            margin: 20px;
            padding: 20px;
            border-radius: 12px;
            border: 2px solid #005EB8;
            color: #005EB8;
        }}
        .scotland-card h2 {{
            margin: 0 0 15px 0;
            color: #005EB8;
        }}
        .stat-row {{
            display: flex;
            justify-content: space-between;
            margin: 8px 0;
            padding: 8px 0;
            border-bottom: 1px solid rgba(0,94,184,0.2);
        }}
        .stat-label {{
            font-weight: 600;
        }}
        .stat-value {{
            font-weight: bold;
        }}
        .positive {{ color: #27ae60; }}
        .negative {{ color: #e74c3c; }}
        .tabs {{
            display: flex;
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
        }}
        .tab {{
            flex: 1;
            padding: 15px;
            text-align: center;
            background: none;
            border: none;
            cursor: pointer;
            font-weight: 600;
            color: #6c757d;
        }}
        .tab.active {{
            background: white;
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
        }}
        .tab-content {{
            display: none;
            padding: 20px;
        }}
        .tab-content.active {{
            display: block;
        }}
        .team-card {{
            background: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #dee2e6;
        }}
        .team-card.scotland {{
            background: #e3f2fd;
            border-left-color: #005EB8;
        }}
        .team-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        .team-name {{
            font-weight: bold;
            font-size: 16px;
        }}
        .team-ranks {{
            font-size: 12px;
            color: #6c757d;
        }}
        .team-stats {{
            font-size: 14px;
            color: #495057;
        }}
        .fixture-info {{
            background: rgba(0,0,0,0.05);
            padding: 8px;
            border-radius: 6px;
            margin-top: 8px;
            font-size: 12px;
        }}
        .update-time {{
            text-align: center;
            padding: 10px;
            color: #6c757d;
            font-size: 12px;
            background: #f8f9fa;
        }}
        .summary-stats {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin: 15px 0;
        }}
        .summary-stat {{
            background: rgba(255,255,255,0.8);
            padding: 12px;
            border-radius: 8px;
            text-align: center;
        }}
        .summary-stat-value {{
            font-size: 20px;
            font-weight: bold;
            color: #005EB8;
        }}
        .summary-stat-label {{
            font-size: 12px;
            color: #666;
            margin-top: 4px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏆 FIFA Rankings</h1>
            <p>UEFA Teams Analysis - November 2025</p>
        </div>
        
        <div class="scotland-card">
            <h2>🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland Analysis</h2>
            
            <div class="summary-stats">
                <div class="summary-stat">
                    <div class="summary-stat-value">#{scotland_data['current_rank'] if scotland_data else 'N/A'}</div>
                    <div class="summary-stat-label">FIFA Rank</div>
                </div>
                <div class="summary-stat">
                    <div class="summary-stat-value">#{scotland_data.get('uefa_rank', 'N/A') if scotland_data else 'N/A'}</div>
                    <div class="summary-stat-label">UEFA Rank</div>
                </div>
            </div>
            
            <div class="stat-row">
                <span class="stat-label">Current Points:</span>
                <span class="stat-value">{scotland_data['initial_points']:.2f if scotland_data else 'N/A'}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">Best Case:</span>
                <span class="stat-value positive">{scotland_data['best_points']:.2f + ' (' + f"{scotland_data['best_change']:+.2f}" + ')' if scotland_data else 'N/A'}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">Worst Case:</span>
                <span class="stat-value negative">{scotland_data['worst_points']:.2f + ' (' + f"{scotland_data['worst_change']:+.2f}" + ')' if scotland_data else 'N/A'}</span>
            </div>
            <div class="stat-row">
                <span class="stat-label">Points Range:</span>
                <span class="stat-value">{scotland_data['range']:.2f if scotland_data else 'N/A'}</span>
            </div>
            
            {generate_fixtures_info(scotland_data) if scotland_data and 'fixture1_opponent' in scotland_data else ""}
            
            {generate_summary_info(scotland_summary) if scotland_summary else ""}
        </div>
        
        <div class="tabs">
            <button class="tab active" onclick="showTab(event, 'top20')">Top 20</button>
            <button class="tab" onclick="showTab(event, 'all')">All Teams</button>
        </div>
        
        <div id="top20" class="tab-content active">
            {generate_team_cards(all_results[:20])}
        </div>
        
        <div id="all" class="tab-content">
            {generate_team_cards(all_results)}
        </div>
        
        <div class="update-time">
            Last updated: {get_current_time()}<br>
            Data source: UEFA fixtures November 11-18, 2025
        </div>
    </div>

    <script>
        function showTab(evt, tabName) {{
            var i, tabcontent, tabs;
            
            tabcontent = document.getElementsByClassName("tab-content");
            for (i = 0; i < tabcontent.length; i++) {{
                tabcontent[i].classList.remove("active");
            }}
            
            tabs = document.getElementsByClassName("tab");
            for (i = 0; i < tabs.length; i++) {{
                tabs[i].classList.remove("active");
            }}
            
            document.getElementById(tabName).classList.add("active");
            evt.currentTarget.classList.add("active");
        }}
    </script>
</body>
</html>'''
    
    return html_content

def generate_fixtures_info(scotland_data):
    """Generate fixtures info HTML"""
    return f'''
            <div class="fixture-info">
                <strong>Fixtures:</strong><br>
                &bull; vs {scotland_data['fixture1_opponent']} ({'H' if scotland_data['fixture1_home'] else 'A'}) - {scotland_data['fixture1_competition']}<br>
                &bull; vs {scotland_data['fixture2_opponent']} ({'H' if scotland_data['fixture2_home'] else 'A'}) - {scotland_data['fixture2_competition']}
            </div>
            '''

def generate_summary_info(scotland_summary):
    """Generate summary info HTML"""
    return f'''
            <div style="margin-top: 15px;">
                <strong>Ranking Movement Potential:</strong><br>
                &bull; UEFA Rank: #{scotland_summary['best_uefa_rank']} to #{scotland_summary['worst_uefa_rank']}<br>
                &bull; Max gain: {scotland_summary['max_uefa_gain']} places up<br>
                &bull; Max loss: {scotland_summary['max_uefa_loss']} places down
            </div>
            '''

def generate_fixture_card_info(result):
    """Generate fixture info for team card"""
    return f'''
            <div class="fixture-info">
                vs {result['fixture1_opponent']} ({'H' if result['fixture1_home'] else 'A'}), 
                vs {result['fixture2_opponent']} ({'H' if result['fixture2_home'] else 'A'})
            </div>
            '''

def generate_team_cards(results):
    """Generate HTML for team cards"""
    cards_html = ""
    
    for result in results:
        if not result.get('valid_data', True):
            continue
        
        is_scotland = result['team_name'] == 'Scotland'
        card_class = 'team-card scotland' if is_scotland else 'team-card'
        
        best_change = result['best_change']
        worst_change = result['worst_change']
        
        best_class = 'positive' if best_change >= 0 else 'negative'
        worst_class = 'positive' if worst_change >= 0 else 'negative'
        
        cards_html += f'''
        <div class="{card_class}">
            <div class="team-header">
                <div class="team-name">{result['team_name']}</div>
                <div class="team-ranks">FIFA #{result['current_rank']} / UEFA #{result.get('uefa_rank', 'N/A')}</div>
            </div>
            <div class="team-stats">
                <strong>{result['initial_points']:.2f}</strong> → 
                <span class="{best_class}">{result['best_points']:.2f}</span> / 
                <span class="{worst_class}">{result['worst_points']:.2f}</span>
                (Range: {result['range']:.2f})
            </div>
            {generate_fixture_card_info(result) if 'fixture1_opponent' in result else ''}
        </div>
        '''
    
    return cards_html

def get_current_time():
    """Get current time as string"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def main():
    """Generate the mobile report"""
    print("📱 MOBILE FIFA ANALYZER")
    print("=" * 30)
    
    try:
        html_content = generate_mobile_report()
        
        # Save to file
        output_file = 'fifa_mobile_report.html'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Mobile report generated: {output_file}")
        print(f"📱 Open this file on your mobile browser")
        print(f"🔗 File path: {os.path.abspath(output_file)}")
        
        # Try to open in default browser
        try:
            import webbrowser
            webbrowser.open(f'file://{os.path.abspath(output_file)}')
            print("🌐 Opened in default browser")
        except:
            print("💡 Manually open the HTML file in your browser")
            
    except Exception as e:
        print(f"❌ Error generating report: {e}")

if __name__ == "__main__":
    main()