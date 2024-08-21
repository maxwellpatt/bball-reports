# Basketball Reports

## Purpose
The purpose of this project is multifaceted. The initial ideas are to automate a report that is sent each night containing informatino on player performances, as well as developing a dynasty trade value to assess players relative value in this league format. Here's running list of things I want to accomplish:
- League matchup predictor
- Target trade acquisitions to optimize fantasy playoff schedule

### Repository Structure
```
.
├── LICENSE
├── README.md
├── check_csv.py
├── config
│   ├── config.yaml
│   └── email_config.yml
├── data
│   ├── all_time_stats
│   │   ├── Players.csv
│   │   ├── Seasons_Stats.csv
│   │   └── player_data.csv
│   ├── player_data.db
│   ├── processed
│   │   ├── all_player_game_logs_20240820_222851.csv
│   │   └── fantrax_8_9_24_modified.csv
│   ├── raw
│   │   └── fantrax_8_9_24.csv
│   └── setup_db.py
├── main.py
├── repo_structure.txt
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-312.pyc
│   │   ├── __init__.cpython-38.pyc
│   │   ├── csv_utils.cpython-312.pyc
│   │   ├── csv_utils.cpython-38.pyc
│   │   └── nba_data_fetcher.cpython-312.pyc
│   ├── analysis
│   │   ├── __init__.py
│   │   └── performance_analyzer.py
│   ├── data
│   │   ├── __init__.py
│   │   ├── data_loader.py
│   │   └── player_data.db
│   ├── data_processing
│   │   ├── __pycache__
│   │   ├── fetch_nba_data.py
│   │   └── modify_fantasy_data.py
│   ├── dynasty
│   │   ├── analyze_player_trends.py
│   │   ├── calculate_fantasy_points.py
│   │   ├── dynasty_trade_value.py
│   │   └── kmeans_clustering.py
│   ├── email
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── email_nba_data.py
│   │   └── email_top_nba_performers.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── game.py
│   │   ├── league.py
│   │   ├── players.py
│   │   └── team.py
│   ├── nba_data_fetcher.py
│   └── utils
│       ├── __init__.py
│       ├── __pycache__
│       └── config.py
└── tests
    ├── __init__.py
    ├── test_data_loader.py
    ├── test_email_sender.py
    ├── test_models.py
    └── test_performance_analyzer.py
    
```