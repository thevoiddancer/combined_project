import csv
import os
import hashlib

def hash_password(password):
    """Hashiranje lozinke."""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(first_name, last_name, phone_number, username, password, user_type):
    """Kreira novog korisnika u CSV datoteci."""
    filename = '/opt/repos/combined_project/users.csv'

    try:
        if os.path.exists(filename):
            with open(filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                headers = next(reader, None)
                expected_headers = ["First Name", "Last Name", "Phone Number", "Username", "Password", "User Type"]
                if headers != expected_headers:
                    return False
                for row in reader:
                    if len(row) >= 6 and row[3] == username:
                        return False

        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(["First Name", "Last Name", "Phone Number", "Username", "Password", "User Type"])
            hashed_password = hash_password(password)
            writer.writerow([first_name, last_name, phone_number, username, hashed_password, user_type])

        return True

    except Exception as e:
        print(f"[ERROR] Dogodila se greška: {e}")
        return False
