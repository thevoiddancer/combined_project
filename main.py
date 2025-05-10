import os
import tkinter as tk
from gui_app import KozmetickiSalonApp

if __name__ == "__main__":
    # Postavi radni direktorij na onaj u kojem se nalazi ovaj skript
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # Pokretanje GUI aplikacije
    root = tk.Tk()
    root.geometry("1000x700")
    app = KozmetickiSalonApp(root)
    root.mainloop()

