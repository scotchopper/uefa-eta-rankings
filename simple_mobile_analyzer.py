#!/usr/bin/env python3
"""
Simple Mobile FIFA Analyzer - Basic HTML Generation
"""

import json
import os
from enhanced_team_range_analysis import EnhancedTeamRangeAnalyzer
from datetime import datetime

def main():
    """Generate a simple mobile-friendly HTML report"""
    print("📱 GENERATING SIMPLE MOBILE REPORT")
    print("=" * 40)
    
    try:
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
        
        # Create simple HTML
        html = create_simple_html(scotland_data, scotland_summary, all_results)
        
        # Save to file
        output_file = 'fifa_mobile_simple.html'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Mobile report generated: {output_file}")
        print(f"📱 File size: {os.path.getsize(output_file) / 1024:.1f}KB")
        
        # Show access options
        print(f"\n🌐 ACCESS OPTIONS:")
        print(f"1. Local file: file://{os.path.abspath(output_file)}")
        print(f"2. Copy file to mobile device")
        print(f"3. Upload to cloud storage (Google Drive, Dropbox)")
        print(f"4. Email as attachment")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_simple_html(scotland_data, scotland_summary, all_results):
    """Create simple HTML without complex formatting"""
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Scotland section
    scotland_html = ""
    if scotland_data:
        scotland_html = f"""
        <div class="scotland-section">
            <h2>🏴󠁧󠁢󠁳󠁣󠁴󠁿 Scotland Analysis</h2>
            <div class="stats">
                <p><strong>Current:</strong> FIFA #{scotland_data['current_rank']} / UEFA #{scotland_data.get('uefa_rank', 'N/A')}</p>
                <p><strong>Points:</strong> {scotland_data['initial_points']:.2f}</p>
                <p><strong>Best Case:</strong> {scotland_data['best_points']:.2f} ({scotland_data['best_change']:+.2f})</p>
                <p><strong>Worst Case:</strong> {scotland_data['worst_points']:.2f} ({scotland_data['worst_change']:+.2f})</p>
                <p><strong>Range:</strong> {scotland_data['range']:.2f} points</p>
            </div>
        """
        
        if 'fixture1_opponent' in scotland_data:
            scotland_html += f"""
            <div class="fixtures">
                <h3>Fixtures:</h3>
                <p>• vs {scotland_data['fixture1_opponent']} ({'Home' if scotland_data['fixture1_home'] else 'Away'})</p>
                <p>• vs {scotland_data['fixture2_opponent']} ({'Home' if scotland_data['fixture2_home'] else 'Away'})</p>
            </div>
            """
        
        if scotland_summary:
            scotland_html += f"""
            <div class="movement">
                <h3>Potential Movement:</h3>
                <p><strong>UEFA Rank:</strong> #{scotland_summary['best_uefa_rank']} to #{scotland_summary['worst_uefa_rank']}</p>
                <p><strong>Max Gain:</strong> {scotland_summary['max_uefa_gain']} places up</p>
                <p><strong>Max Loss:</strong> {scotland_summary['max_uefa_loss']} places down</p>
            </div>
            """
        
        scotland_html += "</div>"
    
    # Teams table
    teams_html = "<div class='teams-section'><h2>📊 All UEFA Teams</h2>"
    
    for i, result in enumerate(all_results[:20]):  # Top 20 for mobile
        if not result.get('valid_data', True):
            continue
        
        is_scotland = result['team_name'] == 'Scotland'
        class_name = 'team-card scotland' if is_scotland else 'team-card'
        
        teams_html += f"""
        <div class="{class_name}">
            <div class="team-header">
                <span class="team-name">{result['team_name']}</span>
                <span class="ranks">#{result['current_rank']} FIFA / #{result.get('uefa_rank', 'N/A')} UEFA</span>
            </div>
            <div class="team-stats">
                <strong>{result['initial_points']:.2f}</strong> → 
                {result['best_points']:.2f} / {result['worst_points']:.2f}
                (Range: {result['range']:.2f})
            </div>
        </div>
        """
    
    teams_html += f"<p style='text-align: center; color: #666; margin-top: 20px;'>Showing top 20 of {len(all_results)} teams</p></div>"
    
    # Complete HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FIFA Rankings Mobile</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 15px;
            background: #f5f5f5;
            color: #333;
        }}
        .header {{
            background: linear-gradient(135deg, #2c3e50, #3498db);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 20px;
        }}
        .scotland-section {{
            background: #e3f2fd;
            border: 2px solid #005EB8;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        .scotland-section h2 {{
            color: #005EB8;
            margin-top: 0;
        }}
        .stats p, .fixtures p, .movement p {{
            margin: 8px 0;
            line-height: 1.4;
        }}
        .team-card {{
            background: white;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #ddd;
        }}
        .team-card.scotland {{
            background: #e3f2fd;
            border-left-color: #005EB8;
        }}
        .team-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }}
        .team-name {{
            font-weight: bold;
            font-size: 16px;
        }}
        .ranks {{
            font-size: 12px;
            color: #666;
        }}
        .team-stats {{
            color: #555;
            font-size: 14px;
        }}
        .footer {{
            text-align: center;
            color: #666;
            font-size: 12px;
            margin-top: 30px;
            padding: 15px;
            background: white;
            border-radius: 8px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🏆 FIFA Rankings</h1>
        <p>UEFA Teams Analysis - November 2025</p>
    </div>
    
    {scotland_html}
    {teams_html}
    
    <div class="footer">
        Generated: {current_time}<br>
        Data: UEFA fixtures November 11-18, 2025<br>
        <small>Best/worst case analysis based on FIFA Elo system</small>
    </div>
</body>
</html>"""
    
    return html

if __name__ == "__main__":
    main()