from functools import reduce
from typing import List

from click import command
from toolz import pipe
from toolz.curried import groupby, partial

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
                INSERT INTO players (playerId, playerName, position, assists, turnovers, season, games, points, twoPercent, threePercent, team)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
            """,
                           (player.playerid,
                            player.playername,
                            player.position,
                            player.assists,
                            player.turnovers,
                            player.season,
                            player.games,
                            player.points,
                            player.twopercent,
                            player.threepercent,
                            player.team))
            new_id = cursor.fetchone()['id']
            connection.commit()
            return new_id


def filter_players_by_position_and_season(position, season):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                '''
                SELECT DISTINCT playerName FROM players
                WHERE position = %s AND season = %s
                '''
            , (position, season))
            res = cursor.fetchall()
            player_names = [row["playername"] for row in res]
            return convert_res_to_the_requirements(player_names)

def filter_players_by_position(position):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                '''
                SELECT DISTINCT playerName FROM players
                WHERE position = %s
                '''
            , (position,))
            res = cursor.fetchall()
            player_names = [row["playername"] for row in res]
            return convert_res_to_the_requirements(player_names)

def convert_res_to_the_requirements(names):
    res= {}
    for name in names:
        res[name] = get_statistics(name)
    return res

def get_statistics(name:str):
    result = {}
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                '''
                SELECT * FROM players
                WHERE playerName = %s;
                '''
            , (name,))
            res = cursor.fetchall()
            players = [Player(**f) for f in res]
            result["team"] = players[0].team
            result["position"] = players[0].position
            result["season"] = list(set([player.season for player in players]))
            result["points"] = sum([player.points for player in players])
            result["games"] = sum([player.games for player in players])
            two_percents = [player.twopercent for player in players if player.twopercent is not None]
            result["twoPercent"] = sum(two_percents) / len(two_percents) if two_percents else 0
            three_percents = [player.threepercent for player in players if player.threepercent is not None]
            result["threePercent"] = sum(three_percents) / len(three_percents) if three_percents else 0
            total_assists = sum([player.assists for player in players if player.assists is not None])
            total_turnovers = sum([player.turnovers for player in players if player.turnovers is not None])
            result["ATR"] = total_assists / total_turnovers if total_turnovers != 0 else None
            result["PPG Ratio"] = calculate_ppg(result["points"]/result["games"], result["position"])
            return result

def calculate_ppg(score, position):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                '''
                SELECT SUM(points)/ SUM(games) AS sum FROM players
                WHERE position = %s
                '''
            , (position,))
            res = cursor.fetchone()["sum"]
            return score/ res if res else 0