from toolz import pipe
from toolz.curried import partial

from model.team_model import Team
from repository.database import get_db_connection
from repository.players_repository import find_player_by_playerid, find_player_position_by_playerid

def find_all_team():
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM team")
            res = cursor.fetchall()
            teams = [Team(**f) for f in res]
            return teams

def add_team_to_database(team: Team) -> int:
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO team (teamname, playeridc, playeridpf, playeridpg, playeridsf, playeridsg)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
            """,
                           (team.teamname,
                            team.playeridc,
                            team.playeridpf,
                            team.playeridpg,
                            team.playeridsf,
                            team.playeridsg))
            new_id = cursor.fetchone()['id']
            connection.commit()
            return new_id

def delete_team_by_id(team_id):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('''DELETE FROM team WHERE id = %s; ''',(team_id,))
            connection.commit()


def find_team_by_id(team_id):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM team WHERE id = %s;",(team_id,))
            res = cursor.fetchone()
            return Team(**res) if len(res) > 0 else None

def team_details(team:Team):
    res = {"name": team.teamname, "players":[]}
    res["players"].append(find_player_by_playerid(team.playeridc))
    res["players"].append(find_player_by_playerid(team.playeridpf))
    res["players"].append(find_player_by_playerid(team.playeridsf))
    res["players"].append(find_player_by_playerid(team.playeridsg))
    res["players"].append(find_player_by_playerid(team.playeridpg))
    return res

def valdition(team:Team):
    player_ids = [team.playeridc, team.playeridpf, team.playeridsf, team.playeridsg, team.playeridpg]
    result = pipe(
        player_ids,
        partial(map,lambda x: find_player_position_by_playerid(x)),
        list,
        set,
        len
    )
    return result == 5


def update_team(team:Team):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('''
            UPDATE team
            SET teamname = %s, playeridpf= %s,  playeridsf= %s,  playeridc= %s,  playeridsg= %s, playeridpg= %s 
            WHERE id = %s
                            ''',(team.teamname, team.playeridpf, team.playeridsf, team.playeridc, team.playeridsg, team.playeridpg, team.id))
            connection.commit()
