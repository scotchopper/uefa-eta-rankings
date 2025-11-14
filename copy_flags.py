#!/usr/bin/env python3
"""
Utility script to copy key flag images from the country-flags directory
to the local project for use in charts.
"""

import os
import shutil

# Source directory (adjust if needed)
FLAGS_SOURCE = r"C:\Users\david\OneDrive\Documents\git\country-flags\svg"
PNG_SOURCE = r"C:\Users\david\OneDrive\Documents\git\country-flags\png250px"

# Local flags directory
LOCAL_FLAGS_DIR = "flags"

# Key countries from ETA data
KEY_FLAGS = [
    'lt',  # Lithuania
    'cz',  # Czechia  
    'dk',  # Denmark
    'fo',  # Faroe Islands
    'nl',  # Netherlands
    'no',  # Norway
    'gb-eng',  # England
    'at',  # Austria
    'hr',  # Croatia
    'il',  # Israel
    'be',  # Belgium
    'ie',  # Republic of Ireland
    'pl',  # Poland
    'fr',  # France
    'gb-wls',  # Wales
    'de',  # Germany
    'es',  # Spain
    'it',  # Italy
    'pt',  # Portugal
    'ch',  # Switzerland
]

def copy_flag_files():
    """Copy flag files to local directory."""
    print("🏳️  Copying flag files for ETA charts...")
    
    # Create local flags directory
    if not os.path.exists(LOCAL_FLAGS_DIR):
        os.makedirs(LOCAL_FLAGS_DIR)
        print(f"   📁 Created directory: {LOCAL_FLAGS_DIR}")
    
    copied_count = 0
    
    for flag_code in KEY_FLAGS:
        # Try PNG first, then SVG
        png_file = f"{flag_code}.png"
        svg_file = f"{flag_code}.svg"
        
        png_source = os.path.join(PNG_SOURCE, png_file)
        svg_source = os.path.join(FLAGS_SOURCE, svg_file)
        
        destination_png = os.path.join(LOCAL_FLAGS_DIR, png_file)
        destination_svg = os.path.join(LOCAL_FLAGS_DIR, svg_file)
        
        try:
            if os.path.exists(png_source):
                shutil.copy2(png_source, destination_png)
                print(f"   ✅ Copied PNG: {png_file}")
                copied_count += 1
            elif os.path.exists(svg_source):
                shutil.copy2(svg_source, destination_svg)
                print(f"   ✅ Copied SVG: {svg_file}")
                copied_count += 1
            else:
                print(f"   ⚠️  Not found: {flag_code}")
        except Exception as e:
            print(f"   ❌ Error copying {flag_code}: {e}")
    
    print(f"\n🎉 Copied {copied_count} flag files to {LOCAL_FLAGS_DIR}/")
    print(f"💡 You can now update create_eta_charts.py to use FLAGS_DIR = '{LOCAL_FLAGS_DIR}'")

if __name__ == "__main__":
    copy_flag_files()