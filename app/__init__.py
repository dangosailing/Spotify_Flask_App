from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.routes import bp

config = Config()
db = SQLAlchemy()
login_manager=LoginManager()
login_manager.login_view = "login"

def create_app():
    app = Flask(__name__)
    # Store our configurations in the Flask app
    app.config.from_object(config)
    db.init_app(app)
    #Registers all the routes in the app's blueprint
    app.register_blueprint(bp)

    with app.app_context():
        from . import routes, models
        db.create_all()

    return app
