import tkinter as tk
from tkinter import ttk, messagebox
import datetime as dt
import csv
import os
import hashlib

from auth_functions import login_user, create_user, get_user
from calendar_functions import get_days_in_month, get_available_times, save_appointment
from service_functions import load_services, add_service, delete_service
from receipt_functions import generate_receipt

MJESECI = [
    'Siječanj','Veljača','Ožujak','Travanj','Svibanj','Lipanj',
    'Srpanj','Kolovoz','Rujan','Listopad','Studeni','Prosinac'
]
DANI = ['PON','UTO','SRI','ČET','PET','SUB','NED']

def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode('utf-8')).hexdigest()

class KozmetickiSalonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kozmetički Salon")
        self.logged_in_user = None
        now = dt.datetime.now()
        self.current_year, self.current_month = now.year, now.month
        self.current_context = None
        self.start_screen()

    def clear_frame(self):
        for w in self.root.winfo_children():
            w.destroy()

    # --- Start Screen ---
    def start_screen(self):
        self.clear_frame()
        f = tk.Frame(self.root); f.pack(expand=True, pady=50)
        tk.Label(f, text="Dobrodošli", font=("Arial",40)).pack(pady=20)
        tk.Button(f, text="Prijava", font=("Arial",20), width=20,
                  command=self.login_screen).pack(pady=10)
        tk.Button(f, text="Registracija", font=("Arial",20), width=20,
                  command=self.register_screen).pack(pady=10)
        tk.Button(f, text="Izlaz", font=("Arial",20), width=20,
                  command=self.root.quit).pack(pady=10)

    # --- Login ---
    def login_screen(self):
        self.clear_frame()
        f = tk.Frame(self.root); f.pack(expand=True, pady=50)
        tk.Label(f, text="Korisničko ime:", font=("Arial",16)).pack(pady=5)
        self.e_user = tk.Entry(f, font=("Arial",16)); self.e_user.pack(pady=5)
        tk.Label(f, text="Lozinka:", font=("Arial",16)).pack(pady=5)
        self.e_pass = tk.Entry(f, show="*", font=("Arial",16)); self.e_pass.pack(pady=5)
        tk.Button(f, text="Prijavi se", font=("Arial",16),
                  command=self.do_login).pack(pady=10)
        tk.Button(f, text="Natrag", font=("Arial",16),
                  command=self.start_screen).pack()

    def do_login(self):
        user = self.e_user.get().strip()
        pw_plain = self.e_pass.get().strip()
        pw_hashed = hash_password(pw_plain)
        if login_user(user, pw_hashed):
            info = get_user(user)
            role = info.get('User Type','Korisnik')
            self.logged_in_user = user
            messagebox.showinfo("Uspjeh", f"Uspješno ste prijavljeni kao {role}.")
            if role == "Administrator":
                self.admin_main_menu()
            elif role == "Zaposlenik":
                self.employee_main_menu()
            else:
                self.calendar_screen()
        else:
            messagebox.showerror("Greška","Pogrešno korisničko ime ili lozinka.")

    # --- Registration (always Korisnik) ---
    def register_screen(self):
        self.clear_frame()
        f = tk.Frame(self.root); f.pack(expand=True, pady=20)
        self.reg_entries = {}
        for label in ["Ime","Prezime","Telefon","Korisničko ime","Lozinka"]:
            tk.Label(f, text=label, font=("Arial",14)).pack(pady=3)
            show = "*" if label=="Lozinka" else None
            e = tk.Entry(f, font=("Arial",14), show=show)
            e.pack(pady=3)
            self.reg_entries[label] = e
        tk.Button(f, text="Registriraj se", font=("Arial",14),
                  command=self.do_register).pack(pady=10)
        tk.Button(f, text="Natrag", font=("Arial",14),
                  command=self.start_screen).pack()

    def do_register(self):
        d = {k: e.get().strip() for k,e in self.reg_entries.items()}
        if not all(d.values()):
            messagebox.showerror("Greška","Popunite sva polja.")
            return
        if os.path.exists("users.csv"):
            with open("users.csv", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    if row["Username"] == d["Korisničko ime"]:
                        messagebox.showerror("Greška","Korisničko ime već postoji!")
                        return
        pw_hashed = hash_password(d["Lozinka"])
        ok = create_user(d["Ime"], d["Prezime"], d["Telefon"],
                         d["Korisničko ime"], pw_hashed, "Korisnik")
        if ok:
            messagebox.showinfo("Uspjeh","Registracija uspješna!")
            self.start_screen()
        else:
            messagebox.showerror("Greška","Registracija nije uspjela.")

    # --- Administrator Main Menu ---
    def admin_main_menu(self):
        self.clear_frame()
        f = tk.Frame(self.root); f.pack(expand=True, pady=30)
        tk.Label(f, text="Administracijske opcije", font=("Arial",24)).pack(pady=10)
        options = [
            ("Rezerviraj termin",    self.admin_booking_screen),
            ("Rezervacije & Račun",  self.admin_reservations_screen),
            ("Dodaj administratora", self.add_admin_screen),
            ("Dodaj zaposlenika",    self.add_employee_screen),
            ("Obriši usera",         self.delete_user_screen),
            ("Dodaj uslugu",         self.add_service_screen),
            ("Obriši uslugu",        self.delete_service_screen),
        ]
        for text, cmd in options:
            tk.Button(f, text=text, font=("Arial",16), width=30,
                      command=cmd).pack(pady=5)
        tk.Button(f, text="Odjava", font=("Arial",14),
                  command=self.start_screen).pack(pady=20)
        tk.Button(f, text="Izlaz", font=("Arial",14),
                  command=self.root.quit).pack()

    # --- Employee Main Menu ---
    def employee_main_menu(self):
        self.clear_frame()
        f = tk.Frame(self.root); f.pack(expand=True, pady=30)
        tk.Label(f, text="Zaposlenik – opcije", font=("Arial",24)).pack(pady=10)
        options = [
            ("Rezerviraj termin",    self.admin_booking_screen),
            ("Rezervacije & Račun",  self.admin_reservations_screen),
        ]
        for text, cmd in options:
            tk.Button(f, text=text, font=("Arial",16), width=30,
                      command=cmd).pack(pady=5)
        tk.Button(f, text="Odjava", font=("Arial",14),
                  command=self.start_screen).pack(pady=20)
        tk.Button(f, text="Izlaz", font=("Arial",14),
                  command=self.root.quit).pack()

    # --- Calendar Helpers ---
    def _draw_calendar(self, day_callback):
        hdr = tk.Frame(self.root); hdr.pack(pady=5)
        tk.Button(hdr, text="<", command=self._prev_month).grid(row=0,column=0)
        self.lbl_mes = tk.Label(hdr, font=("Arial",18)); self.lbl_mes.grid(row=0,column=1,columnspan=5)
        tk.Button(hdr, text=">", command=self._next_month).grid(row=0,column=6)
        self.calendar_frame = tk.Frame(self.root); self.calendar_frame.pack()
        for i, dan in enumerate(DANI):
            tk.Label(self.calendar_frame, text=dan, font=("Arial",12)).grid(row=1,column=i,padx=2)
        y,m = self.current_year, self.current_month
        self.lbl_mes.config(text=f"{MJESECI[m-1]} {y}")
        first = dt.date(y,m,1); start = first.weekday()
        row, col = 2, start
        for d in range(1, get_days_in_month(y,m)+1):
            tk.Button(self.calendar_frame, text=str(d), width=4,
                      command=lambda d=d: day_callback(y,m,d))\
              .grid(row=row,column=col,padx=2,pady=2)
            col+=1
            if col>6: col, row = 0, row+1

    def _prev_month(self):
        if self.current_month==1:
            self.current_month, self.current_year = 12, self.current_year-1
        else:
            self.current_month-=1
        if self.current_context=='booking':
            self.admin_booking_screen()
        else:
            self.admin_reservations_screen()

    def _next_month(self):
        if self.current_month==12:
            self.current_month, self.current_year = 1, self.current_year+1
        else:
            self.current_month+=1
        if self.current_context=='booking':
            self.admin_booking_screen()
        else:
            self.admin_reservations_screen()

    # --- Booking Screen (Admin/Employee) ---
    def admin_booking_screen(self):
        self.current_context = 'booking'
        self.clear_frame()
        self._draw_calendar(self._admin_booking_day)
        btns = tk.Frame(self.root); btns.pack(pady=5)
        role = get_user(self.logged_in_user)['User Type']
        back = self.admin_main_menu if role=="Administrator" else self.employee_main_menu
        tk.Button(btns, text="Natrag", font=("Arial",14), command=back).pack(side="left", padx=5)
        tk.Button(btns, text="Odjava", font=("Arial",14), command=self.start_screen).pack(side="left")

    def _admin_booking_day(self, y, m, d):
        if hasattr(self,'detail_frame'): self.detail_frame.destroy()
        self.detail_frame = tk.Frame(self.root, bd=1, relief="sunken")
        self.detail_frame.pack(fill="x", pady=10, padx=10)
        if dt.date(y,m,d).weekday()>=5:
            tk.Label(self.detail_frame, text="Samo radni dani (Pon–Pet).", fg="red").pack(pady=5)
            return
        tk.Label(self.detail_frame, text=f"Rezervacija za {d:02d}.{m:02d}.{y}",
                 font=("Arial",12,"bold")).pack(pady=5)
        users = [u["Username"] for u in csv.DictReader(open("users.csv", encoding="utf-8"))]
        tk.Label(self.detail_frame, text="Korisnik:").pack(anchor="w")
        cb_u = ttk.Combobox(self.detail_frame, values=users, state="readonly"); cb_u.pack(pady=2)
        tk.Label(self.detail_frame, text="Termin:").pack(anchor="w")
        cb_t = ttk.Combobox(self.detail_frame, values=get_available_times(y,m,d), state="readonly"); cb_t.pack(pady=2)
        tk.Label(self.detail_frame, text="Usluga:").pack(anchor="w")
        cb_s = ttk.Combobox(self.detail_frame, values=[s['name'] for s in load_services()], state="readonly"); cb_s.pack(pady=2)
        tk.Button(self.detail_frame, text="Rezerviraj", font=("Arial",12),
                  command=lambda: self._admin_book_and_confirm(y,m,d,cb_u.get(),cb_t.get(),cb_s.get())
                 ).pack(pady=10)

    def _admin_book_and_confirm(self, y, m, d, user, t, srv):
        if not (user and t and srv):
            messagebox.showwarning("Upozorenje","Popunite sve podatke.")
            return
        save_appointment(y,m,d,t,srv,user)
        messagebox.showinfo("Uspjeh", f"Termin za {user} rezerviran: {d:02d}.{m:02d}.{y} u {t}.")

    # --- Reservations & Receipt Screen ---
    def admin_reservations_screen(self):
        self.current_context = 'review'
        self.clear_frame()
        self._draw_calendar(self._admin_review_day)
        btns = tk.Frame(self.root); btns.pack(pady=5)
        role = get_user(self.logged_in_user)['User Type']
        back = self.admin_main_menu if role=="Administrator" else self.employee_main_menu
        tk.Button(btns, text="Natrag", font=("Arial",14), command=back).pack(side="left", padx=5)
        tk.Button(btns, text="Odjava", font=("Arial",14), command=self.start_screen).pack(side="left")

    def _admin_review_day(self, y, m, d):
        if hasattr(self,'detail_frame'): self.detail_frame.destroy()
        self.detail_frame = tk.Frame(self.root, bd=1, relief="sunken")
        self.detail_frame.pack(fill="both", expand=True, pady=10, padx=10)
        tk.Label(self.detail_frame, text=f"Rezervacije za {d:02d}.{m:02d}.{y}",
                 font=("Arial",12,"bold")).pack(pady=5)
        self.list_reservations(self.detail_frame, y, m, d)

    # --- Filtered Reservations List ---
    def list_reservations(self, parent, y, m, d):
        for w in parent.winfo_children():
            if not (isinstance(w, tk.Label) and w.cget("font")==("Arial",12,"bold")):
                w.destroy()
        svi = [r for r in csv.DictReader(open("appointments.csv", encoding="utf-8"))
               if int(r["Godina"])==y and int(r["Mjesec"])==m and int(r["Dan"])==d]
        if self.get_user_type()=="Korisnik":
            svi = [r for r in svi if r["Korisnik"]==self.logged_in_user]
        if not svi:
            tk.Label(parent, text="Nema rezervacija.", anchor="w").pack(fill="x")
            return
        for r in svi:
            f = tk.Frame(parent); f.pack(fill="x", pady=2)
            txt = f"{r['Vrijeme']} – {r['Usluga']} ({r['Korisnik']})"
            tk.Label(f, text=txt, anchor="w").pack(side="left", fill="x", expand=True)
            if self.get_user_type() in ("Zaposlenik","Administrator"):
                tk.Button(f, text="Ispiši račun", font=("Arial",10),
                          command=lambda r=r: self.print_txt_receipt(
                              r["Korisnik"], y, m, d, r["Vrijeme"], r["Usluga"]
                          )).pack(side="right")

    # --- Add Service / Delete Service ---
    def add_service_screen(self):
        self.clear_frame()
        f = tk.Frame(self.root); f.pack(pady=20)
        tk.Label(f, text="Ime usluge:", font=("Arial",14)).pack(pady=3)
        self.svc_name = tk.Entry(f, font=("Arial",14)); self.svc_name.pack(pady=3)
        tk.Label(f, text="Cijena:", font=("Arial",14)).pack(pady=3)
        self.svc_price = tk.Entry(f, font=("Arial",14)); self.svc_price.pack(pady=3)
        tk.Button(f, text="Dodaj", font=("Arial",14),
                  command=self.do_add_service).pack(pady=10)
        tk.Button(f, text="Natrag", font=("Arial",14), command=self.admin_main_menu).pack()

    def do_add_service(self):
        ime, cij = self.svc_name.get().strip(), self.svc_price.get().strip()
        if add_service(ime, cij):
            messagebox.showinfo("Uspjeh","Usluga dodana.")
        else:
            messagebox.showerror("Greška","Neuspjelo dodavanje.")
        self.admin_main_menu()

    def delete_service_screen(self):
        self.clear_frame()
        f = tk.Frame(self.root); f.pack(pady=20)
        tk.Label(f, text="Odaberi uslugu za brisanje:", font=("Arial",14)).pack(pady=3)
        svcs = [s['name'] for s in load_services()]
        self.del_svc_cb = ttk.Combobox(f, values=svcs); self.del_svc_cb.pack(pady=3)
        tk.Button(f, text="Obriši", font=("Arial",14), command=self.do_delete_service).pack(pady=10)
        tk.Button(f, text="Natrag", font=("Arial",14), command=self.admin_main_menu).pack()

    def do_delete_service(self):
        ime = self.del_svc_cb.get()
        delete_service(ime)
        messagebox.showinfo("Uspjejh","Usluga obrisana.")
        self.admin_main_menu()

    # --- Add Administrator ---
    def add_admin_screen(self):
        self.clear_frame()
        f = tk.Frame(self.root); f.pack(pady=20)
        self.admin_entries = {}
        for label in ["Ime","Prezime","Telefon","Korisničko ime","Lozinka"]:
            tk.Label(f, text=label, font=("Arial",14)).pack(pady=3)
            show = "*" if label=="Lozinka" else None
            entry = tk.Entry(f, font=("Arial",14), show=show)
            entry.pack(pady=3)
            self.admin_entries[label] = entry
        tk.Button(f, text="Dodaj administratora", font=("Arial",14),
                  command=self.do_add_admin).pack(pady=10)
        tk.Button(f, text="Natrag", font=("Arial",14), command=self.admin_main_menu).pack()

    def do_add_admin(self):
        d = {k: e.get().strip() for k,e in self.admin_entries.items()}
        if "" in d.values():
            messagebox.showerror("Greška","Popunite sva polja.")
            return
        pw_hashed = hash_password(d["Lozinka"])
        ok = create_user(d["Ime"], d["Prezime"], d["Telefon"],
                         d["Korisničko ime"], pw_hashed, "Administrator")
        if ok:
            messagebox.showinfo("Uspjeh","Administrator dodan.")
        else:
            messagebox.showerror("Greška","Neuspjelo dodavanje.")
        self.admin_main_menu()

    # --- Add Employee ---
    def add_employee_screen(self):
        self.clear_frame()
        f = tk.Frame(self.root); f.pack(pady=20)
        self.emp_entries = {}
        for label in ["Ime","Prezime","Telefon","Korisničko ime","Lozinka"]:
            tk.Label(f, text=label, font=("Arial",14)).pack(pady=3)
            show = "*" if label=="Lozinka" else None
            e = tk.Entry(f, font=("Arial",14), show=show)
            e.pack(pady=3)
            self.emp_entries[label] = e
        tk.Button(f, text="Dodaj zaposlenika", font=("Arial",14),
                  command=self.do_add_employee).pack(pady=10)
        tk.Button(f, text="Natrag", font=("Arial",14), command=self.admin_main_menu).pack()

    def do_add_employee(self):
        d = {k: e.get().strip() for k,e in self.emp_entries.items()}
        if "" in d.values():
            messagebox.showerror("Greška","Popunite sva polja.")
            return
        pw_hashed = hash_password(d["Lozinka"])
        ok = create_user(d["Ime"], d["Prezime"], d["Telefon"],
                         d["Korisničko ime"], pw_hashed, "Zaposlenik")
        if ok:
            messagebox.showinfo("Uspjeh","Zaposlenik dodan.")
        else:
            messagebox.showerror("Greška","Dodavanje nije uspjelo.")
        self.admin_main_menu()

    # --- Delete User ---
    def delete_user_screen(self):
        """Show a list of all users and allow deletion."""
        self.clear_frame()
        f = tk.Frame(self.root); f.pack(pady=20, fill="both", expand=True)
        tk.Label(f, text="Obriši usera", font=("Arial",18)).pack(pady=10)

        users = [r["Username"]
                 for r in csv.DictReader(open("users.csv", encoding="utf-8"))]

        tk.Label(f, text="Odaberi usera za brisanje:", font=("Arial",14)).pack(pady=5)
        self.del_user_cb = ttk.Combobox(f, values=users, state="readonly", font=("Arial",14))
        self.del_user_cb.pack(pady=5)

        btns = tk.Frame(f); btns.pack(pady=15)
        tk.Button(btns, text="Obriši usera", font=("Arial",14),
                  command=self.do_delete_user).pack(side="left", padx=10)
        tk.Button(btns, text="Natrag", font=("Arial",14),
                  command=self.admin_main_menu).pack(side="left")

    def do_delete_user(self):
        """Remove the selected user from users.csv."""
        username = self.del_user_cb.get()
        if not username:
            messagebox.showwarning("Upozorenje", "Odaberite usera.")
            return

        rows = list(csv.DictReader(open("users.csv", encoding="utf-8")))
        new_rows = [r for r in rows if r["Username"] != username]

        with open("users.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(new_rows)

        messagebox.showinfo("Uspjeh", f"User '{username}' obrisan.")
        self.admin_main_menu()

    # --- Generate TXT Receipt ---
    def print_txt_receipt(self, user, y, m, d, t, srv):
        dirr = os.path.join(os.path.dirname(__file__),'racuni')
        os.makedirs(dirr, exist_ok=True)
        fname = os.path.join(dirr, f"racun_{user}_{d}_{m}_{y}.txt")
        price = next((s['price'] for s in load_services() if s['name']==srv), 0)
        with open(fname, 'w', encoding='utf-8') as f:
            f.write("      RAČUN\n========================\n")
            f.write(f"Korisnik: {user}\nDatum: {d}.{m}.{y}\nVrijeme: {t}\n")
            f.write(f"Usluga: {srv}\nCijena: {price:.2f} EUR\n========================\n")
            f.write("Hvala na povjerenju!\n")
        messagebox.showinfo("Račun","TXT račun spremljen u 'racuni' folderu.")

    # --- Customer Calendar & Booking ---
    def calendar_screen(self):
        self.clear_frame()
        hdr = tk.Frame(self.root); hdr.pack(pady=5)
        tk.Button(hdr, text="<", command=self.prev_month).grid(row=0,column=0)
        self.lbl_mes = tk.Label(hdr, font=("Arial",18)); self.lbl_mes.grid(row=0,column=1,columnspan=5)
        tk.Button(hdr, text=">", command=self.next_month).grid(row=0,column=6)

        self.calendar_frame = tk.Frame(self.root); self.calendar_frame.pack()
        for i, dan in enumerate(DANI):
            tk.Label(self.calendar_frame, text=dan, font=("Arial",12))\
              .grid(row=1,column=i,padx=2)
        self.draw_days()

        self.detail_frame = tk.Frame(self.root, bd=1, relief="sunken")
        self.detail_frame.pack(fill="x", pady=10, padx=10)
        review = tk.LabelFrame(self.detail_frame, text="Pregled rezervacija", padx=5, pady=5)
        review.pack(fill="x", pady=5)
        self.list_reservations(review, self.current_year, self.current_month, 1)

        nav = tk.Frame(self.root); nav.pack(pady=5)
        tk.Button(nav, text="Natrag", font=("Arial",14), command=self.start_screen).pack(side="left", padx=5)
        tk.Button(nav, text="Odjava", font=("Arial",14), command=self.start_screen).pack(side="left")

    def prev_month(self):
        if self.current_month==1:
            self.current_month, self.current_year = 12, self.current_year-1
        else:
            self.current_month-=1
        self.calendar_screen()

    def next_month(self):
        if self.current_month==12:
            self.current_month, self.current_year = 1, self.current_year+1
        else:
            self.current_month+=1
        self.calendar_screen()

    def draw_days(self):
        for w in self.calendar_frame.winfo_children():
            if w.grid_info().get("row",0)>=2: w.destroy()
        y,m = self.current_year, self.current_month
        self.lbl_mes.config(text=f"{MJESECI[m-1]} {y}")
        first = dt.date(y,m,1); start = first.weekday()
        row,col = 2,start
        for d in range(1, get_days_in_month(y,m)+1):
            tk.Button(self.calendar_frame, text=str(d), width=4,
                      command=lambda d=d: self.user_day_screen(y,m,d))\
              .grid(row=row, column=col, padx=2, pady=2)
            col+=1
            if col>6: col, row = 0, row+1

    def user_day_screen(self, y, m, d):
        for w in self.detail_frame.winfo_children(): w.destroy()
        role = self.get_user_type()
        weekday = dt.date(y,m,d).weekday()

        review = tk.LabelFrame(self.detail_frame, text="Pregled rezervacija", padx=5, pady=5)
        review.pack(fill="x", pady=5)
        self.list_reservations(review, y, m, d)

        if role=="Korisnik":
            if weekday>=5:
                tk.Label(self.detail_frame, text="Samo radni dani (Pon–Pet).", fg="red").pack()
                return
            tk.Label(self.detail_frame, text="Termin:").pack(anchor="w")
            cb_t = ttk.Combobox(self.detail_frame, values=get_available_times(y,m,d)); cb_t.pack(pady=2)
            tk.Label(self.detail_frame, text="Usluga:").pack(anchor="w")
            cb_s = ttk.Combobox(self.detail_frame, values=[s['name'] for s in load_services()]); cb_s.pack(pady=2)
            tk.Button(self.detail_frame, text="Rezerviraj", font=("Arial",12),
                      command=lambda: self._user_book(y,m,d,cb_t.get(),cb_s.get())).pack(pady=10)

    def _user_book(self, y, m, d, t, srv):
        if not (t and srv):
            messagebox.showwarning("Upozorenje","Popunite sve."); return
        save_appointment(y,m,d,t,srv,self.logged_in_user)
        messagebox.showinfo("Uspjeh", f"Termin rezerviran: {d:02d}.{m:02d}.{y} u {t}.")
        self.user_day_screen(y,m,d)

    def get_user_type(self):
        info = get_user(self.logged_in_user)
        return info.get("User Type","") if info else ""
