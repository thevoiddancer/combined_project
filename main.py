import tkinter as tk
from gui_app import KozmetickiSalonApp

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x700")
    app = KozmetickiSalonApp(root)
    root.mainloop()

