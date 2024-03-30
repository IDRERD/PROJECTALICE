import json
import flask
import logging
import random
import requests
import math
from geo import get_coordinates, get_country, get_distance

app = flask.Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}


@app.route("/", methods=["POST"])
def main():
    # logging.info(f'Request: {flask.request.json!r}')
    # print(flask.request)
    # print(flask.request.json)
    response = {
        "session": flask.request.json["session"],
        "version": flask.request.json["version"],
        "response": {
            "end_session": False
        }
    }
    handle_dialog(flask.request.json, response)
    # logging.info(f'Response: {response!r}')
    # print(response)
    return flask.jsonify(response)


def handle_dialog(req, res):
    user_id = req["session"]["user_id"]
    if req["session"]["new"]:
        res['response']['text'] = 'Привет! Я могу показать город или сказать расстояние между городами!'
        sessionStorage[user_id] = {"first_name": None}
        return
    cities = get_cities(req)
    if not cities:
        res["response"]["text"] = "Ты не написал название ни одного города!"
    elif len(cities) == 1:
        res["response"]["text"] = "Этот город находится в стране " + get_country(cities[0])
    elif len(cities) == 2:
        distance = get_distance(get_coordinates(cities[0]), get_coordinates(cities[1]))
        res["response"]["text"] = "Расстояние между этими городами: " + str(round(distance)) + " км."
    else:
        res["response"]["text"] = "Слишком много городов!"


def get_cities(req):
    cities = []
    for entity in req["request"]["nlu"]["entities"]:
        if entity["type"] == "YANDEX.GEO":
            cities.append(entity["value"].get("city", None))
    return cities


if __name__ == "__main__":
    app.run()