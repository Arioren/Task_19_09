from flask import Flask

from repository.database import create_tables
from repository.players_repository import load_players_from_api

app = Flask(__name__)

if __name__ == '__main__':
    create_tables()
    load_players_from_api()
    # app.register_blueprint(fighter_blueprint, url_prefix="/api/user")
    # app.register_blueprint(question_blueprint, url_prefix="/api/question")
    app.run(debug=True)