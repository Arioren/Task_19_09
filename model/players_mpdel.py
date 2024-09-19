from dataclasses import dataclass


@dataclass
class Player:
    playerId:str
    playerName:str
    position:str
    assists:int
    turnovers:int
    season:int
    games:int
    points:int
    id:int = None
