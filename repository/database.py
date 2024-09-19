import psycopg2
from psycopg2.extras import RealDictCursor

from config.sql_config import SQL_URI


def get_db_connection():
    return psycopg2.connect(SQL_URI,cursor_factory=RealDictCursor)

def create_tables():
    create_my_table("""
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                playerId VARCHAR(100) NOT NULL,
                playerName VARCHAR(100) NOT NULL,
                position VARCHAR(100) NOT NULL,
                assists INT,
                turnovers INT,
                season INT,      
                games INT,
                points INT,
                twoPercent FLOAT,
                threePercent FLOAT,
                team VARCHAR(100)
                )
    """)



def create_my_table(command: str):
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(command)
            connection.commit()