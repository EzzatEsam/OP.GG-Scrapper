from enum import Enum
from dataclasses import dataclass


class GameResult(Enum):
    WIN = 1
    LOSE = 2
    REMAKE = 3

class Team(Enum):
    RED = 1
    BLUE = 2




@dataclass
class GameRecordPlayer :
    name : str
    champion : str
    rank : int
    kda : str 
    damage_given : int
    damage_taken : int
    cs : int
    vision : list[int] # [control wards , wards placed , wards destroyed]
    summoner_spells : list[str]
    runes : list[str]
    items : list[str]


# class for lol game
@dataclass
class GameRecord :
    result : GameResult
    winning_team : Team
    game_type : str
    game_time_seconds : int 
    red_team_players : list[GameRecordPlayer]
    blue_team_players : list[GameRecordPlayer]

    red_team_barons : int
    blue_team_barons : int

    red_team_dragons : int
    blue_team_dragons : int

    red_team_towers : int
    blue_team_towers : int

    record_owner : str 
    owner_champion : str
    

@dataclass
class Player :
    name : str
    rank : str
    lp : int
    level : int
    wins : int
    losses : int
    most_played_champs : list[str , str , str]
    games : list[GameRecord]
    
    def __str__(self):
        return f"Name: {self.name}\nRank: {self.rank}\nLP: {self.lp}\nLevel: {self.level}\nWins: {self.wins}\nLosses: {self.losses}\nMost Played Champions: {', '.join(self.most_played_champs)}"
