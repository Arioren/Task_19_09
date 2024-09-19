from dataclasses import dataclass
from typing import List


@dataclass
class Team:
    team_name:str
    ids_player:List[str]