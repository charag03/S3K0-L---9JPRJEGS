from __future__ import annotations
import tkinter as tk
from tkinter import messagebox, ttk


APP_BACKGROUND = "#F7F7F5"
CARD_BACKGROUND = "#FFFFFF"
CARD_BORDER = "#D7D8DB"
TEXT_PRIMARY = "#2A2B2E"
TEXT_SECONDARY = "#7A7D82"
INPUT_BORDER = "#D9D9DE"
BUTTON_BACKGROUND = "#F2F2F2"
BUTTON_ACTIVE = "#E5E5E5"
BUTTON_FONT = ("Segoe UI", 10)
BUTTON_PADX = 14
BUTTON_PADY = 6


SPECIALTIES = {
    "Dermatologists": {
        "Dr. Julian Sterling": ["17:00 - 17:45", "18:00 - 18:45", "19:00 - 19:45"],
        "Dr. Amelia Hart": ["09:00 - 09:45", "10:00 - 10:45", "11:00 - 11:45"],
    },
    "Cardiologists": {
        "Dr. Noah Bennett": ["08:30 - 09:15", "10:30 - 11:15", "12:00 - 12:45"],
        "Dr. Irene Wells": ["14:00 - 14:45", "15:00 - 15:45", "16:00 - 16:45"],
    },
    "Orthopedists": {
        "Dr. Lucas Reed": ["09:30 - 10:15", "13:00 - 13:45", "15:30 - 16:15"],
        "Dr. Sofia Lane": ["10:00 - 10:45", "11:30 - 12:15", "17:00 - 17:45"],
    },
}


class PatientPortalFrame(tk.Frame):
    def __init__(self, parent, controller) -> None:
        # parent is the container from MasterApp
        # controller is the MasterApp instance itself
        super().__init__(parent, bg=APP_BACKGROUND)
        self.controller = controller

        # Apply styles to the root window (controller)
        self._setup_styles()

        # The internal container for sub-pages (Dashboard/Appointments)
        self.sub_container = tk.Frame(self, bg=APP_BACKGROUND)
        self.sub_container.pack(fill="both", expand=True)

        self.user_display_name = controller.current_user_name

        self.pages: dict[str, tk.Frame] = {
            "dashboard": DashboardPage(self.sub_container, self),
            "appointments": AppointmentPage(self.sub_container, self),
        }

        for page in self.pages.values():
            page.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.show_page("dashboard")

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Portal.TCombobox",
            fieldbackground=CARD_BACKGROUND,
            background=CARD_BACKGROUND,
            bordercolor=INPUT_BORDER,
            lightcolor=INPUT_BORDER,
            darkcolor=INPUT_BORDER,
            arrowsize=16,
            padding=(10, 8),
            relief="flat",
        )

    def show_page(self, page_name: str) -> None:
        if page_name in self.pages:
            self.pages[page_name].tkraise()
        elif page_name == "login":
            # If the user clicks logout, tell the master controller
            self.controller.show_login(user_name="")


class ScrollablePage(tk.Frame):
    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent, bg=APP_BACKGROUND)

        self.canvas = tk.Canvas(self, bg=APP_BACKGROUND, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.content = tk.Frame(self.canvas, bg=APP_BACKGROUND)
        self.window_id = self.canvas.create_window((0, 0), window=self.content, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.content.bind("<Configure>", self._update_scrollregion)
        self.canvas.bind("<Configure>", self._resize_inner_frame)

        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)

    def _update_scrollregion(self, _event: tk.Event) -> None:
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _resize_inner_frame(self, event: tk.Event) -> None:
        self.canvas.itemconfig(self.window_id, width=event.width)

    def _bind_mousewheel(self, _event: tk.Event) -> None:
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, _event: tk.Event) -> None:
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event: tk.Event) -> None:
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


class CardFrame(tk.Frame):
    def __init__(self, parent: tk.Widget, *, height: int | None = None) -> None:
        super().__init__(
            parent,
            bg=CARD_BACKGROUND,
            highlightbackground=CARD_BORDER,
            highlightthickness=1,
            bd=0,
        )
        if height is not None:
            self.configure(height=height)
            self.pack_propagate(False)


