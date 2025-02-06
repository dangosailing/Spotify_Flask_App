from app import create_app
from config import Config

if __name__ == "__main__":
    create_app(Config).run(debug=True)
