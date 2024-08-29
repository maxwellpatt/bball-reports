from fantraxapi import FantraxAPI
from src.config.config import config

class FantraxAPIWrapper:
    def __init__(self):
        self.league_id = config.FANTRAX_LEAGUE_ID
        self.api = None
        self.is_logged_in = False
        self.league = None

    def login(self):
        try:
            # Create the FantraxAPI instance with league_id and username
            self.api = FantraxAPI(self.league_id, config.FANTRAX_USERNAME)
            # Authenticate separately
            self.api.authenticate(config.FANTRAX_PASSWORD)
            self.is_logged_in = True
            print("Login successful")
        except Exception as e:
            print(f"Login failed: {str(e)}")
            self.is_logged_in = False

    def get_league(self):
        if not self.is_logged_in:
            self.login()
        if self.is_logged_in:
            # Assuming the league information is now directly accessible
            self.league = self.api
            return self.league
        return None

    def get_players(self):
        if not self.league:
            self.get_league()
        if self.league:
            return self.league.get_players()
        return None

    def get_scoring_periods(self):
        if not self.league:
            self.get_league()
        if self.league:
            return self.league.scoring_periods()
        return None

    def logout(self):
        self.is_logged_in = False
        self.league = None
        self.api = None