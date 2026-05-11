from __future__ import annotations

import json
from pathlib import Path
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
DATA_FILE = Path(__file__).with_name("saved_shifts.json")

DEPARTMENTS = [
    "Emergency",
    "Pediatrics",
    "Radiology",
    "Administration",
    "Pharmacy",
]

SHIFT_TYPES = [
    "Morning",
    "Afternoon",
    "Night",
]

SHIFT_ROLES = [
    "Head Nurse",
    "Staff Nurse",
    "Coordinator",
    "Technician",
    "Support Staff",
]

TIME_OPTIONS = [
    "06:00",
    "07:00",
    "08:00",
    "09:00",
    "10:00",
    "11:00",
    "12:00",
    "13:00",
    "14:00",
    "15:00",
    "16:00",
    "17:00",
    "18:00",
    "19:00",
    "20:00",
    "21:00",
    "22:00",
]


# Change the class definition and inheritance
class HRManagerPortalFrame(tk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent, bg=APP_BACKGROUND)
        self.controller = controller  # Reference to HospitalMaster

        # Initialize tracking variables within this frame
        self.employee_var = tk.StringVar()
        self.shift_date_var = tk.StringVar(value="2026-03-24")
        self.department_var = tk.StringVar(value=DEPARTMENTS[0])
        self.shift_type_var = tk.StringVar(value=SHIFT_TYPES[0])
        self.role_var = tk.StringVar(value=SHIFT_ROLES[0])
        self.start_time_var = tk.StringVar(value="08:00")
        self.end_time_var = tk.StringVar(value="16:00")
        self.notes_var = tk.StringVar()
        self.preview_var = tk.StringVar()

        self.saved_shifts = self._load_shifts()
        self._bind_preview_updates()
        self.update_shift_preview()

        # Internal container for HR sub-pages
        self.sub_container = tk.Frame(self, bg=APP_BACKGROUND)
        self.sub_container.pack(fill="both", expand=True)

        self.user_display_name = controller.current_user_name

        self.pages = {
            "dashboard": HRDashboardPage(self.sub_container, self),
            "schedule_shift": ShiftSchedulePage(self.sub_container, self),
        }

        for page in self.pages.values():
            page.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.show_page("dashboard")

    def show_page(self, page_name: str) -> None:
        if page_name in self.pages:
            self.pages[page_name].tkraise()
        elif page_name == "login":
            # Access the Master controller to handle the global logout
            self.controller.show_login(user_name="")

    # ... Keep all logic methods (_load_shifts, save_shift, etc.) here ...
    def _load_shifts(self) -> list[dict[str, str]]:
        if not DATA_FILE.exists():
            return []

        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []

    def save_shift(self) -> bool:
        employee = self.employee_var.get().strip()
        shift_date = self.shift_date_var.get().strip()
        department = self.department_var.get().strip()
        shift_type = self.shift_type_var.get().strip()
        role = self.role_var.get().strip()
        start_time = self.start_time_var.get().strip()
        end_time = self.end_time_var.get().strip()
        notes = self.notes_var.get().strip()

        if not employee or not shift_date or not department or not shift_type or not role or not start_time or not end_time:
            messagebox.showerror("Missing details", "Please complete all shift fields before saving.")
            return False

        new_shift = {
            "employee": employee,
            "shift_date": shift_date,
            "department": department,
            "shift_type": shift_type,
            "role": role,
            "start_time": start_time,
            "end_time": end_time,
            "notes": notes,
        }
        self.saved_shifts.append(new_shift)

        try:
            DATA_FILE.write_text(json.dumps(self.saved_shifts, indent=2), encoding="utf-8")
        except OSError as error:
            messagebox.showerror("Save failed", f"Could not write shifts to disk.\n{error}")
            return False

        messagebox.showinfo(
            "Shift Saved",
            f"Saved {shift_type.lower()} shift for {employee} in {department} on {shift_date}, {start_time} to {end_time}.",
        )
        return True

    def clear_shift_form(self) -> None:
        self.employee_var.set("")
        self.shift_date_var.set("2026-03-24")
        self.department_var.set(DEPARTMENTS[0])
        self.shift_type_var.set(SHIFT_TYPES[0])
        self.role_var.set(SHIFT_ROLES[0])
        self.start_time_var.set("08:00")
        self.end_time_var.set("16:00")
        self.notes_var.set("")

    def _bind_preview_updates(self) -> None:
        for variable in (
            self.employee_var,
            self.shift_date_var,
            self.department_var,
            self.shift_type_var,
            self.role_var,
            self.start_time_var,
            self.end_time_var,
            self.notes_var,
        ):
            variable.trace_add("write", self._on_shift_field_changed)

    def _on_shift_field_changed(self, *_args: object) -> None:
        self.update_shift_preview()

    def update_shift_preview(self) -> None:
        employee = self.employee_var.get().strip() or "Select an employee"
        role = self.role_var.get().strip() or "Role pending"
        department = self.department_var.get().strip() or "Department pending"
        shift_date = self.shift_date_var.get().strip() or "Date pending"
        shift_type = self.shift_type_var.get().strip() or "Shift pending"
        start_time = self.start_time_var.get().strip() or "--:--"
        end_time = self.end_time_var.get().strip() or "--:--"
        notes = self.notes_var.get().strip() or "No handoff notes added yet."

        self.preview_var.set(
            f"{employee}\n"
            f"{role} | {department}\n"
            f"{shift_type} shift on {shift_date}\n"
            f"Time window: {start_time} - {end_time}\n"
            f"Notes: {notes}"
        )


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
        description: str,
        button_text: str,
        icon_drawer,
        command,
    ) -> None:
        super().__init__(parent)

        inner = tk.Frame(self, bg=CARD_BACKGROUND)
        inner.pack(fill="both", expand=True, padx=18, pady=12)

        icon = tk.Canvas(
            inner,
            width=112,
            height=74,
            bg=CARD_BACKGROUND,
            highlightthickness=0,
        )
        icon.pack(anchor="w", pady=(0, 6))
        icon_drawer(icon)

        tk.Label(
            inner,
            text=title,
            font=("Segoe UI", 14, "bold"),
            bg=CARD_BACKGROUND,
            fg=TEXT_PRIMARY,
        ).pack(anchor="w")

        tk.Label(
            inner,
            text=description,
            font=("Segoe UI", 9),
            bg=CARD_BACKGROUND,
            fg=TEXT_SECONDARY,
            wraplength=900,
            justify="left",
        ).pack(anchor="w", pady=(4, 8))

        tk.Button(
            inner,
            text=button_text,
            font=BUTTON_FONT,
            bg=BUTTON_BACKGROUND,
            activebackground=BUTTON_ACTIVE,
            fg=TEXT_PRIMARY,
            relief="solid",
            bd=1,
            padx=BUTTON_PADX,
            pady=BUTTON_PADY,
            command=command,
            cursor="hand2",
        ).pack(anchor="w")


