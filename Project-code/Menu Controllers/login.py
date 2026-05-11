import tkinter as tk
from tkinter import messagebox
import recognizer
import pandas as pd

#patients
patients = pd.read_csv('archive (1)/patients.csv')
patients_creds = patients[['email', 'password']]

#doctors
doctors = pd.read_csv('archive (1)/doctors.csv')
doctors_creds = doctors[['email', 'password']]

#inventory managers
inv_managers = pd.read_csv('archive (1)/inventory_managers.csv')
inv_managers_creds = inv_managers[['email', 'password']]

#HR managers
hr_managers = pd.read_csv('archive (1)/hr_managers.csv')
hr_managers_creds = hr_managers[['email', 'password']]

#pharmacists
pharmacists = pd.read_csv('archive (1)/pharmacists.csv')
pharmacists_creds = pharmacists[['email', 'password']]



class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        inner_frame = tk.Frame(self, bg="white")
        inner_frame.pack(expand=True)

        # UI Elements
        tk.Label(inner_frame, text="Login", font=("Arial", 18, "bold"), bg="white").grid(
            row=0, column=0, columnspan=2, pady=20
        )

        tk.Label(inner_frame, text="Username:", bg="white").grid(row=1, column=0, sticky="w")
        self.entry_user = tk.Entry(inner_frame, highlightthickness=1, highlightbackground="#ccc")
        self.entry_user.grid(row=1, column=1, pady=5)

        tk.Label(inner_frame, text="Password:", bg="white").grid(row=2, column=0, sticky="w")
        self.entry_pass = tk.Entry(inner_frame, show="*", highlightthickness=1, highlightbackground="#ccc")
        self.entry_pass.grid(row=2, column=1, pady=5)

        login_btn = tk.Button(inner_frame, text="Login", command=self.handle_login,
                              bg="#f0f0f0", relief="flat", width=10)
        login_btn.grid(row=3, column=0, columnspan=2, pady=20)

    def authenticate(self, data_frame, usr_email, usr_password):
        user_fname = data_frame.query(f'email == "{usr_email}" and password == "{usr_password}"')['first_name'].iloc[0]
        user_lname = data_frame.query(f'email == "{usr_email}" and password == "{usr_password}"')['last_name'].iloc[0]
        return f"{user_fname} {user_lname}"

    def handle_login(self):
        email = self.entry_user.get()
        password = self.entry_pass.get()

        # 1. Access the dataframes from the global scope (since you imported them in this file)
        # 2. Check roles and call the EXACT methods in HospitalMaster

        if recognizer.is_patient(patients_creds, email, password) == 1:
            # Matches your Master method: show_patient_portal()
            user_name = self.authenticate(patients, email, password)
            self.controller.show_patient_portal(user_name)

        elif recognizer.is_doctor(doctors_creds, email, password) == 1:
            # If you haven't made a Doctor frame yet, you can use a placeholder
            user_name = self.authenticate(doctors, email, password)
            self.controller.show_doctor_portal(user_name)

        elif recognizer.is_inv_manager(inv_managers_creds, email, password) == 1:
            user_name = self.authenticate(inv_managers, email, password)
            self.controller.show_inventory_manager_portal(user_name)

        elif recognizer.is_pharmacist(pharmacists_creds, email, password) == 1:
            user_name = self.authenticate(pharmacists, email, password)
            self.controller.show_pharmacist_portal(user_name)

        elif recognizer.is_hr_manager(hr_managers_creds, email, password) == 1:
            user_name = self.authenticate(hr_managers, email, password)
            self.controller.show_hr_portal(user_name)

        # ... repeat for other roles ...

        else:
            messagebox.showerror("Error", "Invalid credentials")


























''''
def handle_login():
    email = entry_user.get()
    password = entry_pass.get()

    if recognizer.is_patient(patients_creds, email, password) == 1:
        return

    if recognizer.is_doctor(doctors_creds, email, password) == 1:
        return

    if recognizer.is_inv_manager(inv_managers_creds, email, password) == 1:
        return

    if recognizer.is_hr_manager(hr_managers_creds, email, password) == 1:
        return

    if recognizer.is_pharmacist(pharmacists_creds, email, password) == 1:
        return

    messagebox.showerror("Error", "Invalid credentials")

# Initialize the main window
root = tk.Tk()
root.title("Login")
root.geometry("500x500")
root.configure(bg="white")

# Main Container (to add some padding)
frame = tk.Frame(root, bg="white")
frame.pack(expand=True)

# Title
label_title = tk.Label(frame, text="Login", font=("Arial", 18, "bold"), bg="white")
label_title.grid(row=0, column=0, columnspan=2, pady=20)

# Username
tk.Label(frame, text="Username:", bg="white").grid(row=1, column=0, sticky="w")
entry_user = tk.Entry(frame, highlightthickness=1, highlightbackground="#ccc")
entry_user.grid(row=1, column=1, pady=5)

# Password
tk.Label(frame, text="Password:", bg="white").grid(row=2, column=0, sticky="w")
entry_pass = tk.Entry(frame, show="*", highlightthickness=1, highlightbackground="#ccc")
entry_pass.grid(row=2, column=1, pady=5)

# Login Button
login_btn = tk.Button(frame, text="Login", command=handle_login,
                      bg="#f0f0f0", relief="flat", width=10)
login_btn.grid(row=3, column=0, columnspan=2, pady=20)

root.mainloop()
'''