import tkinter as tk
from gui_app import KozmetickiSalonApp
import os

if __name__ == "__main__":
    file_path = __file__
    working_directory = file_path.rsplit("\\", maxsplit=1)[0]
    os.chdir(working_directory)

    root = tk.Tk()
    root.geometry("1000x700")
    app = KozmetickiSalonApp(root)
    root.mainloop()

