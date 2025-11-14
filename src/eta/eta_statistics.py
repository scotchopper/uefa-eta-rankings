"""
Scotland National Football Team Statistics Analysis

This module reads Scotland national team results from an Excel spreadsheet and
generates various statistical analyses including aggregations by opposition,
venue, competition, and manager.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScotlandFootballAnalyzer:
    """Analyzer for Scotland national football team statistics."""
    
    def __init__(self, excel_file_path: str, worksheet_name: str = 'Results'):
        """
        Initialize the analyzer with the Excel file path.
        
        Args:
            excel_file_path: Path to the Excel file containing results
            worksheet_name: Name of the worksheet containing the data
        """
        self.excel_file_path = Path(excel_file_path)
        self.worksheet_name = worksheet_name
        self.df: Optional[pd.DataFrame] = None
        
    def load_data(self) -> pd.DataFrame:
        """
        Load data from the Excel spreadsheet into a DataFrame.
        
        Returns:
            DataFrame containing the Scotland results data
            
        Raises:
            FileNotFoundError: If the Excel file doesn't exist
            ValueError: If the worksheet doesn't exist
        """
        if not self.excel_file_path.exists():
            raise FileNotFoundError(f"Excel file not found: {self.excel_file_path}")
            
        try:
            self.df = pd.read_excel(self.excel_file_path, sheet_name=self.worksheet_name)
            logger.info(f"Loaded {len(self.df)} records from {self.excel_file_path}")
            
            # Handle different possible column names for goals
            scotland_goals_col = None
            opposition_goals_col = None
            home_away_col = None
            
            # Check for various column name variations
            for col in self.df.columns:
                if col.lower() in ['scot', 'scotland_goals', 'scotland goals']:
                    scotland_goals_col = col
                elif col.lower() in ['opp', 'opposition_goals', 'opposition goals']:
                    opposition_goals_col = col
                elif col.lower() in ['home\\away', 'home/away', 'home_away', 'venue_type']:
                    home_away_col = col
            
            # Standardize column names
            if scotland_goals_col:
                self.df['Scotland_Goals'] = self.df[scotland_goals_col]
            if opposition_goals_col:
                self.df['Opposition_Goals'] = self.df[opposition_goals_col]
            if home_away_col:
                self.df['Home_Away'] = self.df[home_away_col]
            
            # Basic data validation
            expected_columns = ['Date', 'Opposition', 'Venue', 'Competition', 'Manager']
            if scotland_goals_col:
                expected_columns.append('Scotland_Goals')
            if opposition_goals_col:
                expected_columns.append('Opposition_Goals')
            if home_away_col:
                expected_columns.append('Home_Away')
            
            missing_columns = [col for col in expected_columns if col not in self.df.columns]
            
            if missing_columns:
                logger.warning(f"Missing expected columns: {missing_columns}")
                logger.info(f"Available columns: {list(self.df.columns)}")
            
            # Convert date column to datetime
            if 'Date' in self.df.columns:
                self.df['Date'] = pd.to_datetime(self.df['Date'])
            
            # If Result column doesn't exist, create it from goals
            if 'Result' not in self.df.columns and scotland_goals_col and opposition_goals_col:
                self.df['Result'] = self.df.apply(self._determine_result, axis=1)
            elif 'Result' in self.df.columns:
                # Standardize result values
                self.df['Result'] = self.df['Result'].map({'W': 'Win', 'WP': 'WinPens','D': 'Draw', 'L': 'Loss'}).fillna(self.df['Result'])
                
            # Create goal difference column
            if scotland_goals_col and opposition_goals_col:
                self.df['Goal_Difference'] = self.df['Scotland_Goals'] - self.df['Opposition_Goals']
                
            return self.df
            
        except Exception as e:
            raise ValueError(f"Error loading data from worksheet '{self.worksheet_name}': {e}")
    
    def _determine_result(self, row) -> str:
        """Determine match result (Win/Draw/Loss) from goals scored."""
        scotland_goals = row.get('Scotland_Goals', 0)
        opposition_goals = row.get('Opposition_Goals', 0)
        
        if scotland_goals > opposition_goals:
            return 'Win'
        elif scotland_goals == opposition_goals:
            return 'Draw'
        else:
            return 'Loss'
    
    def get_overall_statistics(self) -> Dict[str, Union[int, float]]:
        """
        Get overall statistics for Scotland's performance.
        
        Returns:
            Dictionary containing overall statistics
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
            
        total_matches = len(self.df)
        wins = len(self.df[self.df['Result'] == 'Win'])
        draws = len(self.df[self.df['Result'] == 'Draw'])
        losses = len(self.df[self.df['Result'] == 'Loss'])
        
        total_goals_scored = self.df['Scotland_Goals'].sum()
        total_goals_conceded = self.df['Opposition_Goals'].sum()
        
        return {
            'total_matches': total_matches,
            'wins': wins,
            'draws': draws,
            'losses': losses,
            'win_percentage': (wins / total_matches * 100) if total_matches > 0 else 0,
            'total_goals_scored': total_goals_scored,
            'total_goals_conceded': total_goals_conceded,
            'goal_difference': total_goals_scored - total_goals_conceded,
            'goals_per_match': total_goals_scored / total_matches if total_matches > 0 else 0,
            'goals_conceded_per_match': total_goals_conceded / total_matches if total_matches > 0 else 0
        }
    
    def analyze_by_opposition(self, filter_query: Optional[str] = None) -> pd.DataFrame:
        """
        Analyze results and goals by opposition team with optional dynamic filtering.
        
        Args:
            filter_query: Optional pandas query string to filter the data.
                         Examples:
                         - "Home_Away != 'H'" (exclude home games)
                         - "Home_Away == 'N'" (only neutral games)  
                         - "Home_Away in ['A', 'N']" (away and neutral only)
                         - "Competition == 'World Cup'" (only World Cup games)
                         - "Date >= '2000-01-01'" (games from 2000 onwards)
        
        Returns:
            DataFrame with statistics grouped by opposition
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        # Create a copy of the dataframe to work with
        df_filtered = self.df.copy()
        
        # Apply dynamic filter if provided
        if filter_query:
            try:
                df_filtered = df_filtered.query(filter_query)
                if df_filtered.empty:
                    logger.warning(f"No games found matching filter: {filter_query}")
                    return pd.DataFrame()
                logger.info(f"Applied filter '{filter_query}': {len(df_filtered)} games selected from {len(self.df)} total games")
            except Exception as e:
                logger.error(f"Error applying filter '{filter_query}': {e}")
                logger.info("Available columns for filtering: " + ", ".join(self.df.columns))
                raise ValueError(f"Invalid filter query: {filter_query}. Error: {e}")
            
        opposition_stats = df_filtered.groupby('Opposition').agg({
            'Result': ['count', lambda x: sum(x == 'Win'), lambda x: sum(x == 'Draw'), lambda x: sum(x == 'Loss')],
            'Scotland_Goals': ['sum', 'mean'],
            'Opposition_Goals': ['sum', 'mean'],
            'Goal_Difference': ['sum', 'mean']
        }).round(2)
        
        # Flatten column names
        opposition_stats.columns = [
            'matches_played', 'wins', 'draws', 'losses',
            'goals_scored', 'avg_goals_scored',
            'goals_conceded', 'avg_goals_conceded',
            'goal_difference', 'avg_goal_difference'
        ]
        
        # Calculate win percentage
        opposition_stats['win_percentage'] = (
            opposition_stats['wins'] / opposition_stats['matches_played'] * 100
        ).round(2)
        
        return opposition_stats.sort_values('matches_played', ascending=False)
    
    def analyze_by_venue(self) -> pd.DataFrame:
        """
        Analyze results and goals by specific venue/ground.
        
        Returns:
            DataFrame with statistics grouped by venue (city/ground)
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
            
        venue_stats = self.df.groupby('Venue').agg({
            'Result': ['count', lambda x: sum(x == 'Win'), lambda x: sum(x == 'Draw'), lambda x: sum(x == 'Loss')],
            'Scotland_Goals': ['sum', 'mean'],
            'Opposition_Goals': ['sum', 'mean'],
            'Goal_Difference': ['sum', 'mean']
        }).round(2)
        
        # Flatten column names
        venue_stats.columns = [
            'matches_played', 'wins', 'draws', 'losses',
            'goals_scored', 'avg_goals_scored',
            'goals_conceded', 'avg_goals_conceded',
            'goal_difference', 'avg_goal_difference'
        ]
        
        # Calculate win percentage
        venue_stats['win_percentage'] = (
            venue_stats['wins'] / venue_stats['matches_played'] * 100
        ).round(2)

        return venue_stats.sort_values(['matches_played', 'wins', 'draws'], ascending=[False, False, False])
    
    def analyze_by_city(self) -> pd.DataFrame:
        """
        Analyze results and goals by city, aggregating multiple venues within each city.
        
        Returns:
            DataFrame with statistics grouped by city
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
        
        # Define city-to-venue mappings
        city_venue_mapping = {
            "Glasgow": ["Celtic Park", "Ibrox", "Hampden","Hampden I","Hampden II","Ibrox I","Hamilton Crescent"],
            "Edinburgh": ["Easter Road", "Tynecastle","Hibernian Park"],
            "London": ["Wembley", "Emirates", "London", "Craven Cottage", "The Oval", "Crystal Palace", "Stamford Bridge"],
            "Dundee": ["Dens Park", "Dundee"]
        }
        
        # Create a copy of the dataframe to work with
        df_city = self.df.copy()
        
        # Map venues to cities
        def map_venue_to_city(venue):
            for city, venues in city_venue_mapping.items():
                if venue in venues:
                    return city
            return venue  # Return original venue name if not in mapping
        
        df_city['City'] = df_city['Venue'].apply(map_venue_to_city)
        
        # Aggregate by city
        city_stats = df_city.groupby('City').agg({
            'Result': ['count', lambda x: sum(x == 'Win'), lambda x: sum(x == 'Draw'), lambda x: sum(x == 'Loss')],
            'Scotland_Goals': ['sum', 'mean'],
            'Opposition_Goals': ['sum', 'mean'],
            'Goal_Difference': ['sum', 'mean']
        }).round(2)
        
        # Flatten column names
        city_stats.columns = [
            'matches_played', 'wins', 'draws', 'losses',
            'goals_scored', 'avg_goals_scored',
            'goals_conceded', 'avg_goals_conceded',
            'goal_difference', 'avg_goal_difference'
        ]
        
        # Calculate win percentage
        city_stats['win_percentage'] = (
            city_stats['wins'] / city_stats['matches_played'] * 100
        ).round(2)
        
        # Add venue details for cities with multiple venues
        city_details = {}
        for city, venues in city_venue_mapping.items():
            city_venues_in_data = [v for v in venues if v in self.df['Venue'].values]
            if len(city_venues_in_data) > 1:
                city_details[city] = city_venues_in_data
        
        # Add a column showing which venues are included for multi-venue cities
        city_stats['venues_included'] = city_stats.index.map(
            lambda city: ', '.join(city_details.get(city, [city]))
        )
        
        return city_stats.sort_values(['matches_played', 'win_percentage'], ascending=[False, False])

    def analyze_by_home_away(self) -> pd.DataFrame:
        """
        Analyze results and goals by home/away/neutral status.
        
        Returns:
            DataFrame with statistics grouped by home/away/neutral
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
            
        if 'Home_Away' not in self.df.columns:
            logger.warning("Home_Away column not found. Cannot analyze by home/away status.")
            return pd.DataFrame()
            
        home_away_stats = self.df.groupby('Home_Away').agg({
            'Result': ['count', lambda x: sum(x == 'Win'), lambda x: sum(x == 'Draw'), lambda x: sum(x == 'Loss')],
            'Scotland_Goals': ['sum', 'mean'],
            'Opposition_Goals': ['sum', 'mean'],
            'Goal_Difference': ['sum', 'mean']
        }).round(2)
        
        # Flatten column names
        home_away_stats.columns = [
            'matches_played', 'wins', 'draws', 'losses',
            'goals_scored', 'avg_goals_scored',
            'goals_conceded', 'avg_goals_conceded',
            'goal_difference', 'avg_goal_difference'
        ]
        
        # Calculate win percentage
        home_away_stats['win_percentage'] = (
            home_away_stats['wins'] / home_away_stats['matches_played'] * 100
        ).round(2)
        
        return home_away_stats
    
    def analyze_by_competition(self) -> pd.DataFrame:
        """
        Analyze results and goals by competition type.
        
        Returns:
            DataFrame with statistics grouped by competition
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
            
        competition_stats = self.df.groupby('Competition').agg({
            'Result': ['count', lambda x: sum(x == 'Win'), lambda x: sum(x == 'Draw'), lambda x: sum(x == 'Loss')],
            'Scotland_Goals': ['sum', 'mean'],
            'Opposition_Goals': ['sum', 'mean'],
            'Goal_Difference': ['sum', 'mean']
        }).round(2)
        
        # Flatten column names
        competition_stats.columns = [
            'matches_played', 'wins', 'draws', 'losses',
            'goals_scored', 'avg_goals_scored',
            'goals_conceded', 'avg_goals_conceded',
            'goal_difference', 'avg_goal_difference'
        ]
        
        # Calculate win percentage
        competition_stats['win_percentage'] = (
            competition_stats['wins'] / competition_stats['matches_played'] * 100
        ).round(2)
        
        return competition_stats.sort_values('matches_played', ascending=False)
    
    def analyze_by_manager(self) -> pd.DataFrame:
        """
        Analyze results and goals by manager.
        
        Returns:
            DataFrame with statistics grouped by manager
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
            
        manager_stats = self.df.groupby('Manager').agg({
            'Result': ['count', lambda x: sum(x == 'Win'), lambda x: sum(x == 'Draw'), lambda x: sum(x == 'Loss')],
            'Scotland_Goals': ['sum', 'mean'],
            'Opposition_Goals': ['sum', 'mean'],
            'Goal_Difference': ['sum', 'mean']
        }).round(2)
        
        # Flatten column names
        manager_stats.columns = [
            'matches_played', 'wins', 'draws', 'losses',
            'goals_scored', 'avg_goals_scored',
            'goals_conceded', 'avg_goals_conceded',
            'goal_difference', 'avg_goal_difference'
        ]
        
        # Calculate win percentage
        manager_stats['win_percentage'] = (
            manager_stats['wins'] / manager_stats['matches_played'] * 100
        ).round(2)
        
        return manager_stats.sort_values('matches_played', ascending=False)
    
    def get_year_by_year_analysis(self) -> pd.DataFrame:
        """
        Analyze performance year by year.
        
        Returns:
            DataFrame with statistics grouped by year
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
            
        # Extract year from date
        self.df['Year'] = self.df['Date'].dt.year
        
        yearly_stats = self.df.groupby('Year').agg({
            'Result': ['count', lambda x: sum(x == 'Win'), lambda x: sum(x == 'Draw'), lambda x: sum(x == 'Loss')],
            'Scotland_Goals': ['sum', 'mean'],
            'Opposition_Goals': ['sum', 'mean'],
            'Goal_Difference': ['sum', 'mean']
        }).round(2)
        
        # Flatten column names
        yearly_stats.columns = [
            'matches_played', 'wins', 'draws', 'losses',
            'goals_scored', 'avg_goals_scored',
            'goals_conceded', 'avg_goals_conceded',
            'goal_difference', 'avg_goal_difference'
        ]
        
        # Calculate win percentage
        yearly_stats['win_percentage'] = (
            yearly_stats['wins'] / yearly_stats['matches_played'] * 100
        ).round(2)
        
        return yearly_stats.sort_values('Year', ascending=False)
    
    def get_top_scorers_against_opposition(self, top_n: int = 10) -> pd.DataFrame:
        """
        Get opponents against whom Scotland scored the most goals on average.
        
        Args:
            top_n: Number of top opponents to return
            
        Returns:
            DataFrame with top scoring opponents
        """
        opposition_scoring = self.analyze_by_opposition()
        return opposition_scoring.nlargest(top_n, 'avg_goals_scored')[
            ['matches_played', 'avg_goals_scored', 'goals_scored', 'win_percentage']
        ]
    
    def get_toughest_opponents(self, min_matches: int = 3, top_n: int = 10) -> pd.DataFrame:
        """
        Get the toughest opponents (lowest win percentage) with minimum matches played.
        
        Args:
            min_matches: Minimum number of matches played against opponent
            top_n: Number of opponents to return
            
        Returns:
            DataFrame with toughest opponents
        """
        opposition_stats = self.analyze_by_opposition()
        qualified_opponents = opposition_stats[opposition_stats['matches_played'] >= min_matches]
        return qualified_opponents.nsmallest(top_n, 'win_percentage')[
            ['matches_played', 'wins', 'draws', 'losses', 'win_percentage', 'avg_goal_difference']
        ]
    
    def categorize_opponents_by_venue_type(self) -> Dict[str, List[str]]:
        """
        Categorize opponents based on where Scotland has played them (Home/Away/Neutral).
        
        Returns:
            Dictionary with 4 lists:
            - 'home_and_away': Opponents played both home and away
            - 'home_only': Opponents only played at home
            - 'away_only': Opponents only played away
            - 'neutral_only': Opponents only played at neutral venues
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
            
        if 'Home_Away' not in self.df.columns:
            logger.warning("Home_Away column not found. Cannot categorize opponents by venue type.")
            return {
                'home_and_away': [],
                'home_only': [],
                'away_only': [],
                'neutral_only': []
            }
        
        # Get unique opponents and their venue types
        opponent_venues = {}
        
        for _, row in self.df.iterrows():
            opponent = row['Opposition']
            venue_type = row['Home_Away']
            
            if opponent not in opponent_venues:
                opponent_venues[opponent] = set()
            opponent_venues[opponent].add(venue_type)
        
        # Categorize opponents
        home_and_away = []
        home_only = []
        away_only = []
        neutral_only = []
        
        for opponent, venues in opponent_venues.items():
            if 'H' in venues and 'A' in venues:
                # Played both home and away (regardless of neutral)
                home_and_away.append(opponent)
            elif 'H' in venues and 'A' not in venues:
                # Only played at home (may include neutral)
                if venues == {'H'} or venues == {'H', 'N'}:
                    home_only.append(opponent)
                else:
                    home_and_away.append(opponent)  # Edge case
            elif 'A' in venues and 'H' not in venues:
                # Only played away (may include neutral)
                if venues == {'A'} or venues == {'A', 'N'}:
                    away_only.append(opponent)
                else:
                    home_and_away.append(opponent)  # Edge case
            elif venues == {'N'}:
                # Only played at neutral venues
                neutral_only.append(opponent)
        
        # Sort all lists alphabetically
        home_and_away.sort()
        home_only.sort()
        away_only.sort()
        neutral_only.sort()
        
        return {
            'home_and_away': home_and_away,
            'home_only': home_only,
            'away_only': away_only,
            'neutral_only': neutral_only
        }
    
    def print_opponent_venue_categories(self) -> None:
        """
        Print the 4 lists of opponents categorized by venue type.
        """
        categories = self.categorize_opponents_by_venue_type()
        
        print("🏟️  OPPONENTS CATEGORIZED BY VENUE TYPE")
        print("=" * 50)
        
        # List 1: Home and Away opponents
        print(f"\n1️⃣  OPPONENTS PLAYED BOTH HOME AND AWAY ({len(categories['home_and_away'])}):")
        print("-" * 50)
        if categories['home_and_away']:
            for i, opponent in enumerate(categories['home_and_away'], 1):
                print(f"   {i:2}. {opponent}")
        else:
            print("   None")
        
        # List 2: Home only opponents
        print(f"\n2️⃣  OPPONENTS PLAYED ONLY AT HOME ({len(categories['home_only'])}):")
        print("-" * 40)
        if categories['home_only']:
            for i, opponent in enumerate(categories['home_only'], 1):
                print(f"   {i:2}. {opponent}")
        else:
            print("   None")
        
        # List 3: Away only opponents
        print(f"\n3️⃣  OPPONENTS PLAYED ONLY AWAY ({len(categories['away_only'])}):")
        print("-" * 35)
        if categories['away_only']:
            for i, opponent in enumerate(categories['away_only'], 1):
                print(f"   {i:2}. {opponent}")
        else:
            print("   None")
        
        # List 4: Neutral only opponents
        print(f"\n4️⃣  OPPONENTS PLAYED ONLY AT NEUTRAL VENUES ({len(categories['neutral_only'])}):")
        print("-" * 50)
        if categories['neutral_only']:
            for i, opponent in enumerate(categories['neutral_only'], 1):
                print(f"   {i:2}. {opponent}")
        else:
            print("   None")
        
        # Summary
        total_opponents = sum(len(lst) for lst in categories.values())
        print(f"\n📊 SUMMARY:")
        print(f"   Total unique opponents: {total_opponents}")
        print(f"   Home & Away: {len(categories['home_and_away'])}")
        print(f"   Home only: {len(categories['home_only'])}")
        print(f"   Away only: {len(categories['away_only'])}")
        print(f"   Neutral only: {len(categories['neutral_only'])}")
    
    def analyze_goalscorers(self) -> pd.DataFrame:
        """
        Analyze Scotland goalscorers from the Scotland Scorers column.
        
        Returns:
            DataFrame with goalscorer statistics (goals and games scored in only)
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
            
        if 'Scotland Scorers' not in self.df.columns:
            logger.warning("Scotland Scorers column not found.")
            return pd.DataFrame()
        
        # Extract all goalscorers
        all_scorers = []
        for _, row in self.df.iterrows():
            scorers_text = row.get('Scotland Scorers', '')
            if pd.isna(scorers_text) or scorers_text == '':
                continue
                
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
                        import re
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
                    
                    # Handle own goals
                    if 'og' in name.lower():
                        # Check if it's a standalone 'og' entry
                        if name.lower().strip() == 'og':
                            name = 'Own Goal (og)'
                        else:
                            # It's a player name with og attached
                            name = name.replace('og', '').replace('OG', '').strip()
                            if name:  # Only if there's a name left
                                name += ' (og)'
                            else:
                                # Edge case: somehow became empty after removing og
                                name = 'Own Goal (og)'
                    
                    if name:  # Only add if name is not empty
                        all_scorers.extend([name] * goals)
        
        if not all_scorers:
            return pd.DataFrame(columns=['goals', 'games_scored_in'])
        
        # Count goals per player
        scorer_counts = pd.Series(all_scorers).value_counts()
        
        # Count matches where each player scored (not total appearances)
        scorer_matches = {}
        for scorer in scorer_counts.index:
            clean_scorer = scorer.replace(' (og)', '')
            matches = 0
            for _, row in self.df.iterrows():
                scorers_text = str(row.get('Scotland Scorers', ''))
                if clean_scorer.lower() in scorers_text.lower():
                    matches += 1
            scorer_matches[scorer] = matches
        
        # Create DataFrame
        goalscorers_df = pd.DataFrame({
            'goals': scorer_counts,
            'games_scored_in': [scorer_matches[scorer] for scorer in scorer_counts.index]
        })
        
        # Calculate goals per scoring game (more accurate than misleading "goals per match")
        goalscorers_df['goals_per_scoring_game'] = (goalscorers_df['goals'] / goalscorers_df['games_scored_in']).round(2)
        
        return goalscorers_df.sort_values('goals', ascending=False)
    
    def get_player_scoring_details(self, player_name: str) -> pd.DataFrame:
        """
        Get detailed scoring record for a specific player.
        
        Args:
            player_name: Name of the player to analyze
            
        Returns:
            DataFrame with all games where the player scored
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
            
        if 'Scotland Scorers' not in self.df.columns:
            logger.warning("Scotland Scorers column not found.")
            return pd.DataFrame()
        
        # Find all games where the player scored
        player_games = self.df[
            self.df['Scotland Scorers'].str.contains(player_name, case=False, na=False)
        ].copy()
        
        if player_games.empty:
            return pd.DataFrame()
        
        # Extract goals scored by this player in each game
        goals_in_games = []
        for idx, row in player_games.iterrows():
            scorers_text = str(row['Scotland Scorers'])
            goals_in_game = 0
            
            # Split by comma and check each scorer
            scorers_list = [s.strip() for s in scorers_text.split(',')]
            for scorer in scorers_list:
                if player_name.lower() in scorer.lower():
                    # Handle cases like "Dalglish 2", "Dalglish(   2)", or "Dalglish(2)" (scored 2 goals)
                    goals_to_add = 1  # default
                    
                    # Check for parenthetical format first (handles both spaced and non-spaced)
                    if '(' in scorer and ')' in scorer:
                        # Extract number from parentheses
                        import re
                        match = re.search(r'\((\s*\d+\s*)\)', scorer)
                        if match:
                            goals_to_add = int(match.group(1).strip())
                    else:
                        # Check for space-separated format like "Player 2"
                        parts = scorer.split()
                        if len(parts) > 1 and parts[-1].isdigit():
                            goals_to_add = int(parts[-1])
                    
                    goals_in_game += goals_to_add
            
            goals_in_games.append(goals_in_game)
        
        player_games['goals_in_game'] = goals_in_games
        
        return player_games[['Date', 'Opposition', 'Venue', 'Competition', 'Result', 
                           'Scotland_Goals', 'Opposition_Goals', 'Scotland Scorers', 'goals_in_game']].sort_values('Date')

    def identify_potential_duplicate_surnames(self, min_gap_years: int = 20) -> pd.DataFrame:
        """
        Identify goalscorers who may represent multiple players with the same surname
        by looking for significant time gaps between goals.
        
        Args:
            min_gap_years: Minimum gap in years to flag as potential different players
            
        Returns:
            DataFrame with players showing suspicious time gaps
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
            
        suspicious_players = []
        goalscorers = self.analyze_goalscorers()
        
        # Only check players with multiple goals to avoid false positives
        multi_goal_scorers = goalscorers[goalscorers['goals'] > 1]
        
        for player_name in multi_goal_scorers.index:
            # Get exact matches for this player name (not substring matches)
            exact_goal_games = []
            for _, row in self.df.iterrows():
                scorers_text = str(row.get('Scotland Scorers', ''))
                if scorers_text and not pd.isna(scorers_text):
                    scorers_list = [s.strip() for s in scorers_text.split(',')]
                    for scorer in scorers_list:
                        if scorer and scorer.lower() not in ['', 'nan']:
                            # Apply same parsing logic as analyze_goalscorers to get final name
                            parsed_name = scorer
                            import re
                            if '(' in scorer and ')' in scorer:
                                match = re.search(r'\((\s*\d+\s*)\)', scorer)
                                if match:
                                    goals = int(match.group(1).strip())
                                    parsed_name = re.sub(r'\(\s*\d+\s*\)', '', scorer).strip()
                                else:
                                    penalty_match = re.search(r'\(\s*p\s*\)', scorer, re.IGNORECASE)
                                    if penalty_match:
                                        parsed_name = re.sub(r'\(\s*p\s*\)', '', scorer, flags=re.IGNORECASE).strip()
                                        goals = 1
                                    else:
                                        parsed_name = scorer.strip()
                                        goals = 1
                            elif '[' in scorer and ']' in scorer:
                                parsed_name = scorer.strip()
                                goals = 1
                            else:
                                parts = scorer.split()
                                if len(parts) > 1 and parts[-1].isdigit():
                                    parsed_name = ' '.join(parts[:-1])
                                    goals = int(parts[-1])
                                else:
                                    parsed_name = scorer.strip()
                                    goals = 1
                            
                            # Handle own goals
                            if 'og' in parsed_name.lower():
                                parsed_name = parsed_name.replace('og', '').replace('OG', '').strip()
                                if parsed_name:
                                    parsed_name += ' (og)'
                            
                            # Check for exact match
                            if parsed_name == player_name:
                                exact_goal_games.append({
                                    'Date': row['Date'],
                                    'Opposition': row.get('Opposition', ''),
                                    'Venue': row.get('Venue', ''),
                                    'Competition': row.get('Competition', ''),
                                    'Result': row.get('Result', ''),
                                    'Scotland_Goals': row.get('Scotland_Goals', 0),
                                    'Opposition_Goals': row.get('Opposition_Goals', 0),
                                    'Scotland Scorers': scorers_text,
                                    'goals_in_game': goals
                                })
            
            if len(exact_goal_games) < 2:  # Need at least 2 games to check gaps
                continue
            
            # Convert to DataFrame for processing
            player_details = pd.DataFrame(exact_goal_games)
                
            # Sort by date and calculate gaps between consecutive goals
            player_details = player_details.sort_values('Date')
            dates = pd.to_datetime(player_details['Date'])
            
            max_gap_days = 0
            max_gap_start = None
            max_gap_end = None
            
            for i in range(1, len(dates)):
                gap_days = (dates.iloc[i] - dates.iloc[i-1]).days
                if gap_days > max_gap_days:
                    max_gap_days = gap_days
                    max_gap_start = dates.iloc[i-1]
                    max_gap_end = dates.iloc[i]
            
            max_gap_years = max_gap_days / 365.25
            
            if max_gap_years >= min_gap_years:
                # Get details about the periods before and after the gap
                before_gap = player_details[player_details['Date'] <= max_gap_start]
                after_gap = player_details[player_details['Date'] >= max_gap_end]
                
                # Get goal count - convert to Python int safely
                total_goals = goalscorers.loc[player_name, 'goals']
                
                suspicious_players.append({
                    'player': player_name,
                    'total_goals': total_goals,
                    'total_games': len(player_details),
                    'career_span_years': round((dates.max() - dates.min()).days / 365.25, 1),
                    'max_gap_years': round(max_gap_years, 1),
                    'gap_start_date': max_gap_start.strftime('%Y-%m-%d') if max_gap_start is not None else '',
                    'gap_end_date': max_gap_end.strftime('%Y-%m-%d') if max_gap_end is not None else '',
                    'goals_before_gap': int(before_gap['goals_in_game'].sum()),
                    'games_before_gap': len(before_gap),
                    'goals_after_gap': int(after_gap['goals_in_game'].sum()),
                    'games_after_gap': len(after_gap),
                    'first_goal_date': dates.min().strftime('%Y-%m-%d'),
                    'last_goal_date': dates.max().strftime('%Y-%m-%d')
                })
        
        if not suspicious_players:
            return pd.DataFrame()
            
        result_df = pd.DataFrame(suspicious_players)
        return result_df.sort_values('max_gap_years', ascending=False)

    def get_player_career_timeline(self, player_name: str) -> pd.DataFrame:
        """
        Get a detailed timeline of a player's international career.
        
        Args:
            player_name: Name of the player to analyze
            
        Returns:
            DataFrame with chronological career details
        """
        player_details = self.get_player_scoring_details(player_name)
        
        if player_details.empty:
            return pd.DataFrame()
            
        # Sort by date and add year column for easier analysis
        timeline = player_details.sort_values('Date').copy()
        timeline['Year'] = pd.to_datetime(timeline['Date']).dt.year
        
        # Add cumulative goals
        timeline['cumulative_goals'] = timeline['goals_in_game'].cumsum()
        
        return timeline[['Date', 'Year', 'Opposition', 'Venue', 'goals_in_game', 'cumulative_goals', 'Scotland Scorers']]

    def generate_summary_report(self) -> str:
        """
        Generate a comprehensive summary report.
        
        Returns:
            String containing formatted summary report
        """
        if self.df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
            
        overall_stats = self.get_overall_statistics()
        
        report = f"""
