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
DATA_FILE = Path(__file__).with_name("saved_prescriptions.json")

MEDICINES = [
    "Amoxicillin",
    "Ibuprofen",
    "Metformin",
    "Lisinopril",
    "Atorvastatin",
]

DOSAGES = [
    "250 mg",
    "500 mg",
    "850 mg",
    "10 mg",
    "20 mg",
]

FREQUENCIES = [
    "Once daily",
    "Twice daily",
    "Three times daily",
    "Every 8 hours",
    "As needed",
]

DURATIONS = [
    "3 days",
    "5 days",
    "7 days",
    "14 days",
    "30 days",
]

ROUTES = [
    "Oral",
    "IV",
    "Topical",
    "Inhalation",
    "Subcutaneous",
]


# Change the class definition and __init__
class DoctorPortalFrame(tk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent, bg=APP_BACKGROUND)
        self.controller = controller  # This is the HospitalMaster

        # Move the StringVars from the old App class to here
        self.patient_var = tk.StringVar()
        self.visit_date_var = tk.StringVar(value="2026-03-24")
        self.diagnosis_var = tk.StringVar()
        self.medicine_var = tk.StringVar(value=MEDICINES[0])
        self.dosage_var = tk.StringVar(value=DOSAGES[1])
        self.route_var = tk.StringVar(value=ROUTES[0])
        self.frequency_var = tk.StringVar(value=FREQUENCIES[1])
        self.duration_var = tk.StringVar(value=DURATIONS[2])
        self.prescription_code_var = tk.StringVar(value="RX-1107")
        self.notes_var = tk.StringVar()
        self.preview_var = tk.StringVar()

        self.saved_prescriptions = self._load_prescriptions()
        self._bind_preview_updates()
        self.update_prescription_preview()

        # The internal container for sub-pages
        self.sub_container = tk.Frame(self, bg=APP_BACKGROUND)
        self.sub_container.pack(fill="both", expand=True)

        self.user_display_name = controller.current_user_name

        self.pages = {
            "dashboard": DoctorDashboardPage(self.sub_container, self),
            "issue_prescription": PrescriptionPage(self.sub_container, self),
        }

        for page in self.pages.values():
            page.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.show_page("dashboard")

    def show_page(self, page_name: str) -> None:
        if page_name in self.pages:
            self.pages[page_name].tkraise()
        elif page_name == "login":
            self.controller.show_login(user_name="")  # Reference the Master to logout

    # Keep your _load_prescriptions, save_prescription, and logic methods here...
    def _load_prescriptions(self) -> list[dict[str, str]]:
        if not DATA_FILE.exists():
            return []

        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []

    def save_prescription(self) -> bool:
        patient = self.patient_var.get().strip()
        visit_date = self.visit_date_var.get().strip()
        diagnosis = self.diagnosis_var.get().strip()
        medicine = self.medicine_var.get().strip()
        dosage = self.dosage_var.get().strip()
        route = self.route_var.get().strip()
        frequency = self.frequency_var.get().strip()
        duration = self.duration_var.get().strip()
        prescription_code = self.prescription_code_var.get().strip()
        notes = self.notes_var.get().strip()

        if not patient or not visit_date or not diagnosis or not medicine or not dosage or not route or not frequency or not duration or not prescription_code:
            messagebox.showerror("Missing details", "Please complete all prescription fields before saving.")
            return False

        prescription = {
            "patient": patient,
            "visit_date": visit_date,
            "diagnosis": diagnosis,
            "medicine": medicine,
            "dosage": dosage,
            "route": route,
            "frequency": frequency,
            "duration": duration,
            "prescription_code": prescription_code,
            "notes": notes,
        }
        self.saved_prescriptions.append(prescription)

        try:
            DATA_FILE.write_text(json.dumps(self.saved_prescriptions, indent=2), encoding="utf-8")
        except OSError as error:
            messagebox.showerror("Save failed", f"Could not write prescriptions to disk.\n{error}")
            return False

        messagebox.showinfo(
            "Prescription Saved",
            f"Saved prescription {prescription_code} for {patient}: {medicine} {dosage}.",
        )
        return True

    def clear_prescription_form(self) -> None:
        self.patient_var.set("")
        self.visit_date_var.set("2026-03-24")
        self.diagnosis_var.set("")
        self.medicine_var.set(MEDICINES[0])
        self.dosage_var.set(DOSAGES[1])
        self.route_var.set(ROUTES[0])
        self.frequency_var.set(FREQUENCIES[1])
        self.duration_var.set(DURATIONS[2])
        self.prescription_code_var.set("RX-1107")
        self.notes_var.set("")

    def _bind_preview_updates(self) -> None:
        for variable in (
            self.patient_var,
            self.visit_date_var,
            self.diagnosis_var,
            self.medicine_var,
            self.dosage_var,
            self.route_var,
            self.frequency_var,
            self.duration_var,
            self.prescription_code_var,
            self.notes_var,
        ):
            variable.trace_add("write", self._on_field_changed)

    def _on_field_changed(self, *_args: object) -> None:
        self.update_prescription_preview()

    def update_prescription_preview(self) -> None:
        patient = self.patient_var.get().strip() or "Select a patient"
        visit_date = self.visit_date_var.get().strip() or "Date pending"
        diagnosis = self.diagnosis_var.get().strip() or "Diagnosis pending"
        medicine = self.medicine_var.get().strip() or "Medicine pending"
        dosage = self.dosage_var.get().strip() or "Dose pending"
        route = self.route_var.get().strip() or "Route pending"
        frequency = self.frequency_var.get().strip() or "Frequency pending"
        duration = self.duration_var.get().strip() or "Duration pending"
        prescription_code = self.prescription_code_var.get().strip() or "Prescription pending"
        notes = self.notes_var.get().strip() or "No clinical note added yet."

        self.preview_var.set(
            f"{prescription_code}\n"
            f"{patient} | {visit_date}\n"
            f"Diagnosis: {diagnosis}\n"
            f"{medicine} {dosage} via {route}\n"
            f"{frequency} for {duration}\n"
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
        draw_doctor_summary_icon(icon)

        text_col = tk.Frame(row, bg=CARD_BACKGROUND)
        text_col.pack(side="left", fill="both", expand=True)

        tk.Label(
            text_col,
            text="Clinical Actions Dashboard",
            font=("Segoe UI", 16, "bold"),
            bg=CARD_BACKGROUND,
            fg=TEXT_PRIMARY,
        ).pack(anchor="w")

        tk.Label(
            text_col,
            text="Your dashboard surfaces admissions, prescriptions, and patient records for today's shift.",
            font=("Segoe UI", 10),
            bg=CARD_BACKGROUND,
            fg=TEXT_SECONDARY,
            wraplength=840,
            justify="left",
        ).pack(anchor="w", pady=(6, 0))


class DoctorDashboardPage(ScrollablePage):
    def __init__(self, parent: tk.Widget, app: DoctorPortalFrame) -> None:
        super().__init__(parent)
        self.app = app
        self._build()

    def _build(self) -> None:
        header = tk.Frame(self.content, bg=APP_BACKGROUND)
        header.pack(fill="x", padx=64, pady=(34, 18))

        tk.Label(
            header,
            text=f"Hello, Dr. {self.app.user_display_name}",
            font=("Segoe UI", 22, "bold"),
            bg=APP_BACKGROUND,
            fg=TEXT_PRIMARY,
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Doctor",
            font=("Segoe UI", 15),
            bg=APP_BACKGROUND,
            fg=TEXT_SECONDARY,
        ).pack(anchor="w", pady=(6, 0))

        summary_card = SummaryCard(self.content)
        summary_card.pack(fill="x", padx=64, pady=12)

        cards = (
            (
                "Admissions",
                "Create or review patient admissions and move incoming visits into treatment workflow.",
                "Open admissions",
                draw_admissions_icon,
                self._show_admissions_message,
            ),
            (
                "Prescriptions",
                "Manage medication orders, dosage instructions, and renewal follow-ups.",
                "Issue prescription",
                draw_prescriptions_icon,
                lambda: self.app.show_page("issue_prescription"),
            ),
            (
                "Records",
                "Open and update medical files, diagnoses, and treatment notes.",
                "Open records",
                draw_records_icon,
                self._show_records_message,
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
    def _show_admissions_message() -> None:
        messagebox.showinfo("Admissions", "Admission workflow tools can be added here.")

    @staticmethod
    def _show_records_message() -> None:
        messagebox.showinfo("Records", "Medical record tools can be added here.")


class PrescriptionPage(ScrollablePage):
    def __init__(self, parent: tk.Widget, app: DoctorPortalFrame) -> None:
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
        self._build_plan_section()
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
        draw_prescriptions_icon(icon)

        text_col = tk.Frame(row, bg=CARD_BACKGROUND)
        text_col.pack(side="left", fill="both", expand=True)

        tk.Label(
            text_col,
            text="Issue Prescription",
            font=("Segoe UI", 16, "bold"),
            bg=CARD_BACKGROUND,
            fg=TEXT_PRIMARY,
        ).pack(anchor="w")

        tk.Label(
            text_col,
            text="Capture a medication order, set the treatment plan, and review the prescription summary before saving it locally.",
            font=("Segoe UI", 10),
            bg=CARD_BACKGROUND,
            fg=TEXT_SECONDARY,
            wraplength=820,
            justify="left",
        ).pack(anchor="w", pady=(6, 0))

    def _build_patient_section(self) -> None:
        section = self._section_card("Patient Visit", "Capture the patient, visit date, and diagnosis", height=168)
        row = tk.Frame(section, bg=CARD_BACKGROUND)
        row.pack(anchor="w")

        self._labeled_entry(row, "Patient", self.app.patient_var, width=24).pack(side="left", padx=(0, 16))
        self._labeled_entry(row, "Visit Date", self.app.visit_date_var, width=16).pack(side="left", padx=(0, 16))
        self._labeled_entry(row, "Diagnosis", self.app.diagnosis_var, width=26).pack(side="left")

    def _build_medication_section(self) -> None:
        section = self._section_card("Medication", "Select the medication, dosage, and route", height=168)
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
            width=22,
        )
        medicine_combo.pack(anchor="w", ipadx=4, ipady=3)
        medicine_block.pack(side="left", padx=(0, 16))

        dosage_block = self._labeled_container(row, "Dosage")
        dosage_combo = ttk.Combobox(
            dosage_block,
            textvariable=self.app.dosage_var,
            values=DOSAGES,
            state="readonly",
            style="Portal.TCombobox",
            font=("Segoe UI", 10),
            width=14,
        )
        dosage_combo.pack(anchor="w", ipadx=4, ipady=3)
        dosage_block.pack(side="left", padx=(0, 16))

        route_block = self._labeled_container(row, "Route")
        route_combo = ttk.Combobox(
            route_block,
            textvariable=self.app.route_var,
            values=ROUTES,
            state="readonly",
            style="Portal.TCombobox",
            font=("Segoe UI", 10),
            width=16,
        )
        route_combo.pack(anchor="w", ipadx=4, ipady=3)
        route_block.pack(side="left")

    def _build_plan_section(self) -> None:
        section = self._section_card("Treatment Plan", "Set frequency, duration, and prescription code", height=168)
        row = tk.Frame(section, bg=CARD_BACKGROUND)
        row.pack(anchor="w")

        frequency_block = self._labeled_container(row, "Frequency")
        frequency_combo = ttk.Combobox(
            frequency_block,
            textvariable=self.app.frequency_var,
            values=FREQUENCIES,
            state="readonly",
            style="Portal.TCombobox",
            font=("Segoe UI", 10),
            width=18,
        )
        frequency_combo.pack(anchor="w", ipadx=4, ipady=3)
        frequency_block.pack(side="left", padx=(0, 16))

        duration_block = self._labeled_container(row, "Duration")
        duration_combo = ttk.Combobox(
            duration_block,
            textvariable=self.app.duration_var,
            values=DURATIONS,
            state="readonly",
            style="Portal.TCombobox",
            font=("Segoe UI", 10),
            width=14,
        )
        duration_combo.pack(anchor="w", ipadx=4, ipady=3)
        duration_block.pack(side="left", padx=(0, 16))

        self._labeled_entry(row, "Prescription Code", self.app.prescription_code_var, width=16).pack(side="left")

    def _build_notes_section(self) -> None:
        section = self._section_card("Clinical Notes", "Add a short treatment note or patient instruction", height=140)
        self._make_entry(section, self.app.notes_var, width=86).pack(anchor="w")

    def _build_preview_section(self) -> None:
        section = self._section_card("Prescription Preview", "Review the order summary before you save it", height=170)
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
            text="Save Prescription",
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
            command=self.app.clear_prescription_form,
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
        if self.app.save_prescription():
            self.app.clear_prescription_form()


def draw_doctor_summary_icon(canvas: tk.Canvas) -> None:
    canvas.create_oval(20, 18, 44, 42, width=3, outline="#111111")
    canvas.create_arc(12, 36, 52, 70, start=0, extent=180, style="arc", width=3)
    canvas.create_line(58, 18, 58, 44, width=3, fill="#111111", capstyle=tk.ROUND)
    canvas.create_line(46, 31, 70, 31, width=3, fill="#111111", capstyle=tk.ROUND)


def draw_admissions_icon(canvas: tk.Canvas) -> None:
    canvas.create_rectangle(18, 14, 60, 66, width=3, outline="#111111")
    canvas.create_line(28, 28, 50, 28, width=3, fill="#111111", capstyle=tk.ROUND)
    canvas.create_line(28, 40, 50, 40, width=3, fill="#111111", capstyle=tk.ROUND)
    canvas.create_line(76, 22, 76, 48, width=3, fill="#111111", capstyle=tk.ROUND)
    canvas.create_line(63, 35, 89, 35, width=3, fill="#111111", capstyle=tk.ROUND)


def draw_prescriptions_icon(canvas: tk.Canvas) -> None:
    canvas.create_rectangle(18, 18, 44, 64, width=3, outline="#111111")
    canvas.create_rectangle(22, 10, 40, 20, width=3, outline="#111111")
    canvas.create_line(31, 28, 31, 52, width=3, fill="#111111", capstyle=tk.ROUND)
    canvas.create_line(22, 40, 40, 40, width=3, fill="#111111", capstyle=tk.ROUND)
    canvas.create_oval(56, 28, 92, 54, width=3, outline="#111111")
    canvas.create_line(63, 41, 85, 41, width=3, fill="#111111", capstyle=tk.ROUND)


def draw_records_icon(canvas: tk.Canvas) -> None:
    canvas.create_rectangle(18, 18, 60, 64, width=3, outline="#111111")
    canvas.create_line(28, 30, 50, 30, width=3, fill="#111111", capstyle=tk.ROUND)
    canvas.create_line(28, 42, 50, 42, width=3, fill="#111111", capstyle=tk.ROUND)
    canvas.create_line(70, 54, 90, 34, width=4, fill="#111111", capstyle=tk.ROUND)
    canvas.create_line(90, 34, 98, 42, width=4, fill="#111111", capstyle=tk.ROUND)

