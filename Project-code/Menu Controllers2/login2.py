import customtkinter as ctk
from tkinter import messagebox
import recognizer
import pandas as pd
import tkinter as tk


ctk.set_appearance_mode("light") 
ctk.set_default_color_theme("blue")

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

#secretary
secretaries = pd.read_csv('archive (1)/secretaries.csv')
secretaries_creds = secretaries[['email', 'password']]


class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=15)
        self.controller = controller
        self.configure(fg_color="#FFFFFF") 

       
        self.inner_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.inner_frame.place(relx=0.5, rely=0.5, anchor="center")


        try:
            
            self.logo_img = tk.PhotoImage(file="archive (1)/app_icon.png")
            self.logo_img = self.logo_img.subsample(2, 2)
            self.image_label = ctk.CTkLabel(
                self.inner_frame, 
                image=self.logo_img, 
                text="" 
            )
            self.image_label.grid(row=0, column=0, pady=(0, 20))
        except Exception as e:
            print(f"Could not load image: {e}")


        self.title_label = ctk.CTkLabel(
            self.inner_frame, 
            text="Welcome !", 
            font=("Segoe UI", 24, "bold"),
            text_color="#1a5fb4"
        )
        self.title_label.grid(row=1, column=0, pady=(0, 10))

        self.title_label = ctk.CTkLabel(
            self.inner_frame, 
            text="Welcome !", 
            font=("Segoe UI", 24, "bold"),
            text_color="#1a5fb4"
        )
    
        self.title_label.grid(row=1, column=0, pady=(0, 10))

        # Username Entry
        self.entry_user = ctk.CTkEntry(
            self.inner_frame, 
            placeholder_text="Email",
            width=300,
            height=45,
            border_width=1,
            corner_radius=8
        )
        self.entry_user.grid(row=3, column=0, pady=10)

        # Password Entry
        self.entry_pass = ctk.CTkEntry(
            self.inner_frame, 
            placeholder_text="Password",
            show="*",
            width=300,
            height=45,
            border_width=1,
            corner_radius=8
        )
        self.entry_pass.grid(row=4, column=0, pady=10)

        # Login Button
        self.login_btn = ctk.CTkButton(
            self.inner_frame, 
            text="Login", 
            command=self.handle_login,
            width=300,
            height=45,
            corner_radius=8,
            font=("Segoe UI", 14, "bold"),
            fg_color= "#1a5fb4",
            hover_color="#000080"
        )
        self.login_btn.grid(row=5, column=0, pady=(30, 0))

        self.footer_label = ctk.CTkLabel(
            self.inner_frame, 
            text="© 2026 Hospital Management System ", 
            font=("Segoe UI", 10),
            text_color="#AAA"
        )
        self.footer_label.grid(row=12, column=0, pady=(40, 0))


    def authenticate(self, data_frame, usr_email, usr_password):
        user_fname = data_frame.query(f'email == "{usr_email}" and password == "{usr_password}"')['first_name'].iloc[0]
        user_lname = data_frame.query(f'email == "{usr_email}" and password == "{usr_password}"')['last_name'].iloc[0]
        return f"{user_fname} {user_lname}"

    def handle_login(self):
        email = self.entry_user.get()
        password = self.entry_pass.get()

        if recognizer.is_patient(patients_creds, email, password) == 1 :
            user_name = self.authenticate(patients, email, password)
            self.controller.show_patient_portal(user_name)

        elif recognizer.is_doctor(doctors_creds, email, password) == 1 :
            user_name = self.authenticate(doctors, email, password)
            self.controller.show_doctor_portal(user_name)

        elif recognizer.is_inv_manager(inv_managers_creds, email, password) == 1 :
            user_name = self.authenticate(inv_managers, email, password)
            self.controller.show_inventory_manager_portal(user_name)

        elif recognizer.is_pharmacist(pharmacists_creds, email, password) == 1 :
            user_name = self.authenticate(pharmacists, email, password)
            self.controller.show_pharmacist_portal(user_name)

        elif recognizer.is_hr_manager(hr_managers_creds, email, password) == 1 :
            user_name = self.authenticate(hr_managers, email, password)
            self.controller.show_hr_portal(user_name)

        elif recognizer.is_secretary(secretaries_creds, email, password) == 1:
            user_name = self.authenticate(secretaries, email, password)
            self.controller.show_secretary_portal(user_name)

        else:
            messagebox.showerror("Error", "Invalid credentials")