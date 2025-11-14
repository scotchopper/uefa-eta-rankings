import pandas as pd
import re
import sys
import os

# Add the src directory to the path so we can import our existing module
sys.path.append(os.path.join(os.getcwd(), 'src'))

from eta.eta_statistics import ScotlandFootballAnalyzer

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

def validate_hampden_goalscorer_data():
    """
    Validate that goalscorer parsing matches the Scot column for all Hampden matches
    """
    # Read the ETA30th data
    df = pd.read_excel('scot_games_eta_source.xlsx', sheet_name='ETA30th')
    
    # Filter for Hampden matches only
    hampden_matches = df[df['Venue'] == 'Hampden']
    
    print(f"Validating goalscorer data for {len(hampden_matches)} Hampden matches")
    print("=" * 70)
    
    total_matches = len(hampden_matches)
    perfect_matches = 0
    mismatches = []
    total_goals_scot_column = 0
    total_goals_parsed = 0
    all_scorers = []
    
    for idx, match in hampden_matches.iterrows():
        scot_goals = match['Scot']
        scorers_text = match['Scotland Scorers']
        date = match['Date']
        opponent = match['Opposition']
        
        total_goals_scot_column += scot_goals if pd.notna(scot_goals) else 0
        
        parsed_goals, match_scorers = parse_goalscorers_for_match(scorers_text)
        total_goals_parsed += parsed_goals
        all_scorers.extend(match_scorers)
        
        if parsed_goals == scot_goals:
            perfect_matches += 1
        else:
            mismatches.append({
                'date': date,
                'opponent': opponent,
                'scot_goals': scot_goals,
                'parsed_goals': parsed_goals,
                'scorers_text': scorers_text,
                'difference': scot_goals - parsed_goals
            })
    
    # Print validation results
    print(f"VALIDATION RESULTS:")
    print(f"Perfect matches: {perfect_matches}/{total_matches} ({perfect_matches/total_matches*100:.1f}%)")
    print(f"Mismatches: {len(mismatches)}")
    print()
    
    print(f"GOAL TOTALS:")
    print(f"Total goals from Scot column: {total_goals_scot_column}")
    print(f"Total goals from parsed scorers: {total_goals_parsed}")
    print(f"Difference: {total_goals_scot_column - total_goals_parsed}")
    print()
    
    # Analyze unique scorers
    unique_scorers = list(set(all_scorers))
    unique_scorers.sort()
    
    print(f"GOALSCORER ANALYSIS:")
    print(f"Total individual goals by named players: {len(all_scorers)}")
    print(f"Total different players who scored: {len(unique_scorers)}")
    print(f"Own goals by opponents: {total_goals_scot_column - len(all_scorers)}")
    print()
    
    # Show top scorers
    scorer_counts = {}
    for scorer in all_scorers:
        scorer_counts[scorer] = scorer_counts.get(scorer, 0) + 1
    
    top_scorers = sorted(scorer_counts.items(), key=lambda x: x[1], reverse=True)
    
    print("TOP 10 HAMPDEN GOALSCORERS:")
    for i, (scorer, count) in enumerate(top_scorers[:10], 1):
        print(f"{i:2d}. {scorer}: {count} goals")
    print()
    
    # Show mismatches if any
    if mismatches:
        print("DETAILED MISMATCHES:")
        print("-" * 70)
        for mismatch in mismatches:
            print(f"Date: {mismatch['date']}")
            print(f"Opponent: {mismatch['opponent']}")
            print(f"Scot column: {mismatch['scot_goals']} goals")
            print(f"Parsed from scorers: {mismatch['parsed_goals']} goals")
            print(f"Difference: {mismatch['difference']}")
            print(f"Scorers text: '{mismatch['scorers_text']}'")
            print("-" * 70)
    
    return {
        'total_goals': total_goals_scot_column,
        'parsed_goals': total_goals_parsed,
        'unique_scorers': len(unique_scorers),
        'individual_goals': len(all_scorers),
        'own_goals': total_goals_scot_column - len(all_scorers),
        'perfect_matches': perfect_matches,
        'total_matches': total_matches,
        'top_scorers': top_scorers[:10]
    }

if __name__ == "__main__":
    results = validate_hampden_goalscorer_data()