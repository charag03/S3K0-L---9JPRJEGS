from __future__ import annotations
import json
import customtkinter as ctk
from pathlib import Path
from tkinter import messagebox
from MenuControllers.centralMenu import CentralMenu

BG_COLOR = "#F8F9FA"
CARD_WHITE = "#FFFFFF"
ACCENT_BLUE = "#2563EB"
TEXT_DARK = "#1E293B"
TEXT_MUTE = "#64748B"

class HRManagerPortalFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color=BG_COLOR)


        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.top_bar = ctk.CTkFrame(self, height=70, fg_color=CARD_WHITE, corner_radius=0, border_width=1, border_color="#E2E8F0")
        self.top_bar.grid(row=0, column=0, sticky="ew")
        self.top_bar.grid_propagate(False)

        self.lbl_title = ctk.CTkLabel(self.top_bar, text="✚ Vitalink | HR Manager Portal", font=ctk.CTkFont(size=20, weight="bold"), text_color="#3D59AB")
        self.lbl_title.pack(side="left", padx=30)
       
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=1, column=0, sticky="nsew", padx=40, pady=40)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        
        self.sub_pages = {
            "menu": HRManagerCentralMenu(self.container, self)}
        
        for sp in self.sub_pages.values():
            sp.grid(row=0, column=0, sticky="nsew")
        
        self.show_sub_page("menu")
        self.btn_logout = ctk.CTkButton(
            self, text="\U0001F6AA Logout", width=100, fg_color="transparent", 
            text_color=	"#800000", hover_color="#DC143C",
            command=self.handle_logout
        )
        self.btn_logout.place(relx=0.02, rely=0.95, anchor="sw")
        self.btn_logout.lift()


    def show_sub_page(self, name):
        self.sub_pages[name].tkraise()

    def handle_logout(self):
        try:
            self.controller.show_frame("LoginPage")
        except:
            self.controller.show_login(user_name="")


class HRManagerCentralMenu(CentralMenu):
    def __init__(self,parent,portal):
        super().__init__(parent, portal,user_t="HR")

