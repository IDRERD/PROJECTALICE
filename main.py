import json

import flask
import logging
import random

app = flask.Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}

cities = {"москва": ["1030494/8268a73fe117c863d035", "1030494/088ba131f5ff7da3af9f"], "нью-йорк": ["1533899/1d07b6e28338e958792f", "1652229/452d32b4fcedbf33e558"], "париж": ["1540737/026f02af5a7d48ed30bf", "1030494/755263442c0656415837"]}
sessionStorage["cities"] = {key for key in cities.keys()}


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
        res['response']['text'] = 'Привет! Назови своё имя!'
        sessionStorage[user_id] = {"first_name": None}
        res["response"]["buttons"] = [{"title": "Помощь", "hide": True}]
        return
    if req["request"]["command"] == "помощь":
        res["response"]["text"] = f"""Это игра на угадывание городов
Городов угадано: {3 - len(sessionStorage["cities"])}"""
        return
    if sessionStorage[user_id]["first_name"] is None:
        first_name = get_first_name(req)
        if first_name is None:
            res["response"]["text"] = "Не расслышала имя. Повтори пожалуйста!"
        else:
            sessionStorage[user_id]["first_name"] = first_name
            res["response"]["text"] = "Приятно познакомиться, " + first_name.title() + ". Я - Алиса. Отгадаешь город по фото?"
            res["response"]["buttons"] = [{"title": i, "hide": True} for i in ["Да", "Нет"]]
    else:
        if not sessionStorage.get("play_flag", False):
            r = len({"да", "нет"}.intersection(set(req["request"]["nlu"]["tokens"])))
            if r != 1:
                res["response"]["text"] = "Не поняла ответа. Да или нет?"
                res["response"]["buttons"] = [{"title": "Помощь", "hide": True}]
                return
            else:
                if "нет" in req["request"]["nlu"]["tokens"]:
                    res["response"]["text"] = "До свидания!"
                    res["response"]["buttons"] = [{"title": "Помощь", "hide": True}]
                    return
                else:
                    sessionStorage["play_flag"] = True
        if sessionStorage.get("play_flag", False):
            if len(sessionStorage["cities"]) == 0 and sessionStorage["img_id"] == -1:
                res["response"]["text"] = "Все города уже отгаданы"
                res["response"]["buttons"] = [{"title": "Помощь", "hide": True}]
                return
            else:
                guess_city(res, req)
    res["response"]["buttons"] = [{"title": "Помощь", "hide": True}]


def get_city(req):
    for entity in req["request"]["nlu"]["entities"]:
        if entity["type"] == "YANDEX.GEO":
            return entity["value"].get("city", None)


def get_first_name(req):
    for entity in req["request"]["nlu"]["entities"]:
        if entity["type"] == "YANDEX.FIO":
            return entity["value"].get("first_name", None)


def guess_city(res, req):
    print(sessionStorage.get("img_id", -1))
    if sessionStorage.get("img_id", -1) == -1:
        sessionStorage["city"] = random.choice(list(sessionStorage["cities"]))
        sessionStorage["cities"].remove(sessionStorage["city"])
        sessionStorage["img_id"] = 0
        res["response"]["text"] = "Попробуйте отгадать этот город"
        load_img(res, req)
        return
    if get_city(req) == sessionStorage["city"]:
        res["response"]["text"] = "Правильно! Сыграем ещё?"
        sessionStorage["play_flag"] = False
        sessionStorage["img_id"] = -1
        if len(sessionStorage["cities"]) == 0:
            res["response"]["text"] = "Поздравляю, вы отгадали все города!"
        return
    else:
        res["response"]["text"] = "Неверно. Попробуйте ещё раз"
        sessionStorage["img_id"] += 1
        if sessionStorage.get("img_id", -1) == 2:
            res["response"]["text"] = "Неправильно. Сыграем ещё?"
            sessionStorage["play_flag"] = False
            sessionStorage["img_id"] = -1
            return
        load_img(res, req)
    # sessionStorage["img_id"] += 1
    return


def load_img(res, req):
    res["response"]["card"] = {}
    res["response"]["card"]["type"] = "BigImage"
    res["response"]["card"]["title"] = res["response"][
        "text"]  # "Вот другая картинка" if sessionStorage["img_id"] else "Попробуйте угадать этот город"
    res["response"]["card"]["image_id"] = cities[sessionStorage["city"]][sessionStorage["img_id"]]


if __name__ == "__main__":
    app.run()