class ActionCard(CardFrame):
    def __init__(
        self,
        parent: tk.Widget,
        *,
        title: str,
        button_text: str,
        icon_drawer,
        command,
    ) -> None:
        super().__init__(parent, height=230)

        inner = tk.Frame(self, bg=CARD_BACKGROUND)
        inner.pack(fill="both", expand=True, padx=22, pady=22)

        icon = tk.Canvas(
            inner,
            width=120,
            height=88,
            bg=CARD_BACKGROUND,
            highlightthickness=0,
        )
        icon.pack(anchor="w", pady=(0, 28))
        icon_drawer(icon)

        title_label = tk.Label(
            inner,
            text=title,
            font=("Segoe UI", 17, "bold"),
            bg=CARD_BACKGROUND,
            fg=TEXT_PRIMARY,
        )
        title_label.pack(anchor="w", pady=(0, 16))

        button = tk.Button(
            inner,
            text=button_text,
            font=("Segoe UI", 11),
            bg=BUTTON_BACKGROUND,
            activebackground=BUTTON_ACTIVE,
            fg=TEXT_PRIMARY,
            relief="solid",
            bd=1,
            padx=12,
            pady=6,
            command=command,
            cursor="hand2",
        )
        button.pack(anchor="w")


class DashboardPage(ScrollablePage):
    def __init__(self, parent: tk.Widget, app: PatientPortalFrame) -> None:
        super().__init__(parent)
        self.app = app
        self._build()

    def _build(self) -> None:
        header = tk.Frame(self.content, bg=APP_BACKGROUND)
        header.pack(fill="x", padx=64, pady=(58, 22))

        tk.Label(
            header,
            text=f"Hello, {self.app.user_display_name}",
            font=("Segoe UI", 24, "bold"),
            bg=APP_BACKGROUND,
            fg=TEXT_PRIMARY,
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Patient",
            font=("Segoe UI", 17),
            bg=APP_BACKGROUND,
            fg=TEXT_SECONDARY,
        ).pack(anchor="w", pady=(6, 0))

        cards = (
            (
                "Appointment Scheduling",
                "Schedule appointment",
                draw_calendar_icon,
                lambda: self.app.show_page("appointments"),
            ),
            (
                "Bill Payment",
                "View billing",
                draw_receipt_icon,
                self._show_billing_message,
            ),
            (
                "Profile Management",
                "Open profile",
                draw_profile_icon,
                self._show_profile_message,
            ),
        )

        for title, button_text, drawer, command in cards:
            card = ActionCard(
                self.content,
                title=title,
                button_text=button_text,
                icon_drawer=drawer,
                command=command,
            )
            card.pack(fill="x", padx=64, pady=12)

        action_row = tk.Frame(self.content, bg=APP_BACKGROUND)
        action_row.pack(fill="x", padx=64, pady=(6, 0))

        tk.Button(
            action_row,
            text="Logout",
            font=BUTTON_FONT,
            bg=BUTTON_BACKGROUND,
            activebackground=BUTTON_ACTIVE,
            fg=TEXT_PRIMARY,
            relief="solid",
            bd=1,
            padx=BUTTON_PADX,
            pady=BUTTON_PADY,
            command=lambda: self.app.show_page("login"),
            cursor="hand2",
        ).pack(anchor="w")

        footer = tk.Frame(self.content, bg=APP_BACKGROUND, height=40)
        footer.pack(fill="x")

    @staticmethod
    def _show_billing_message() -> None:
        messagebox.showinfo("Bill Payment", "Billing actions can be added here.")

    @staticmethod
    def _show_profile_message() -> None:
        messagebox.showinfo("Profile Management", "Profile actions can be added here.")


