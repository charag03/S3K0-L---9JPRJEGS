from __future__ import annotations
import json
import customtkinter as ctk
from pathlib import Path
from tkinter import messagebox

BG_COLOR = "#F8F9FA"
CARD_WHITE = "#FFFFFF"
ACCENT_BLUE = "#2563EB"
TEXT_DARK = "#1E293B"
TEXT_MUTE = "#64748B"


class SecretaryPortalFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color=BG_COLOR)


        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.top_bar = ctk.CTkFrame(self, height=70, fg_color=CARD_WHITE, corner_radius=0, border_width=1, border_color="#E2E8F0")
        self.top_bar.grid(row=0, column=0, sticky="ew")
        self.top_bar.grid_propagate(False)

        self.lbl_title = ctk.CTkLabel(self.top_bar, text="✚ Vitalink | Secretary Portal", font=ctk.CTkFont(size=20, weight="bold"), text_color="#3D59AB")
        self.lbl_title.pack(side="left", padx=30)

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=1, column=0, sticky="nsew", padx=40, pady=40)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        
        self.sub_pages = {
            "menu": SecretaryCentralMenu(self.container, self)}
        
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


class SecretaryCentralMenu(ctk.CTkFrame):
    def __init__(self, parent, portal):
        super().__init__(parent, fg_color="transparent")
        
        user = getattr(portal.controller, "current_user_name", "Secretary")
        ctk.CTkLabel(self, text=f"Welcome,  {user}", font=ctk.CTkFont(size=28, weight="bold"), text_color="#3D59AB").pack(pady=(20, 10))
    
        grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        grid_frame.pack(expand=True)

        
        self.create_tile(grid_frame, "Account statement Issuance", "📜", lambda: messagebox.showinfo("Info", "Coming soon :)"), 0, 0)
        self.create_tile(grid_frame, "Surgery Scheduling", "🕙", lambda: messagebox.showinfo("Info", "Coming soon :)"), 0, 1)
        self.create_tile(grid_frame, "Profile Management", "👤", lambda: messagebox.showinfo("Info", "Coming soon :)"), 1, 0)
       

    def create_tile(self, master, text, icon, command, row, col):
        tile = ctk.CTkButton(
            master, text=f"{icon}\n\n{text}", width=250, height=200, corner_radius=20,
            fg_color=CARD_WHITE, text_color="#3D59AB", border_width=1, border_color="#104E8B",
            hover_color="#87CEFA", font=ctk.CTkFont(size=16, weight="bold"), command=command
        )
        tile.grid(row=row, column=col, padx=15, pady=15)
