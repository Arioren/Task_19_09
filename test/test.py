from datetime import timedelta
from tkinter import Listbox
from typing import List

import pytest
from flask import Flask

from controller.team_controller import team_blueprint
from model.players_mpdel import Player
from repository.database import get_db_connection
from repository.players_repository import find_all_players, create_player, filter_players_by_position


# @pytest.fixture(scope="module")
# def setup_database():
#     with get_db_connection() as connection:
#         with connection.cursor() as cursor:
#             yield cursor


def test_to_find_all_players():
    res = find_all_players()
    assert len(res) > 2000

def test_to_filter_players_by_position():
    res = filter_players_by_position("PG")
    assert len(res) > 50


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(team_blueprint)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_search_team(client):
    response = client.get('/3')
    assert response.status_code == 200
