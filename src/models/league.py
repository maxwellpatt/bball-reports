from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class Player(BaseModel):
    id: str
    name: str
    team: str
    position: str
    salary: float
    points_per_game: float
    rebounds_per_game: float
    assists_per_game: float
    steals_per_game: float
    blocks_per_game: float

class Team(BaseModel):
    id: str
    name: str
    players: List[Player]

class League(BaseModel):
    id: str
    name: str
    teams: List[Team]
    season_start: date
    season_end: date

def create_league_from_data(data: List[Dict[str, Any]]) -> League:
    # This is where you'll implement the logic to create a League object
    # from the loaded CSV data. For now, we'll return a placeholder.
    return League(
        id="sample_id",
        name="Sample League",
        teams=[],
        season_start=date(2024, 10, 1),
        season_end=date(2025, 4, 30)
    )