from toolz import pipe

import requests
from toolz.curried import partial


def get_players_by_api(season):
    url = lambda x: \
        f"http://b8c40s8.143.198.70.30.sslip.io/api/PlayerDataTotals/season/{x}"
    try:
        response = requests.request("GET", url(season))
        return pipe(
            response.json(),
            partial(map,
                    lambda x: {
                        "playerId":x["playerId"],
                        'playerName': x['playerName'],
                        'position': x["position"],
                        "games": x['games'],
                        'points': x["points"],
                        "season": x["season"],
                        "assists": x['assists'],
                        "turnovers":x["turnovers"],
                        "twoPercent":x["twoPercent"],
                        "threePercent":x["threePercent"],
                        "team":x["team"]}),
            list
        )
    except Exception as e:
        print(e)
        return []