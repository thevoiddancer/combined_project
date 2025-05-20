import tkinter as tk
from tkinter import messagebox
import csv
import os
import hashlib
from utils.data_manager import hash_password

class LoginFrame(tk.Frame):
    def __init__(self, master, on_success, on_back):
        super().__init__(master, padx=20, pady=20, bg="light salmon")
        self.on_success = on_success
        self.on_back = on_back
        self.setup_ui()

    def setup_ui(self):
        # Username field
        tk.Label(self, text="Nadimak").grid(row=0, column=0, pady=10, padx=10, sticky="e")
        self.username_entry = tk.Entry(self, width=30)
        self.username_entry.grid(row=0, column=1, pady=10)

        # Password field
        tk.Label(self, text="Lozinka").grid(row=1, column=0, pady=10, padx=10, sticky="e")
        self.password_entry = tk.Entry(self, width=30, show="*")
        self.password_entry.grid(row=1, column=1, pady=10)

        # Login button
        tk.Button(self, text="Potvrdi", command=self.login).grid(row=2, columnspan=2, pady=20)
        
        # Back button
        tk.Button(self, text="Nazad", command=self.on_back).grid(row=6, column=3, pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Admin check
        if username == "Caskey" and password == "#Caskey123":
            self.on_success("admin", {"ime": "Antonio", "prezime": "Šiljac"})
            return

        # User check
        if self.check_credentials("data/korisnici.csv", username, password):
            user_data = self.get_user_data("data/korisnici.csv", username)
            self.on_success("user", user_data)
            return

        # Employee check
        if self.check_credentials("data/zaposlenici.csv", username, password):
            employee_data = self.get_user_data("data/zaposlenici.csv", username)
            self.on_success("employee", employee_data)
            return

        messagebox.showerror("Greška", "Pogrešan nadimak ili lozinka.")

    def check_credentials(self, filepath, username, password):
        if not os.path.isfile(filepath):
            return False
        hashed_password = hash_password(password)
        with open(filepath, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Nadimak"] == username and row["Lozinka"] == hashed_password:
                    return True
        return False

    def get_user_data(self, filepath, username):
        with open(filepath, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Nadimak"] == username:
                    return row
        return None 