#!/usr/bin/env python3
"""
FIFA Men's World Ranking Calculator
Automatic calculation system based on the current FIFA methodology (2018+)
Using the Elo rating system formula as described in Wikipedia
"""

import math
import json
import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class MatchResult(Enum):
    """Match result values as per FIFA formula"""
    LOSS = 0.0
    DRAW_OR_PENALTY_LOSS = 0.5
    PENALTY_WIN = 0.75
    WIN = 1.0

class CompetitionType(Enum):
    """Competition importance coefficients (I values)"""
    FRIENDLY_OUTSIDE_WINDOW = 5
    FRIENDLY_INSIDE_WINDOW = 10
    NATIONS_LEAGUE_GROUP = 15
    NATIONS_LEAGUE_FINALS = 25
    CONFEDERATION_QUALIFIERS = 25
    WORLD_CUP_QUALIFIERS = 25
    CONFEDERATION_FINALS_EARLY = 35
    CONFEDERATION_FINALS_LATE = 40
    WORLD_CUP_EARLY = 50
    WORLD_CUP_LATE = 60

@dataclass
class Match:
    """Represents a FIFA-recognized international match"""
    date: datetime.date
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    competition: CompetitionType
    penalty_winner: Optional[str] = None  # Team name if decided by penalties
    is_knockout: bool = False  # True if knockout stage where negative points don't apply

@dataclass
class Team:
    """Represents a national team with FIFA ranking data"""
    name: str
    fifa_code: str
    points: float
    confederation: str
    
    def __post_init__(self):
        self.points = round(self.points, 2)

