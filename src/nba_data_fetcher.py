from nba_api.stats.endpoints import playergamelog, commonplayerinfo
from nba_api.stats.static import players
import pandas as pd

def get_player_id(player_name):
    """Get the NBA player ID for a given player name."""
    nba_players = players.get_players()
    player = [p for p in nba_players if p['full_name'].lower() == player_name.lower()]
    return player[0]['id'] if player else None

def get_player_game_logs(player_name, season='2023-24'):
    """Fetch game logs for a player in a given season."""
    player_id = get_player_id(player_name)
    if not player_id:
        return None
    
    game_log = playergamelog.PlayerGameLog(player_id=player_id, season=season)
    df = game_log.get_data_frames()[0]
    return df

def get_player_info(player_name):
    """Fetch general information about a player."""
    player_id = get_player_id(player_name)
    if not player_id:
        return None
    
    player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
    df = player_info.get_data_frames()[0]
    return df

def get_all_players_game_logs(player_names, season='2023-24'):
    """Fetch game logs for multiple players and combine them into a single DataFrame."""
    all_logs = []
    for player in player_names:
        logs = get_player_game_logs(player, season)
        if logs is not None:
            logs['PLAYER_NAME'] = player  # Add player name to each row
            all_logs.append(logs)
    
    if all_logs:
        return pd.concat(all_logs, ignore_index=True)
    else:
        return None

# Example usage
if __name__ == "__main__":
    # Example: Fetch game logs for a single player
    player_name = "LeBron James"
    logs = get_player_game_logs(player_name)
    if logs is not None:
        print(f"Game logs for {player_name}:")
        print(logs.head())
    else:
        print(f"No data found for {player_name}")

    # Example: Fetch info for a single player
    info = get_player_info(player_name)
    if info is not None:
        print(f"\nPlayer info for {player_name}:")
        print(info)
    else:
        print(f"No info found for {player_name}")

    # Example: Fetch game logs for multiple players
    player_list = ["LeBron James", "Stephen Curry", "Kevin Durant"]
    all_logs = get_all_players_game_logs(player_list)
    if all_logs is not None:
        print(f"\nCombined game logs for multiple players:")
        print(all_logs.head())
    else:
        print("No data found for the specified players")