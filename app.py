from flask import Flask

from controller.players_controller import player_blueprint
from controller.team_controller import team_blueprint
from repository.database import create_tables
from repository.players_repository import load_players_from_api

app = Flask(__name__)

if __name__ == '__main__':
    create_tables()
    load_players_from_api()
    app.register_blueprint(player_blueprint, url_prefix="/api/players")
    app.register_blueprint(team_blueprint, url_prefix="/api/teams")
    # app.register_blueprint(question_blueprint, url_prefix="/api/question")
    app.run(debug=True)