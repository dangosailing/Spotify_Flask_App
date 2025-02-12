from app.api_geo import get_lat_long, get_weather, convert_weather_code, get_weather_conditions

def test_get_lat_long():
  """
  GIVEN a get_lat_long function
  WHEN calling the function
  THEN make sure the return value is of list type with correct length and that the values are floats
  """
  result = get_lat_long()  
  assert isinstance(result, list) # make sure the return type is list 
  assert all(isinstance(item, float) for item in result) # make sure the return values are floats 
  assert len(result) == 2 # make sure that the list only contains the two coordinates

def test_get_weather_with_fixture(mocker):
  """
  GIVEN the get_weather function with a mock fixture to simulate the API resposne
  WHEN calling the function with test coordinates
  THEN make sure the return value is a dict that matches the supplied mock response
  """
  test_coords = [10, -21]
  weather_mock_data = {'latitude': -21.0,
 'longitude': 10.0,
 'generationtime_ms': 0.03266334533691406,
 'utc_offset_seconds': 0,
 'timezone': 'GMT',
 'timezone_abbreviation': 'GMT',
 'elevation': 0.0,
 'current_weather_units': {'time': 'iso8601',
                           'interval': 'seconds',
                           'temperature': '°C',
                           'windspeed': 'km/h',
                           'winddirection': '°',
                           'is_day': '',
                           'weathercode': 'wmo code'},
 'current_weather': {'time': '2025-02-12T12:15',
                     'interval': 900,
                     'temperature': 21.4,
                     'windspeed': 18.4,
                     'winddirection': 174,
                     'is_day': 1,
                     'weathercode': 2}}
  
  # Using pytest-mock fixture to set up a mock json response
  mock_response = mocker.MagicMock()
  mock_response.json.return_value = weather_mock_data

  # For this test we patch the request method used in get weather
  # to use our mock data instead of pinging the actual external API
  mocker.patch("requests.get", return_value=mock_response)

  result = get_weather(lat=test_coords[0], long=test_coords[1])
  assert type(result) is dict
  assert result == weather_mock_data

def test_convert_weather_code() -> str:
  """
  GIVEN the convert_weather_code function
  WHEN calling the function with a weather code
  THEN make sure the return value matches the correct weather code value
  """
  weather_codes = {
  "0": "Clear sky", 
  "1": "Mainly clear",
  "2": "partly cloudy",
  "3": "Overcast",
  "45": "Fog",
  "48": "Depositing rime fog",
  "51": "Drizzle: Light",
  "53": "Drizzle: Moderate",
  "55": "Drizzle: Dense",
  "56": "Freezing Drizzle: Light",
  "57": "Freezing Drizzle: Dense",
  "61": "Rain: Slight",
  "63": "Rain: Moderate",
  "65": "Rain: Heavy",
  "66": "Freezing Rain: Light",
  "67": "Freezing Rain: Heavy",
  "71": "Snow fall: Slight",
  "73": "Snow fall: Moderate",
  "75": "Snow fall: Heavy",
  "77": "Snow grains",
  "80": "Rain Showers: Slight",
  "81": "Rain Showers: Moderate",
  "82": "Rain Showers: Violent",
  "85": "Snow showers: Slight",
  "86": "Snow showers: Heavy",
  "95": "Thunderstorm: Slight",
  "96": "Thunderstorm with slight hail",
  "99": "Thunderstorm with heavy hail"
}
  result = convert_weather_code("45")
  assert result == weather_codes["45"] # Fog
