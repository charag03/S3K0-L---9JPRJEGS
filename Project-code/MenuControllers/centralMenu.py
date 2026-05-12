import customtkinter as ctk
from tkinter import messagebox

CARD_WHITE = "#FFFFFF"


ui_json = {
    "HR" :
    {
        "user" : "HR Manager",
        "tiles": [   
            {
               "title": "Shift and Staff Assignment",
               "row" : 0,
               "column" : 0
            }
            ,
            {
                "title": "Weekly Shift Schedule",
                "row" : 0,
               "column" : 1
            }
            ,
            {
                "title": "Profile Management",
                "row" : 1,
               "column" : 0
            }
        ]
    }
    
    ,
    "DOC" :
    {
        "user" : "Doctor",
        "tiles": [   
            {
               "title": "Patient Admission",
               "row" : 0,
               "column" : 0
            }
            ,
            {
                "title": "Prescription Issuance",
                "row" : 0,
               "column" : 1
            }
            ,
            {
                "title": "Patient Record Processing",
                "row" : 1,
               "column" : 0
            },
                        {
                "title": "Profile Management",
                "row" : 1,
               "column" : 1
            }
        ]
    } ,
    "INV" :
    {
        "user" : "Inventory Manager",
        "tiles": [   
            {
               "title": "Order of Equipment and Medicines",
               "row" : 0,
               "column" : 0
            }
            ,
            {
                "title": "Manage Requests for Medicines and Equipment",
                "row" : 0,
               "column" : 1
            }
            ,
            {
                "title": "Profile Management",
                "row" : 1,
               "column" : 0
            }
        ]
    } 
    ,
    "PATIENT" :
    {
        "user" : "Patient",
        "tiles": [   
            {
               "title": "Schedule Appointment",
               "row" : 0,
               "column" : 0
            }
            ,
            {
                "title": "Bill Payment",
                "row" : 0,
               "column" : 1
            }
            ,
            {
                "title": "Manage Profile",
                "row" : 1,
               "column" : 0
            }
        ]
    } 
        ,
    "PHARMACIST" :
    {
        "user" : "Pharmacist",
        "tiles": [   
            {
               "title": "Drug Administration",
               "row" : 0,
               "column" : 0
            }
            ,
            {
                "title": "Request for Medicines and Equipment",
                "row" : 0,
               "column" : 1
            }
            ,
            {
                "title": "Profile Management",
                "row" : 1,
               "column" : 0
            }
        ]
    } 
            ,
    "SECRETARY" :
    {
        "user" : "Secretary",
        "tiles": [   
            {
               "title": "Account statement Issuance",
               "row" : 0,
               "column" : 0
            }
            ,
            {
                "title": "Surgery Scheduling",
                "row" : 0,
               "column" : 1
            }
            ,
            {
                "title": "Profile Management",
                "row" : 1,
               "column" : 0
            }
        ]
    } 
}

class CentralMenu(ctk.CTkFrame):
    def __init__(self,parent, portal, user_t):
        super().__init__(parent, fg_color="transparent")
        
        # print(ui_json[user_t])

        user = getattr(portal.controller, "current_user_name", ui_json[user_t].get("user"))

        # print(user)

        ctk.CTkLabel(self, text=f"Welcome, {user}", font=ctk.CTkFont(size=28, weight="bold"), text_color="#3D59AB").pack(pady=(20, 10))
    
        grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        grid_frame.pack(expand=True)
        
        for tile in ui_json[user_t].get("tiles"):
            self.create_tile(grid_frame, tile["title"], lambda: messagebox.showinfo("Info", "Coming soon :)"), tile["row"], tile["column"])
        
    def create_tile(self, master, text, command, row, col):
        tile = ctk.CTkButton(
            master, text=f"\n\n{text}", width=250, height=200, corner_radius=20,
            fg_color=CARD_WHITE, text_color="#3D59AB", border_width=1, border_color="#104E8B",
            hover_color="#87CEFA", font=ctk.CTkFont(size=16, weight="bold"), command=command
        )
        tile.grid(row=row, column=col, padx=15, pady=15)