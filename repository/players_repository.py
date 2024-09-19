from typing import List

from api.players_api import get_players_by_api
from model.players_mpdel import Player
from repository.database import get_db_connection


def load_players_from_api():
    all_players = find_all_players()
    if all_players and len(all_players) > 0:
        return
    players_json = get_players_by_api(2024)
    players_json += get_players_by_api(2023)
    players_json += get_players_by_api(2022)
    for f in [Player(**f) for f in players_json]:
        create_player(f)



def find_all_players()->List[Player]:
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM players")
            res = cursor.fetchall()
            players = [Player(**f) for f in res]
            return players


def create_player(player: Player) -> int:
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO players (playerId, playerName, position, assists, turnovers, season, games, points)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
            """,
                           (player.playerId,
                            player.playerName,
                            player.position,
                            player.assists,
                            player.turnovers,
                            player.season,
                            player.games,
                            player.points))
            new_id = cursor.fetchone()['id']
            connection.commit()
            return new_id