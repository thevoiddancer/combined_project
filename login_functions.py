import csv
import os
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(username, password):
    filename = '/opt/repos/combined_project/users.csv'
    if not os.path.exists(filename):
        return False

    hashed_password = hash_password(password)
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Username'] == username and row['Password'] == hashed_password:
                return True
    return False