SCOTLAND NATIONAL TEAM STATISTICS SUMMARY
==========================================
Data period: {self.df['Date'].min().strftime('%Y-%m-%d')} to {self.df['Date'].max().strftime('%Y-%m-%d')}

OVERALL PERFORMANCE:
- Total Matches: {overall_stats['total_matches']}
- Wins: {overall_stats['wins']} ({overall_stats['win_percentage']:.1f}%)
- Draws: {overall_stats['draws']}
- Losses: {overall_stats['losses']}
- Goals Scored: {overall_stats['total_goals_scored']}
- Goals Conceded: {overall_stats['total_goals_conceded']}
- Goal Difference: {overall_stats['goal_difference']:+d}
- Goals per Match: {overall_stats['goals_per_match']:.2f}
"""
        
        # Add home/away performance if available
        if 'Home_Away' in self.df.columns:
            home_away_stats = self.analyze_by_home_away()
            if not home_away_stats.empty:
                report += "\nPERFORMANCE BY HOME/AWAY:\n"
                for location in home_away_stats.index:
                    stats = home_away_stats.loc[location]
                    report += f"- {location}: {stats['wins']}-{stats['draws']}-{stats['losses']} ({stats['win_percentage']:.1f}% win rate)\n"
        
        # Add top 5 most played opponents
        top_opponents = self.analyze_by_opposition().head(5)
        report += f"\nMOST FREQUENT OPPONENTS:\n"
        for opponent in top_opponents.index:
            stats = top_opponents.loc[opponent]
            report += f"- {opponent}: {stats['matches_played']} matches ({stats['win_percentage']:.1f}% win rate)\n"
        
        # Add top goalscorers if available
        goalscorers = self.analyze_goalscorers()
        if not goalscorers.empty:
            report += f"\nTOP 5 GOALSCORERS:\n"
            top_scorers = goalscorers.head(5)
            for scorer in top_scorers.index:
                stats = top_scorers.loc[scorer]
                report += f"- {scorer}: {stats['goals']} goals in {stats['matches']} matches ({stats['goals_per_match']:.2f} per match)\n"
        
        return report


def main():
    """Main function to demonstrate the analyzer."""
    # Example usage - you'll need to provide the actual Excel file path
    excel_file = "scotland_results.xlsx"  # Update this path
    
    try:
        analyzer = ScotlandFootballAnalyzer(excel_file)
        
        # Load data
        print("Loading Scotland football results data...")
        df = analyzer.load_data()
        print(f"Loaded {len(df)} matches")
        
        # Generate overall statistics
        print("\n" + "="*50)
        print("OVERALL STATISTICS")
        print("="*50)
        overall_stats = analyzer.get_overall_statistics()
        for key, value in overall_stats.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        
        # Analyze by opposition
        print("\n" + "="*50)
        print("TOP 10 MOST PLAYED OPPONENTS")
        print("="*50)
        opposition_stats = analyzer.analyze_by_opposition().head(10)
        print(opposition_stats[['matches_played', 'wins', 'draws', 'losses', 'win_percentage']])
        
        # Analyze by venue
        print("\n" + "="*50)
        print("PERFORMANCE BY VENUE")
        print("="*50)
        venue_stats = analyzer.analyze_by_venue()
        print(venue_stats[['matches_played', 'wins', 'draws', 'losses', 'win_percentage']])
        
        # Generate summary report
        print("\n" + analyzer.generate_summary_report())
        
    except FileNotFoundError:
        print(f"Excel file '{excel_file}' not found.")
        print("Please provide the correct path to your Scotland results Excel file.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()