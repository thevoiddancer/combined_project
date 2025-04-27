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

def create_user(first_name, last_name, phone, username, password, user_type):
    filename = '/opt/repos/combined_project/users.csv'

    if os.path.exists(filename):
        with open(filename, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Username'] == username:
                    return False

    with open(filename, 'a', newline='', encoding='utf-8') as file:
        fieldnames = ['First Name', 'Last Name', 'Phone', 'Username', 'Password', 'User Type']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if os.stat(filename).st_size == 0:
            writer.writeheader()
        writer.writerow({
            'First Name': first_name,
            'Last Name': last_name,
            'Phone': phone,
            'Username': username,
            'Password': hash_password(password),
            'User Type': user_type
        })
    return True
