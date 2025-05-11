
# 1. Project Title

**Beauty Salon / Kozmetički Salon**

# 2. Project Description

This is a student project developed as part of the *Machina Game Dev Academy – Python Programming* course.  
The application is a desktop solution written in Python and Tkinter for managing appointments in a beauty salon.  
It supports three user roles (Customer, Employee, Administrator), each with its own GUI and permissions:

- **Customer**  
  - Register and log in  
  - View own appointments  
  - Book appointments on weekdays  
- **Employee**  
  - Log in with their own account  
  - Book appointments for any customer  
  - View all appointments for a selected day  
  - Generate a **.txt** receipt for a selected appointment  
- **Administrator**  
  - All Employee functionalities  
  - Add and remove services  
  - Add new administrators  
  - Main menu with separate options:  
    - Book appointment  
    - View appointments & generate receipt  
    - Add administrator  
    - Add service  
    - Remove service

Passwords are stored as SHA‑256 hashes upon registration, and during login the application compares the hash of the entered password with the stored hash.

Receipts (.txt) are saved in the `racuni/` directory within the main project folder.

# 3. Table of Contents
1. Project Title
2. Project Description
3. Table of Contents 
4. How to install and run the project
5. How to use the project
6. Notes

# 4. How to Install and Run the Project "Kozmetički Salon" / "Beauty Salon"

**Requirements:**
- Python version 3.10 or newer
- Tkinter (comes pre-installed with Python)
- Recommended IDE: Visual Studio Code
- CSV files:  
  - `users.csv` (user storage)  
  - `appointments.csv` (appointment storage)  
  - `services.csv` (service storage)  

**Installation:**
1. Clone the repository or download all project files.
2. Ensure all `.csv` files and the `racuni/` directory are present in the project.
3. Open the terminal in the project folder and run:  
   `python3 main.py`  
   or simply use **Run Python File** in Visual Studio Code.

# 5. How to Use the Project

## 5.1 Starting the Application
- After running `main.py`, the start screen will open with options:
  - **Login** (for existing users)
  - **Register** (for new users)
  - **Exit** (will close the app)

## 5.2 User Registration
- Enter: First Name, Last Name, Phone, Username, Password
- The password is hashed (SHA‑256) before storage.
- Click Register → confirmation → return to the start screen.
- Click the **Register** (**Registriraj**) button.

> *Note:* You can navigate back to the main screen anytime by clicking the **Back** (**Natrag**) button.

- After successful registration, the app will return to the start screen.

## 5.3 User Login
- Enter Username and Password (plain‑text).
- Login_user hashes the input and compares it to the stored hash.
- Upon successful login, the main menu opens according to the user role.

### 5.3.1 Role‑specific Main Menus
-> Customer
  - After login, the primary screen is the Calendar:
  - View own appointments (top section)
  - Select a date → available times and services appear → book

-> Employee
  - Menu with options:
    Book appointment
    View Appointments & Receipt
    Logout
    Exit

-> Administrator
  - Menu with options:
    Book appointment
    View Appointments & Receipt
    Add administrator
    Add employee
    Add service
    Remove service

Pressing Back returns to the corresponding main menu, Logout returns to the start screen.

## 5.4 Calendar & Booking
- Navigate months with < and > buttons. Context (booking or review) is preserved.
- Weekdays only (Monday–Friday) are available for booking; weekends show an error message.

## 5.5 Viewing & Generating Receipts
- View Appointments (Admin/Employee) lists all appointments for the selected day.
- Customer sees only their own appointments.
- Each entry (Admin/Employee) has a Generate Receipt button to create a .txt receipt under racuni/.
- Customer receives a confirmation pop-up with date and time immediately after booking.

## 5.6 Logging Out
- You can log out anytime by clicking the **Logout** (**Odjava**) button to return to the main menu.

## 6. Notes 
- Passwords are stored only as hashes (SHA‑256). The frontend does not hash on login—login_user handles hashing internally. 
- CSV files act as the single “database”; you can manually edit them if needed.
- To refresh lists of services or appointments, restart the application.
- For security reasons, the registration form only allows creating “Customer” or accounts. Administrator accounts must be  added manually to the users.csv file (with a SHA-256 hashed password). Once an Administrator user exists in users.csv, they can log in through the app and manage services.
