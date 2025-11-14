"""
ETA Scotland Football Statistics - Test Suite

This package contains comprehensive tests for the Scotland football statistics analyzer:

- test_goalscorer_parsing.py: Tests for goalscorer parsing accuracy and known totals
- test_data_quality.py: Tests for duplicate surname detection and data quality
- test_competition_analysis.py: Tests for competition/venue analysis and win rates  
- test_edge_cases.py: Tests for edge cases, robustness, and performance
- test_full_suite.py: Complete test suite runner

Run tests with:
- pytest tests/ -v (full pytest output)
- python tests/test_full_suite.py (custom runner)
- python tests/test_full_suite.py --smoke (quick smoke test)

All tests use the main data file: scot_games_eta_source.xlsx
"""