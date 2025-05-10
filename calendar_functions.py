import csv
import os
import datetime as dt

def get_days_in_month(year, month):
    if month == 12:
        return 31
    next_month = dt.date(year if month < 12 else year + 1, month % 12 + 1, 1)
    this_month = dt.date(year, month, 1)
    return (next_month - this_month).days

def save_appointment(year, month, day, time_slot, service, username):
    filename = 'appointments.csv'
    appointments = []

    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file)
            appointments = list(reader)

    appointments.append({
        'Godina': year,
        'Mjesec': month,
        'Dan': day,
        'Vrijeme': time_slot,
        'Usluga': service,
        'Korisnik': username
    })

    appointments.sort(key=lambda x: (
        int(x['Godina']), int(x['Mjesec']), int(x['Dan']),
        int(x['Vrijeme'].split(':')[0]), int(x['Vrijeme'].split(':')[1])
    ))

    with open(filename, 'w', encoding='utf-8', newline='') as file:
        fieldnames = ['Godina', 'Mjesec', 'Dan', 'Vrijeme', 'Usluga', 'Korisnik']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(appointments)

def get_available_times(year, month, day, timeslots=None):
    filename = 'appointments.csv'
    booked = set()

    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if (int(row['Godina']) == year and
                    int(row['Mjesec']) == month and
                    int(row['Dan']) == day):
                    booked.add(row['Vrijeme'])

    if timeslots is None:
        timeslots = [f"{h:02}:00" for h in range(8, 17)]

    available = [slot for slot in timeslots if slot not in booked]
    return available
