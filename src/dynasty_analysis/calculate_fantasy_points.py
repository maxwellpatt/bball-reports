import sqlite3
import pandas as pd

def convert_to_per_game(row):
    """Convert season totals to per-game stats."""
    games_played = row['G']
    if games_played > 0:
        per_game_stats = {
            'AST': row['AST'] / games_played,
            'BLK': row['BLK'] / games_played,
            'FGA': row['FGA'] / games_played,
            'FG': row['FG'] / games_played,
            'FTA': row['FTA'] / games_played,
            'FT': row['FT'] / games_played,
            'PTS': row['PTS'] / games_played,
            'TRB': row['TRB'] / games_played,
            'STL': row['STL'] / games_played,
            '3P': row['3P'] / games_played,
            'TOV': row['TOV'] / games_played,
            # Include any other relevant stats that are cumulative
        }
    else:
        per_game_stats = {key: 0 for key in ['AST', 'BLK', 'FGA', 'FG', 'FTA', 'FT', 'PTS', 'TRB', 'STL', '3P', 'TOV']}
    return per_game_stats

def calculate_fantasy_points(per_game_stats):
    """Calculate fantasy points per game for a player based on league scoring rules."""
    fantasy_points = (
        per_game_stats['AST'] * 2 +
        per_game_stats['BLK'] * 4 +
        per_game_stats['FGA'] * -1 +
        per_game_stats['FG'] * 2 +
        per_game_stats['FTA'] * -1 +
        per_game_stats['FT'] * 1 +
        per_game_stats['PTS'] * 1 +
        per_game_stats['TRB'] * 1 +
        per_game_stats['STL'] * 4 +
        per_game_stats['3P'] * 1 +
        per_game_stats['TOV'] * -2
    )
    return fantasy_points

def add_fantasy_points_column(db_path='data/player_data.db'):
    """Add a Fantasy Points Per Game (FP/G) column to the all-time data."""
    conn = sqlite3.connect(db_path)
    
    # Load the all-time stats data into a DataFrame
    query = "SELECT * FROM all_time_stats"
    all_time_data = pd.read_sql_query(query, conn)
    
    # Convert season totals to per-game stats and calculate fantasy points per game
    fp_per_game = []
    for index, row in all_time_data.iterrows():
        per_game_stats = convert_to_per_game(row)
        fp_per_game.append(calculate_fantasy_points(per_game_stats))
    
    all_time_data['FP/G'] = fp_per_game
    
    # Update the database with the new column
    all_time_data.to_sql('all_time_stats', conn, if_exists='replace', index=False)
    
    conn.close()
    print("Fantasy Points Per Game (FP/G) column added successfully.")

if __name__ == "__main__":
    add_fantasy_points_column()
