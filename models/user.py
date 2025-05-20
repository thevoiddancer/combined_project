class User:
    def __init__(self, ime, prezime, broj, nadimak, lozinka):
        self.ime = ime
        self.prezime = prezime
        self.broj = broj
        self.nadimak = nadimak
        self.lozinka = lozinka

    @property
    def full_name(self):
        return f"{self.ime} {self.prezime}" 