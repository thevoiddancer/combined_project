import tkinter as tk
from tkinter import ttk, messagebox
import datetime as dt
from auth_functions import login_user, create_user
from calendar_functions import get_days_in_month, save_appointment
from receipt_functions import generate_receipt
import os

MJESECI = ['Siječanj', 'Veljača', 'Ožujak', 'Travanj', 'Svibanj', 'Lipanj', 'Srpanj', 'Kolovoz', 'Rujan', 'Listopad', 'Studeni', 'Prosinac']
DANI = ['PON', 'UTO', 'SRI', 'ČET', 'PET', 'SUB', 'NED']

SERVICES = ["Manikura", "Pedikura", "Masaža", "Šminkanje"]
SERVICE_PRICES = {
    "Manikura": 20,
    "Pedikura": 25,
    "Masaža": 30,
    "Šminkanje": 35
}

class KozmetickiSalonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kozmetički Salon")
        self.logged_in_user = None
        self.start_screen()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def start_screen(self):
        self.clear_frame()
        frame = tk.Frame(self.root)
        frame.pack(expand=True)

        tk.Label(frame, text="Dobrodošli", font=("Arial", 40)).pack(pady=20)
        tk.Button(frame, text="Prijava", font=("Arial", 20), command=self.login_screen).pack(pady=10)
        tk.Button(frame, text="Registracija", font=("Arial", 20), command=self.register_screen).pack(pady=10)
        tk.Button(frame, text="Izlaz", font=("Arial", 20), command=self.root.quit).pack(pady=10)

    def login_screen(self):
        self.clear_frame()
        frame = tk.Frame(self.root)
        frame.pack(expand=True)

        tk.Label(frame, text="Korisničko ime:", font=("Arial", 20)).pack(pady=5)
        self.entry_username = tk.Entry(frame, font=("Arial", 20))
        self.entry_username.pack(pady=5)

        tk.Label(frame, text="Lozinka:", font=("Arial", 20)).pack(pady=5)
        self.entry_password = tk.Entry(frame, show="*", font=("Arial", 20))
        self.entry_password.pack(pady=5)

        tk.Button(frame, text="Prijavi se", font=("Arial", 20), command=self.do_login).pack(pady=10)
        tk.Button(frame, text="Natrag", font=("Arial", 20), command=self.start_screen).pack(pady=10)

    def do_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if login_user(username, password):
            self.logged_in_user = username
            messagebox.showinfo("Uspjeh", f"Dobrodošli, {username}!")
            self.calendar_screen()
        else:
            messagebox.showerror("Greška", "Pogrešno korisničko ime ili lozinka.")

    def register_screen(self):
        self.clear_frame()
        frame = tk.Frame(self.root)
        frame.pack(expand=True)

        self.entry_first_name = tk.Entry(frame, font=("Arial", 20))
        self.entry_last_name = tk.Entry(frame, font=("Arial", 20))
        self.entry_phone = tk.Entry(frame, font=("Arial", 20))
        self.entry_username_reg = tk.Entry(frame, font=("Arial", 20))
        self.entry_password_reg = tk.Entry(frame, show="*", font=("Arial", 20))
        self.user_type_combo = ttk.Combobox(frame, values=["Korisnik", "Zaposlenik"], font=("Arial", 20))

        labels = ["Ime", "Prezime", "Broj mobitela", "Korisničko ime", "Lozinka", "Tip korisnika"]
        entries = [self.entry_first_name, self.entry_last_name, self.entry_phone, self.entry_username_reg, self.entry_password_reg, self.user_type_combo]

        for label_text, entry in zip(labels, entries):
            tk.Label(frame, text=label_text, font=("Arial", 20)).pack(pady=5)
            entry.pack(pady=5)

        tk.Button(frame, text="Registriraj", font=("Arial", 20), command=self.do_register).pack(pady=10)
        tk.Button(frame, text="Natrag", font=("Arial", 20), command=self.start_screen).pack(pady=10)

    def do_register(self):
        data = [
            self.entry_first_name.get(),
            self.entry_last_name.get(),
            self.entry_phone.get(),
            self.entry_username_reg.get(),
            self.entry_password_reg.get(),
            self.user_type_combo.get()
        ]

        if all(data):
            if create_user(*data):
                messagebox.showinfo("Uspjeh", "Registracija uspješna!")
                self.start_screen()
            else:
                messagebox.showerror("Greška", "Korisnik već postoji.")
        else:
            messagebox.showerror("Greška", "Molimo popunite sva polja.")

    def calendar_screen(self):
        self.clear_frame()

        now = dt.datetime.now()
        self.year = now.year
        self.month = now.month

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack()

        self.create_calendar()

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        logout_button = tk.Button(button_frame, text="Odjava", font=("Arial", 20), command=self.start_screen)
        logout_button.pack()


    def create_calendar(self):
        for widget in self.canvas.winfo_children():
            widget.destroy()

        tk.Label(self.canvas, text=f"{MJESECI[self.month-1]} {self.year}", font=("Arial", 30)).grid(row=0, column=1, columnspan=5)

        tk.Button(self.canvas, text="<", font=("Arial", 20), command=lambda: self.change_month(-1)).grid(row=0, column=0)
        tk.Button(self.canvas, text=">", font=("Arial", 20), command=lambda: self.change_month(1)).grid(row=0, column=6)

        for idx, dan in enumerate(DANI):
            tk.Label(self.canvas, text=dan, font=("Arial", 18)).grid(row=1, column=idx)

        day_1 = dt.date(self.year, self.month, 1).weekday()

        for i in range(1, get_days_in_month(self.year, self.month)+1):
            tk.Button(self.canvas, text=i, font=("Arial", 18), command=lambda d=i: self.select_time(d)).grid(row=2+(day_1+i-1)//7, column=(day_1+i-1)%7)

    def change_month(self, direction):
        self.month += direction
        if self.month < 1:
            self.month = 12
            self.year -= 1
        elif self.month > 12:
            self.month = 1
            self.year += 1
        self.create_calendar()

    def select_time(self, dan):
        self.clear_frame()

        self.dan = dan
        self.available_times = ['8:00', '9:00', '10:00', '11:00']
        frame = tk.Frame(self.root)
        frame.pack(expand=True)

        tk.Label(frame, text=f"Odaberi vrijeme za {dan}.{self.month}.{self.year}", font=("Arial", 30)).pack(pady=10)

        self.selected_time = tk.StringVar()
        time_menu = ttk.Combobox(frame, textvariable=self.selected_time, values=self.available_times, font=("Arial", 20))
        time_menu.pack(pady=10)
        time_menu.current(0)

        tk.Label(frame, text="Odaberi uslugu:", font=("Arial", 25)).pack(pady=10)

        self.selected_service = tk.StringVar()
        service_menu = ttk.Combobox(frame, textvariable=self.selected_service, values=SERVICES, font=("Arial", 20))
        service_menu.pack(pady=10)
        service_menu.current(0)

        self.label_cijena = tk.Label(frame, text="", font=("Arial", 20))
        self.label_cijena.pack(pady=10)

        service_menu.bind("<<ComboboxSelected>>", self.update_price)

        tk.Button(frame, text="Rezerviraj", font=("Arial", 20), command=self.do_reservation).pack(pady=10)

    def update_price(self, event):
        usluga = self.selected_service.get()
        cijena = SERVICE_PRICES.get(usluga, 0)
        self.label_cijena.config(text=f"Cijena: {cijena} EUR")

    def do_reservation(self):
        if self.selected_time.get() and self.selected_service.get():
            save_appointment(self.year, self.month, self.dan, self.selected_time.get(), self.selected_service.get(), self.logged_in_user)
            messagebox.showinfo("Uspješno", "Rezervacija spremljena!")
            self.show_after_reservation()
        else:
            messagebox.showerror("Greška", "Molimo odaberite vrijeme i uslugu.")

    def show_after_reservation(self):
        self.clear_frame()
        frame = tk.Frame(self.root)
        frame.pack(expand=True)

        tk.Label(frame, text="Rezervacija uspješna!", font=("Arial", 30)).pack(pady=20)

        tk.Button(frame, text="Ispiši račun", font=("Arial", 20), command=self.generate_receipt).pack(pady=10)
        tk.Button(frame, text="Natrag na kalendar", font=("Arial", 20), command=self.calendar_screen).pack(pady=10)
        tk.Button(frame, text="Odjava", font=("Arial", 20), command=self.start_screen).pack(pady=10)

    def generate_receipt(self):
        generate_receipt(self.logged_in_user, self.year, self.month, self.dan, self.selected_time.get(), self.selected_service.get())
        messagebox.showinfo("Račun", "Račun je uspješno generiran!")