class FIFARankingCalculator:
    """FIFA Men's World Ranking Calculator using current Elo-based system"""
    
    def __init__(self):
        self.teams: Dict[str, Team] = {}
        self.matches: List[Match] = []
        self.scale_constant = 600  # c = 600 in the FIFA formula
        
    def add_team(self, name: str, fifa_code: str, initial_points: float, confederation: str):
        """Add a team to the ranking system"""
        self.teams[name] = Team(name, fifa_code, initial_points, confederation)
    
    def add_match(self, match: Match):
        """Add a match to be processed"""
        self.matches.append(match)
    
    def calculate_expected_result(self, team_a_points: float, team_b_points: float) -> float:
        """
        Calculate expected result (We) for team A against team B
        Formula: We = 1 / (10^(-Δ/c) + 1)
        where Δ = team_a_points - team_b_points, c = 600
        """
        delta = team_a_points - team_b_points
        expected = 1 / (10**(-delta / self.scale_constant) + 1)
        return expected
    
    def get_match_result_value(self, match: Match, team_name: str) -> float:
        """
        Get the W value for a specific team in a match
        Returns: 0, 0.5, 0.75, or 1.0 based on match outcome
        """
        if match.home_team == team_name:
            # Team is home
            if match.home_score > match.away_score:
                return MatchResult.WIN.value
            elif match.home_score < match.away_score:
                return MatchResult.LOSS.value
            else:
                # Draw - check for penalties
                if match.penalty_winner == team_name:
                    return MatchResult.PENALTY_WIN.value
                elif match.penalty_winner is not None:
                    return MatchResult.DRAW_OR_PENALTY_LOSS.value
                else:
                    return MatchResult.DRAW_OR_PENALTY_LOSS.value
        else:
            # Team is away
            if match.away_score > match.home_score:
                return MatchResult.WIN.value
            elif match.away_score < match.home_score:
                return MatchResult.LOSS.value
            else:
                # Draw - check for penalties
                if match.penalty_winner == team_name:
                    return MatchResult.PENALTY_WIN.value
                elif match.penalty_winner is not None:
                    return MatchResult.DRAW_OR_PENALTY_LOSS.value
                else:
                    return MatchResult.DRAW_OR_PENALTY_LOSS.value
    
    def process_match(self, match: Match):
        """
        Process a single match and update team rankings
        FIFA Formula: P = P_before + I(W - We)
        """
        if match.home_team not in self.teams or match.away_team not in self.teams:
            print(f"Warning: Teams {match.home_team} or {match.away_team} not found in system")
            return
        
        home_team = self.teams[match.home_team]
        away_team = self.teams[match.away_team]
        
        # Get points before the match
        home_points_before = home_team.points
        away_points_before = away_team.points
        
        # Calculate expected results
        home_expected = self.calculate_expected_result(home_points_before, away_points_before)
        away_expected = 1 - home_expected  # Expected results must sum to 1
        
        # Get actual results
        home_result = self.get_match_result_value(match, match.home_team)
        away_result = self.get_match_result_value(match, match.away_team)
        
        # Calculate importance coefficient
        importance = match.competition.value
        
        # Calculate point changes
        home_change = importance * (home_result - home_expected)
        away_change = importance * (away_result - away_expected)
        
        # Apply knockout rule (negative points don't affect teams in knockout stages)
        if match.is_knockout:
            if home_change < 0:
                home_change = 0
            if away_change < 0:
                away_change = 0
        
        # Update team points
        home_team.points = round(home_points_before + home_change, 2)
        away_team.points = round(away_points_before + away_change, 2)
        
        print(f"Match: {match.home_team} {match.home_score}-{match.away_score} {match.away_team}")
        print(f"  {match.home_team}: {home_points_before:.2f} → {home_team.points:.2f} ({home_change:+.2f})")
        print(f"  {match.away_team}: {away_points_before:.2f} → {away_team.points:.2f} ({away_change:+.2f})")
        print()
    
    def process_all_matches(self):
        """Process all matches in chronological order"""
        # Sort matches by date
        self.matches.sort(key=lambda m: m.date)
        
        print("=" * 80)
        print("FIFA WORLD RANKING CALCULATOR - PROCESSING MATCHES")
        print("=" * 80)
        
        for match in self.matches:
            self.process_match(match)
    
    def get_rankings(self) -> List[Team]:
        """Get current rankings sorted by points (descending)"""
        return sorted(self.teams.values(), key=lambda t: t.points, reverse=True)
    
    def display_rankings(self, top_n: Optional[int] = None):
        """Display current FIFA rankings"""
        rankings = self.get_rankings()
        
        if top_n:
            rankings = rankings[:top_n]
        
        print("=" * 80)
        print("FIFA MEN'S WORLD RANKING - CURRENT STANDINGS")
        print("=" * 80)
        print(f"{'Rank':<4} {'Team':<25} {'Points':<10} {'FIFA Code':<10} {'Confederation'}")
        print("-" * 80)
        
        for i, team in enumerate(rankings, 1):
            print(f"{i:<4} {team.name:<25} {team.points:<10.2f} {team.fifa_code:<10} {team.confederation}")
    
    def save_rankings_json(self, filename: str):
        """Save current rankings to JSON file"""
        rankings = self.get_rankings()
        data = {
            "calculation_date": datetime.date.today().isoformat(),
            "total_teams": len(rankings),
            "rankings": [
                {
                    "rank": i + 1,
                    "team": team.name,
                    "fifa_code": team.fifa_code,
                    "points": team.points,
                    "confederation": team.confederation
                }
                for i, team in enumerate(rankings)
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Rankings saved to {filename}")

def load_sample_teams() -> Dict[str, Team]:
    """Load sample teams with approximate current FIFA points"""
    # These are approximate values based on October 2025 rankings
    sample_teams = {
        "Spain": Team("Spain", "ESP", 1880.76, "UEFA"),
        "Argentina": Team("Argentina", "ARG", 1872.43, "CONMEBOL"),
        "France": Team("France", "FRA", 1862.71, "UEFA"),
        "England": Team("England", "ENG", 1824.30, "UEFA"),
        "Portugal": Team("Portugal", "POR", 1778.00, "UEFA"),
        "Netherlands": Team("Netherlands", "NED", 1759.96, "UEFA"),
        "Brazil": Team("Brazil", "BRA", 1758.85, "CONMEBOL"),
        "Belgium": Team("Belgium", "BEL", 1740.01, "UEFA"),
        "Italy": Team("Italy", "ITA", 1717.15, "UEFA"),
        "Germany": Team("Germany", "GER", 1713.30, "UEFA"),
        "Croatia": Team("Croatia", "CRO", 1710.15, "UEFA"),
        "Morocco": Team("Morocco", "MAR", 1710.11, "CAF"),
        "Colombia": Team("Colombia", "COL", 1695.72, "CONMEBOL"),
        "Mexico": Team("Mexico", "MEX", 1682.52, "CONCACAF"),
        "Uruguay": Team("Uruguay", "URU", 1677.57, "CONMEBOL"),
        "United States": Team("United States", "USA", 1673.49, "CONCACAF"),
        "Switzerland": Team("Switzerland", "SUI", 1653.32, "UEFA"),
        "Senegal": Team("Senegal", "SEN", 1650.61, "CAF"),
        "Japan": Team("Japan", "JPN", 1645.34, "AFC"),
        "Denmark": Team("Denmark", "DEN", 1641.02, "UEFA"),
    }
    return sample_teams

def create_sample_matches() -> List[Match]:
    """Create sample matches for demonstration"""
    sample_matches = [
        # Recent UEFA Nations League matches
        Match(
            date=datetime.date(2025, 11, 15),
            home_team="Spain",
            away_team="France",
            home_score=2,
            away_score=1,
            competition=CompetitionType.NATIONS_LEAGUE_FINALS
        ),
        Match(
            date=datetime.date(2025, 11, 15),
            home_team="Germany",
            away_team="Italy",
            home_score=1,
            away_score=1,
            competition=CompetitionType.NATIONS_LEAGUE_FINALS
        ),
        # World Cup 2026 Qualifiers
        Match(
            date=datetime.date(2025, 11, 18),
            home_team="Brazil",
            away_team="Uruguay",
            home_score=3,
            away_score=0,
            competition=CompetitionType.WORLD_CUP_QUALIFIERS
        ),
        Match(
            date=datetime.date(2025, 11, 18),
            home_team="Argentina",
            away_team="Colombia",
            home_score=2,
            away_score=2,
            competition=CompetitionType.WORLD_CUP_QUALIFIERS
        ),
        # Friendlies
        Match(
            date=datetime.date(2025, 11, 20),
            home_team="England",
            away_team="Netherlands",
            home_score=1,
            away_score=2,
            competition=CompetitionType.FRIENDLY_INSIDE_WINDOW
        ),
    ]
    return sample_matches

def main():
    """Main demonstration function"""
    print("🏆 FIFA MEN'S WORLD RANKING CALCULATOR")
    print("Based on current FIFA methodology (2018+ Elo system)")
    print("=" * 80)
    
    # Initialize calculator
    calculator = FIFARankingCalculator()
    
    # Load sample teams
    teams = load_sample_teams()
    for team in teams.values():
        calculator.add_team(team.name, team.fifa_code, team.points, team.confederation)
    
    # Display initial rankings
    print("INITIAL RANKINGS (Before new matches):")
    calculator.display_rankings(20)
    print()
    
    # Add sample matches
    sample_matches = create_sample_matches()
    for match in sample_matches:
        calculator.add_match(match)
    
    # Process matches
    calculator.process_all_matches()
    
    # Display updated rankings
    print("UPDATED RANKINGS (After processing matches):")
    calculator.display_rankings(20)
    
    # Save to file
    calculator.save_rankings_json("fifa_rankings_updated.json")
    
    print("\n" + "=" * 80)
    print("FORMULA EXPLANATION:")
    print("=" * 80)
    print("FIFA Formula: P = P_before + I(W - We)")
    print("Where:")
    print("  P_before = Points before the match")
    print("  I = Importance coefficient (5-60 based on competition)")
    print("  W = Match result (0=loss, 0.5=draw/penalty loss, 0.75=penalty win, 1=win)")
    print("  We = Expected result = 1/(10^(-Δ/600) + 1)")
    print("  Δ = Difference in team points before match")
    print()
    print("Competition Importance Coefficients:")
    for comp in CompetitionType:
        print(f"  {comp.name.replace('_', ' ').title()}: {comp.value}")

if __name__ == "__main__":
    main()