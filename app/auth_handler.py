from app.models import User
from app.extensions import db
from bcrypt import gensalt, hashpw, checkpw

class AuthHandler:

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
