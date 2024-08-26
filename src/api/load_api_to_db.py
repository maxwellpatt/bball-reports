import logging
import sqlite3
from nba_api.stats.endpoints import playercareerstats, leaguedashplayerstats, leaguedashteamstats, leaguedashplayershotlocations, leaguedashplayerclutch
from nba_api.stats.static import players
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Connect to SQLite database
conn = sqlite3.connect('nba_data.db')

def save_to_db(df, table_name):
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    logging.info(f"Saved {len(df)} rows to {table_name}")

def get_all_active_players():
    return [player for player in players.get_players() if player['is_active']]

def load_career_stats():
    active_players = get_all_active_players()
    all_stats = []
    for player in active_players:
        try:
            career = playercareerstats.PlayerCareerStats(player_id=player['id']).get_data_frames()[0]
            career['PLAYER_NAME'] = player['full_name']
            all_stats.append(career)
        except Exception as e:
            logging.error(f"Error fetching career stats for {player['full_name']}: {str(e)}")
    
    if all_stats:
        df = pd.concat(all_stats)
        save_to_db(df, 'player_career_stats')

def load_season_stats(season='2022-23'):
    try:
        stats = leaguedashplayerstats.LeagueDashPlayerStats(season=season).get_data_frames()[0]
        save_to_db(stats, f'player_season_stats_{season.replace("-", "_")}')
    except Exception as e:
        logging.error(f"Error fetching season stats for {season}: {str(e)}")

def load_team_stats(season='2022-23'):
    try:
        stats = leaguedashteamstats.LeagueDashTeamStats(season=season).get_data_frames()[0]
        save_to_db(stats, f'team_stats_{season.replace("-", "_")}')
    except Exception as e:
        logging.error(f"Error fetching team stats for {season}: {str(e)}")

def load_player_shooting_stats(season='2022-23'):
    try:
        stats = leaguedashplayershotlocations.LeagueDashPlayerShotLocations(season=season).get_data_frames()[0]
        save_to_db(stats, f'player_shooting_stats_{season.replace("-", "_")}')
    except Exception as e:
        logging.error(f"Error fetching player shooting stats for {season}: {str(e)}")

def load_player_clutch_stats(season='2022-23'):
    try:
        stats = leaguedashplayerclutch.LeagueDashPlayerClutch(season=season).get_data_frames()[0]
        save_to_db(stats, f'player_clutch_stats_{season.replace("-", "_")}')
    except Exception as e:
        logging.error(f"Error fetching player clutch stats for {season}: {str(e)}")

def main():
    load_career_stats()
    load_season_stats()
    load_team_stats()
    load_player_shooting_stats()
    load_player_clutch_stats()

    conn.close()
    logging.info("Data loading complete")

if __name__ == "__main__":
    main()