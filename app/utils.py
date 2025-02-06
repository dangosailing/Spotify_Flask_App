from bcrypt import gensalt, hashpw
from app.models import User

def create_user(username:str, password:str) -> User:
    """ Returns a User object with hashed password """
    salt = gensalt()
    hashed_pw = hashpw(password.encode(), salt).decode()
    return User(username=username, password=hashed_pw)