class AppointmentPage(ScrollablePage):
    def __init__(self, parent: tk.Widget, app: PatientPortalFrame) -> None:
        super().__init__(parent)
        self.app = app

        self.day_var = tk.StringVar(value="30")
        self.month_var = tk.StringVar(value="06")
        self.year_var = tk.StringVar(value="2026")
        self.specialty_var = tk.StringVar(value="Dermatologists")
        self.doctor_var = tk.StringVar()
        self.slot_var = tk.StringVar()

        self.doctor_combo: ttk.Combobox | None = None
        self.slot_combo: ttk.Combobox | None = None

        self._build()
        self._refresh_doctors()

    def _build(self) -> None:
        top_bar = tk.Frame(self.content, bg=APP_BACKGROUND)
        top_bar.pack(fill="x", padx=64, pady=(30, 10))

        back_button = tk.Button(
            top_bar,
            text="Back to dashboard",
            font=("Segoe UI", 11),
            bg=BUTTON_BACKGROUND,
            activebackground=BUTTON_ACTIVE,
            fg=TEXT_PRIMARY,
            relief="solid",
            bd=1,
            padx=12,
            pady=6,
            cursor="hand2",
            command=lambda: self.app.show_page("dashboard"),
        )
        back_button.pack(anchor="w")

        self._build_date_section()
        self._build_specialty_section()
        self._build_doctor_section()
        self._build_slot_section()
        self._build_submit_row()

        footer = tk.Frame(self.content, bg=APP_BACKGROUND, height=48)
        footer.pack(fill="x")

    def _build_date_section(self) -> None:
        section = self._section_card("Date", "Select a date", height=190)
        row = tk.Frame(section, bg=CARD_BACKGROUND)
        row.pack(fill="x")

        self._make_entry(row, self.day_var, width=16).pack(side="left", fill="x", expand=True)
        self._make_entry(row, self.month_var, width=16).pack(side="left", fill="x", expand=True, padx=8)
        self._make_entry(row, self.year_var, width=18).pack(side="left", fill="x", expand=True)

    def _build_specialty_section(self) -> None:
        section = self._section_card("Medical Specialties", "Select a Specialty", height=170)

        self.specialty_combo = ttk.Combobox(
            section,
            textvariable=self.specialty_var,
            values=list(SPECIALTIES.keys()),
            state="readonly",
            style="Portal.TCombobox",
            font=("Segoe UI", 11),
            width=52,
        )
        self.specialty_combo.pack(anchor="w", ipadx=4, ipady=3)
        self.specialty_combo.bind("<<ComboboxSelected>>", lambda _event: self._refresh_doctors())

    def _build_doctor_section(self) -> None:
        section = self._section_card("Doctors", "Select a Doctor", height=170)

        self.doctor_combo = ttk.Combobox(
            section,
            textvariable=self.doctor_var,
            state="readonly",
            style="Portal.TCombobox",
            font=("Segoe UI", 11),
            width=52,
        )
        self.doctor_combo.pack(anchor="w", ipadx=4, ipady=3)
        self.doctor_combo.bind("<<ComboboxSelected>>", lambda _event: self._refresh_slots())

    def _build_slot_section(self) -> None:
        section = self._section_card("Time Slots", "Select a Time Slot", height=170)

        self.slot_combo = ttk.Combobox(
            section,
            textvariable=self.slot_var,
            state="readonly",
            style="Portal.TCombobox",
            font=("Segoe UI", 11),
            width=52,
        )
        self.slot_combo.pack(anchor="w", ipadx=4, ipady=3)

    def _build_submit_row(self) -> None:
        row = tk.Frame(self.content, bg=APP_BACKGROUND)
        row.pack(fill="x", padx=64, pady=(6, 0))

        submit = tk.Button(
            row,
            text="Book appointment",
            font=("Segoe UI", 11),
            bg=BUTTON_BACKGROUND,
            activebackground=BUTTON_ACTIVE,
            fg=TEXT_PRIMARY,
            relief="solid",
            bd=1,
            padx=18,
            pady=8,
            command=self._book_appointment,
            cursor="hand2",
        )
        submit.pack(anchor="w")

    def _section_card(self, title: str, subtitle: str, height: int) -> tk.Frame:
        card = CardFrame(self.content, height=height)
        card.pack(fill="x", padx=64, pady=12)

        inner = tk.Frame(card, bg=CARD_BACKGROUND)
        inner.pack(fill="both", expand=True, padx=22, pady=22)

        tk.Label(
            inner,
            text=title,
            font=("Segoe UI", 16, "bold"),
            bg=CARD_BACKGROUND,
            fg="#4E5258",
        ).pack(anchor="w")

        tk.Label(
            inner,
            text=subtitle,
            font=("Segoe UI", 11),
            bg=CARD_BACKGROUND,
            fg=TEXT_PRIMARY,
        ).pack(anchor="w", pady=(18, 8))

        return inner

    @staticmethod
    def _make_entry(parent: tk.Widget, variable: tk.StringVar, width: int) -> tk.Entry:
        return tk.Entry(
            parent,
            textvariable=variable,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground=INPUT_BORDER,
            highlightcolor=INPUT_BORDER,
            bg=CARD_BACKGROUND,
            fg=TEXT_PRIMARY,
            width=width,
            insertbackground=TEXT_PRIMARY,
        )

    def _refresh_doctors(self) -> None:
        doctors = list(SPECIALTIES[self.specialty_var.get()].keys())
        self.doctor_var.set(doctors[0])
        if self.doctor_combo is not None:
            self.doctor_combo.configure(values=doctors)
        self._refresh_slots()

    def _refresh_slots(self) -> None:
        slots = SPECIALTIES[self.specialty_var.get()][self.doctor_var.get()]
        self.slot_var.set(slots[0])
        if self.slot_combo is not None:
            self.slot_combo.configure(values=slots)

    def _book_appointment(self) -> None:
        message = (
            f"Appointment booked for {self.day_var.get()}/{self.month_var.get()}/{self.year_var.get()}\n"
            f"Specialty: {self.specialty_var.get()}\n"
            f"Doctor: {self.doctor_var.get()}\n"
            f"Time: {self.slot_var.get()}"
        )
        messagebox.showinfo("Appointment Scheduled", message)


