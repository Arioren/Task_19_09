from model.team_model import Team
from repository.database import get_db_connection


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
