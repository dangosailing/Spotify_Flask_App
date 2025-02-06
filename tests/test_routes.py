from flask import request, url_for

# ------------------ UNIT TEST----------------------
def test_index_route_with_fixture(test_app):
    response = test_app.get("/")
    assert response.status_code == 200
    
def test_register_route_with_fixture(test_app):
    response = test_app.get("/register")
    assert response.status_code == 200
    
def test_404(test_app):
    response = test_app.get("/nonexistantroute")
    assert response.status_code == 404

# ------------------ FUNCTIONAL TEST----------------------
def test_register_user_with_fixture(test_app, test_user):
    """
    GIVEN the test client
    WHEN a form request is made to the "register" route
    THEN check if the user exists in the database
    """
    form_data = {
        "username": test_user.username,
        "password": test_user.password
    }
    response = test_app.post("/register", data=form_data)
    assert response.status_code == 200
    
def test_login_user_with_fixture(test_app, test_user):
    """
    GIVEN the test client
    WHEN a form request is made to the "register" route
    THEN check if the user exists in the database
    """
    form_data = {
        "username": test_user.username,
        "password": test_user.password
    }
    response = test_app.post("/login", data=form_data)
    """ USER IS REDIRECTED UPON SUCESS, HENCE 302 """
    assert response.status_code == 302
    