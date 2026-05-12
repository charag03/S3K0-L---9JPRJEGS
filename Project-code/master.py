from __future__ import annotations
from MenuControllers2.login2 import LoginFrame
from MenuControllers2.patient_dashboard2 import PatientPortalFrame
from MenuControllers2.doctor_page2 import DoctorPortalFrame
from MenuControllers2.pharmacist_page2 import PharmacistPortalFrame
from MenuControllers2.inventory_manager_page2 import InventoryManagerPortalFrame
from MenuControllers2.hr_manager_page2 import HRManagerPortalFrame
from MenuControllers2.secretary_page2 import SecretaryPortalFrame
import tkinter as tk

APP_BACKGROUND = "#F7F7F5"
CARD_BACKGROUND = "#FFFFFF"
CARD_BORDER = "#D7D8DB"
TEXT_PRIMARY = "#2A2B2E"
TEXT_SECONDARY = "#7A7D82"
INPUT_BORDER = "#D9D9DE"
BUTTON_BACKGROUND = "#F2F2F2"
BUTTON_ACTIVE = "#E5E5E5"


class HospitalMaster(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hospital Management System")
        self.geometry("1365x900")
        self.configure(bg=APP_BACKGROUND)

        # The master container
        self.main_container = tk.Frame(self)
        self.main_container.pack(fill="both", expand=True)

        self.current_frame = None
        self.show_login(user_name='User')

        self.current_user_name = "User"

    def show_login(self, user_name):
        self.current_user_name = user_name
        self._switch_frame(LoginFrame)

    def show_patient_portal(self, user_name):
        self.current_user_name = user_name
        self._switch_frame(PatientPortalFrame)

    def show_doctor_portal(self, user_name):
        self.current_user_name = user_name
        self._switch_frame(DoctorPortalFrame)

    def show_pharmacist_portal(self, user_name):
        self.current_user_name = user_name
        self._switch_frame(PharmacistPortalFrame)

    def show_inventory_manager_portal(self, user_name):
        self.current_user_name = user_name
        self._switch_frame(InventoryManagerPortalFrame)

    def show_hr_portal(self, user_name):
        self.current_user_name = user_name
        self._switch_frame(HRManagerPortalFrame)

    def show_secretary_portal(self, user_name):
        self.current_user_name = user_name
        self._switch_frame(SecretaryPortalFrame)

    def _switch_frame(self, frame_class):
        new_frame = frame_class(self.main_container, self)
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = HospitalMaster()
    app.mainloop()