import json

import flask
import logging
import random

app = flask.Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}

cities = {"москва": ["1030494/8268a73fe117c863d035", "1030494/088ba131f5ff7da3af9f"], "нью-йорк": ["1533899/1d07b6e28338e958792f", "1652229/452d32b4fcedbf33e558"], "париж": ["1540737/026f02af5a7d48ed30bf", "1030494/755263442c0656415837"]}


@app.route("/", methods=["POST"])
def main():
    # logging.info(f'Request: {flask.request.json!r}')
    print(flask.request)
    print(flask.request.json)
    response = {
        "session": flask.request.json["session"],
        "version": flask.request.json["version"],
        "response": {
            "end_session": False
        }
    }
    handle_dialog(flask.request.json, response)
    # logging.info(f'Response: {response!r}')
    print(response)
    return flask.jsonify(response)


def handle_dialog(req, res):
    user_id = req["session"]["user_id"]
    if req["session"]["new"]:
        res['response']['text'] = 'Привет! Назови своё имя!'
        sessionStorage[user_id] = {"first_name": None}
        return
    if sessionStorage[user_id]["first_name"] is None:
        first_name = get_first_name(req)
        if first_name is None:
            res["response"]["text"] = "Не расслышала имя. Повтори пожалуйста!"
        else:
            sessionStorage[user_id]["first_name"] = first_name
            res["response"]["text"] = "Приятно познакомиться, " + first_name.title() + ". Я - Алиса. Какой город хочешь увидеть?"
            res["response"]["buttons"] = [{"title": city.title(), "hide": True} for city in cities]
    else:
        city = get_city(req)
        if city in cities:
            res["response"]["card"] = {}
            res["response"]["card"]["type"] = "BigImage"
            res["response"]["card"]["title"] = "Этот город я знаю"
            res["response"]["card"]["image_id"] = random.choice(cities[city])
            res["response"]["text"] = "Я угадала!"
        else:
            res["response"]["text"] = "Первый раз слышу об этом городе. Попробуй ещё раз!"


def get_city(req):
    for entity in req["request"]["nlu"]["entities"]:
        if entity["type"] == "YANDEX.GEO":
            return entity["value"].get("city", None)


def get_first_name(req):
    for entity in req["request"]["nlu"]["entities"]:
        if entity["type"] == "YANDEX.FIO":
            return entity["value"].get("first_name", None)


if __name__ == "__main__":
    app.run()