import pandas as pd
import re
import sys
import os

# Add the src directory to the path so we can import our existing module
sys.path.append(os.path.join(os.getcwd(), 'src'))

def parse_goalscorers_for_match(scorers_text):
    """
    Parse goalscorers text and return total goals count using the same logic as eta_statistics.py
    """
    if pd.isna(scorers_text) or scorers_text == '':
        return 0, []
    
    total_goals = 0
    scorer_names = []
    
    # Parse scorers (handle various formats like "Smith, Jones", "Smith 2", "Smith, og", etc.)
    scorers_text = str(scorers_text)
    
    # Split by comma and clean up
    scorers_list = [s.strip() for s in scorers_text.split(',')]
    
    for scorer in scorers_list:
        if scorer and scorer.lower() not in ['', 'nan']:
            # Handle cases like "Smith 2", "Smith(   2)", or "Smith(2)" (scored 2 goals)
            name = scorer
            goals = 1  # default
            
            # Check for parenthetical format first (handles both spaced and non-spaced)
            if '(' in scorer and ')' in scorer:
                # Extract number from parentheses
                match = re.search(r'\((\s*\d+\s*)\)', scorer)
                if match:
                    goals = int(match.group(1).strip())
                    # Remove the parenthetical part from the name
                    name = re.sub(r'\(\s*\d+\s*\)', '', scorer).strip()
                else:
                    # Check if it's a penalty notation that should be removed
                    penalty_match = re.search(r'\(\s*p\s*\)', scorer, re.IGNORECASE)
                    if penalty_match:
                        # Remove penalty notation but keep the name
                        name = re.sub(r'\(\s*p\s*\)', '', scorer, flags=re.IGNORECASE).strip() 
                    else:
                        # Keep the name as-is - it might contain player identifiers like initials
                        name = scorer.strip()
            # Also check for bracketed formats like "Hamilton J[I]"
            elif '[' in scorer and ']' in scorer:
                # Keep bracketed content as it likely contains player identifiers
                name = scorer.strip()
            else:
                # Check for space-separated format like "Player 2"
                parts = scorer.split()
                if len(parts) > 1 and parts[-1].isdigit():
                    name = ' '.join(parts[:-1])
                    goals = int(parts[-1])
                else:
                    # Keep the name as-is - this handles cases like "Gibson N", "Gibson J D", etc.
                    name = scorer.strip()
            
            if name:  # Only add if name is not empty
                total_goals += goals
                scorer_names.extend([name] * goals)
    
    return total_goals, scorer_names

