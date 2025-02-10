from flask import Flask
from app.routes import bp
from config import Config
from app.extensions import db, bp, login_manager, csrf


def create_app(config: Config) -> Flask:
    """Create an instance of the Spotify App"""
    app = Flask(__name__)

    # Store our configurations in the Flask app
    app.config.from_object(config)
    # Registers all the routes in the app's blueprint
    # Login
    login_manager.init_app(app)
    csrf.init_app(app)
    with app.app_context():
        from . import models

        app.register_blueprint(bp)
        db.init_app(app)
        db.create_all()

    return app
