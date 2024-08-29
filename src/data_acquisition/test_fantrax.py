from fantraxapi import FantraxAPI
from src.config.config import config

class FantraxAPIWrapper:
    def __init__(self):
        self.league_id = config.FANTRAX_LEAGUE_ID
        self.api = FantraxAPI(self.league_id)
        self.is_logged_in = False

    def login(self):
        try:
            # The FantraxAPI now uses authenticate method
            self.api.authenticate(config.FANTRAX_USERNAME, config.FANTRAX_PASSWORD)
            self.is_logged_in = True
            print("Login successful")
        except Exception as e:
            print(f"Login failed: {str(e)}")
            self.is_logged_in = False

    def get_league(self):
        if not self.is_logged_in:
            self.login()
        if self.is_logged_in:
            return self.api  # The API object itself represents the league

    def get_players(self):
        league = self.get_league()
        if league:
            return league.get_players()
        return None

    def get_scoring_periods(self):
        league = self.get_league()
        if league:
            return league.scoring_periods()
        return None

    def logout(self):
        self.is_logged_in = False