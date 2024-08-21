import sqlite3
import pandas as pd

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

    print(f"Data from {csv_file} loaded into {table_name} table.")

if __name__ == "__main__":
    # Example usage
    load_csv_to_db('data/processed/all_player_game_logs_20240820_222851.csv', 'player_game_logs')
    load_csv_to_db('data/processed/fantrax_8_9_24_modified.csv', 'player_fantasy_stats')
    load_csv_to_db('data/all_time_stats/Seasons_Stats.csv', 'all_time_stats')
