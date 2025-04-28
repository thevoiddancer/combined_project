
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import csv
import os
from validation.validators import is_valid_password


def start_app():
    root = tk.Tk()
    root.title("Kozmetički salon")
    root.geometry("700x500")
    root.resizable(False, False)

    # Učitavanje pozadinske slike
    bg_image = Image.open("slike/pozadina.png")
    bg_image = bg_image.resize((700, 500))
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo 
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Dobrodošlica
    welcome_label = tk.Label(
        root, 
        text="Dobro došli u kozmetički salon",
        font=("Helvetica", 20, "bold"),
        fg="black"
)
    welcome_label.place(relx=0.5, rely=0.4, anchor="center")

    # Gumbi -> Signup i login
    def show_buttons():
        welcome_label.place_forget()
        signup_btn.place(relx=0.3, rely=0.6, anchor='center')
        login_btn.place(relx=0.7, rely=0.6, anchor='center')

    signup_btn = tk.Button(
        root, 
        text="Sign up", 
        font=("Helvetica", 14), width=12,
        command=lambda: open_signup()
)
    login_btn = tk.Button(
        root, 
        text="Login", 
        font=("Helvetica", 14), 
        width=12,
        command=lambda: open_login()
)

#----------------------------------------------------------------------------------------------------

    def open_signup():
        signup_btn.place_forget()
        login_btn.place_forget()

        # Centriranje signup prozora
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(2, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(2, weight=1)

        # Signup frame
        signup_frame = tk.Frame(root, padx=20, pady=20, bg="light salmon")
        signup_frame.grid(row=1, column=1)

        labels = [
            "Ime", 
            "Prezime", 
            "Broj mobitela", 
            "Nadimak", 
            "Lozinka", 
            "Potvrdi lozinku"
]
        
        entries = []

        for i, label_text in enumerate(labels):
            label = tk.Label(signup_frame, text=label_text)
            label.grid(row=i, column=0, pady=10, padx=10, sticky="e")

            entry = tk.Entry(
            signup_frame,
            width=30, 
            show="*" if "lozinka" in label_text.lower() else "")

            entry.grid(row=i, column=1, pady=10)
            entries.append(entry)


        def save_user():
            ime, prezime, broj, nadimak, lozinka, potvrda = [e.get() for e in entries]

            if not all([ime, prezime, broj, nadimak, lozinka, potvrda]):
                messagebox.showerror("Greška", "Sva polja su obavezna.")
                return
            
            if lozinka != potvrda:
                messagebox.showerror("Greška", "Lozinke se ne podudaraju.")
                return

            if not is_valid_password(lozinka):
                messagebox.showerror("Greška", "Lozinka mora imati veliko slovo, broj i poseban znak.")
                return

            filepath = "data/users.csv"
            os.makedirs("data", exist_ok=True)
            file_exists = os.path.isfile(filepath)

            with open(filepath, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(
                        ["Ime", 
                         "Prezime", 
                         "Broj", 
                         "Nadimak", 
                         "Lozinka"]
)
                    
                writer.writerow([ime, prezime, broj, nadimak, lozinka])

            messagebox.showinfo("Uspješno", "Registracija je uspješna!")
            open_user_dashboard(ime, prezime, broj)

        # Gumb za registraciju
        register_btn = tk.Button(
            signup_frame, 
            text="Registriraj se", 
            command=lambda: [save_user(), signup_frame.destroy()] 
    )
        register_btn.grid(row=len(labels), columnspan=2, pady=20)

            # Gumb za nazad
        back_signup = tk.Button(
            signup_frame, 
            text="Nazad",
            command=lambda: [signup_frame.destroy(), show_buttons()]
    )
        
        back_signup.grid(row=6, column=3, pady=20)

#----------------------------------------------------------------------------------------------------------
    def open_login():
        signup_btn.place_forget()
        login_btn.place_forget()

        # Centriranje login prozora
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(2, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(2, weight=1)

        # Login frame
        login_frame = tk.Frame(root, padx=20, pady=20, bg="light salmon")
        login_frame.grid(row=1, column=1)

        # Label i unos za Nadimak
        tk.Label(login_frame, text="Nadimak").grid(
            row=0, 
            column=0, 
            pady=10, 
            padx=10, 
            sticky="e"
)
        
        username_entry = tk.Entry(login_frame, width=30)
        username_entry.grid(row=0, column=1, pady=10)

        # Labela i unos za Lozinku
        tk.Label(login_frame, text="Lozinka").grid(
            row=1, 
            column=0, 
            pady=10, 
            padx=10, 
            sticky="e"
)
        
        password_entry = tk.Entry(login_frame, width=30, show="*")
        password_entry.grid(row=1, column=1, pady=10)

        def login():
            username = username_entry.get()
            password = password_entry.get()

            # ADMIN provjera
            if username == "Caskey" and password == "#Caskey123":
                open_admin_dashboard("Antonio", "Šiljac")
                return

            # Provjera korisnika u users.csv
            user_filepath = "data/users.csv"
            if os.path.isfile(user_filepath):
                with open(user_filepath, newline="", encoding="utf-8") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if row["Nadimak"] == username and row["Lozinka"] == password:
                            ime = row["Ime"]
                            prezime = row["Prezime"]
                            broj = row["Broj"]
                            open_user_dashboard(ime, prezime, broj)
                            return

            # Provjera zaposlenika u zaposlenici.csv
            zaposlenik_filepath = "data/zaposlenici.csv"
            if os.path.isfile(zaposlenik_filepath):
                with open(zaposlenik_filepath, newline="", encoding="utf-8") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if row["Nadimak"] == username and row["Lozinka"] == password:
                            ime = row["Ime"]
                            prezime = row["Prezime"]
                            open_zaposlenik_dashboard(ime, prezime)
                            return

            # Ako nitko nije pronađen
            messagebox.showerror("Greška", "Pogrešan nadimak ili lozinka.")
            show_buttons()
            
        # Gumb za potvrdu
        potvrdi_btn = tk.Button(
            login_frame, 
            text="Potvrdi", 
            command=lambda:[login(), login_frame.destroy()]
)
        potvrdi_btn.grid(row=2, columnspan=2, pady=20)

        back_login = tk.Button(
            login_frame, 
            text="Nazad", 
            command=lambda:[login_frame.destroy(), show_buttons()]
)
        back_login.grid(row=6, column=3, pady=20)

#--------------------------------------------------------------------------------------------------------

    def open_admin_dashboard(ime, prezime):

        def clear_root():
            for widget in root.winfo_children():
                if isinstance(widget, tk.Frame):
                    widget.destroy()

        clear_root()

        admin_frame = tk.Frame(root, padx=20, pady=20, bg="light salmon")
        admin_frame.grid(row=1, column=1)

        tk.Label(
            admin_frame, 
            text=f"ADMIN: {ime} {prezime}", 
            font=("Helvetica", 16, "bold")).pack(pady=10)


        def prikazi_termine():
            filepath = "data/zakazani_termini.csv"
            if not os.path.isfile(filepath):
                messagebox.showinfo("Nema termina", "Nema zakazanih termina.")
                return

            tekst = ""
            with open(filepath, newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    tekst += f"{row['Ime']} {row['Prezime']} - {row['Datum']} u {row['Vrijeme']}\n"

            clear_root()
            
            termini_frame = tk.Frame(
                root, 
                padx=20, 
                pady=20, 
                bg="light salmon"
)
            termini_frame.grid(row=1, column=1)

            tk.Label(
                termini_frame, 
                text="Zakazani termini", 
                font=("Helvetica", 14, "bold")).pack(pady=10)
            
            text_box = tk.Text(termini_frame, wrap="word", height=15, width=50)
            text_box.insert("1.0", tekst if tekst else "Nema zakazanih termina.")
            text_box.config(state="disabled")
            text_box.pack()

            tk.Button(
                termini_frame, 
                text="Nazad", 
                command=lambda: [termini_frame.destroy(), open_admin_dashboard(ime, prezime)]).pack(pady=10)


        def dodaj_zaposlenika():
            clear_root()

            dodaj_frame = tk.Frame(root, padx=20, pady=20, bg="light salmon")
            dodaj_frame.grid(row=1, column=1)

            labels = [
                "Ime", 
                "Prezime", 
                "Pozicija", 
                "Broj", 
                "Nadimak", 
                "Lozinka"
]
            entries = []

            for i, label_text in enumerate(labels):
                label = tk.Label(dodaj_frame, text=label_text)
                label.grid(row=i, column=0, pady=10, padx=10, sticky="e")

                entry = tk.Entry(
                    dodaj_frame, 
                    width=30, 
                    show="*" if "lozinka" in label_text.lower() else ""
)
                entry.grid(row=i, column=1, pady=10)
                entries.append(entry)


            def spremi():
                values = [e.get() for e in entries]

                if not all(values):
                    messagebox.showerror("Greška", "Sva polja su obavezna.")
                    return

                filepath = "data/zaposlenici.csv"
                os.makedirs("data", exist_ok=True)

                with open(filepath, "a", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    if os.stat(filepath).st_size == 0:
                        writer.writerow(["Ime", "Prezime", "Pozicija", "Broj", "Nadimak", "Lozinka"])
                    writer.writerow(values)

                messagebox.showinfo("Uspjeh", "Zaposlenik dodan.")
                open_admin_dashboard(ime, prezime)

            spremi_admin = tk.Button(
                dodaj_frame, 
                text="Spremi", 
                command=spremi
)
            spremi_admin.grid(row=len(labels), columnspan=2,pady=20 )

            nazad_admin = tk.Button(
                dodaj_frame, 
                text="Nazad", 
                command=lambda: [dodaj_frame.destroy(), open_admin_dashboard(ime, prezime)]
)
            nazad_admin.grid(row=6, column=3, pady=20)


        def ukloni_zaposlenika():
            filepath = "data/zaposlenici.csv"
            if not os.path.isfile(filepath):
                messagebox.showinfo("Info", "Nema zaposlenika.")
                return

            clear_root()
            ukloni_frame = tk.Frame(root, padx=20, pady=20, bg="light salmon")
            ukloni_frame.grid(row=1, column=1)

            with open(filepath, newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                zaposlenici = list(reader)

            tk.Label(
                ukloni_frame, 
                text="Ukloni zaposlenika", 
                font=("Helvetica", 16, "bold")).pack(pady=10)

            lista = tk.Listbox(ukloni_frame, height=10, width=50)
            entries = [f"{z['Ime']} {z['Prezime']} ({z['Nadimak']}) - {z['Pozicija']}" for z in zaposlenici]
                
            for entry in entries:
                lista.insert("end", entry)
            lista.pack(pady=10)


            def obrisi():
                idx = lista.curselection()
                if not idx:
                    messagebox.showerror("Greška", "Odaberi zaposlenika.")
                    return

                del zaposlenici[idx[0]]

                with open(filepath, "w", newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(
                        file, 
                        fieldnames=["Ime", "Prezime", "Pozicija", "Broj", "Nadimak", "Lozinka"]
)
                    writer.writeheader()
                    writer.writerows(zaposlenici)

                messagebox.showinfo("Uspjeh", "Zaposlenik uklonjen.")
                open_admin_dashboard(ime, prezime)

            tk.Button(
                ukloni_frame, 
                text="Ukloni", 
                command=obrisi).pack(pady=5)

            tk.Button(
                ukloni_frame, 
                text="Nazad", 
                command=lambda: [ukloni_frame.destroy(), open_admin_dashboard(ime, prezime)]).pack(pady=5)

        # Glavni gumbi
        tk.Button(
            admin_frame, 
            text="Dodaj zaposlenika", 
            width=25, 
            command=dodaj_zaposlenika).pack(pady=10)
        
        tk.Button(
            admin_frame, 
            text="Ukloni zaposlenika", 
            width=25, 
            command=ukloni_zaposlenika).pack(pady=10)
        
        tk.Button(
            admin_frame, 
            text="Zakazani termini", 
            width=25, 
            command=prikazi_termine).pack(pady=10)
        
        tk.Button(
            admin_frame, 
            text="Logout", 
            width=25, 
            command=lambda: [admin_frame.destroy(), show_buttons()]).pack(pady=10)

#-----------------------------------------------------------------------------------------------------------------------------------------------
    def open_zaposlenik_dashboard(ime, prezime):
        def clear_root():
            for widget in root.winfo_children():
                if isinstance(widget, tk.Frame):
                    widget.destroy()

        zaposlenik_frame = tk.Frame(root, padx=20, pady=20, bg="light salmon")
        zaposlenik_frame.grid(row=1, column=1)

        tk.Label(
            zaposlenik_frame, 
            text=f"Zaposlenik: {ime} {prezime}", font=("Helvetica", 16, "bold")).pack(pady=20)


        def zakazi_termin():
            clear_root()
            zakazi_frame_korisnik = tk.Frame(root, padx=20, pady=20, bg="light salmon")
            zakazi_frame_korisnik.grid(row=1, column=1)

            labels = [
                "Ime", 
                "Prezime", 
                "Broj", 
                "Datum (YYYY-MM-DD)", 
                "Vrijeme (HH:MM)", 
                "Zahvat"
]
            entries = []

            for i, label in enumerate(labels):
                label = tk.Label(zakazi_frame_korisnik, text=label)
                label.grid(row=i, column=0, pady=10, padx=10, sticky="e")

                entry = tk.Entry(zakazi_frame_korisnik, width=30)
                entry.grid(row=i, column=1, pady=10)
                entries.append(entry)
                

            def spremi():
                ime, prezime, broj, datum, vrijeme, zahvat = [e.get() for e in entries]

                if not all([ime, prezime, broj, datum, vrijeme, zahvat]):
                    messagebox.showerror("Greška", "Sva polja su obavezna.")
                    return
                
                filepath = "data/zakazani_termini.csv"
                novi_termin = {
                    "Ime": ime,
                    "Prezime": prezime,
                    "Broj": broj,
                    "Datum": datum,
                    "Vrijeme": vrijeme,
                    "Zahvat": zahvat
                }

                # Ako CSV ne postoji – napravi ga s headerom
                file_exists = os.path.isfile(filepath)
                if not file_exists:
                    with open(filepath, "w", newline="", encoding="utf-8") as file:
                        writer = csv.DictWriter(file, fieldnames=novi_termin.keys())
                        writer.writeheader()

                # Provjera postoji li već termin s istim datumom i vremenom
                with open(filepath, newline="", encoding="utf-8") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if row["Datum"] == datum and row["Vrijeme"] == vrijeme:
                            messagebox.showerror("Zauzeto", "Termin je već zauzet. Odaberite drugo vrijeme.")
                            return

                # Ako termin nije zauzet – upiši novi
                with open(filepath, "a", newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(file, fieldnames=novi_termin.keys())
                    writer.writerow(novi_termin)

                messagebox.showinfo("Uspjeh", "Termin je uspješno zakazan.")

            spremi_zaposlenik = tk.Button(
                zakazi_frame_korisnik, 
                text="Spremi", 
                command=lambda: [spremi(), zakazi_frame_korisnik.destroy(), open_zaposlenik_dashboard(ime, prezime)])
            
            spremi_zaposlenik.grid(row=len(labels), columnspan=2,pady=20 )

            nazad_zaposlenik = tk.Button(
                zakazi_frame_korisnik, 
                text="Nazad", 
                command=lambda: [zakazi_frame_korisnik.destroy(), open_zaposlenik_dashboard(ime, prezime)])
            
            nazad_zaposlenik.grid(row=6, column=3, pady=20)


        def prikazi_termine():
            clear_root()
            prikaz_frame = tk.Frame(root, padx=20, pady=20, bg="light salmon")
            prikaz_frame.grid(row=1, column=1)

            filepath = "data/zakazani_termini.csv"
            if not os.path.isfile(filepath):
                messagebox.showinfo("Nema termina", "Nema zakazanih termina.")
                return open_zaposlenik_dashboard(ime, prezime)

            with open(filepath, newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                tekst = ""
                for row in reader:
                    tekst += f"{row['Ime']} {row['Prezime']} - {row['Datum']} u {row['Vrijeme']} -> {row['Zahvat']}\n"

            text_box = tk.Text(prikaz_frame, wrap="word", height=20)
            text_box.insert("1.0", tekst if tekst else "Nema zakazanih termina.")
            text_box.config(state="disabled")
            text_box.pack(expand=True, fill="both", padx=10, pady=10)

            tk.Button(
                prikaz_frame, 
                text="Natrag", 
                command=lambda:[prikaz_frame.destroy(), open_zaposlenik_dashboard(ime, prezime)]).pack(pady=10)

        tk.Button(
            zaposlenik_frame, 
            text="Zakaži termin", 
            command=zakazi_termin).pack(pady=10)

        tk.Button(
            zaposlenik_frame, 
            text="Zakazani termini", 
            command=prikazi_termine).pack(pady=10)
        
        tk.Button(
            zaposlenik_frame, 
            text="Logout", 
            command=lambda: [zaposlenik_frame.destroy(), show_buttons()]).pack(pady=10)
#---------------------------------------------------------------------------------------------------------

    def open_user_dashboard(ime, prezime, broj):
        def clear_root():
            for widget in root.winfo_children():
                if isinstance(widget, tk.Frame):
                    widget.destroy()

        clear_root()

        user_frame = tk.Frame(root, padx=20, pady=20, bg="light salmon")
        user_frame.grid(row=1, column=1, sticky="nsew")

        welcome_text = f"Korisnik: {ime} {prezime}"
        tk.Label(
            user_frame, 
            text=welcome_text, 
            font=("Helvetica", 16, "bold")
        ).grid(row=0, column=0, pady=30, columnspan=2)

        def zakazi_termin_korisnik():
            clear_root()
            zakazi_frame_korisnik = tk.Frame(root, padx=20, pady=20, bg="light salmon")
            zakazi_frame_korisnik.grid(row=1, column=1)

            labels = [
                "Ime", 
                "Prezime", 
                "Broj", 
                "Datum (DD-MM-YYYY)", 
                "Vrijeme (HH:MM)", 
                "Zahvat"
            ]
            entries = []

            for i, label in enumerate(labels):
                label_widget = tk.Label(zakazi_frame_korisnik, text=label)
                label_widget.grid(row=i, column=0, pady=10, padx=10, sticky="e")

                entry = tk.Entry(zakazi_frame_korisnik, width=30)
                entry.grid(row=i, column=1, pady=10)
                entries.append(entry)

            entries[0].insert(0, ime)
            entries[1].insert(0, prezime)
            entries[2].insert(0, broj)

            def spremi():
                ime, prezime, broj, datum, vrijeme, zahvat = [e.get() for e in entries]

                if not all([ime, prezime, broj, datum, vrijeme, zahvat]):
                    messagebox.showerror("Greška", "Sva polja su obavezna.")
                    return

                filepath = "data/zakazani_termini.csv"
                novi_termin = {
                    "Ime": ime,
                    "Prezime": prezime,
                    "Broj": broj,
                    "Datum": datum,
                    "Vrijeme": vrijeme,
                    "Zahvat": zahvat
                }

                
                file_exists = os.path.isfile(filepath)
                if not file_exists:
                    with open(filepath, "w", newline="", encoding="utf-8") as file:
                        writer = csv.DictWriter(file, fieldnames=novi_termin.keys())
                        writer.writeheader()

                
                with open(filepath, newline="", encoding="utf-8") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if row["Datum"] == datum and row["Vrijeme"] == vrijeme:
                            messagebox.showerror("Zauzeto", "Termin je već zauzet. Odaberite drugo vrijeme.")
                            return

                
                with open(filepath, "a", newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(file, fieldnames=novi_termin.keys())
                    writer.writerow(novi_termin)

                messagebox.showinfo("Uspjeh", "Termin je uspješno zakazan.")

            spremi_zaposlenik = tk.Button(
                zakazi_frame_korisnik, 
                text="Spremi", 
                command=lambda: [spremi(), zakazi_frame_korisnik.destroy(), open_user_dashboard(ime, prezime, broj)]
            )
            spremi_zaposlenik.grid(row=len(labels), columnspan=2, pady=20)

            nazad_zaposlenik = tk.Button(
                zakazi_frame_korisnik, 
                text="Nazad", 
                command=lambda: [zakazi_frame_korisnik.destroy(), open_user_dashboard(ime, prezime, broj)]
            )
            nazad_zaposlenik.grid(row=6, column=3, pady=20)

        def otkazi_termin_korisnik(ime, prezime, broj):
            clear_root()

            otkazi_frame = tk.Frame(root, padx=20, pady=20, bg="light salmon")
            otkazi_frame.grid(row=1, column=1)

            tk.Label(
                otkazi_frame,
                text=f"Korisnik: {ime} {prezime} ",
                font=("Helvetica", 16, "bold")
            ).grid(row=0, column=0, pady=10)

            filepath = "data/zakazani_termini.csv"
            listbox = tk.Listbox(otkazi_frame, width=60, height=10)
            listbox.grid(row=1, column=0, pady=10)

            # Učitaj sve termine
            if not os.path.isfile(filepath):
                messagebox.showinfo("Nema termina", "Nema zakazanih termina.")
                return open_user_dashboard(ime, prezime, broj)

            with open(filepath, newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                svi_termini = list(reader)

            korisnik_termini = [
                row for row in svi_termini
                if row["Ime"] == ime and row["Prezime"] == prezime and row["Broj"] == broj
            ]

            for t in korisnik_termini:
                listbox.insert(tk.END, f"{t['Datum']} u {t['Vrijeme']} - {t['Zahvat']}")

            def otkazi_termin():
                selected = listbox.curselection()
                if not selected:
                    messagebox.showerror("Greška", "Odaberite termin za otkazivanje.")
                    return

                index = selected[0]
                termin_za_brisanje = korisnik_termini[index]
                svi_termini.remove(termin_za_brisanje)

                with open(filepath, "w", newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(file, fieldnames=["Ime", "Prezime", "Broj", "Datum", "Vrijeme", "Zahvat"])
                    writer.writeheader()
                    writer.writerows(svi_termini)

                messagebox.showinfo("Uspješno", "Termin je otkazan.")
                otkazi_frame.destroy()
                otkazi_termin_korisnik(ime, prezime, broj)

            if korisnik_termini:
                tk.Button(
                    otkazi_frame,
                    text="Otkaži odabrani termin",
                    command=otkazi_termin
                ).grid(row=2, column=0, pady=10)
            else:
                tk.Label(otkazi_frame, text="Nemate zakazanih termina.").grid(row=2, column=0, pady=10)

            tk.Button(
                otkazi_frame,
                text="Natrag",
                command=lambda: [otkazi_frame.destroy(), open_user_dashboard(ime, prezime, broj)]
            ).grid(row=3, column=0, pady=10)

        def prikazi_termine(ime, prezime, broj):
            clear_root()

            prikaz_frame = tk.Frame(root, padx=20, pady=20, bg="light salmon")
            prikaz_frame.grid(row=1, column=1)

            filepath = "data/zakazani_termini.csv"
            if not os.path.isfile(filepath):
                messagebox.showinfo("Nema termina", "Nema zakazanih termina.")
                return open_user_dashboard(ime, prezime, broj)

            with open(filepath, newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                tekst = ""
                for row in reader:
                    if row["Ime"] == ime and row["Prezime"] == prezime and row["Broj"] == broj:
                        tekst += f"{row['Datum']} u {row['Vrijeme']} -> {row['Zahvat']} (Kontakt: {row['Broj']})\n"

            text_box = tk.Text(prikaz_frame, wrap="word", height=20)
            text_box.insert("1.0", tekst if tekst else "Nema zakazanih termina.")
            text_box.config(state="disabled")
            text_box.grid(row=1, column=0, padx=10, pady=10)

            tk.Button(
                prikaz_frame,
                text="Natrag",
                command=lambda: [prikaz_frame.destroy(), open_user_dashboard(ime, prezime, broj)]
            ).grid(row=2, column=0, pady=10)

        # Gumbi za termine
        tk.Button(
            user_frame,
            text="Zakaži termin",
            width=20,
            font=("Helvetica", 12),
            command=lambda: zakazi_termin_korisnik()).grid(row=1, column=0, pady=10)

        tk.Button(
            user_frame,
            text="Otkaži termin",
            width=20,
            font=("Helvetica", 12),
            command=lambda: otkazi_termin_korisnik(ime, prezime, broj)).grid(row=2, column=0, pady=10)

        # Dodavanje gumba za pregled zakazanih termina
        tk.Button(
            user_frame,
            text="Moji termini",
            width=20,
            font=("Helvetica", 12),
            command=lambda: prikazi_termine(ime, prezime, broj)).grid(row=3, column=0, pady=10)

        tk.Button(
            user_frame, 
            text="Logout",
            width=20,
            font=("Helvetica", 12), 
            command=lambda: [user_frame.destroy(), show_buttons()]).grid(row=4, column=0, pady=10)
#-------------------------------------------------------------------------------------------------------


    root.after(2000, show_buttons)
    root.mainloop()   
       
start_app() 













