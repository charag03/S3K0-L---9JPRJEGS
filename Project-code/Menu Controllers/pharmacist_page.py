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
DATA_FILE = Path(__file__).with_name("saved_dispensings.json")

MEDICINES = [
    "Amoxicillin 500 mg",
    "Ibuprofen 200 mg",
    "Metformin 850 mg",
    "Lisinopril 10 mg",
    "Atorvastatin 20 mg",
]

DOSAGE_FORMS = [
    "Tablet",
    "Capsule",
    "Suspension",
    "Injection",
    "Inhaler",
]

PRIORITY_LEVELS = [
    "Routine",
    "Urgent",
    "STAT",
]

DISPENSE_WINDOWS = [
    "Now",
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
]


# Change the class name and inheritance
class PharmacistPortalFrame(tk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent, bg=APP_BACKGROUND)
        self.controller = controller  # This points to HospitalMaster

        # Initialize all StringVars within this frame
        self.patient_var = tk.StringVar()
        self.prescription_var = tk.StringVar(value="RX-2401")
        self.medicine_var = tk.StringVar(value=MEDICINES[0])
        self.form_var = tk.StringVar(value=DOSAGE_FORMS[0])
        self.quantity_var = tk.StringVar(value="30")
        self.dispense_time_var = tk.StringVar(value="Now")
        self.priority_var = tk.StringVar(value=PRIORITY_LEVELS[0])
        self.notes_var = tk.StringVar()
        self.preview_var = tk.StringVar()

        self.saved_dispensings = self._load_dispensings()
        self._bind_preview_updates()
        self.update_dispensing_preview()

        # Internal container for the Pharmacist's sub-pages
        self.sub_container = tk.Frame(self, bg=APP_BACKGROUND)
        self.sub_container.pack(fill="both", expand=True)

        self.user_display_name = controller.current_user_name

        self.pages = {
            "dashboard": PharmacistDashboardPage(self.sub_container, self),
            "record_dispensing": RecordDispensingPage(self.sub_container, self),
        }

        for page in self.pages.values():
            page.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.show_page("dashboard")

    def show_page(self, page_name: str) -> None:
        if page_name in self.pages:
            self.pages[page_name].tkraise()
        elif page_name == "login":
            # Call the logout logic in the Master controller
            self.controller.show_login(user_name="")

