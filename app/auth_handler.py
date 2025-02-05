from app.models import User
from app.utils import hash_password
from app.extensions import db

class AuthHandler:
    """ Registers user, returns False if username taken or True if user is registered"""
    def register(self, username:str, password:str) -> bool:
        # Register user and redirect user to login
        if User.query.filter_by(username=username).first():
            return False
        hashed_pwd = hash_password(password)
        new_user= User(username=username, password=hashed_pwd)
        
        db.session.add(new_user)
        db.session.commit()
        return True
        
    def login(self, username:str, password:str) -> None:
        pass

    def logout(self) -> None:
        pass