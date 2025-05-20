import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import csv
import os
import datetime

class EmployeeDashboard:
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
            text=f"Zaposlenik: {self.ime} {self.prezime}",
            font=("Helvetica", 16, "bold")
        ).pack(pady=20)

        tk.Button(
            self.frame,
            text="Zakaži termin",
            width=25,
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
                    writer.writerow([ime, prezime, broj, selected_date, selected_time, selected_service])

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
        self.clear_root()
        frame = tk.Frame(self.root, padx=20, pady=20, bg="light salmon")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        filepath = "data/zakazani_termini.csv"
        if not os.path.isfile(filepath):
            messagebox.showinfo("Nema termina", "Nema zakazanih termina.")
            return self.setup_ui()

        text = ""
        with open(filepath, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                text += f"{row['Ime']} {row['Prezime']} - {row['Datum']} u {row['Vrijeme']} -> {row['Zahvat']}\n"

        text_box = tk.Text(frame, wrap="word", height=20)
        text_box.insert("1.0", text if text else "Nema zakazanih termina.")
        text_box.config(state="disabled")
        text_box.pack(expand=True, fill="both", padx=10, pady=10)

        tk.Button(frame, text="Natrag", command=self.setup_ui).pack(pady=10)

    def logout(self):
        self.frame.destroy()
        self.on_logout() 