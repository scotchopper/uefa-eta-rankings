# UEFA Fixtures Template System - Quick Start Guide

## 🎯 Overview
This system allows you to:
1. **Input all UEFA fixtures** for any time period
2. **Update with results** after games complete
3. **Calculate FIFA ranking changes** automatically
4. **Track multiple competitions** (World Cup Qualifiers, Nations League, Friendlies)

## 📁 Files Created
- `uefa_fixtures_template.py` - Interactive fixture management system
- `csv_fixture_manager.py` - Bulk import/export via CSV
- `uefa_fixtures_template.csv` - Pre-made CSV template with examples

## 🚀 Quick Start Options

### Option 1: Interactive System (Recommended for beginners)
```bash
python uefa_fixtures_template.py
```
- Menu-driven interface
- Add fixtures one by one
- Immediate feedback and validation
- Built-in FIFA ranking calculations

### Option 2: CSV Bulk Management (Best for many fixtures)
```bash
python csv_fixture_manager.py
```
- Create CSV template with examples
- Edit in Excel/Google Sheets
- Import all fixtures at once
- Export results for analysis

## 📝 CSV Template Format

| Column | Description | Example |
|--------|-------------|---------|
| match_id | Unique identifier | WCQ001 |
| date | Match date | 2025-11-14 |
| home_team | Home team name | Scotland |
| away_team | Away team name | Greece |
| competition | Competition type | World Cup Qualifiers |
| importance | FIFA coefficient | 25 (WCQ), 15 (Nations League), 10 (Friendly) |
| venue | Stadium/location | Hampden Park |
| home_goals | Home team goals (empty until played) | 2 |
| away_goals | Away team goals (empty until played) | 1 |
| notes | Additional info | "Home advantage crucial" |
| status | scheduled/completed | scheduled |

## 🎮 Usage Workflow

### Before Games:
1. **Add all fixtures** for the week
2. **Review win probabilities** based on FIFA rankings
3. **Plan scenarios** using the prediction system

### After Games:
1. **Input results** (goals scored)
2. **View ranking changes** automatically calculated
3. **Export data** for further analysis
4. **Save progress** for future reference

## 🏆 Competition Types & Importance Values
- **World Cup Qualifiers**: 25 points
- **Nations League**: 15 points  
- **International Friendlies**: 10 points
- **Regional Championships**: 20 points

## 📊 Features Included
✅ **FIFA Ranking Integration** - Uses real current rankings  
✅ **Win Probability Calculations** - Based on FIFA Elo system  
✅ **Home Advantage** - 100-point boost for home teams  
✅ **Sequential Match Effects** - Rankings update after each game  
✅ **Data Persistence** - Save/load your fixture data  
✅ **Multiple Formats** - Interactive menus or CSV bulk editing  
✅ **Result Tracking** - Goals, outcomes, and notes  
✅ **Automatic Calculations** - Rating changes computed instantly  

## 🎯 Example Scenarios

### Scotland's Week (November 14-17, 2025):
- **Nov 14**: Scotland vs Greece (Home) - WCQ
- **Nov 17**: Denmark vs Scotland (Away) - WCQ

### How to Track:
1. Add both fixtures before Nov 14
2. After Scotland vs Greece, input result
3. This updates Scotland's points for the Denmark game
4. After Denmark vs Scotland, input final result
5. View total ranking change for the week

## 💡 Tips for Best Results
- **Team Names**: Use official FIFA names (system has fuzzy matching)
- **Sequential Updates**: Input results chronologically for accurate tracking
- **Save Regularly**: Use the save function to preserve your work
- **Backup Data**: Export to CSV periodically

## 🔧 Troubleshooting
- **"Team not found"**: Check spelling or use alternative team name
- **"File not found"**: Run `fetch_fifa_rankings.py` first to get current rankings
- **CSV import errors**: Check column headers match exactly

## 📈 Next Steps
After using this template, you can:
- Analyze ranking trajectories over time
- Compare different scenario outcomes  
- Track team performance across competitions
- Export data for visualization tools

---
*This system builds on the FIFA ranking analysis we created for Scotland's World Cup Qualifiers.*