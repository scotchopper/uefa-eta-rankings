#!/usr/bin/env python3
"""
Quick Mobile Update - Fastest way to update rankings from mobile
"""

import json
import subprocess
import sys
from datetime import datetime

# Quick results format - just paste results here and run
MOBILE_RESULTS = """
# Paste your mobile results here in this format:
# GRE_SCO: Greece 2-1 Scotland
# SCO_DEN: Scotland 1-2 Denmark
# ESP_TUR: Spain 3-0 Türkiye

"""

def quick_update():
    """Quick update from hardcoded results above"""
    
    if "Greece 2-1 Scotland" in MOBILE_RESULTS:
        print("📝 Edit the MOBILE_RESULTS section above with your actual results")
        print("   Then run this script again")
        return
    
    # Parse results from the MOBILE_RESULTS string
    results = []
    lines = MOBILE_RESULTS.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#') and ':' in line:
            results.append(line)
    
    if not results:
        print("❌ No results found! Edit MOBILE_RESULTS section above")
        return
    
    print(f"🔄 Processing {len(results)} results...")
    
    # Process each result
    try:
        with open('uefa_fixtures_data.json', 'r') as f:
            data = json.load(f)
    except:
        print("❌ uefa_fixtures_data.json not found!")
        return
    
    for result_line in results:
        print(f"✅ {result_line}")
        # Add your processing logic here
    
    # Run analysis
    print("\n🔄 Running analysis...")
    subprocess.run([sys.executable, 'enhanced_team_range_analysis.py'])
    
    print("\n🎉 Update complete!")

if __name__ == "__main__":
    quick_update()