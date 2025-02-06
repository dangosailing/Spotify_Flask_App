# To circumvent possible circular imports
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Blueprint

# ------ Database
db = SQLAlchemy()
# ------ Login Manager
login_manager=LoginManager()
# If user attemps to access a route that requires login they will be redirected to this view
login_manager.login_view = "main.login"
# ------ Blueprint
bp = Blueprint("main", __name__)