class SummaryCard(CardFrame):
    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent, height=126)

        inner = tk.Frame(self, bg=CARD_BACKGROUND)
        inner.pack(fill="both", expand=True, padx=18, pady=16)

        row = tk.Frame(inner, bg=CARD_BACKGROUND)
        row.pack(fill="both", expand=True)

        icon = tk.Canvas(
            row,
            width=82,
            height=78,
            bg=CARD_BACKGROUND,
            highlightthickness=0,
        )
        icon.pack(side="left", anchor="n", padx=(0, 16))
        draw_hr_calendar_icon(icon)

        text_col = tk.Frame(row, bg=CARD_BACKGROUND)
        text_col.pack(side="left", fill="both", expand=True)

        tk.Label(
            text_col,
            text="HR Staffing Dashboard",
            font=("Segoe UI", 16, "bold"),
            bg=CARD_BACKGROUND,
            fg=TEXT_PRIMARY,
        ).pack(anchor="w")

        tk.Label(
            text_col,
            text="Your dashboard is the control center for staffing, shifts, and schedule conflicts.",
            font=("Segoe UI", 10),
            bg=CARD_BACKGROUND,
            fg=TEXT_SECONDARY,
            wraplength=840,
            justify="left",
        ).pack(anchor="w", pady=(6, 0))


