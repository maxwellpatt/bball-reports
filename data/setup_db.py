import sqlite3
import os
import pandas as pd

def setup_database():
    db_path = os.path.join(os.path.dirname(__file__), 'player_data.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_game_logs (
            SEASON_ID INTEGER,
            Player_ID INTEGER,
            Game_ID INTEGER,
            GAME_DATE TEXT,
            MATCHUP TEXT,
            WL TEXT,
            MIN INTEGER,
            FGM INTEGER,
            FGA INTEGER,
            FG_PCT REAL,
            FG3M INTEGER,
            FG3A INTEGER,
            FG3_PCT REAL,
            FTM INTEGER,
            FTA INTEGER,
            FT_PCT REAL,
            OREB INTEGER,
            DREB INTEGER,
            REB INTEGER,
            AST INTEGER,
            STL INTEGER,
            BLK INTEGER,
            TOV INTEGER,
            PF INTEGER,
            PTS INTEGER,
            PLUS_MINUS REAL,
            PLAYER_NAME TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_fantasy_stats (
            ID TEXT PRIMARY KEY,
            Player TEXT,
            Team TEXT,
            Position TEXT,
            RkOv INTEGER,
            fantasy_team TEXT,
            Age INTEGER,
            Opponent TEXT,
            FPts REAL,
            FP_G REAL,
            FGM REAL,
            FGA REAL,
            FTM REAL,
            FTA REAL,
            PTS REAL,
            REB REAL,
            AST REAL,
            ST REAL,
            BLK REAL,
            "TO" REAL
            -- Remove PTM, D3, and D2 if they are not in the CSV file
        )
    ''')

    conn.commit()
    conn.close()

def load_and_insert_data_from_processed():
    db_path = os.path.join(os.path.dirname(__file__), 'player_data.db')
    processed_folder_path = os.path.join(os.path.dirname(__file__), 'processed')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Load and insert the game logs data
    game_logs_path = os.path.join(processed_folder_path, 'all_player_game_logs_20240820_222851.csv')
    if os.path.exists(game_logs_path):
        game_logs_df = pd.read_csv(game_logs_path)
        game_logs_df.to_sql('player_game_logs', conn, if_exists='append', index=False)

    # Load and insert the fantasy stats data
    fantasy_stats_path = os.path.join(processed_folder_path, 'fantrax_8_9_24_modified.csv')
    if os.path.exists(fantasy_stats_path):
        fantasy_stats_df = pd.read_csv(fantasy_stats_path)
        
        # Rename problematic columns
        fantasy_stats_df.rename(columns={'FP/G': 'FP_G'}, inplace=True)
        
        # Align DataFrame columns with SQL table, ignore missing columns
        expected_columns = [
            "ID", "Player", "Team", "Position", "RkOv", "fantasy_team", "Age", "Opponent",
            "FPts", "FP_G", "FGM", "FGA", "FTM", "FTA", "PTS", "REB", "AST", "ST", "BLK", "TO"
        ]
        available_columns = [col for col in expected_columns if col in fantasy_stats_df.columns]
        fantasy_stats_df = fantasy_stats_df[available_columns]

        # Insert into the database
        fantasy_stats_df.to_sql('player_fantasy_stats', conn, if_exists='append', index=False)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
    load_and_insert_data_from_processed()
    print("Database setup and data insertion complete.")
