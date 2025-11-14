# Scotland Football Statistics Analyzer

## Overview
The `eta_statistics.py` module provides comprehensive analysis of Scotland national football team results from an Excel spreadsheet. It generates various aggregations and statistics by opposition, venue, competition, and manager.

## Features

### Data Loading
- Reads Scotland football results from Excel spreadsheet
- Automatically calculates match results (Win/Draw/Loss)
- Computes goal differences
- Validates data and handles missing columns gracefully

### Statistical Analysis
- **Overall Statistics**: Total matches, wins, draws, losses, win percentage, goals scored/conceded
- **Opposition Analysis**: Performance against each opponent team
- **Venue Analysis**: Home vs Away vs Neutral venue performance  
- **Competition Analysis**: Performance by competition type (World Cup, Euros, Friendlies, etc.)
- **Manager Analysis**: Performance under different managers
- **Year-by-Year Analysis**: Annual performance trends
- **Top Performers**: Identify best scoring opponents and toughest opponents

## Required Excel Format

Your Excel file should contain a worksheet with the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| Date | Match date | 2023-06-15 |
| Opposition | Opponent team name | England |
| Venue | City/ground where match was played | Glasgow |
| Competition | Competition type | World Cup Qualifier |
| Manager | Scotland manager | Steve Clarke |
| Scot | Goals scored by Scotland | 2 |
| Opp | Goals scored by opponent | 1 |
| Scotland Scorers | Goal scorers for Scotland | Dalglish, Law 2 |
| Home\Away | Home/Away/Neutral status | H |

**Note**: The analyzer handles flexible column naming and will work with variations like:
- Goals: `Scot`/`Scotland_Goals`, `Opp`/`Opposition_Goals`  
- Home/Away: `Home\Away`, `Home/Away`, `Home_Away`
- Existing `Result` column (W/D/L) will be used if present

## Usage Examples

### Basic Usage
```python
from src.eta.eta_statistics import ScotlandFootballAnalyzer

# Initialize analyzer with your Excel file
analyzer = ScotlandFootballAnalyzer('scotland_results.xlsx', 'Results')

# Load the data
df = analyzer.load_data()

# Get overall statistics
overall_stats = analyzer.get_overall_statistics()
print(f"Win percentage: {overall_stats['win_percentage']:.1f}%")
```

### Detailed Analysis
```python
# Analyze performance by opposition
opposition_stats = analyzer.analyze_by_opposition()
print("Most frequent opponents:")
print(opposition_stats.head(10))

# Analyze performance by venue
venue_stats = analyzer.analyze_by_venue()
print("Home vs Away performance:")
print(venue_stats)

# Analyze performance by manager
manager_stats = analyzer.analyze_by_manager()
print("Manager records:")
print(manager_stats)

# Get toughest opponents (min 5 matches played)
toughest = analyzer.get_toughest_opponents(min_matches=5, top_n=10)
print("Toughest opponents:")
print(toughest)
```

### Generate Summary Report
```python
# Generate a comprehensive text report
report = analyzer.generate_summary_report()
print(report)
```

## Running the Demo

To see the analyzer in action with sample data:

```bash
python -m src.eta.demo_statistics  
```

This will:
1. Generate realistic sample Scotland football data for the last 30 years
2. Save it to `sample_scotland_results.xlsx`
3. Demonstrate all the analysis features
4. Show formatted output of various statistics

## Running Tests

To run the test suite:

```bash
python -m pytest tests/test_eta_statistics.py -v
```

## Dependencies

- `pandas`: Data manipulation and analysis
- `numpy`: Numerical operations  
- `openpyxl`: Excel file reading/writing
- `pathlib`: File path handling

## Installation

The required dependencies are already included in `requirements.txt`. Install with:

```bash
python -m pip install -r requirements.txt
```

## Customization

You can easily extend the analyzer by:
- Adding new aggregation methods
- Creating custom visualizations
- Adding more sophisticated statistical analyses
- Implementing data export to different formats

## File Structure

```
src/eta/
├── eta_statistics.py      # Main analyzer class
├── demo_statistics.py     # Demo script with sample data
└── ...

tests/ 
├── test_eta_statistics.py # Comprehensive test suite
└── ...
```

Replace the sample data with your actual Scotland football results Excel file and you'll have comprehensive statistics and analysis of their performance over the last 30 years!