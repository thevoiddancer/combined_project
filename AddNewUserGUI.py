import csv
import os
import hashlib
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk  # Dodan import za ttk

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(first_name, last_name, phone_number, username, password, user_type):
    filename = '/opt/repos/combined_project/users.csv'
    print(f"[INFO] Spremam u datoteku: {filename}")

    try:
        if os.path.exists(filename):
            print(f"[INFO] Datoteka {filename} postoji, provjeravam postojeće korisnike...")
            with open(filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                headers = next(reader, None)
                expected_headers = ["First Name", "Last Name", "Phone Number", "Username", "Password", "User Type"]
                if headers != expected_headers:
                    print(f"[ERROR] Neispravan format datoteke {filename}. Očekivana zaglavlja: {expected_headers}")
                    return False
                for row in reader:
                    print(f"[DEBUG] Provjeravam korisnika: {row}")
                    if len(row) >= 6 and row[3] == username:  # Provjera da li je redak ispravan i da korisničko ime postoji
                        print(f"[ERROR] Korisnik {username} već postoji!")
                        return False
        else:
            print(f"[INFO] Datoteka {filename} ne postoji, kreiram novu...")

        # Ako korisnik ne postoji, dodajemo novog
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # Check if the file is empty
                print("[INFO] Datoteka je prazna, dodajem zaglavlje...")
                writer.writerow(["first_name", "Last Name", "Phone Number", "Username", "Password", "User Type"])
            hashed_password = hash_password(password)
            writer.writerow([first_name, last_name, phone_number, username, hashed_password, user_type])
            print(f"[SUCCESS] Dodan novi korisnik: {username}")

        return True
    

    except Exception as e:
        print(f"[ERROR] Dogodila se greška: {e}")
        return False
    
    

def kreiraj_korisnika():
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    phone_number = entry_phone_number.get()
    username = entry_username.get()
    password = entry_password.get()
    user_type = user_type_combobox.get()  # Odabrani tip korisnika

    # Provjera da li su svi podaci uneseni
    if not first_name or not last_name or not phone_number or not username or not password or not user_type:
        messagebox.showerror("Greška", "Unesite sve podatke!")
        return

    uspjeh = create_user(first_name, last_name, phone_number, username, password, user_type)

    if uspjeh:
        messagebox.showinfo("Uspjeh", f"Korisnik '{username}' je uspješno kreiran!")
        entry_first_name.delete(0, tk.END)
        entry_last_name.delete(0, tk.END)
        entry_phone_number.delete(0, tk.END)
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        user_type_combobox.set("")  # Resetiraj odabrani tip
    else:
        messagebox.showerror("Greška", "Korisnik nije uspješno kreiran. Provjerite podatke.")
# Kreiranje korisničkog sučelja za unos podataka o korisniku

# ---------- GUI DIO ----------

root = tk.Tk()
root.title("Kreiraj korisnika")

# Ime
label_first_name = tk.Label(root, text="Ime:")
label_first_name.grid(row=0, column=0, padx=5, pady=5)
entry_first_name = tk.Entry(root)
entry_first_name.grid(row=0, column=1, padx=5, pady=5)

# Prezime
label_last_name = tk.Label(root, text="Prezime:")
label_last_name.grid(row=1, column=0, padx=5, pady=5)
entry_last_name = tk.Entry(root)
entry_last_name.grid(row=1, column=1, padx=5, pady=5)

# Broj mobitela
label_phone_number = tk.Label(root, text="Broj mobitela:")
label_phone_number.grid(row=2, column=0, padx=5, pady=5)
entry_phone_number = tk.Entry(root)
entry_phone_number.grid(row=2, column=1, padx=5, pady=5)

# Korisničko ime
label_username = tk.Label(root, text="Korisničko ime:")
label_username.grid(row=3, column=0, padx=5, pady=5)
entry_username = tk.Entry(root)
entry_username.grid(row=3, column=1, padx=5, pady=5)

# Lozinka
label_password = tk.Label(root, text="Lozinka:")
label_password.grid(row=4, column=0, padx=5, pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.grid(row=4, column=1, padx=5, pady=5)

# Tip korisnika
label_user_type = tk.Label(root, text="Tip korisnika:")
label_user_type.grid(row=5, column=0, padx=5, pady=5)
user_types = ["Korisnik", "Zaposlenik"]
user_type_combobox = ttk.Combobox(root, values=user_types, state="readonly")
user_type_combobox.grid(row=5, column=1, padx=5, pady=5)

# Kreiraj korisnika
button_create = tk.Button(root, text="Kreiraj korisnika", command=kreiraj_korisnika)
button_create.grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()   



