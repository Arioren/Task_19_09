from dataclasses import asdict

from flask import Blueprint, request, jsonify

from model.respone_model import ResponseDto
from model.team_model import Team
from repository.database import create_tables, create_table_team
from repository.team_repository import add_team_to_database, delete_team_by_id, find_team_by_id, team_details, \
    valdition, find_all_team, update_team

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


@team_blueprint.route("/<int:team_id>", methods=['PUT'])
def update_user_from_internet(team_id):
    json = request.json
    team_to_update:Team = next(filter(lambda x: x.id == team_id, find_all_team()), None)
    if not team_to_update:
        return jsonify(asdict(ResponseDto(message="team doesnt exists"))), 200

    team_to_update.playeridpg = json["playeridpg"]
    team_to_update.playeridsg = json["playeridsg"]
    team_to_update.playeridc = json["playeridc"]
    team_to_update.playeridsf = json["playeridsf"]
    team_to_update.playeridpf = json["playeridpf"]
    team_to_update.teamname = json["teamname"]

    if not valdition(team_to_update):
        return jsonify(asdict(ResponseDto(message="validation error"))), 200

    update_team(team_to_update)

    return jsonify(asdict(ResponseDto(body=team_to_update))), 200
