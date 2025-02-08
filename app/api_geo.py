import geocoder
import requests
import json

def get_lat_long(ip: str = "me") -> list:
    """Returns the Latitude and Longitude in list format, defaults to"""
    g = geocoder.ip(ip)
    return g.latlng


def get_weather(lat, long):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": long,
        "current_weather": True,
        "temperature_unit": "celsius",
    }
    return requests.get(url=url, params=params).json()


def convert_weather_code(weather_code: str):
    with open("app/weather_codes.json") as weather_codes:
        codes_dict = json.load(weather_codes)
        return codes_dict[weather_code]


def get_weather_conditions():
    lat_long = get_lat_long()
    weather_data = get_weather(lat_long[0], lat_long[1])
    weather_code = weather_data["current_weather"]["weathercode"]
    current_weather = convert_weather_code(str(weather_code))
    return current_weather
