import sqlite3
import os
import pandas as pd

def fetch_game_logs():
    db_path = os.path.join('data', 'player_data.db')
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM player_game_logs"
    game_logs_df = pd.read_sql_query(query, conn)
    conn.close()
    return game_logs_df

def fetch_fantasy_stats():
    db_path = os.path.join('data', 'player_data.db')
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM player_fantasy_stats"
    fantasy_stats_df = pd.read_sql_query(query, conn)
    conn.close()
    return fantasy_stats_df

def main():
    # Fetch data from the database
    game_logs = fetch_game_logs()
    fantasy_stats = fetch_fantasy_stats()

    # Example: Print the first few rows of each dataframe
    print("Game Logs Data:")
    print(game_logs.head())

    print("\nFantasy Stats Data:")
    print(fantasy_stats.head())

    # You can now add additional processing, analysis, or reporting based on the data

if __name__ == "__main__":
    main()
