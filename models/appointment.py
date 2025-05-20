class Appointment:
    def __init__(self, ime, prezime, broj, datum, vrijeme, zahvat):
        self.ime = ime
        self.prezime = prezime
        self.broj = broj
        self.datum = datum
        self.vrijeme = vrijeme
        self.zahvat = zahvat

    def __str__(self):
        return f"{self.ime} {self.prezime} - {self.datum} u {self.vrijeme} -> {self.zahvat}" 