# Keep all helper methods (_load_dispensings, save_dispensing, etc.) here...
    def _load_dispensings(self) -> list[dict[str, str]]:
        if not DATA_FILE.exists():
            return []

        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []

    def save_dispensing(self) -> bool:
        patient = self.patient_var.get().strip()
        prescription = self.prescription_var.get().strip()
        medicine = self.medicine_var.get().strip()
        form = self.form_var.get().strip()
        quantity = self.quantity_var.get().strip()
        dispense_time = self.dispense_time_var.get().strip()
        priority = self.priority_var.get().strip()
        notes = self.notes_var.get().strip()

        if not patient or not prescription or not medicine or not form or not quantity or not dispense_time or not priority:
            messagebox.showerror("Missing details", "Please complete all dispensing fields before saving.")
            return False

        if not quantity.isdigit():
            messagebox.showerror("Invalid quantity", "Quantity should be a whole number.")
            return False

        record = {
            "patient": patient,
            "prescription": prescription,
            "medicine": medicine,
            "form": form,
            "quantity": quantity,
            "dispense_time": dispense_time,
            "priority": priority,
            "notes": notes,
        }
        self.saved_dispensings.append(record)

        try:
            DATA_FILE.write_text(json.dumps(self.saved_dispensings, indent=2), encoding="utf-8")
        except OSError as error:
            messagebox.showerror("Save failed", f"Could not write dispensings to disk.\n{error}")
            return False

        messagebox.showinfo(
            "Dispensing Saved",
            f"Saved {medicine} for {patient}, quantity {quantity}, pickup {dispense_time}.",
        )
        return True

    def clear_dispensing_form(self) -> None:
        self.patient_var.set("")
        self.prescription_var.set("RX-2401")
        self.medicine_var.set(MEDICINES[0])
        self.form_var.set(DOSAGE_FORMS[0])
        self.quantity_var.set("30")
        self.dispense_time_var.set("Now")
        self.priority_var.set(PRIORITY_LEVELS[0])
        self.notes_var.set("")

    def _bind_preview_updates(self) -> None:
        for variable in (
            self.patient_var,
            self.prescription_var,
            self.medicine_var,
            self.form_var,
            self.quantity_var,
            self.dispense_time_var,
            self.priority_var,
            self.notes_var,
        ):
            variable.trace_add("write", self._on_field_changed)

    def _on_field_changed(self, *_args: object) -> None:
        self.update_dispensing_preview()

    def update_dispensing_preview(self) -> None:
        patient = self.patient_var.get().strip() or "Select a patient"
        prescription = self.prescription_var.get().strip() or "Prescription pending"
        medicine = self.medicine_var.get().strip() or "Medication pending"
        form = self.form_var.get().strip() or "Form pending"
        quantity = self.quantity_var.get().strip() or "--"
        dispense_time = self.dispense_time_var.get().strip() or "--:--"
        priority = self.priority_var.get().strip() or "Priority pending"
        notes = self.notes_var.get().strip() or "No pharmacist note added yet."

        self.preview_var.set(
            f"{patient}\n"
            f"{prescription} | {priority}\n"
            f"{medicine} ({form})\n"
            f"Quantity: {quantity} units | Pickup: {dispense_time}\n"
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
        draw_pharmacy_summary_icon(icon)

        text_col = tk.Frame(row, bg=CARD_BACKGROUND)
        text_col.pack(side="left", fill="both", expand=True)

        tk.Label(
            text_col,
            text="Pharmacy Operations Dashboard",
            font=("Segoe UI", 16, "bold"),
            bg=CARD_BACKGROUND,
            fg=TEXT_PRIMARY,
        ).pack(anchor="w")

        tk.Label(
            text_col,
            text="Your dashboard centralizes medication dispensing, stock visibility, and patient treatment requests.",
            font=("Segoe UI", 10),
            bg=CARD_BACKGROUND,
            fg=TEXT_SECONDARY,
            wraplength=840,
            justify="left",
        ).pack(anchor="w", pady=(6, 0))


class PharmacistDashboardPage(ScrollablePage):
    def __init__(self, parent: tk.Widget, app: PharmacistPortalFrame) -> None:
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
            text="Pharmacist",
            font=("Segoe UI", 15),
            bg=APP_BACKGROUND,
            fg=TEXT_SECONDARY,
        ).pack(anchor="w", pady=(6, 0))

        summary_card = SummaryCard(self.content)
        summary_card.pack(fill="x", padx=64, pady=12)

        cards = (
            (
                "Dispensing",
                "Process medication handoffs, verify requests, and keep the pharmacy queue moving.",
                "Record dispensing",
                draw_dispensing_icon,
                lambda: self.app.show_page("record_dispensing"),
            ),
            (
                "Stock",
                "Track medicine availability, low-stock items, and refill priorities.",
                "Open stock",
                draw_stock_icon,
                self._show_stock_message,
            ),
            (
                "Patients",
                "Review current treatment requests and active medication follow-ups.",
                "Open patients",
                draw_patients_icon,
                self._show_patients_message,
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
            command=lambda: self.app.show_page("login"),
            cursor="hand2",
        ).pack(anchor="w")

        footer = tk.Frame(self.content, bg=APP_BACKGROUND, height=20)
        footer.pack(fill="x")

    @staticmethod
    def _show_stock_message() -> None:
        messagebox.showinfo("Stock", "Stock tracking tools can be added here.")

    @staticmethod
    def _show_patients_message() -> None:
        messagebox.showinfo("Patients", "Patient medication tools can be added here.")


class RecordDispensingPage(ScrollablePage):
    def __init__(self, parent: tk.Widget, app: PharmacistPortalFrame) -> None:
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
        self._build_patient_section()
        self._build_medication_section()
        self._build_fulfillment_section()
        self._build_notes_section()
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
        draw_dispensing_icon(icon)

        text_col = tk.Frame(row, bg=CARD_BACKGROUND)
        text_col.pack(side="left", fill="both", expand=True)

        tk.Label(
            text_col,
            text="Record Dispensing",
            font=("Segoe UI", 16, "bold"),
            bg=CARD_BACKGROUND,
            fg=TEXT_PRIMARY,
        ).pack(anchor="w")

        tk.Label(
            text_col,
            text="Track a medication handoff, confirm the pickup window, and review the dispensing summary before saving.",
            font=("Segoe UI", 10),
            bg=CARD_BACKGROUND,
            fg=TEXT_SECONDARY,
            wraplength=820,
            justify="left",
        ).pack(anchor="w", pady=(6, 0))

    def _build_patient_section(self) -> None:
        section = self._section_card("Patient And Prescription", "Capture who the medication is for and the active prescription", height=152)
        row = tk.Frame(section, bg=CARD_BACKGROUND)
        row.pack(anchor="w")

        self._labeled_entry(row, "Patient", self.app.patient_var, width=28).pack(side="left", padx=(0, 16))
        self._labeled_entry(row, "Prescription ID", self.app.prescription_var, width=24).pack(side="left")

    def _build_medication_section(self) -> None:
        section = self._section_card("Medication", "Select the item being dispensed and the dosage form", height=152)
        row = tk.Frame(section, bg=CARD_BACKGROUND)
        row.pack(anchor="w")

        medicine_block = self._labeled_container(row, "Medicine")
        medicine_combo = ttk.Combobox(
            medicine_block,
            textvariable=self.app.medicine_var,
            values=MEDICINES,
            state="readonly",
            style="Portal.TCombobox",
            font=("Segoe UI", 10),
            width=28,
        )
        medicine_combo.pack(anchor="w", ipadx=4, ipady=3)
        medicine_block.pack(side="left", padx=(0, 16))

        form_block = self._labeled_container(row, "Form")
        form_combo = ttk.Combobox(
            form_block,
            textvariable=self.app.form_var,
            values=DOSAGE_FORMS,
            state="readonly",
            style="Portal.TCombobox",
            font=("Segoe UI", 10),
            width=20,
        )
        form_combo.pack(anchor="w", ipadx=4, ipady=3)
        form_block.pack(side="left")

    def _build_fulfillment_section(self) -> None:
        section = self._section_card("Fulfillment", "Set the quantity, pickup time, and handling priority", height=174)
        row = tk.Frame(section, bg=CARD_BACKGROUND)
        row.pack(anchor="w")

        self._labeled_entry(row, "Quantity", self.app.quantity_var, width=12).pack(side="left", padx=(0, 14))

        window_block = self._labeled_container(row, "Pickup Time")
        window_combo = ttk.Combobox(
            window_block,
            textvariable=self.app.dispense_time_var,
            values=DISPENSE_WINDOWS,
            state="readonly",
            style="Portal.TCombobox",
            font=("Segoe UI", 10),
            width=16,
        )
        window_combo.pack(anchor="w", ipadx=4, ipady=3)
        window_block.pack(side="left", padx=(0, 14))

        priority_block = self._labeled_container(row, "Priority")
        priority_combo = ttk.Combobox(
            priority_block,
            textvariable=self.app.priority_var,
            values=PRIORITY_LEVELS,
            state="readonly",
            style="Portal.TCombobox",
            font=("Segoe UI", 10),
            width=16,
        )
        priority_combo.pack(anchor="w", ipadx=4, ipady=3)
        priority_block.pack(side="left")

    def _build_notes_section(self) -> None:
        section = self._section_card("Dispensing Notes", "Add any pharmacist note or handoff instruction", height=140)
        self._make_entry(section, self.app.notes_var, width=86).pack(anchor="w")

    def _build_preview_section(self) -> None:
        section = self._section_card("Dispensing Preview", "Review the medication handoff before you save it", height=156)
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
            text="Save Dispensing",
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
            command=self.app.clear_dispensing_form,
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
        if self.app.save_dispensing():
            self.app.clear_dispensing_form()


def draw_pharmacy_summary_icon(canvas: tk.Canvas) -> None:
    canvas.create_rectangle(14, 16, 44, 64, width=3, outline="#111111")
    canvas.create_rectangle(19, 8, 39, 18, width=3, outline="#111111")
    canvas.create_line(29, 28, 29, 52, width=3, fill="#111111", capstyle=tk.ROUND)
    canvas.create_line(19, 40, 39, 40, width=3, fill="#111111", capstyle=tk.ROUND)
    canvas.create_oval(52, 24, 74, 38, width=3, outline="#111111")
    canvas.create_line(56, 31, 70, 31, width=2, fill="#111111", capstyle=tk.ROUND)


def draw_dispensing_icon(canvas: tk.Canvas) -> None:
    canvas.create_rectangle(18, 18, 48, 66, width=3, outline="#111111")
    canvas.create_rectangle(22, 10, 44, 20, width=3, outline="#111111")
    canvas.create_line(33, 29, 33, 52, width=3, fill="#111111", capstyle=tk.ROUND)
    canvas.create_line(23, 40, 43, 40, width=3, fill="#111111", capstyle=tk.ROUND)
    canvas.create_line(60, 45, 69, 54, width=4, fill="#111111", capstyle=tk.ROUND)
    canvas.create_line(69, 54, 88, 24, width=4, fill="#111111", capstyle=tk.ROUND)


def draw_stock_icon(canvas: tk.Canvas) -> None:
    canvas.create_rectangle(18, 24, 44, 48, width=3, outline="#111111")
    canvas.create_rectangle(44, 24, 70, 48, width=3, outline="#111111")
    canvas.create_rectangle(31, 48, 57, 72, width=3, outline="#111111")
    canvas.create_line(31, 36, 44, 36, width=2, fill="#111111")
    canvas.create_line(44, 36, 57, 36, width=2, fill="#111111")
    canvas.create_line(57, 36, 70, 36, width=2, fill="#111111")


def draw_patients_icon(canvas: tk.Canvas) -> None:
    canvas.create_oval(22, 18, 46, 42, width=3, outline="#111111")
    canvas.create_arc(14, 36, 54, 70, start=0, extent=180, style="arc", width=3)
    canvas.create_oval(56, 22, 76, 42, width=3, outline="#111111")
    canvas.create_arc(49, 37, 83, 66, start=0, extent=180, style="arc", width=3)
    canvas.create_line(88, 22, 104, 22, width=3, fill="#111111", capstyle=tk.ROUND)
    canvas.create_line(96, 14, 96, 30, width=3, fill="#111111", capstyle=tk.ROUND)

