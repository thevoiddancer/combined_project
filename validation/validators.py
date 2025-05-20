import re

def is_valid_password(password):
    """
    Validates that password contains:
    - At least one uppercase letter
    - At least one number
    - At least one special character
    """
    if len(password) < 8:
        return False
    
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    
    return has_upper and has_digit and has_special 