import math

import requests


def get_coordinates(city_name):
    try:
        url = f"https://geocode-maps.yandex.ru/1.x/"
        params = {"apikey": "40d1649f-0493-4b70-98ba-98533de7710b", "geocode": city_name, "format": "json"}
        response = requests.get(url, params=params)
        js = response.json()
        coordinates_str = js["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
        lng, lat = map(float, coordinates_str.split())
        return lng, lat
    except Exception as e:
        return e


def get_country(city_name):
    try:
        url = f"https://geocode-maps.yandex.ru/1.x/"
        params = {"apikey": "40d1649f-0493-4b70-98ba-98533de7710b", "geocode": city_name, "format": "json"}
        response = requests.get(url, params=params)
        js = response.json()
        return js["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["AddressDetails"]["Country"]["CountryName"]
    except Exception as e:
        return e


def get_distance(p1, p2):
    radius = 6373.0
    lon1 = math.radians(p1[0])
    lat1 = math.radians(p1[1])
    lon2 = math.radians(p2[0])
    lat2 = math.radians(p2[1])
    d_lon = lon2 - lon1
    d_lat = lat2 - lat1
    a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2) ** 2
    c = 2 * math.atan2(a ** 0.5, (1 - a) ** 0.5)
    distance = radius * c
    return distance


def get_geo_info(city_name, type_info):
    if type_info == "coordinates":
        try:
            url = f"https://geocode-maps.yandex.ru/1.x/"
            params = {"apikey": "40d1649f-0493-4b70-98ba-98533de7710b", "geocode": city_name, "format": "json"}
            response = requests.get(url, params=params)
            js = response.json()
            coordinates_str = js["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
            lng, lat = map(float, coordinates_str.split())
            return lng, lat
        except Exception as e:
            return e
    elif type_info == "country":
        try:
            url = f"https://geocode-maps.yandex.ru/1.x/"
            params = {"apikey": "40d1649f-0493-4b70-98ba-98533de7710b", "geocode": city_name, "format": "json"}
            response = requests.get(url, params=params)
            js = response.json()
            return js["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"][
                "GeocoderMetaData"]["AddressDetails"]["Country"]["CountryName"]
        except Exception as e:
            return e