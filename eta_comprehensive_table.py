#!/usr/bin/env python3
"""
Complete ETA Analysis Table - Scotland International Players
Comprehensive table showing total career caps/goals alongside ETA period contributions
Sorted by total caps descending, then total goals descending
"""

def get_all_eta_analysis_data():
    """Get complete dataset combining post-ETA and spanning players"""
    
    # Post-ETA only players (career started after Nov 5, 1995)
    post_eta_players = [
        {'name': 'Darren Fletcher', 'total_caps': 80, 'total_goals': 5, 'eta_caps': 80, 'eta_goals': 5, 'category': 'Post-ETA'},
        {'name': 'Scott Brown', 'total_caps': 62, 'total_goals': 4, 'eta_caps': 62, 'eta_goals': 4, 'category': 'Post-ETA'},
        {'name': 'Kenny Miller', 'total_caps': 69, 'total_goals': 18, 'eta_caps': 69, 'eta_goals': 18, 'category': 'Post-ETA'},
        {'name': 'James McFadden', 'total_caps': 48, 'total_goals': 15, 'eta_caps': 48, 'eta_goals': 15, 'category': 'Post-ETA'},
        {'name': 'Barry Ferguson', 'total_caps': 45, 'total_goals': 8, 'eta_caps': 45, 'eta_goals': 8, 'category': 'Post-ETA'},
        {'name': 'Russell Anderson', 'total_caps': 11, 'total_goals': 1, 'eta_caps': 11, 'eta_goals': 1, 'category': 'Post-ETA'},
        {'name': 'Gary Naysmith', 'total_caps': 46, 'total_goals': 0, 'eta_caps': 46, 'eta_goals': 0, 'category': 'Post-ETA'},
        {'name': 'Neil McCann', 'total_caps': 26, 'total_goals': 2, 'eta_caps': 26, 'eta_goals': 2, 'category': 'Post-ETA'},
        {'name': 'Christian Dailly', 'total_caps': 67, 'total_goals': 6, 'eta_caps': 67, 'eta_goals': 6, 'category': 'Post-ETA'},
        {'name': 'Paul Lambert', 'total_caps': 40, 'total_goals': 1, 'eta_caps': 40, 'eta_goals': 1, 'category': 'Post-ETA'},
        {'name': 'Don Hutchison', 'total_caps': 26, 'total_goals': 7, 'eta_caps': 26, 'eta_goals': 7, 'category': 'Post-ETA'},
        {'name': 'Shaun Maloney', 'total_caps': 47, 'total_goals': 7, 'eta_caps': 47, 'eta_goals': 7, 'category': 'Post-ETA'},
        {'name': 'Lee McCulloch', 'total_caps': 18, 'total_goals': 3, 'eta_caps': 18, 'eta_goals': 3, 'category': 'Post-ETA'},
        {'name': 'Craig Gordon', 'total_caps': 81, 'total_goals': 0, 'eta_caps': 81, 'eta_goals': 0, 'category': 'Post-ETA'},
        {'name': 'Steven Pressley', 'total_caps': 32, 'total_goals': 1, 'eta_caps': 32, 'eta_goals': 1, 'category': 'Post-ETA'},
        {'name': 'Scott McTominay', 'total_caps': 55, 'total_goals': 9, 'eta_caps': 55, 'eta_goals': 9, 'category': 'Post-ETA'},
        {'name': 'Andy Robertson', 'total_caps': 88, 'total_goals': 3, 'eta_caps': 88, 'eta_goals': 3, 'category': 'Post-ETA'},
        {'name': 'John McGinn', 'total_caps': 81, 'total_goals': 17, 'eta_caps': 81, 'eta_goals': 17, 'category': 'Post-ETA'},
        {'name': 'Kieran Tierney', 'total_caps': 45, 'total_goals': 1, 'eta_caps': 45, 'eta_goals': 1, 'category': 'Post-ETA'},
        {'name': 'Callum McGregor', 'total_caps': 70, 'total_goals': 12, 'eta_caps': 70, 'eta_goals': 12, 'category': 'Post-ETA'},
        {'name': 'Ryan Fraser', 'total_caps': 25, 'total_goals': 1, 'eta_caps': 25, 'eta_goals': 1, 'category': 'Post-ETA'},
        {'name': 'Stuart Armstrong', 'total_caps': 35, 'total_goals': 3, 'eta_caps': 35, 'eta_goals': 3, 'category': 'Post-ETA'},
        {'name': 'Lyndon Dykes', 'total_caps': 35, 'total_goals': 8, 'eta_caps': 35, 'eta_goals': 8, 'category': 'Post-ETA'},
        {'name': 'Che Adams', 'total_caps': 30, 'total_goals': 5, 'eta_caps': 30, 'eta_goals': 5, 'category': 'Post-ETA'},
        {'name': 'Grant Hanley', 'total_caps': 45, 'total_goals': 2, 'eta_caps': 45, 'eta_goals': 2, 'category': 'Post-ETA'},
        {'name': 'David Marshall', 'total_caps': 47, 'total_goals': 0, 'eta_caps': 47, 'eta_goals': 0, 'category': 'Post-ETA'},
        {'name': 'Steven Fletcher', 'total_caps': 33, 'total_goals': 5, 'eta_caps': 33, 'eta_goals': 5, 'category': 'Post-ETA'},
        {'name': 'Robert Snodgrass', 'total_caps': 28, 'total_goals': 7, 'eta_caps': 28, 'eta_goals': 7, 'category': 'Post-ETA'},
        {'name': 'Ikechi Anya', 'total_caps': 24, 'total_goals': 2, 'eta_caps': 24, 'eta_goals': 2, 'category': 'Post-ETA'},
        {'name': 'Matt Ritchie', 'total_caps': 16, 'total_goals': 1, 'eta_caps': 16, 'eta_goals': 1, 'category': 'Post-ETA'},
        {'name': 'Oliver Burke', 'total_caps': 15, 'total_goals': 1, 'eta_caps': 15, 'eta_goals': 1, 'category': 'Post-ETA'},
    ]
    
    # Spanning players (career spanned Nov 5, 1995) with manually researched ETA contributions
    spanning_players = [
        {'name': 'Kenny Dalglish', 'total_caps': 102, 'total_goals': 30, 'eta_caps': 1, 'eta_goals': 0, 'category': 'Spanning'},
        {'name': 'Jim Leighton', 'total_caps': 91, 'total_goals': 0, 'eta_caps': 21, 'eta_goals': 0, 'category': 'Spanning'},
        {'name': 'Tom Boyd', 'total_caps': 72, 'total_goals': 1, 'eta_caps': 42, 'eta_goals': 1, 'category': 'Spanning'},
        {'name': 'Ally McCoist', 'total_caps': 61, 'total_goals': 19, 'eta_caps': 13, 'eta_goals': 2, 'category': 'Spanning'},
        {'name': 'John Collins', 'total_caps': 58, 'total_goals': 12, 'eta_caps': 30, 'eta_goals': 4, 'category': 'Spanning'},
        {'name': 'Gary McAllister', 'total_caps': 57, 'total_goals': 5, 'eta_caps': 21, 'eta_goals': 1, 'category': 'Spanning'},
        {'name': 'Kevin Gallacher', 'total_caps': 53, 'total_goals': 9, 'eta_caps': 26, 'eta_goals': 7, 'category': 'Spanning'},
        {'name': 'Colin Hendry', 'total_caps': 51, 'total_goals': 3, 'eta_caps': 38, 'eta_goals': 2, 'category': 'Spanning'},
        {'name': 'Craig Burley', 'total_caps': 46, 'total_goals': 3, 'eta_caps': 41, 'eta_goals': 3, 'category': 'Spanning'},
        {'name': 'Gordon Durie', 'total_caps': 43, 'total_goals': 15, 'eta_caps': 17, 'eta_goals': 7, 'category': 'Spanning'},
        {'name': 'Andy Goram', 'total_caps': 43, 'total_goals': 0, 'eta_caps': 9, 'eta_goals': 0, 'category': 'Spanning'},
        {'name': 'Stuart McCall', 'total_caps': 40, 'total_goals': 1, 'eta_caps': 9, 'eta_goals': 0, 'category': 'Spanning'},
        {'name': 'Stewart McKimmie', 'total_caps': 40, 'total_goals': 1, 'eta_caps': 4, 'eta_goals': 0, 'category': 'Spanning'},
        {'name': 'Colin Calderwood', 'total_caps': 36, 'total_goals': 1, 'eta_caps': 28, 'eta_goals': 0, 'category': 'Spanning'},
        {'name': 'Billy McKinlay', 'total_caps': 29, 'total_goals': 4, 'eta_caps': 15, 'eta_goals': 0, 'category': 'Spanning'},
        {'name': 'Pat Nevin', 'total_caps': 28, 'total_goals': 5, 'eta_caps': 2, 'eta_goals': 1, 'category': 'Spanning'},
        {'name': 'Darren Jackson', 'total_caps': 28, 'total_goals': 4, 'eta_caps': 20, 'eta_goals': 4, 'category': 'Spanning'},
        {'name': 'Scot Gemmill', 'total_caps': 26, 'total_goals': 1, 'eta_caps': 23, 'eta_goals': 1, 'category': 'Spanning'},
        {'name': 'Alan McLaren', 'total_caps': 24, 'total_goals': 0, 'eta_caps': 1, 'eta_goals': 0, 'category': 'Spanning'},
        {'name': 'Scott Booth', 'total_caps': 22, 'total_goals': 6, 'eta_caps': 13, 'eta_goals': 2, 'category': 'Spanning'},
        {'name': 'Eoin Jess', 'total_caps': 18, 'total_goals': 2, 'eta_caps': 9, 'eta_goals': 2, 'category': 'Spanning'},
        {'name': 'John McGinlay', 'total_caps': 13, 'total_goals': 4, 'eta_caps': 4, 'eta_goals': 1, 'category': 'Spanning'},
        {'name': 'Duncan Shearer', 'total_caps': 7, 'total_goals': 1, 'eta_caps': 7, 'eta_goals': 1, 'category': 'Spanning'},
    ]
    
    # Combine all players
    all_players = post_eta_players + spanning_players
    
    return all_players

