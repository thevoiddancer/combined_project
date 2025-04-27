
# 1. Project Title

**Beauty Salon / Kozmetički Salon**

# 2. Project Description

This is a student project, created as part of the *Machina Game Dev Academy - Python Programming* course.  
It is a simple desktop application built with Python and Tkinter that allows users to register, log in, book appointments for various beauty services, and generate receipts.  
The application features an intuitive calendar system, service selection, and invoice creation after reservation.  

**Main Features:**
- User registration
- User login
- Calendar for selecting dates
- Time and service selection
- Receipt generation in .txt format
- Clean and simple GUI
- Application is in Croatian language

# 3. Table of Contents
- Project Title
- Project Description
- Table of Contents
- How to Install and Run the Project
- How to Use the Project

# 4. How to Install and Run the Project "Kozmetički Salon" / "Beauty Salon"

**Requirements:**
- Python version 3.10 or newer
- Tkinter (comes pre-installed with Python)
- Recommended IDE: Visual Studio Code

**Installation:**
1. Clone the repository or download all project files.
2. Open the terminal in the project folder and run:  
   `python3 main.py`  
   or simply use **Run Python File** in Visual Studio Code.

# 5. How to Use the Project

## 5.1 Starting the Application
- After running `main.py`, the start screen will open with options:
  - **Login** (for existing users)
  - **Register** (for new users)
  - **Exit** (will close the app)

## 5.2 User Registration
- Fill in all required fields: 
  - First name (Ime)
  - Last name (Prezime)
  - Phone number (Broj mobitela)
  - Username (Korisničko ime)
  - Password (Lozinka)
  - User type (Tip korisnika)

- Click the **Register** (**Registriraj**) button.

> *Note:* You can navigate back to the main screen anytime by clicking the **Back** (**Natrag**) button.

- After successful registration, the app will return to the start screen.

## 5.3 User Login
- Enter your username (Korisničko ime) and password (Lozinka).
- After successful login, the calendar view will be displayed.

## 5.4 Booking an Appointment
- Select a date from the calendar.
- Choose an available time and a service.
- Click **Book** (**Rezerviraj**) to confirm the reservation.

## 5.5 Generating a Receipt
- After booking, you will have the option to **Generate Receipt** (**Ispiši račun**).
- Receipts are automatically saved in the `receipts/` folder as `.txt` files.

## 5.6 Logging Out
- You can log out anytime by clicking the **Logout** (**Odjava**) button to return to the main menu.

> *Note:* Users will receive a pop-up message informing them about the success or failure of login, registration, appointment booking, or logout actions.
