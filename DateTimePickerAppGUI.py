import tkinter as tk
import datetime as dt
from random import shuffle
import csv
from tkinter import messagebox

MJESECI = ['Siječanj', 'Veljača', 'Ožujak', 'Travanj', 'Svibanj', 'Lip', 'Srp', 'Kol', 'Ruj', 'Lis', 'Stu', 'Pro']
DANI = ['PON', 'UTO', 'SRI', 'CET', 'PET', 'SUB', 'NED']

def get_days_in_month(year, month):
    today = dt.datetime.now().date()
    next_month = today.replace(day=1, year=year, month=month % 12 + 1)
    day = dt.timedelta(days=1)
    last_day = next_month - day
    number_of_days = last_day.day
    return number_of_days

def save_appointment(year, month, day, time_slot):
    filename = '/opt/repos/combined_project/appointments.csv'
    
    try:
        with open(filename, mode='r', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file)
            appointments = list(reader)
    except FileNotFoundError:
        appointments = []
    

    appointments.append({
        'Godina': year,
        'Mjesec': month,
        'Dan': day,
        'Vrijeme': time_slot
    })
    
  #sortiranje rez.
    appointments.sort(key=lambda x: (
        int(x['Godina']),
        int(x['Mjesec']),
        int(x['Dan']),
        int(x['Vrijeme'].split(':')[0]),
        int(x['Vrijeme'].split(':')[1])
    ))
    
    # spremanje rezervacije natrag u CSV
    with open(filename, mode='w', encoding='utf-8', newline='') as file:
        fieldnames = ['Godina', 'Mjesec', 'Dan', 'Vrijeme']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(appointments)


class DateTimePickerWidget:
    def __init__(self, root):
        self.root = root
        now = dt.datetime.now()
        self.today = now.date()
        self.year = self.today.year
        self.month = self.today.month
        self.selected_time = None  # Dodajemo varijablu koja će držati odabrano vrijeme

        self.date_picker_canvas = tk.Canvas(self.root)
        self.date_picker_canvas.grid(row=0, column=0)

        self.create_date_picker()
        self.time_picker_canvas = tk.Canvas(self.root)

    def create_date_picker(self):
        for widget in self.date_picker_canvas.winfo_children():
            widget.destroy()

        label_year = tk.Label(self.date_picker_canvas, text=self.year)
        label_year.grid(row=0, column=1, columnspan=5)

        label_month = tk.Label(self.date_picker_canvas, text=MJESECI[self.month - 1])
        label_month.grid(row=1, column=1, columnspan=5)

        year_prev = tk.Button(self.date_picker_canvas, text='<', command=lambda: self.change_year(-1))
        year_prev.grid(row=0, column=0)
        year_next = tk.Button(self.date_picker_canvas, text='>', command=lambda: self.change_year(1))
        year_next.grid(row=0, column=6)

        month_prev = tk.Button(self.date_picker_canvas, text='<', command=lambda: self.change_month(-1))
        month_prev.grid(row=1, column=0)
        month_next = tk.Button(self.date_picker_canvas, text='>', command=lambda: self.change_month(1))
        month_next.grid(row=1, column=6)

        for index, dan in enumerate(DANI):
            dan_label = tk.Label(self.date_picker_canvas, text=dan)
            dan_label.grid(row=2, column=index)
        
        day_1 = self.today.replace(day=1).weekday()

        for i in range(get_days_in_month(self.year, self.month)):
            day_button = tk.Button(self.date_picker_canvas, text=i + 1, command=lambda dan=i+1: self.open_time_picker(dan))
            day_button.grid(row=3 + (day_1 + i) // 7, column=(day_1 + i) % 7)

    def open_time_picker(self, dan):
        self.dan = dan  # Ovdje spremamo točan odabrani dan
        termini = ['8:00', '9:00', '10:00', '11:00']
        shuffle(termini)
        self.create_time_picker(termini)

    def create_time_picker(self, termini):
        self.time_picker_canvas.grid(row=0, column=1)

        label_odaberi = tk.Label(self.time_picker_canvas, text="Odaberi vrijeme")
        label_odaberi.grid(row=0, column=0)

        # Resetiramo odabrano vrijeme kad korisnik odabere novo
        self.selected_time = None

        for index, vrijeme in enumerate(termini):
            vrijeme_gumb = tk.Button(self.time_picker_canvas, text=vrijeme, command=lambda v=vrijeme: self.select_time(v))
            vrijeme_gumb.grid(row=2 + index, column=0)

        # Gumb za potvrdu rezervacije
        rezerviraj = tk.Button(self.time_picker_canvas, text='Rezerviraj', command=self.rezerviraj)
        rezerviraj.grid(row=100, column=0)

    def select_time(self, v):
        self.selected_time = v  # Postavljamo odabrano vrijeme

    def rezerviraj(self):
        if self.selected_time is not None:
            save_appointment(self.year, self.month, self.dan, self.selected_time)
            # Prikazivanje popup poruke za uspješnu rezervaciju
            messagebox.showinfo("Uspješno!", f"Rezervacija za {self.dan}.{self.month}.{self.year} u {self.selected_time} je uspješno napravljena.")
            print(f"Rezervacija za {self.dan}.{self.month}.{self.year} u {self.selected_time}")
        else:
            print("Niste odabrali vrijeme!")
            messagebox.showwarning("Greška", "Molimo odaberite vrijeme prije nego što rezervirate.")

    def change_month(self, x):
        self.time_picker_canvas.grid_remove()
        if self.month == 1 and x == -1:
            self.month = 12
            self.year -= 1
        elif self.month == 12 and x == 1:
            self.month = 1
            self.year += 1
        else:
            self.month += x
        self.today = self.today.replace(month=self.month, year=self.year)

        self.create_date_picker()

    def change_year(self, x):
        self.time_picker_canvas.grid_remove()
        self.year += x
        self.today = self.today.replace(year=self.year)
        self.create_date_picker()


root = tk.Tk()
app = DateTimePickerWidget(root)
root.mainloop()
