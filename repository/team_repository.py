from model.team_model import Team
from repository.database import get_db_connection


def add_team_to_database(team: Team) -> int:
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO players (playerId, playerName, position, assists, turnovers, season, games, points, twoPercent, threePercent, team)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
            """,
                           ())
            new_id = cursor.fetchone()['id']
            connection.commit()
            return new_id