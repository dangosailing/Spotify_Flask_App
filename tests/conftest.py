import pytest
from app.models import User

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