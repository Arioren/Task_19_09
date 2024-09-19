from dataclasses import asdict

from flask import Blueprint, request, jsonify

from model.respone_model import ResponseDto
from model.team_model import Team
from repository.database import create_tables, create_table_team
from repository.team_repository import add_team_to_database

team_blueprint = Blueprint("team", __name__)

@team_blueprint.route("/", methods=['POST'])
def create_team():
    json = request.json

    #From the data class settings there will be an error if not all the data is complete
    my_team = Team(**json)

    #return jsonify(asdict(ResponseDto(message="validation error"))), 200
    create_table_team()
    add_team_to_database(my_team)
    return jsonify(asdict(ResponseDto(body=my_team))), 200
