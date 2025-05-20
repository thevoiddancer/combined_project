import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar
import csv
import os
from utils.data_manager import hash_password
import datetime

class AdminDashboard:
    def __init__(self, root, ime, prezime, on_logout):
        self.root = root
        self.ime = ime
        self.prezime = prezime
        self.on_logout = on_logout
        self.setup_ui()

    def clear_root(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()

    def setup_ui(self):
        self.clear_root()
        self.frame = tk.Frame(self.root, padx=20, pady=20, bg="light salmon")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            self.frame,
            text=f"ADMIN: {self.ime} {self.prezime}",
            font=("Helvetica", 16, "bold")
        ).pack(pady=10)

        # Main buttons
        tk.Button(
            self.frame,
            text="Dodaj zaposlenika",
            width=25,
            command=self.add_employee
        ).pack(pady=10)

        tk.Button(
            self.frame,
            text="Ukloni zaposlenika",
            width=25,
            command=self.remove_employee
        ).pack(pady=10)

        tk.Button(
            self.frame,
            width=25,
            text="Zakaži termin",
            command=self.schedule_appointment
        ).pack(pady=10)

        tk.Button(
            self.frame,
            text="Otkaži termin",
            width=25,
            command=self.cancel_appointment
        ).pack(pady=10)

        tk.Button(
            self.frame,
            text="Zakazani termini",
            width=25,
            command=self.show_appointments
        ).pack(pady=10)

        tk.Button(
            self.frame,
            text="Odjava",
            width=25,
            command=self.logout
        ).pack(pady=10)

    def add_employee(self):
        self.clear_root()
        frame = tk.Frame(self.root, padx=20, pady=20, bg="light salmon")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        labels = ["Ime", "Prezime", "Pozicija", "Broj", "Nadimak", "Lozinka"]
        entries = []
        specijalizacija = ["Pediker", "Fizio", "Njega lica/tijela", "Depilacija/laser"]

        for i, label_text in enumerate(labels):
            tk.Label(frame, text=label_text).grid(row=i, column=0, pady=10, padx=10, sticky="e")
            if label_text == "Pozicija":
                combo = ttk.Combobox(frame, values=specijalizacija, state="readonly", width=28)
                combo.grid(row=i, column=1, pady=10)
                entries.append(combo)
            else:
                entry = tk.Entry(
                    frame,
                    width=30,
                    show="*" if "lozinka" in label_text.lower() else ""
                )
                entry.grid(row=i, column=1, pady=10)
                entries.append(entry)

        def save():
            values = [e.get() for e in entries]
            if not all(values):
                messagebox.showerror("Greška", "Sva polja su obavezna.")
                return
            # Hashiraj lozinku samo ako već nije hashirana
            lozinka = values[-1]
            if len(lozinka) != 64 or not all(c in "0123456789abcdef" for c in lozinka.lower()):
                values[-1] = hash_password(lozinka)
            filepath = "data/zaposlenici.csv"
            os.makedirs("data", exist_ok=True)
            with open(filepath, "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                if os.stat(filepath).st_size == 0:
                    writer.writerow(["Ime", "Prezime", "Pozicija", "Broj", "Nadimak", "Lozinka"])
                writer.writerow(values)
            messagebox.showinfo("Uspjeh", "Zaposlenik dodan.")
            self.setup_ui()

        tk.Button(frame, text="Spremi", command=save).grid(row=len(labels), columnspan=2, pady=20)
        tk.Button(frame, text="Nazad", command=self.setup_ui).grid(row=len(labels), column=2, pady=20)

    def remove_employee(self):
        filepath = "data/zaposlenici.csv"
        if not os.path.isfile(filepath):
            messagebox.showinfo("Info", "Nema zaposlenika.")
            return

        self.clear_root()
        frame = tk.Frame(self.root, padx=20, pady=20, bg="light salmon")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        with open(filepath, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            self.employees = list(reader)

        tk.Label(
            frame,
            text="Ukloni zaposlenika",
            font=("Helvetica", 16, "bold")
        ).pack(pady=10)

        listbox = tk.Listbox(frame, height=10, width=50)
        entries = [f"{z['Ime']} {z['Prezime']} ({z['Nadimak']}) - {z['Pozicija']}" for z in self.employees]
        for entry in entries:
            listbox.insert("end", entry)
        listbox.pack(pady=10)

        def delete():
            idx = listbox.curselection()
            if not idx:
                messagebox.showerror("Greška", "Odaberi zaposlenika.")
                return

            del self.employees[idx[0]]

            with open(filepath, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=["Ime", "Prezime", "Pozicija", "Broj", "Nadimak", "Lozinka"]
                )
                writer.writeheader()
                writer.writerows(self.employees)

            messagebox.showinfo("Uspjeh", "Zaposlenik uklonjen.")
            self.setup_ui()

        tk.Button(frame, text="Ukloni", command=delete).pack(pady=5)
        tk.Button(frame, text="Nazad", command=self.setup_ui).pack(pady=5)

    def load_services_from_csv(self):
        services = []
        try:
            with open("data/usluge.csv", mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    services.append(f"{row['Usluga']} -> {row['Cijena']}")
        except FileNotFoundError:
            messagebox.showerror("Greška", "Nije moguće učitati usluge.")
        return services

    def schedule_appointment(self):
        self.clear_root()
        frame = tk.Frame(self.root, padx=20, pady=20, bg="light salmon")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        radno_vrijeme = ("Radno vrijeme: ponedjeljak - petak 08:00-21:00, subota 08:00-13:00")
        tk.Label(frame, text=radno_vrijeme, font=("Helvetica", 10, "italic"), bg="light salmon").grid(row=0, column=0, columnspan=3, pady=(0, 5))
        time_var = tk.StringVar()
        service_var = tk.StringVar()
        cal = Calendar(frame, selectmode='day', date_pattern='dd-mm-yyyy', mindate=datetime.date.today())
        cal.grid(row=1, column=0, columnspan=3, pady=(10, 20))
        def update_hours(*args):
            selected_date = cal.get_date()
            # Provjera je li nedjelja
            import datetime
            try:
                day, month, year = map(int, selected_date.split("-"))
                dt = datetime.date(year, month, day)
            except Exception:
                hour_dropdown['values'] = ["Vrijeme"]
                hour_dropdown.current(0)
                return
            if dt.weekday() == 6:  # Nedjelja
                messagebox.showwarning("Nedostupno", "Nedjeljom ne radimo. Odaberite drugi dan.")
                cal.selection_clear()
                hour_dropdown['values'] = ["Vrijeme"]
                hour_dropdown.current(0)
                return
            if dt.weekday() == 5:  # Subota
                sati = [f"{i:02d}:00" for i in range(8, 14)]
            else:
                sati = [f"{i:02d}:00" for i in range(8, 22)]
            zauzeti = set()
            if os.path.isfile("data/zakazani_termini.csv"):
                with open("data/zakazani_termini.csv", newline="", encoding="utf-8") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if row["Datum"] == selected_date:
                            zauzeti.add(row["Vrijeme"])
            slobodni = [s for s in sati if s not in zauzeti]
            hour_dropdown['values'] = ["Vrijeme"] + slobodni
            hour_dropdown.current(0)
        cal.bind("<<CalendarSelected>>", update_hours)
        hour_dropdown = ttk.Combobox(
            frame,
            state="readonly",
            textvariable=time_var,
            values=["Vrijeme"] + [f"{i:02d}:00" for i in range(8, 22)]
        )
        hour_dropdown.current(0)
        hour_dropdown.grid(row=2, column=0, columnspan=3, pady=(0, 10))
        update_hours()

        services = self.load_services_from_csv()
        service_dropdown = ttk.Combobox(
            frame,
            state="readonly",
            textvariable=service_var,
            values=["Zahvat"] + services
        )
        service_dropdown.current(0)
        service_dropdown.grid(row=3, column=0, columnspan=3, pady=(0, 10))

        def save():
            selected_date = cal.get_date()
            selected_time = time_var.get()
            selected_service = service_var.get()

            if selected_time == "Vrijeme" or not selected_time:
                messagebox.showwarning("Greška", "Odaberite vrijeme.")
                return
            if selected_service == "Zahvat" or not selected_service:
                messagebox.showwarning("Greška", "Odaberite uslugu.")
                return

            # Create customer info window
            info_window = tk.Toplevel(self.root)
            info_window.title("Unos podataka")
            info_window.geometry("300x200")
            info_window.resizable(False, False)

            tk.Label(info_window, text="Ime:").pack(pady=5)
            ime_entry = tk.Entry(info_window)
            ime_entry.pack()

            tk.Label(info_window, text="Prezime:").pack(pady=5)
            prezime_entry = tk.Entry(info_window)
            prezime_entry.pack()

            tk.Label(info_window, text="Broj:").pack(pady=5)
            broj_entry = tk.Entry(info_window)
            broj_entry.pack()

            def confirm():
                ime = ime_entry.get().strip()
                prezime = prezime_entry.get().strip()
                broj = broj_entry.get().strip()

                if not ime or not prezime or not broj:
                    messagebox.showwarning("Greška", "Sva polja moraju biti popunjena.")
                    return

                filepath = "data/zakazani_termini.csv"
                os.makedirs("data", exist_ok=True)
                file_exists = os.path.isfile(filepath)

                with open(filepath, mode="a", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    if not file_exists:
                        writer.writerow(["Ime", "Prezime", "Broj", "Datum", "Vrijeme", "Zahvat"])
                    writer.writerow([ime, prezime, broj, selected_date, f"{selected_time}", selected_service])

                info_window.destroy()
                self.show_confirmation(selected_date, selected_time, selected_service, ime, prezime)

            tk.Button(info_window, text="Potvrdi", command=confirm).pack(pady=10)

        tk.Button(frame, text="Zakaži termin", command=save).grid(row=4, column=1, pady=(0, 10))
        tk.Button(frame, text="Nazad", command=self.setup_ui).grid(row=6, column=1, pady=20)

    def show_confirmation(self, date, time, service, ime, prezime):
        self.clear_root()
        frame = tk.Frame(self.root, padx=20, pady=20, bg="light salmon")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        message = f"Termin zakazan za {date} u {time}\nZahvat: {service}\nZa: {ime} {prezime}"
        tk.Label(
            frame,
            text=message,
            font=("Arial", 12),
            fg="black",
            bg="light salmon",
            justify="left"
        ).pack(pady=20)

        tk.Button(frame, text="Nazad", command=self.setup_ui).pack(pady=10)


    def cancel_appointment(self):
        self.clear_root()
        frame = tk.Frame(self.root, padx=20, pady=20, bg="light salmon")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        filepath = "data/zakazani_termini.csv"
        if not os.path.isfile(filepath):
            messagebox.showinfo("Nema termina", "Nema zakazanih termina.")
            return self.setup_ui()

        with open(filepath, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            self.appointments = list(reader)

        if not self.appointments:
            messagebox.showinfo("Nema termina", "Nema zakazanih termina.")
            return self.setup_ui()

        listbox = tk.Listbox(frame, width=80, height=20)
        for apt in self.appointments:
            listbox.insert("end", f"{apt['Ime']} {apt['Prezime']} - {apt['Datum']} u {apt['Vrijeme']} ({apt['Zahvat']})")
        listbox.pack(pady=10)

        def delete():
            idx = listbox.curselection()
            if not idx:
                messagebox.showerror("Greška", "Odaberite termin za otkazivanje.")
                return

            del self.appointments[idx[0]]

            with open(filepath, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["Ime", "Prezime", "Broj", "Datum", "Vrijeme", "Zahvat"])
                writer.writeheader()
                writer.writerows(self.appointments)

            messagebox.showinfo("Uspjeh", "Termin je otkazan.")
            self.setup_ui()

        tk.Button(frame, text="Otkaži odabrani termin", command=delete).pack(pady=10)
        tk.Button(frame, text="Natrag", command=self.setup_ui).pack(pady=5)

    def show_appointments(self):
        filepath = "data/zakazani_termini.csv"
        if not os.path.isfile(filepath):
            messagebox.showinfo("Nema termina", "Nema zakazanih termina.")
            return

        self.clear_root()
        frame = tk.Frame(self.root, padx=20, pady=20, bg="light salmon")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="Zakazani termini", font=("Helvetica", 14, "bold")).pack(pady=10)

        text = ""
        with open(filepath, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                text += f"{row['Ime']} {row['Prezime']} - {row['Datum']} u {row['Vrijeme']}\n"

        text_box = tk.Text(frame, wrap="word", height=15, width=50)
        text_box.insert("1.0", text if text else "Nema zakazanih termina.")
        text_box.config(state="disabled")
        text_box.pack()

        tk.Button(frame, text="Nazad", command=self.setup_ui).pack(pady=10)

    def logout(self):
        self.frame.destroy()
        self.on_logout() 