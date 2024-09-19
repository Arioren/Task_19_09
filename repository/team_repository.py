from model.team_model import Team
from repository.database import get_db_connection
from repository.players_repository import find_player_by_playerid, find_player_position_by_playerid


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
    tmp_array = []
    tmp_array.append(find_player_position_by_playerid(team.playeridc))
    tmp_array.append(find_player_position_by_playerid(team.playeridpf))
    tmp_array.append(find_player_position_by_playerid(team.playeridsf))
    tmp_array.append(find_player_position_by_playerid(team.playeridsg))
    tmp_array.append(find_player_position_by_playerid(team.playeridpg))
    return len(set(tmp_array)) == 5
