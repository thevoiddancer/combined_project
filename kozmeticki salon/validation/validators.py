import re

def is_valid_password(password):
    # Bar jedno veliko slovo, broj i poseban znak
    if (re.search(r"[A-Z]", password) and
        re.search(r"\d", password) and
        re.search(r"[^\w\s]", password)):
        return True
    return False
