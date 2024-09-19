from dataclasses import dataclass


@dataclass
class Team:
    teamname:str
    playeridc:str
    playeridpf:str
    playeridsf:str
    playeridsg:str
    playeridpg:str
    id:int = None