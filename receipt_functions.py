
import os
import uuid
from reportlab.lib.pagesizes import A6
from reportlab.pdfgen import canvas
from service_functions import load_services

def get_service_price(usluga):
    for s in load_services():
        if s["name"] == usluga:
            return s["price"]
    return 0

def generate_receipt(username, godina, mjesec, dan, vrijeme, usluga):
    racuni_dir = os.path.join(os.path.dirname(__file__), 'racuni')
    if not os.path.exists(racuni_dir):
        os.makedirs(racuni_dir)

    cijena = get_service_price(usluga)
    unique_id = str(uuid.uuid4())[:8]  # Kratki ID rezervacije

    filename = os.path.join(racuni_dir, f"racun_{unique_id}.pdf")
    c = canvas.Canvas(filename, pagesize=A6)

    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, 270, "RAČUN")
    c.setFont("Helvetica", 10)
    c.drawString(20, 250, f"ID rezervacije: {unique_id}")
    c.drawString(20, 230, f"Korisnik: {username}")
    c.drawString(20, 210, f"Datum: {dan}.{mjesec}.{godina}")
    c.drawString(20, 190, f"Vrijeme: {vrijeme}")
    c.drawString(20, 170, f"Usluga: {usluga}")
    c.drawString(20, 150, f"Cijena: {cijena:.2f} EUR")
    c.line(20, 140, 150, 140)
    c.drawString(20, 120, "Hvala na povjerenju!")

    c.showPage()
    c.save()