class HRDashboardPage(ScrollablePage):
    def __init__(self, parent: tk.Widget, app: HRManagerPortalFrame) -> None:
        super().__init__(parent)
        self.app = app
        self._build()

    def _build(self) -> None:
        header = tk.Frame(self.content, bg=APP_BACKGROUND)
        header.pack(fill="x", padx=64, pady=(34, 18))

        tk.Label(
            header,
            text=f"Hello, {self.app.user_display_name}",
            font=("Segoe UI", 22, "bold"),
            bg=APP_BACKGROUND,
            fg=TEXT_PRIMARY,
        ).pack(anchor="w")

        tk.Label(
            header,
            text="HR Manager",
            font=("Segoe UI", 15),
            bg=APP_BACKGROUND,
            fg=TEXT_SECONDARY,
        ).pack(anchor="w", pady=(6, 0))

        summary_card = SummaryCard(self.content)
        summary_card.pack(fill="x", padx=64, pady=12)

        cards = (
            (
                "Shifts",
                "Create and revise schedules, assign teams, and keep staffing plans organized.",
                "Schedule shift",
                draw_shift_icon,
                lambda: self.app.show_page("schedule_shift"),
            ),
            (
                "Staff",
                "Search personnel and manage assignments across departments.",
                "Open staff",
                draw_staff_icon,
                self._show_staff_message,
            ),
            (
                "Conflicts",
                "Review rest-time, leave requests, and scheduling issues before they escalate.",
                "Review conflicts",
                draw_conflict_icon,
                self._show_conflict_message,
            ),
        )

        for title, description, button_text, drawer, command in cards:
            card = ActionCard(
                self.content,
                title=title,
                description=description,
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
            command=lambda: self.app.show_page("login"), # Change this!,
            cursor="hand2",
        ).pack(anchor="w")

        footer = tk.Frame(self.content, bg=APP_BACKGROUND, height=20)
        footer.pack(fill="x")

    @staticmethod
    def _show_staff_message() -> None:
        messagebox.showinfo("Staff", "Staff management tools can be added here.")

    @staticmethod
    def _show_conflict_message() -> None:
        messagebox.showinfo("Conflicts", "Conflict review tools can be added here.")


