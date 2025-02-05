from flask import Flask
from config import Config

config = Config()

def create_app():
    app = Flask(__name__)
    # Store our configurations in the Flask app
    app.config.from_object(config)
    return app
