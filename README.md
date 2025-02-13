# Spotify App
An app to help manage your playlists and get an overview of your
spotify profile, favorite artists and favorite tracks:
- Search and add tracks to recent playlists
- Create playlists
- Unfollow playlists
- Remove specific tracks from playlists
- You can also create backups of your favorite playlists that are stored in the database that can be used to restore them even if you unfollow them from spotify and loose track of them!
- You can also view data for artist popularity via the "artists stats"
for your top artists to see how their latest singles measure up using the spotifys own popularity (0-100) ranking
- When run, the app uses your local IP address to approximate your
location and feed you the current weather. This is also used to generate
a track suggestion to fit the weather in the embeded spotify player on
your home-page!
- The app uses the spotify oauth flow to guarantee that you
are aware of what data the app has access to when you´re using it
- No sensitive data is stored in the database and no information is used
to corellate your spotify profile with personal information

## APIs
spotify -  used to fetch user profile, songs, playlists and artists data and alter user playlists (API key required)\
open meteo - to fetch weather data to display on home page. The current weather is used to generate a query for a matching track (open API)\

## Dependencies
**spotipy** - handles auth and spotify api requests\
**flask** - webserver interface and session storage of token\
**flask-wtf** - include CSRF protection on forms\
**pandas** - data management\
**numpy** - data management\
**matplotlib** - data visualization (ie create the plot)\
**pytest** - for testing code\
**pytest-cov** - for testing code coverage (pytest --cov=app tests/)\
**pytest-mock** - sets up a mock fixture to help test requests against external api (open-meteo for this app)\
**bcrypt** - for secure password management\
**geocoder** - get coordinates from local ip for weather API\

# How to run project
This project requires either to be registered as a user for my spotify application or to create an application on https://developer.spotify.com/.
You can also contact me if you want to be added as a test user for existing application instead.
The CLIENT_ID and CLIENT_SECRET are acquired from the registered spotify application along with the REDIRECT_URI. Make sure these line up with what you have in the Config file! 
## Registering a spotify applicaiton 
1) Visit https://developer.spotify.com/.
2) You can use an existing spotify account or create an account to sign in.
3) Select dashboard -> create app -> fill in required details. When the app is created you access the "User management" tab and add the email and name for the
spotify account you want to have access. The spotify profile used to register the app itself is automatically registered as an approved user.
4) Grab the CLIENT_ID, CLIENT_SECRET and REDIRECT_URI and put them in the config file! The REDIRECT_URI is the route that spotify will redirect you back to
once the authorization is completed and you´re provided the proper access token from spotify. 

```console
python -m venv venv
```
```console
source venv/Scripts/activate
```
```console
pip install -r requirements.txt
```
rename config_base.py to config.py and enter values for:\
**CLIENT_ID** (from spotify api)\
**CLIENT_SECRET** (from spotify api)\
**SECRET_KEY** (set appropriately - this is used to sign the session cookie and csrf token )\
You get the CLIENT_ID and CLIENT_SECRET from the spotify application you registered online
```console
py main.py
```

# Testing
```console
pytest -v
```
if you want to run the existing tests
These cover the api_geo module and create_user method
the pytest-mock library is used to generate the mock fixture used to 
simulate an API response so the tests to do not contact an exterior
API when run

# Additional notes
- Again, the app requires you to register the spotify users (name and email for account) you want to have access to the app in the spotify API dashboard.
- IF RUNNING ON A MAC PORT 5000 MIGHT BE SPOKEN FOR BY AIR PLAY
- In some cases the user has been re-routed to the login page even after sucessful authorization. If this happens try logging in again 
and it should work

# Course specific goals

## Säker programmering - 
- Relevant API secrets are stored in an config-file added to gitignore. An example config file with relevant keys and non vital information is included in the repo.
- CSRF management added as an extension to the flask app in app/extensions.py that is created when the app is initialized. Each form (see template files: home, login, register, playlist and search results) contains a hiddden input for the csrf token.
- The app uses protected routes (login required decorator) for all routes except index, login and register
- Password validation to ensure a relatively strong password during user registraton (app/utils.py)

## Avancerad datahantering
- Pandas and numpy are used to generate a dataframe that is used to create a plot with matplotlib (app/data_processing.py) that is then displayed in the "artist stats" section found for each listed artist in the "top artists" section in the home route 

## API integrationer - 
- Spotipy third party library is used to handle the spotify requests for
playlists, artists, user profile, track etc
- The open-meteo API is used to get current weather data displayed at the
top of the home route. The weather condition is then fed as a query to the spotify search request to generate a fitting song for the embedded 
spotify player in the home route

## Webbutveckling 
- App built using Flask with flask-login, blueprints for route management etc

## Enhetstestning och felsökning 
pytest used to test: 
- the create_user method in the auth_handler (ensure the password is not stored in clear text). This applies the test_user fixture in tests/conftest.py\
- the api_weather_handler module methods. A mock fixture is included in one of the
tests here to simulate a response from the open-meteo API using the 
pytest-mock library

## Filhantering eller kryptering
- The data processing module converts the artist data into a csv file
that is stored locally and then accessed to generate the plot included in 
the artist stats section under top artists in the home route
- When registering a user (create_user method in app/auth_handler.py) the bcrypt library is used to generate a salt, and hash the password to ensure
the password is not stored in plain text. For user login (validate_user in app/auth_handler.py) bcrypt is again used to check that the user
password enter mathces the encrypted one.

## SQL med Python
- When accessing a specific playlists under "recent playlists" the user can chose to make a backup that is stored in the database as a Playlist item. This is connected to the individual user via an association table. When doing this the tracks and artists for each playlist entry are also stored as individual entities in the database.\
The associations are as follows:\
User - Playlist : n:m\
Playlist - Track n:m\
Track - Artist n:m\
These are then accessed and used to recreate the playlist with the relevant items in spotify by clicking the "restore playlist" link under the specific playlist in the "playlist backups" section