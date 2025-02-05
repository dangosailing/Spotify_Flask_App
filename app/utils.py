from bcrypt import gensalt, hashpw

def hash_password(password: str):
    """ Hash password using bcrypt """
    salt = gensalt()
    return hashpw(password.encode(), salt).decode()