def draw_calendar_icon(canvas: tk.Canvas) -> None:
    canvas.create_rectangle(26, 24, 82, 76, width=3, outline="#111111")
    canvas.create_rectangle(26, 24, 82, 38, width=0, fill="#111111")
    canvas.create_line(39, 18, 39, 32, width=6, fill="#111111", capstyle=tk.ROUND)
    canvas.create_line(62, 18, 62, 32, width=6, fill="#111111", capstyle=tk.ROUND)

    for x in (36, 50, 64):
        for y in (49, 63):
            canvas.create_rectangle(x, y, x + 8, y + 8, width=1, outline="#111111", fill="#111111")

    canvas.create_oval(58, 42, 92, 76, width=3, outline="#111111")
    canvas.create_line(75, 49, 75, 60, width=3, fill="#111111", capstyle=tk.ROUND)
    canvas.create_line(75, 60, 83, 60, width=3, fill="#111111", capstyle=tk.ROUND)


def draw_receipt_icon(canvas: tk.Canvas) -> None:
    canvas.create_rectangle(24, 16, 70, 68, width=3, outline="#111111")
    for y in (28, 40, 52, 64):
        canvas.create_line(33, y, 62, y, width=3, fill="#111111", capstyle=tk.ROUND)
    canvas.create_polygon(24, 68, 46, 68, 46, 90, fill=CARD_BACKGROUND, outline="#111111", width=3)
    canvas.create_oval(58, 56, 88, 86, width=3, outline="#111111")
    canvas.create_text(73, 71, text="$", font=("Segoe UI", 14, "bold"), fill="#111111")


def draw_profile_icon(canvas: tk.Canvas) -> None:
    canvas.create_oval(24, 10, 88, 74, width=3, outline="#111111", fill="#111111")
    canvas.create_oval(43, 22, 57, 36, width=0, fill=CARD_BACKGROUND)
    canvas.create_oval(35, 38, 65, 60, width=0, fill=CARD_BACKGROUND)
