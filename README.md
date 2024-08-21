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
├── bball_reports
│   ├── bin
│   ├── include
│   ├── lib
│   └── pyvenv.cfg
├── check_csv.py
├── config
│   ├── config.yaml
│   └── email_config.yml
├── data
│   ├── processed
│   ├── raw
│   └── setup_db.py
├── main.py
├── repo_structure.txt
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── analysis
│   ├── data
│   ├── data_processing
│   ├── email
│   ├── models
│   ├── nba_data_fetcher.py
│   ├── notifications
│   └── utils
└── tests
    ├── __init__.py
    ├── test_data_loader.py
    ├── test_email_sender.py
    ├── test_models.py
    └── test_performance_analyzer.py

18 directories, 17 files

    
```