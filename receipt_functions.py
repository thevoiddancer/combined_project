import os

SERVICE_PRICES = {
    "Manikura": 20,
    "Pedikura": 25,
    "Masaža": 30,
    "Šminkanje": 35
}

def generate_receipt(username, godina, mjesec, dan, vrijeme, usluga):
    racuni_dir = os.path.join(os.path.dirname(__file__), 'racuni')
    if not os.path.exists(racuni_dir):
        os.makedirs(racuni_dir)

    cijena = SERVICE_PRICES.get(usluga, 0)

    filename = os.path.join(racuni_dir, f"racun_{username}_{dan}_{mjesec}_{godina}.txt")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("      RAČUN\n")
        f.write("========================\n")
        f.write(f"Korisnik: {username}\n")
        f.write(f"Datum: {dan}.{mjesec}.{godina}\n")
        f.write(f"Vrijeme: {vrijeme}\n")
        f.write(f"Usluga: {usluga}\n")
        f.write(f"Cijena: {cijena} EUR\n")
        f.write("========================\n")
        f.write("Hvala na povjerenju!\n")
