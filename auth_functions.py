
import csv
import os
import hashlib
import re

USERS_FILE = 'users.csv'

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_phone(phone):
    return re.fullmatch(r'\d{8,15}', phone) is not None

def is_valid_password(password):
    return len(password) >= 6

def login_user(username, password):
    if not os.path.exists(USERS_FILE):
        return False

    hashed = hash_password(password)
    with open(USERS_FILE, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('Username') == username and row.get('Password') == hashed:
                return True
    return False

def create_user(first_name, last_name, phone, username, password, user_type):
    if not is_valid_phone(phone) or not is_valid_password(password):
        return False

    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'First Name','Last Name','Phone','Username','Password','User Type'
            ])
            writer.writeheader()

    with open(USERS_FILE, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('Username') == username:
                return False

    with open(USERS_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'First Name','Last Name','Phone','Username','Password','User Type'
        ])
        writer.writerow({
            'First Name': first_name,
            'Last Name' : last_name,
            'Phone'     : phone,
            'Username'  : username,
            'Password'  : hash_password(password),
            'User Type' : user_type
        })
    return True

def get_user(username):
    if not os.path.exists(USERS_FILE):
        return None
    with open(USERS_FILE, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('Username') == username:
                return row
    return None
