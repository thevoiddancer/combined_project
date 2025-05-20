import tkinter as tk
from PIL import Image, ImageTk
from components.login_frame import LoginFrame
from components.signup_frame import SignupFrame
from views.admin_dashboard import AdminDashboard
from views.user_dashboard import UserDashboard
from views.employee_dashboard import EmployeeDashboard

class BeautySalonApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Kozmetički salon")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        self.setup_background()
        self.setup_welcome()

    def setup_background(self):
        bg_image = Image.open("pictures/pozadina.png")
        bg_image = bg_image.resize((700, 500))
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.image = self.bg_photo
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def setup_welcome(self):
        self.welcome_label = tk.Label(
            self.root,
            text="Dobro došli u kozmetički salon",
            font=("Helvetica", 20, "bold"),
            fg="black"
        )
        self.welcome_label.place(relx=0.5, rely=0.4, anchor="center")
        self.root.after(2000, self.show_buttons)

    def show_buttons(self):
        self.welcome_label.place_forget()
        
        self.signup_btn = tk.Button(
            self.root,
            text="Sign up",
            font=("Helvetica", 14),
            width=12,
            command=self.open_signup
        )
        self.signup_btn.place(relx=0.3, rely=0.6, anchor='center')

        self.login_btn = tk.Button(
            self.root,
            text="Login",
            font=("Helvetica", 14),
            width=12,
            command=self.open_login
        )
        self.login_btn.place(relx=0.7, rely=0.6, anchor='center')

    def hide_main_buttons(self):
        self.signup_btn.place_forget()
        self.login_btn.place_forget()

    def open_signup(self):
        self.hide_main_buttons()
        signup_frame = SignupFrame(
            self.root,
            on_success=self.on_signup_success,
            on_back=lambda: [signup_frame.destroy(), self.show_buttons()]
        )
        signup_frame.place(relx=0.5, rely=0.5, anchor="center")

    def open_login(self):
        self.hide_main_buttons()

        login_frame = LoginFrame(
            self.root,
            on_success=self.on_login_success,
            on_back=lambda: [login_frame.destroy(), self.show_buttons()]
        )
        login_frame.place(relx=0.5, rely=0.5, anchor="center")


    def on_signup_success(self, ime, prezime, broj):
        self.open_user_dashboard(ime, prezime, broj)

    def on_login_success(self, user_type, user_data):
        if user_type == "admin":
            self.open_admin_dashboard(user_data["ime"], user_data["prezime"])
        elif user_type == "user":
            self.open_user_dashboard(user_data["Ime"], user_data["Prezime"], user_data["Broj"])
        elif user_type == "employee":
            self.open_employee_dashboard(user_data["Ime"], user_data["Prezime"])

    def open_admin_dashboard(self, ime, prezime):
        AdminDashboard(self.root, ime, prezime, on_logout=self.show_buttons)

    def open_user_dashboard(self, ime, prezime, broj):
        UserDashboard(self.root, ime, prezime, broj, on_logout=self.show_buttons)

    def open_employee_dashboard(self, ime, prezime):
        EmployeeDashboard(self.root, ime, prezime, on_logout=self.show_buttons)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = BeautySalonApp()
    app.run() 