from flask import Blueprint, request, jsonify

from repository.players_repository import filter_players_by_position_and_season, filter_players_by_position

player_blueprint = Blueprint("player", __name__)

@player_blueprint.route("/", methods=['GET'])
def search_players_by_position_and_season():
    position = request.args.get("position")
    season = request.args.get("season")
    if season:
        res = filter_players_by_position_and_season(position, season)
    else:
        res = filter_players_by_position(position)
    return jsonify(res), 200