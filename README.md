# Spotify App
Search Spotify artists, tracks and playlists. Manage your own playlists, get a csv doc of your playlists

## Dependencies
spotipy - handles auth and spotify api requests
flask - webserver interface and session storage of token
pandas, numpy - handle managing and visualizing data
pytest - for testing code
pytest-cov - for testing code coverage
bcrypt - for secure password management

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
