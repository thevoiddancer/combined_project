import tkinter as tk
from tkinter import messagebox
import csv
import os
import hashlib
from validation.validators import is_valid_password
from utils.data_manager import hash_password

class SignupFrame(tk.Frame):
    def __init__(self, master, on_success, on_back):
        super().__init__(master, padx=20, pady=20, bg="light salmon")
        self.on_success = on_success
        self.on_back = on_back
        self.setup_ui()

    def setup_ui(self):
        labels = ["Ime", "Prezime", "Broj mobitela", "Nadimak", "Lozinka", "Potvrdi lozinku"]
        self.entries = []

        for i, label_text in enumerate(labels):
            label = tk.Label(self, text=label_text)
            label.grid(row=i, column=0, pady=10, padx=10, sticky="e")

            entry = tk.Entry(
                self,
                width=30,
                show="*" if "lozink" in label_text.lower() else ""
            )
            entry.grid(row=i, column=1, pady=10)
            self.entries.append(entry)

        # Register button
        tk.Button(
            self,
            text="Registriraj se",
            command=self.save_user
        ).grid(row=len(labels), columnspan=2, pady=20)

        # Back button
        tk.Button(
            self,
            text="Nazad",
            command=self.on_back
        ).grid(row=6, column=3, pady=20)

    def save_user(self):
        values = [e.get() for e in self.entries]
        ime, prezime, broj, nadimak, lozinka, potvrda = values

        if not all(values):
            messagebox.showerror("Greška", "Sva polja su obavezna.")
            return False

        if lozinka != potvrda:
            messagebox.showerror("Greška", "Lozinke se ne podudaraju.")
            return False

        if not is_valid_password(lozinka):
            messagebox.showerror("Greška", "Lozinka mora imati veliko slovo, broj i poseban znak.")
            return False

        filepath = "data/korisnici.csv"
        os.makedirs("data", exist_ok=True)
        file_exists = os.path.isfile(filepath)

        hashed_password = hash_password(lozinka)

        with open(filepath, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Ime", "Prezime", "Broj", "Nadimak", "Lozinka"])
            writer.writerow([ime, prezime, broj, nadimak, hashed_password])

        messagebox.showinfo("Uspješno", "Registracija je uspješna!")
        self.on_success(ime, prezime, broj)
        return True 