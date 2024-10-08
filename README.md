# Fantasy Basketball Knowledge Vault 

## Purpose
The purpose of this project is multifaceted. The initial ideas are to automate a report that is sent each night containing informatino on player performances, as well as developing a dynasty trade value to assess players relative value in this league format. Here's running list of things I want to accomplish:
- League matchup predictor
- Target trade acquisitions to optimize fantasy playoff schedule

### Repository Structure
```
.
├── LICENSE
├── README.md
├── config
│   ├── config.yaml
│   └── email_config.yml
├── data
│   ├── __pycache__
│   │   └── setup_db.cpython-312.pyc
│   ├── clean_fantrax.py
│   ├── databases
│   │   ├── nba.sqlite
│   │   └── player_data.db
│   ├── player_data.db
│   ├── processed
│   │   ├── all_player_game_logs_20240820_222851.csv
│   │   ├── bball_ref_players_1998_2023.csv
│   │   ├── fantrax_8_9_24_modified.csv
│   │   └── fpts_since_1998.csv
│   ├── raw
│   │   ├── all_time_stats
│   │   │   ├── Players.csv
│   │   │   ├── Seasons_Stats.csv
│   │   │   └── player_data.csv
│   │   ├── fantrax_8_9_24.csv
│   │   └── kaggle_data
│   │       └── csv
│   │           ├── common_player_info.csv
│   │           ├── draft_combine_stats.csv
│   │           ├── draft_history.csv
│   │           ├── game.csv
│   │           ├── game_info.csv
│   │           ├── game_summary.csv
│   │           ├── inactive_players.csv
│   │           ├── line_score.csv
│   │           ├── officials.csv
│   │           ├── other_stats.csv
│   │           ├── play_by_play.csv
│   │           ├── player.csv
│   │           ├── team.csv
│   │           ├── team_details.csv
│   │           ├── team_history.csv
│   │           └── team_info_common.csv
│   └── setup_db.py
├── images
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
│   │   └── play_by_play_analysis.ipynb
│   ├── data_processing
│   │   ├── __pycache__
│   │   │   ├── fetch_nba_data.cpython-38.pyc
│   │   │   └── modify_fantasy_data.cpython-38.pyc
│   │   ├── bball_ref_scrape.ipynb
│   │   ├── fetch_nba_data.py
│   │   └── modify_fantasy_data.py
│   ├── dynasty_analysis
│   │   ├── analyze_player_trends.py
│   │   ├── calculate_fantasy_points.py
│   │   ├── career_trajectory.py
│   │   ├── dynasty_trade_value.py
│   │   ├── expl.ipynb
│   │   └── kmeans_clustering.py
│   ├── email
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-38.pyc
│   │   │   └── email_nba_data.cpython-38.pyc
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
│       │   ├── __init__.cpython-38.pyc
│       │   └── config.cpython-38.pyc
│       └── config.py
└── tests
    ├── __init__.py
    ├── test_data_loader.py
    ├── test_email_sender.py
    ├── test_models.py
    └── test_performance_analyzer.py
    
```