def create_comprehensive_table():
    """Create comprehensive table sorted by total caps, then goals"""
    
    print("=" * 130)
    print("🏴󠁧󠁢󠁳󠁣󠁴󠁿 SCOTLAND INTERNATIONAL PLAYERS - COMPLETE ETA ANALYSIS TABLE")
    print("Sorted by Total Career Caps (Descending), then Total Career Goals (Descending)")
    print("=" * 130)
    
    # Get all data
    all_players = get_all_eta_analysis_data()
    
    # Sort by total caps (descending), then by total goals (descending)
    sorted_players = sorted(all_players, key=lambda x: (-x['total_caps'], -x['total_goals']))
    
    # Table header
    print(f"{'Rank':<4} {'Player Name':<25} {'Total':<11} {'ETA Period':<13} {'ETA %':<8} {'Category':<9}")
    print(f"{'':>4} {'':>25} {'Caps|Goals':<11} {'Caps|Goals':<13} {'Caps':<8} {'':>9}")
    print("-" * 130)
    
    # Display all players
    for i, player in enumerate(sorted_players, 1):
        total_caps_goals = f"{player['total_caps']}|{player['total_goals']}"
        eta_caps_goals = f"{player['eta_caps']}|{player['eta_goals']}"
        eta_percentage = (player['eta_caps'] / player['total_caps'] * 100) if player['total_caps'] > 0 else 0
        
        print(f"{i:<4} {player['name']:<25} {total_caps_goals:<11} {eta_caps_goals:<13} {eta_percentage:.1f}%{'':<3} {player['category']:<9}")
    
    # Summary statistics
    print("\n" + "=" * 130)
    print("📊 SUMMARY STATISTICS")
    print("=" * 130)
    
    post_eta = [p for p in sorted_players if p['category'] == 'Post-ETA']
    spanning = [p for p in sorted_players if p['category'] == 'Spanning']
    
    total_career_caps = sum(p['total_caps'] for p in sorted_players)
    total_career_goals = sum(p['total_goals'] for p in sorted_players)
    total_eta_caps = sum(p['eta_caps'] for p in sorted_players)
    total_eta_goals = sum(p['eta_goals'] for p in sorted_players)
    
    print(f"Total Players Analyzed: {len(sorted_players)}")
    print(f"  - Post-ETA Only: {len(post_eta)} players")
    print(f"  - Spanning Players: {len(spanning)} players")
    print()
    print(f"CAREER TOTALS:")
    print(f"  Total Career Caps: {total_career_caps:,}")
    print(f"  Total Career Goals: {total_career_goals}")
    print()
    print(f"ETA PERIOD TOTALS:")
    print(f"  Total ETA Caps: {total_eta_caps:,}")
    print(f"  Total ETA Goals: {total_eta_goals}")
    print(f"  ETA as % of Career: {(total_eta_caps/total_career_caps)*100:.1f}% caps, {(total_eta_goals/total_career_goals)*100:.1f}% goals")
    print()
    
    # Top performers summary
    most_caps = sorted_players[0]
    most_goals = max(sorted_players, key=lambda x: x['total_goals'])
    most_eta_caps = max(sorted_players, key=lambda x: x['eta_caps'])
    most_eta_goals = max(sorted_players, key=lambda x: x['eta_goals'])
    
    print(f"TOP PERFORMERS:")
    print(f"  Most Career Caps: {most_caps['name']} ({most_caps['total_caps']} caps)")
    print(f"  Most Career Goals: {most_goals['name']} ({most_goals['total_goals']} goals)")
    print(f"  Most ETA Caps: {most_eta_caps['name']} ({most_eta_caps['eta_caps']} caps)")
    print(f"  Most ETA Goals: {most_eta_goals['name']} ({most_eta_goals['eta_goals']} goals)")

def main():
    """Main execution function"""
    print("🏴󠁧󠁢󠁳󠁣󠁴󠁿 SCOTLAND ETA COMPREHENSIVE TABLE GENERATOR")
    print("Complete analysis of career vs ETA period performance\n")
    
    create_comprehensive_table()

if __name__ == "__main__":
    main()