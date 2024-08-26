import logging
from datetime import datetime, timedelta
import sqlite3
from nba_api.stats.endpoints import leaguegamefinder, boxscoretraditionalv2
import pandas as pd
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_games_for_date(date):
    try:
        # Convert date string to datetime object
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        season = f"{date_obj.year}-{str(date_obj.year + 1)[-2:]}"
        
        # Fetch all games for the season
        games = leaguegamefinder.LeagueGameFinder(season_nullable=season).get_data_frames()[0]
        
        # Filter games for the specific date
        games_for_date = games[games['GAME_DATE'] == date]
        
        # Group by GAME_ID to get both teams for each game
        grouped_games = games_for_date.groupby('GAME_ID').agg({
            'TEAM_ID': lambda x: list(x),
            'MATCHUP': 'first',
            'GAME_DATE': 'first'
        }).reset_index()
        
        # Ensure we have exactly two teams per game
        grouped_games = grouped_games[grouped_games['TEAM_ID'].apply(len) == 2]
        
        # Create separate columns for each team
        grouped_games['TEAM_ID_1'] = grouped_games['TEAM_ID'].apply(lambda x: x[0])
        grouped_games['TEAM_ID_2'] = grouped_games['TEAM_ID'].apply(lambda x: x[1])
        
        return grouped_games[['GAME_ID', 'TEAM_ID_1', 'TEAM_ID_2', 'MATCHUP', 'GAME_DATE']]
    except Exception as e:
        logging.error(f"Error fetching games for {date}: {str(e)}")
        return None

def get_player_stats(game_id):
    try:
        box_score = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id).get_data_frames()[0]
        return box_score[['GAME_ID', 'TEAM_ID', 'PLAYER_ID', 'PLAYER_NAME', 'MIN', 'PTS', 'REB', 'AST']]
    except Exception as e:
        logging.error(f"Error fetching player stats for game {game_id}: {str(e)}")
        return None

def save_to_database(conn, df, table_name):
    if df is not None and not df.empty:
        df.to_sql(table_name, conn, if_exists='append', index=False)
    else:
        logging.warning(f"No data to save for {table_name}")

def fetch_and_save_nba_data(date):
    conn = sqlite3.connect('nba_data.db')
    
    games = get_games_for_date(date)
    if games is not None and not games.empty:
        save_to_database(conn, games, 'games')
        
        for _, game in games.iterrows():
            for team_id in [game['TEAM_ID_1'], game['TEAM_ID_2']]:
                player_stats = get_player_stats(game['GAME_ID'])
                if player_stats is not None:
                    team_stats = player_stats[player_stats['TEAM_ID'] == team_id]
                    save_to_database(conn, team_stats, 'player_stats')
    else:
        logging.warning(f"No games data available for {date}")
    
    conn.close()

def main():
    # For testing, we'll use April 3, 2023
    test_date = '2023-04-03'
    
    while True:
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        try:
            # Use the test date for demonstration
            fetch_and_save_nba_data(test_date)
            logging.info(f"Data fetched and saved for {test_date}")
        except Exception as e:
            logging.error(f"Error in main loop: {str(e)}")
        
        # In real scenario, uncomment the following line and comment out the test_date usage
        # fetch_and_save_nba_data(current_date)
        # logging.info(f"Data fetched and saved for {current_date}")
        
        # Wait for 24 hours before the next fetch
        # time.sleep(24 * 60 * 60)

if __name__ == "__main__":
    main()