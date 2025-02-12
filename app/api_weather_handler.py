import geocoder
import requests
import json

class ApiWeatherHandler:
    def get_lat_long(self, ip: str = "me") -> list:
        """Returns the Latitude and Longitude in list format, defaults to local ip"""
        g = geocoder.ip(ip)
        return g.latlng


    def get_weather(self, lat, long) -> dict:
        """ Fetch weather data from open-meteo"""
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": long,
            "current_weather": True,
            "temperature_unit": "celsius",
        }
        return requests.get(url=url, params=params).json()


    def convert_weather_code(self, weather_code: str) -> str:
        """ Reads the weather code json file and returns the matching value """
        with open("app/weather_codes.json") as weather_codes:
            codes_dict = json.load(weather_codes)
            return codes_dict[weather_code]


    def get_weather_conditions(self) -> str:
        """ Returns current weather as a string value """
        lat_long = self.get_lat_long()
        weather_data = self.get_weather(lat_long[0], lat_long[1])
        weather_code = weather_data["current_weather"]["weathercode"]
        current_weather = self.convert_weather_code(str(weather_code))
        return current_weather