def validate_all_games_goalscorer_data():
    """
    Validate that goalscorer parsing matches the Scot column for ALL matches in the Games sheet
    """
    # Read the Games sheet
    df = pd.read_excel('scot_games_eta_source.xlsx', sheet_name='Games')
    
    print(f"🏴󠁧󠁢󠁳󠁣󠁴󠁿 COMPREHENSIVE GOALSCORER VALIDATION - ALL SCOTLAND MATCHES")
    print(f"Validating goalscorer data for {len(df)} total matches in Games sheet")
    print("=" * 80)
    
    total_matches = len(df)
    perfect_matches = 0
    mismatches = []
    matches_with_no_scorers = 0
    matches_with_goals_but_no_scorers = 0
    total_goals_scot_column = 0
    total_goals_parsed = 0
    all_scorers = []
    
    # Track mismatches by type
    parsing_issues = []
    data_entry_errors = []
    
    for idx, match in df.iterrows():
        scot_goals = match['Scot']
        scorers_text = match['Scotland Scorers']
        date = match['Date']
        opponent = match['Opposition']
        venue = match['Venue']
        competition = match['Competition']
        
        # Handle NaN values
        if pd.isna(scot_goals):
            scot_goals = 0
        
        total_goals_scot_column += scot_goals
        
        parsed_goals, match_scorers = parse_goalscorers_for_match(scorers_text)
        total_goals_parsed += parsed_goals
        all_scorers.extend(match_scorers)
        
        # Check for matches with no scorer data
        if pd.isna(scorers_text) or scorers_text == '':
            matches_with_no_scorers += 1
            if scot_goals > 0:
                matches_with_goals_but_no_scorers += 1
        
        if parsed_goals == scot_goals:
            perfect_matches += 1
        else:
            mismatch_info = {
                'date': date,
                'opponent': opponent,
                'venue': venue,
                'competition': competition,
                'scot_goals': scot_goals,
                'parsed_goals': parsed_goals,
                'scorers_text': scorers_text,
                'difference': scot_goals - parsed_goals
            }
            mismatches.append(mismatch_info)
            
            # Categorize the type of mismatch
            if pd.isna(scorers_text) or scorers_text == '':
                if scot_goals > 0:
                    data_entry_errors.append(mismatch_info)
            else:
                parsing_issues.append(mismatch_info)
    
    # Print validation results
    print(f"📊 VALIDATION SUMMARY:")
    print(f"Perfect matches: {perfect_matches:,}/{total_matches:,} ({perfect_matches/total_matches*100:.1f}%)")
    print(f"Mismatches: {len(mismatches):,}")
    print(f"Matches with no scorer data: {matches_with_no_scorers:,}")
    print(f"Matches with goals but no scorers listed: {matches_with_goals_but_no_scorers:,}")
    print()
    
    print(f"⚽ GOAL TOTALS:")
    print(f"Total goals from Scot column: {total_goals_scot_column:,}")
    print(f"Total goals from parsed scorers: {total_goals_parsed:,}")
    print(f"Difference: {total_goals_scot_column - total_goals_parsed:,}")
    print()
    
    # Analyze unique scorers
    unique_scorers = list(set(all_scorers))
    unique_scorers.sort()
    
    print(f"🎯 GOALSCORER ANALYSIS:")
    print(f"Total individual goals by named players: {len(all_scorers):,}")
    print(f"Total different players who scored: {len(unique_scorers):,}")
    print(f"Own goals by opponents: {total_goals_scot_column - len(all_scorers):,}")
    print()
    
    # Show top scorers
    scorer_counts = {}
    for scorer in all_scorers:
        scorer_counts[scorer] = scorer_counts.get(scorer, 0) + 1
    
    top_scorers = sorted(scorer_counts.items(), key=lambda x: x[1], reverse=True)
    
    print("🏆 TOP 15 ALL-TIME SCOTLAND GOALSCORERS:")
    for i, (scorer, count) in enumerate(top_scorers[:15], 1):
        print(f"{i:2d}. {scorer}: {count} goals")
    print()
    
    # Show mismatch analysis
    if mismatches:
        print(f"🔍 MISMATCH ANALYSIS:")
        print(f"Parsing issues: {len(parsing_issues)}")
        print(f"Data entry errors (goals but no scorers): {len(data_entry_errors)}")
        print()
        
        if len(mismatches) <= 50:  # Only show detailed list if manageable
            print("📋 DETAILED MISMATCHES:")
            print("-" * 100)
            for i, mismatch in enumerate(mismatches, 1):
                print(f"{i:2d}. {mismatch['date']} vs {mismatch['opponent']} ({mismatch['venue']})")
                print(f"    {mismatch['competition']}")
                print(f"    Scot: {mismatch['scot_goals']} | Parsed: {mismatch['parsed_goals']} | Diff: {mismatch['difference']}")
                print(f"    Scorers: '{mismatch['scorers_text']}'")
                print("-" * 100)
        else:
            print(f"⚠️  Too many mismatches to display individually ({len(mismatches)})")
            print("   Consider reviewing the most common patterns:")
            
            # Show most common mismatch patterns
            mismatch_patterns = {}
            for mismatch in mismatches:
                pattern = f"Scot:{mismatch['scot_goals']} -> Parsed:{mismatch['parsed_goals']}"
                mismatch_patterns[pattern] = mismatch_patterns.get(pattern, 0) + 1
            
            print("\n   Most common mismatch patterns:")
            for pattern, count in sorted(mismatch_patterns.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"   {pattern}: {count} occurrences")
    
    return {
        'total_goals': total_goals_scot_column,
        'parsed_goals': total_goals_parsed,
        'unique_scorers': len(unique_scorers),
        'individual_goals': len(all_scorers),
        'own_goals': total_goals_scot_column - len(all_scorers),
        'perfect_matches': perfect_matches,
        'total_matches': total_matches,
        'top_scorers': top_scorers[:15],
        'mismatches': len(mismatches),
        'data_entry_errors': len(data_entry_errors),
        'parsing_issues': len(parsing_issues)
    }

if __name__ == "__main__":
    print("Starting comprehensive goalscorer validation...")
    results = validate_all_games_goalscorer_data()
    print(f"\n🎉 Validation complete!")
    print(f"📈 Data quality: {results['perfect_matches']}/{results['total_matches']} ({results['perfect_matches']/results['total_matches']*100:.1f}%) perfect matches")