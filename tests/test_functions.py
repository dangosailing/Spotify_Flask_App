from app.utils import create_user

def test_create_user():
    """
    GIVEN a create user function
    WHEN the create user function is called with a username and password
    THEN make sure the returned user has the same username and make sure that password is not stored in clear text
    """
    
    username= "John Doe"
    password= "test123"
    user = create_user(username=username, password=password)
    
    assert user.username == "John Doe"
    # Ensure password is hashed
    assert user.password != "test123"