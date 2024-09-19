from dataclasses import asdict

from flask import Blueprint, request, jsonify

from model.respone_model import ResponseDto
from model.team_model import Team
from repository.database import create_tables, create_table_team
from repository.team_repository import add_team_to_database, delete_team_by_id, find_team_by_id, team_details, valdition

team_blueprint = Blueprint("team", __name__)

@team_blueprint.route("/", methods=['POST'])
def create_team():
    json = request.json

    my_team = Team(**json)
    if not valdition(my_team):
        return jsonify(asdict(ResponseDto(message="validation error"))), 200
    create_table_team()
    new_id = add_team_to_database(my_team)
    return jsonify(asdict(ResponseDto(body=new_id))), 200


@team_blueprint.route("/delete/<int:team_id>", methods=['DELETE'])
def delete_team(team_id):
    delete_team_by_id(team_id)
    return jsonify(asdict(ResponseDto(message="team deleted or never existed"))), 200

@team_blueprint.route("/<int:team_id>", methods=['GET'])
def find_by_id(team_id):
    team = find_team_by_id(team_id)
    result = team_details(team)
    return jsonify(asdict(ResponseDto(body=result))), 200
