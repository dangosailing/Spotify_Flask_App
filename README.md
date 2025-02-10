# Spotify App
Search Spotify artists, tracks and playlists. Manage your own playlists, get a csv doc of your playlists

## APIs
spotify -  used to fetch user profile, songs, playlists and artists data and alter user playlists
open meteo - to fetch weather data to display on home page. The current weather is used to generate a query for a matching track

## Dependencies
spotipy - handles auth and spotify api requests
flask - webserver interface and session storage of token
flask-wtf - include CSRF protection on forms
pandas, numpy - handle managing and visualizing data
pytest - for testing code
pytest-cov - for testing code coverage
bcrypt - for secure password management
geocoder - get coordinates from local ip for weather API

# How to run project
>>python -m venv venv
>>source venv/Scripts/activate
>>pip install -r requirements.txt
>>rename config_base.py to config.py and enter values for:
CLIENT_ID (from spotify api)
CLIENT_SECRET (from spotify api)
SECRET_KEY (set appropriately)

# ACTION PLAN
test create user ✅
complete reg route ✅
commit ✅
test register route ✅ (user was properly added in test case, but how to best assert?)
login route redirect to home ✅
create test instance of app ✅
test login route ✅ (need better asserts)
add spotify auth to login 
retool test funtions!!! (NO API HANDLER)

# GOALS
user can save playlist info to csv
user can manipulate playlist
app saves favorite artists
app saves favorite tracks
this cretes a ranking system among user to see the most popular artist, genres, tracks
Backup and recreate playlist from database

# Additional notes
IF TESTING ON A MAC PORT 5000 MIGHT BE SPOKEN FOR BY AIR PLAY
