import logging
from nba_api.stats.endpoints import playercareerstats, leaguedashplayerstats
from nba_api.stats.static import players
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_player_career_stats(player_id):
    try:
        career = playercareerstats.PlayerCareerStats(player_id=player_id)
        df = career.get_data_frames()[0]
        logging.info(f"Successfully fetched career stats for player {player_id}")
        logging.info(f"Number of seasons: {len(df)}")
        return True
    except Exception as e:
        logging.error(f"Error fetching career stats for player {player_id}: {str(e)}")
        return False

def test_league_dash_player_stats(season):
    try:
        stats = leaguedashplayerstats.LeagueDashPlayerStats(season=season)
        df = stats.get_data_frames()[0]
        logging.info(f"Successfully fetched player stats for season {season}")
        logging.info(f"Number of players: {len(df)}")
        return True
    except Exception as e:
        logging.error(f"Error fetching player stats for season {season}: {str(e)}")
        return False

def test_static_player_data():
    try:
        all_players = players.get_players()
        logging.info(f"Successfully fetched static player data")
        logging.info(f"Number of players: {len(all_players)}")
        return True
    except Exception as e:
        logging.error(f"Error fetching static player data: {str(e)}")
        return False

def main():
    # Test player career stats (using LeBron James' ID)
    test_player_career_stats(2544)
    
    # Test league dash player stats for last season (2022-23)
    test_league_dash_player_stats('2022-23')
    
    # Test static player data
    test_static_player_data()

if __name__ == "__main__":
    main()