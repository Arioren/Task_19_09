from dataclasses import dataclass


@dataclass
class Player:
    playerid:str
    playername:str
    position:str
    assists:int
    turnovers:int
    season:int
    games:int
    points:int
    twopercent:float
    threepercent:float
    team:str
    id:int = None
