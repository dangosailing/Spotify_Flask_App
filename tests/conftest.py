import pytest
from app.models import User

@pytest.fixture()
def test_user():
    username = "John Doe"
    password = "password123"
    
    user = User(username=username, password=password)
    return user
