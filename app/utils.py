import re

def validate_pwd(password:str ) -> bool:
    """ Returns true if password matches complexity requirements"""
    # 6 letters minimum, at least one uppercase letter, and one number
    if re.findall(r"^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{6,}$", password):
        return True
    else:
        return False

