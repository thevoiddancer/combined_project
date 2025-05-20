import csv
import os
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

class DataManager:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

    def save_appointment(self, appointment):
        filepath = os.path.join(self.data_dir, "zakazani_termini.csv")
        file_exists = os.path.isfile(filepath)
        
        with open(filepath, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Ime", "Prezime", "Broj", "Datum", "Vrijeme", "Zahvat"])
            writer.writerow([
                appointment.ime,
                appointment.prezime,
                appointment.broj,
                appointment.datum,
                appointment.vrijeme,
                appointment.zahvat
            ])

    def get_appointments(self):
        filepath = os.path.join(self.data_dir, "zakazani_termini.csv")
        if not os.path.isfile(filepath):
            return []
            
        appointments = []
        with open(filepath, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                appointments.append(row)
        return appointments

    def delete_appointment(self, appointment_to_delete):
        filepath = os.path.join(self.data_dir, "zakazani_termini.csv")
        appointments = self.get_appointments()
        
        filtered_appointments = [
            apt for apt in appointments 
            if not (
                apt["Ime"] == appointment_to_delete.ime and
                apt["Prezime"] == appointment_to_delete.prezime and
                apt["Datum"] == appointment_to_delete.datum and
                apt["Vrijeme"] == appointment_to_delete.vrijeme
            )
        ]

        with open(filepath, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["Ime", "Prezime", "Broj", "Datum", "Vrijeme", "Zahvat"])
            writer.writeheader()
            writer.writerows(filtered_appointments) 