from src.eta.eta_statistics import ScotlandFootballAnalyzer

# Quick duplicate ch    print(f"Problematic surnames (no identifiers, careers 7+ years): {len(problematic)}")ck after manual updates
analyzer = ScotlandFootballAnalyzer('scot_games_eta_source.xlsx', 'Games')
analyzer.load_data()

print("🔍 DUPLICATE SURNAME CHECK (7+ YEAR GAPS)")
print("=" * 50)

# Check for duplicates with 7+ year gaps
duplicates_7yr = analyzer.identify_potential_duplicate_surnames(min_gap_years=7)
print(f"Players with 7+ year gaps: {len(duplicates_7yr)}")

# Check for duplicates with 20+ year gaps (more severe)
duplicates_20yr = analyzer.identify_potential_duplicate_surnames(min_gap_years=20)
print(f"Players with 20+ year gaps: {len(duplicates_20yr)}")

if len(duplicates_7yr) > 0:
    print(f"\nTop 10 players with largest gaps:")
    top_gaps = duplicates_7yr.nlargest(10, 'max_gap_years')
    for _, player in top_gaps.iterrows():
        print(f"• {player['player']}: {player['max_gap_years']:.1f} year gap, {player['total_goals']} goals")
        
    # Get filtered list (excluding those with identifiers or short careers)
    import pandas as pd
    all_names = duplicates_7yr['player'].tolist()
    problematic = []
    
    for name in all_names:
        # Check if has identifiers
        has_identifiers = (len(name.split()) > 1 or
                          any(char.isupper() and char != name[0] for char in name[1:]) or
                          any(char in name for char in ['(', ')', '.']) or
                          name in ['unknown'])
        
        # Get career span using EXACT matching (not substring)
        exact_matches = []
        for _, row in analyzer.df.iterrows():
            scorers_text = str(row.get('Scotland Scorers', ''))
            if scorers_text and not pd.isna(scorers_text):
                scorers_list = [s.strip() for s in scorers_text.split(',')]
                for scorer in scorers_list:
                    if scorer and scorer.lower() not in ['', 'nan']:
                        parsed_name = scorer
                        import re
                        if '(' in scorer and ')' in scorer:
                            match = re.search(r'(\s*\d+\s*)', scorer)
                            if match:
                                parsed_name = re.sub(r'\(\s*\d+\s*\)', '', scorer).strip()
                            else:
                                penalty_match = re.search(r'\(\s*p\s*\)', scorer, re.IGNORECASE)
                                if penalty_match:
                                    parsed_name = re.sub(r'\(\s*p\s*\)', '', scorer, flags=re.IGNORECASE).strip()
                                else:
                                    parsed_name = scorer.strip()
                        elif '[' in scorer and ']' in scorer:
                            parsed_name = scorer.strip()
                        else:
                            parts = scorer.split()
                            if len(parts) > 1 and parts[-1].isdigit():
                                parsed_name = ' '.join(parts[:-1])
                            else:
                                parsed_name = scorer.strip()
                        
                        if 'og' in parsed_name.lower():
                            parsed_name = parsed_name.replace('og', '').replace('OG', '').strip()
                            if parsed_name:
                                parsed_name += ' (og)'
                        
                        if parsed_name == name:
                            exact_matches.append(row['Date'])
        
        if exact_matches:
            dates = pd.to_datetime(exact_matches)
            career_span = (dates.max() - dates.min()).days / 365.25
        else:
            career_span = 0
            
        is_short_career = career_span < 7.0
        
        if not has_identifiers and not is_short_career:
            problematic.append(name)
    
    print(f"\nProblematic surnames (no identifiers, long careers): {len(problematic)}")
    if problematic:
        for surname in sorted(problematic):
            print(f"  • {surname}")
else:
    print("\n✅ NO DUPLICATE SURNAME ISSUES FOUND!")
    print("All manual updates appear to have resolved the problems!")