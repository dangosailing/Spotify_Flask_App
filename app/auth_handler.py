from app.models import User
from app.extensions import db
from flask import session
from config import Config
from bcrypt import gensalt, hashpw, checkpw
from spotipy.cache_handler import FlaskSessionCacheHandler
# To allow users to log in in order to track stats we need an Auth Flow
from spotipy.oauth2 import SpotifyOAuth

class AuthHandler:
    def spotify_auth_manager(self):
        """ Returns a SpotifyOAuth object to handle authorization """
        #Allows us to save the token in a session using Flask
        cache_handler = FlaskSessionCacheHandler(session)

        #Handles authorization, the scope of our access to user data 
        auth_manager=SpotifyOAuth(
            client_id=Config().CLIENT_ID,
            client_secret=Config().CLIENT_SECRET,
            redirect_uri=Config().REDIRECT_URI,
            scope="playlist-read-private,user-top-read",
            cache_handler=cache_handler,
            show_dialog=True)
        
        return auth_manager

    def create_user(self, username: str, password: str) -> User:
        """Returns a User object with hashed password"""
        salt = gensalt()
        hashed_pw = hashpw(password.encode(), salt).decode()
        return User(username=username, password=hashed_pw)

    def register(self, username: str, password: str) -> bool:
        """Registers user, returns False if username taken or True if user is registered"""
        if User.query.filter_by(username=username).first():
            return False
        new_user = self.create_user(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return True

    def validate_user(self, username: str, password: str) -> User:
        """Return matched User if username and password  matches existing user"""
        user = User.query.filter_by(username=username).first()
        if user and checkpw(password.encode(), user.password.encode()):
            return user
        else:
            return None
