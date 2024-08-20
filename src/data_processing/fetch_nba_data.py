import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
import time
from datetime import datetime, timedelta
import os

def get_player_id(player_name):
    nba_players = players.get_players()
    player = [p for p in nba_players if p['full_name'].lower() == player_name.lower()]
    return player[0]['id'] if player else None

def fetch_player_data(player_name, season='2023-24'):
    player_id = get_player_id(player_name)
    if not player_id:
        print(f"Player not found: {player_name}")
        return None

    try:
        game_log = playergamelog.PlayerGameLog(player_id=player_id, season=season)
        df = game_log.get_data_frames()[0]
        df['PLAYER_NAME'] = player_name
        return df
    except Exception as e:
        print(f"Error fetching data for {player_name}: {str(e)}")
        return None

def main():

    # Update file paths
    input_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data', 'processed', 'fantrax_8_9_24_modified.csv')
    
    # Read the CSV file
    df = pd.read_csv(input_file)

    # Read the CSV file
    df = pd.read_csv('data/processed/fantrax_8_9_24_modified.csv')
    
    # Filter out players with fantasy_team 'FA'
    df_filtered = df[df['fantasy_team'] != 'FA']

    # Get unique player names
    player_names = df_filtered['Player'].unique()

    all_player_data = []

    for player in player_names:
        print(f"Fetching data for {player}")
        player_data = fetch_player_data(player)
        if player_data is not None:
            all_player_data.append(player_data)
        time.sleep(1)  # To avoid hitting API rate limits

    if all_player_data:
        combined_data = pd.concat(all_player_data, ignore_index=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data', 'processed')
        filename = os.path.join(output_dir, f'all_player_game_logs_{timestamp}.csv')
        combined_data.to_csv(filename, index=False)
        print(f"Data fetched and saved successfully to {filename}.")
        return filename
    else:
        print("No data was fetched.")
        return None

if __name__ == "__main__":
    main()