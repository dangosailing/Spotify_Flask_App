import pytest
from app.models import User
from app import create_app
from tests.config_test import Config

# SCOPES allow us to decide when the fixture is run
# function - once per test class
# module - once per module/file
# session - once per call to pytest 

@pytest.fixture()
def test_user():
    username = "John Doe"
    password = "password123"
    
    user = User(username=username, password=password)
    return user

# Scope set to session to ensure all routes can be tested in the same run
@pytest.fixture(scope="session")
def test_app():
    app = create_app(Config)
    # Creating a testing client allows us to create an instance of the app with our testing config 
    with app.test_client() as testing_client:
        yield testing_client
    