class ShiftSchedulePage(ScrollablePage):
    def __init__(self, parent: tk.Widget, app: HRManagerPortalFrame) -> None:
        super().__init__(parent)
        self.app = app
        self._build()

    def _build(self) -> None:
        top_bar = tk.Frame(self.content, bg=APP_BACKGROUND)
        top_bar.pack(fill="x", padx=64, pady=(22, 8))

        tk.Button(
            top_bar,
            text="Back to dashboard",
            font=BUTTON_FONT,
            bg=BUTTON_BACKGROUND,
            activebackground=BUTTON_ACTIVE,
            fg=TEXT_PRIMARY,
            relief="solid",
            bd=1,
            padx=BUTTON_PADX,
            pady=BUTTON_PADY,
            cursor="hand2",
            command=lambda: self.app.show_page("dashboard"),
        ).pack(anchor="w")

        self._build_intro_section()
        self._build_staffing_section()
        self._build_schedule_section()
        self._build_department_section()
        self._build_preview_section()
        self._build_submit_row()

        footer = tk.Frame(self.content, bg=APP_BACKGROUND, height=20)
        footer.pack(fill="x")

    def _build_intro_section(self) -> None:
        card = CardFrame(self.content, height=126)
        card.pack(fill="x", padx=64, pady=9)

        inner = tk.Frame(card, bg=CARD_BACKGROUND)
        inner.pack(fill="both", expand=True, padx=18, pady=16)

        row = tk.Frame(inner, bg=CARD_BACKGROUND)
        row.pack(fill="both", expand=True)

        icon = tk.Canvas(row, width=82, height=78, bg=CARD_BACKGROUND, highlightthickness=0)
        icon.pack(side="left", anchor="n", padx=(0, 16))
        draw_shift_icon(icon)

        text_col = tk.Frame(row, bg=CARD_BACKGROUND)
        text_col.pack(side="left", fill="both", expand=True)

        tk.Label(
            text_col,
            text="Create Shift",
            font=("Segoe UI", 16, "bold"),
            bg=CARD_BACKGROUND,
            fg=TEXT_PRIMARY,
        ).pack(anchor="w")

        tk.Label(
            text_col,
            text="Set up a staffing assignment, add the time window, and review the shift before saving it locally.",
            font=("Segoe UI", 10),
            bg=CARD_BACKGROUND,
            fg=TEXT_SECONDARY,
            wraplength=820,
            justify="left",
        ).pack(anchor="w", pady=(6, 0))

    def _build_staffing_section(self) -> None:
        section = self._section_card("Staffing", "Choose who is assigned and in what role", height=152)
        row = tk.Frame(section, bg=CARD_BACKGROUND)
        row.pack(anchor="w")

        self._labeled_entry(row, "Employee", self.app.employee_var, width=28).pack(side="left", padx=(0, 16))

        role_block = self._labeled_container(row, "Role")
        role_combo = ttk.Combobox(
            role_block,
            textvariable=self.app.role_var,
            values=SHIFT_ROLES,
            state="readonly",
            style="Portal.TCombobox",
            font=("Segoe UI", 10),
            width=25,
        )
        role_combo.pack(anchor="w", ipadx=4, ipady=3)
        role_block.pack(side="left")

    def _build_schedule_section(self) -> None:
        section = self._section_card("Schedule", "Set the day, shift label, and time range", height=174)
        row = tk.Frame(section, bg=CARD_BACKGROUND)
        row.pack(anchor="w")

        self._labeled_entry(row, "Shift Date", self.app.shift_date_var, width=18).pack(side="left", padx=(0, 14))

        shift_block = self._labeled_container(row, "Shift Type")
        shift_combo = ttk.Combobox(
            shift_block,
            textvariable=self.app.shift_type_var,
            values=SHIFT_TYPES,
            state="readonly",
            style="Portal.TCombobox",
            font=("Segoe UI", 10),
            width=16,
        )
        shift_combo.pack(anchor="w", ipadx=4, ipady=3)
        shift_block.pack(side="left", padx=(0, 14))

        start_block = self._labeled_container(row, "Start")
        start_combo = ttk.Combobox(
            start_block,
            textvariable=self.app.start_time_var,
            values=TIME_OPTIONS,
            state="readonly",
            style="Portal.TCombobox",
            font=("Segoe UI", 10),
            width=12,
        )
        start_combo.pack(anchor="w", ipadx=4, ipady=3)
        start_block.pack(side="left", padx=(0, 14))

        end_block = self._labeled_container(row, "End")
        end_combo = ttk.Combobox(
            end_block,
            textvariable=self.app.end_time_var,
            values=TIME_OPTIONS,
            state="readonly",
            style="Portal.TCombobox",
            font=("Segoe UI", 10),
            width=12,
        )
        end_combo.pack(anchor="w", ipadx=4, ipady=3)
        end_block.pack(side="left")

    def _build_department_section(self) -> None:
        section = self._section_card("Department And Notes", "Choose the area and add a quick handoff note", height=168)
        row = tk.Frame(section, bg=CARD_BACKGROUND)
        row.pack(anchor="w")

        department_block = self._labeled_container(row, "Department")
        combo = ttk.Combobox(
            department_block,
            textvariable=self.app.department_var,
            values=DEPARTMENTS,
            state="readonly",
            style="Portal.TCombobox",
            font=("Segoe UI", 10),
            width=22,
        )
        combo.pack(anchor="w", ipadx=4, ipady=3)
        department_block.pack(side="left", padx=(0, 16))

        notes_block = self._labeled_container(row, "Notes")
        self._make_entry(notes_block, self.app.notes_var, width=42).pack(anchor="w")
        notes_block.pack(side="left")

    def _build_preview_section(self) -> None:
        section = self._section_card("Shift Preview", "Review the assignment before you save it", height=156)
        tk.Label(
            section,
            textvariable=self.app.preview_var,
            font=("Segoe UI", 10),
            bg=CARD_BACKGROUND,
            fg=TEXT_SECONDARY,
            justify="left",
            anchor="w",
        ).pack(anchor="w")

    def _build_submit_row(self) -> None:
        row = tk.Frame(self.content, bg=APP_BACKGROUND)
        row.pack(fill="x", padx=64, pady=(6, 0))

        tk.Button(
            row,
            text="Save Shift",
            font=BUTTON_FONT,
            bg=BUTTON_BACKGROUND,
            activebackground=BUTTON_ACTIVE,
            fg=TEXT_PRIMARY,
            relief="solid",
            bd=1,
            padx=BUTTON_PADX,
            pady=BUTTON_PADY,
            command=self._save_and_reset,
            cursor="hand2",
        ).pack(side="left", anchor="w")

        tk.Button(
            row,
            text="Clear Form",
            font=BUTTON_FONT,
            bg=BUTTON_BACKGROUND,
            activebackground=BUTTON_ACTIVE,
            fg=TEXT_PRIMARY,
            relief="solid",
            bd=1,
            padx=BUTTON_PADX,
            pady=BUTTON_PADY,
            command=self.app.clear_shift_form,
            cursor="hand2",
        ).pack(side="left", padx=(10, 0))

    def _section_card(self, title: str, subtitle: str, height: int) -> tk.Frame:
        card = CardFrame(self.content, height=height)
        card.pack(fill="x", padx=64, pady=9)

        inner = tk.Frame(card, bg=CARD_BACKGROUND)
        inner.pack(fill="both", expand=True, padx=18, pady=16)

        tk.Label(
            inner,
            text=title,
            font=("Segoe UI", 14, "bold"),
            bg=CARD_BACKGROUND,
            fg="#4E5258",
        ).pack(anchor="w")

        tk.Label(
            inner,
            text=subtitle,
            font=("Segoe UI", 10),
            bg=CARD_BACKGROUND,
            fg=TEXT_PRIMARY,
        ).pack(anchor="w", pady=(12, 6))

        return inner

    def _labeled_entry(self, parent: tk.Widget, label: str, variable: tk.StringVar, width: int) -> tk.Frame:
        block = self._labeled_container(parent, label)
        self._make_entry(block, variable, width=width).pack(anchor="w")
        return block

    @staticmethod
    def _labeled_container(parent: tk.Widget, label: str) -> tk.Frame:
        block = tk.Frame(parent, bg=CARD_BACKGROUND)
        tk.Label(
            block,
            text=label,
            font=("Segoe UI", 10),
            bg=CARD_BACKGROUND,
            fg=TEXT_PRIMARY,
        ).pack(anchor="w", pady=(0, 6))
        return block

    @staticmethod
    def _make_entry(parent: tk.Widget, variable: tk.StringVar, width: int) -> tk.Entry:
        return tk.Entry(
            parent,
            textvariable=variable,
            font=("Segoe UI", 10),
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

    def _save_and_reset(self) -> None:
        if self.app.save_shift():
            self.app.clear_shift_form()


def draw_hr_calendar_icon(canvas: tk.Canvas) -> None:
    canvas.create_rectangle(10, 14, 62, 62, width=3, outline="#111111")
    canvas.create_rectangle(10, 14, 62, 27, width=0, fill="#111111")
    canvas.create_line(23, 9, 23, 20, width=5, fill="#111111", capstyle=tk.ROUND)
    canvas.create_line(49, 9, 49, 20, width=5, fill="#111111", capstyle=tk.ROUND)

    for x in (19, 32, 45):
        for y in (36, 49):
            canvas.create_rectangle(x, y, x + 8, y + 8, width=1, outline="#111111", fill="#111111")

    canvas.create_line(68, 28, 68, 56, width=3, fill="#111111", capstyle=tk.ROUND)
    canvas.create_oval(60, 40, 76, 56, width=3, outline="#111111")
    canvas.create_line(68, 44, 68, 49, width=2, fill="#111111", capstyle=tk.ROUND)
    canvas.create_line(68, 49, 72, 49, width=2, fill="#111111", capstyle=tk.ROUND)


def draw_shift_icon(canvas: tk.Canvas) -> None:
    canvas.create_rectangle(22, 18, 82, 72, width=3, outline="#111111")
    canvas.create_rectangle(22, 18, 82, 33, width=0, fill="#111111")
    canvas.create_line(36, 11, 36, 24, width=6, fill="#111111", capstyle=tk.ROUND)
    canvas.create_line(68, 11, 68, 24, width=6, fill="#111111", capstyle=tk.ROUND)
    canvas.create_rectangle(32, 45, 44, 57, width=1, outline="#111111", fill="#111111")
    canvas.create_rectangle(49, 45, 61, 57, width=1, outline="#111111", fill="#111111")
    canvas.create_rectangle(66, 45, 78, 57, width=1, outline="#111111", fill="#111111")
    canvas.create_line(89, 24, 102, 37, width=4, fill="#111111", capstyle=tk.ROUND)
    canvas.create_line(102, 37, 112, 18, width=4, fill="#111111", capstyle=tk.ROUND)


def draw_staff_icon(canvas: tk.Canvas) -> None:
    canvas.create_oval(28, 18, 58, 48, width=3, outline="#111111")
    canvas.create_oval(57, 24, 81, 48, width=3, outline="#111111")
    canvas.create_arc(20, 42, 66, 82, start=0, extent=180, style="arc", width=3)
    canvas.create_arc(50, 42, 92, 78, start=0, extent=180, style="arc", width=3)
    canvas.create_line(95, 20, 111, 20, width=3, fill="#111111", capstyle=tk.ROUND)
    canvas.create_line(103, 12, 103, 28, width=3, fill="#111111", capstyle=tk.ROUND)


def draw_conflict_icon(canvas: tk.Canvas) -> None:
    canvas.create_polygon(58, 14, 98, 78, 18, 78, width=3, outline="#111111", fill="")
    canvas.create_line(58, 30, 58, 52, width=4, fill="#111111", capstyle=tk.ROUND)
    canvas.create_oval(55, 60, 61, 66, width=0, fill="#111111")
    canvas.create_line(90, 22, 106, 22, width=3, fill="#111111", capstyle=tk.ROUND)
    canvas.create_line(98, 14, 98, 30, width=3, fill="#111111", capstyle=tk.ROUND)

