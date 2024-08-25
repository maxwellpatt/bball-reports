import sqlite3
import pandas as pd
import os
import argparse

def load_csv_to_db(csv_file, table_name, db_name='data/player_data.db'):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Load CSV into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Insert DataFrame into the database
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    # Commit and close the connection
    conn.commit()
    conn.close()

def add_dataset_to_db(dataset_name, root_dir='data', db_name='data/player_data.db'):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().startswith(dataset_name.lower()) and filename.endswith('.csv'):
                file_path = os.path.join(dirpath, filename)
                table_name = os.path.splitext(filename)[0].lower().replace(' ', '_')
                load_csv_to_db(file_path, table_name, db_name)
                print(f"Added {filename} to the database as table {table_name}")
                return
    print(f"No CSV file found for dataset: {dataset_name}")

def load_all_csvs_to_db(root_dir='data', db_name='data/player_data.db'):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.csv'):
                file_path = os.path.join(dirpath, filename)
                table_name = os.path.splitext(filename)[0].lower().replace(' ', '_')
                load_csv_to_db(file_path, table_name, db_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load CSV data into SQLite database")
    parser.add_argument("--dataset", help="Name of the specific dataset to add")
    parser.add_argument("--all", action="store_true", help="Load all CSV files")
    args = parser.parse_args()

    if args.dataset:
        add_dataset_to_db(args.dataset)
    elif args.all:
        load_all_csvs_to_db()
    else:
        print("Please specify either --dataset <name> or --all")


'''
if __name__ == "__main__":
    load_csv_to_db('data/processed/all_player_game_logs_20240820_222851.csv', 'player_game_logs')
    load_csv_to_db('data/processed/fantrax_8_9_24_modified.csv', 'player_fantasy_stats')
    load_csv_to_db('data/all_time_stats/Seasons_Stats.csv', 'all_time_stats')
    load_csv_to_db('data/processed/bball_ref_players_1998_2023.csv', 'players_98_23')
    load_csv_to_db('data/kaggle_data/csv/player.csv', 'players_kaggle')
    load_csv_to_db('data/kaggle_data/csv/game_info.csv', 'game_info_kaggle')
    load_csv_to_db('data/kaggle_data/csv/common_player_info.csv', 'common_player_kaggle')
    load_csv_to_db('data/kaggle_data/csv/team_details.csv', 'team_details_kaggle')
    load_csv_to_db('data/kaggle_data/csv/game_summary.csv', 'games_summary_kaggle')
'''

