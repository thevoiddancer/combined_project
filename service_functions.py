
import csv
import os

FILENAME = 'services.csv'

def load_services():
    services = []
    if not os.path.exists(FILENAME):
        with open(FILENAME, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'price'])
        return services

    with open(FILENAME, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                price = float(row['price'])
            except:
                price = 0.0
            services.append({'name': row['name'], 'price': price})
    return services

def add_service(name, price):
    try:
        price_f = float(price)
    except:
        return False
    name = name.strip()
    services = load_services()
    if any(s['name'].lower() == name.lower() for s in services):
        return False
    services.append({'name': name, 'price': price_f})
    _save_services(services)
    return True

def delete_service(name):
    name = name.strip()
    services = load_services()
    services = [s for s in services if s['name'].lower() != name.lower()]
    _save_services(services)

def _save_services(services):
    with open(FILENAME, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'price'])
        writer.writeheader()
        for s in services:
            writer.writerow({'name': s['name'], 'price': s['price']})
