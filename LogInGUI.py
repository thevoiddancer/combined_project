import tkinter as tk
from tkinter import messagebox
import csv
import os
import hashlib

def hash_password(password):
    """Hashes the password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(username, password):
    filename = '/opt/repos/combined_project/users.csv'

    if not os.path.exists(filename):
        messagebox.showerror("Greška", "Baza korisnika ne postoji.")
        return False

    hashed_password = hash_password(password)

    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Username"] == username and row["Password"] == hashed_password:
                    print(f"[SUCCESS] Uspješna prijava: {username}")
                    return True
            print("[ERROR] Neispravno korisničko ime ili lozinka.")
            return False

    except Exception as e:
        print(f"[ERROR] Greška pri prijavi: {e}")
        return False


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")

        
        self.label_username = tk.Label(self.root, text="Korisničko ime:")
        self.label_username.grid(row=0, column=0, padx=5, pady=5)
        self.entry_username = tk.Entry(self.root)
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)

        
        self.label_password = tk.Label(self.root, text="Lozinka:")
        self.label_password.grid(row=1, column=0, padx=5, pady=5)
        self.entry_password = tk.Entry(self.root, show="*")
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)

        
        self.button_login = tk.Button(self.root, text="Prijavi se", command=self.login)
        self.button_login.grid(row=2, column=0, columnspan=2, pady=10)

    def login(self):
        """Funkcija za provjeru korisničkog imena i lozinke."""
        username = self.entry_username.get()
        password = self.entry_password.get()

        if login_user(username, password):
            messagebox.showinfo("Uspješno", f"Dobrodošli, {username}!")
            self.root.quit()  # Zatvori login prozor
        else:
            messagebox.showerror("Greška", "Pogrešno korisničko ime ili lozinka.")


root = tk.Tk()

app = LoginApp(root)

root.mainloop()

