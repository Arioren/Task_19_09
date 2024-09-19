import os

SQL_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:1234@localhost/basketball')
SQLALCHEMY_TRACK_MODIFICATIONS = False