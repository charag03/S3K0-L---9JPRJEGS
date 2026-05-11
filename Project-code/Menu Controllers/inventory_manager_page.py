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
DATA_FILE = Path(__file__).with_name("saved_restock_orders.json")

ITEMS = [
    "Nitrile Gloves",
    "Syringes 5 ml",
    "IV Sets",
    "Surgical Masks",
    "Paracetamol 500 mg",
]

CATEGORIES = [
    "PPE",
    "Consumables",
    "Medication",
    "Equipment",
    "Lab Supplies",
]

SUPPLIERS = [
    "MediCore Supply",
    "HealthBridge Logistics",
    "NovaCare Wholesale",
    "SteriLine Partners",
    "BlueCross Medical",
]

PRIORITY_LEVELS = [
    "Routine",
    "Urgent",
    "Critical",
]

DELIVERY_WINDOWS = [
    "24 Hours",
    "48 Hours",
    "3 Days",
    "1 Week",
]


# Change class definition and __init__
class InventoryManagerPortalFrame(tk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent, bg=APP_BACKGROUND)
        self.controller = controller  # Pointer to HospitalMaster

        # Initialize all tracking variables
        self.item_var = tk.StringVar(value=ITEMS[0])
        self.category_var = tk.StringVar(value=CATEGORIES[0])
        self.quantity_var = tk.StringVar(value="100")
        self.supplier_var = tk.StringVar(value=SUPPLIERS[0])
        self.priority_var = tk.StringVar(value=PRIORITY_LEVELS[0])
        self.delivery_window_var = tk.StringVar(value=DELIVERY_WINDOWS[0])
        self.order_code_var = tk.StringVar(value="PO-4102")
        self.notes_var = tk.StringVar()
        self.preview_var = tk.StringVar()

        self.saved_orders = self._load_orders()
        self._bind_preview_updates()
        self.update_order_preview()

        # Internal container for Inventory sub-pages
        self.sub_container = tk.Frame(self, bg=APP_BACKGROUND)
        self.sub_container.pack(fill="both", expand=True)

        self.user_display_name = controller.current_user_name

        self.pages = {
            "dashboard": InventoryDashboardPage(self.sub_container, self),
            "place_restock_order": RestockOrderPage(self.sub_container, self),
        }

        for page in self.pages.values():
            page.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.show_page("dashboard")

    def show_page(self, page_name: str) -> None:
        if page_name in self.pages:
            self.pages[page_name].tkraise()
        elif page_name == "login":
            self.controller.show_login(user_name="")  # Logout back to Master Login

    # ... Keep all logic methods (_load_orders, save_order, etc.) here ...

    def _load_orders(self) -> list[dict[str, str]]:
        if not DATA_FILE.exists():
            return []

        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []

    def save_order(self) -> bool:
        item = self.item_var.get().strip()
        category = self.category_var.get().strip()
        quantity = self.quantity_var.get().strip()
        supplier = self.supplier_var.get().strip()
        priority = self.priority_var.get().strip()
        delivery_window = self.delivery_window_var.get().strip()
        order_code = self.order_code_var.get().strip()
        notes = self.notes_var.get().strip()

        if not item or not category or not quantity or not supplier or not priority or not delivery_window or not order_code:
            messagebox.showerror("Missing details", "Please complete all order fields before saving.")
            return False

        if not quantity.isdigit():
            messagebox.showerror("Invalid quantity", "Quantity should be a whole number.")
            return False

        order = {
            "item": item,
            "category": category,
            "quantity": quantity,
            "supplier": supplier,
            "priority": priority,
            "delivery_window": delivery_window,
            "order_code": order_code,
            "notes": notes,
        }
        self.saved_orders.append(order)

        try:
            DATA_FILE.write_text(json.dumps(self.saved_orders, indent=2), encoding="utf-8")
        except OSError as error:
            messagebox.showerror("Save failed", f"Could not write orders to disk.\n{error}")
            return False

        messagebox.showinfo(
            "Order Saved",
            f"Saved restock order for {item}, quantity {quantity}, via {supplier}.",
        )
        return True

    def clear_order_form(self) -> None:
        self.item_var.set(ITEMS[0])
        self.category_var.set(CATEGORIES[0])
        self.quantity_var.set("100")
        self.supplier_var.set(SUPPLIERS[0])
        self.priority_var.set(PRIORITY_LEVELS[0])
        self.delivery_window_var.set(DELIVERY_WINDOWS[0])
        self.order_code_var.set("PO-4102")
        self.notes_var.set("")

    def _bind_preview_updates(self) -> None:
        for variable in (
            self.item_var,
            self.category_var,
            self.quantity_var,
            self.supplier_var,
            self.priority_var,
            self.delivery_window_var,
            self.order_code_var,
            self.notes_var,
        ):
            variable.trace_add("write", self._on_field_changed)

    def _on_field_changed(self, *_args: object) -> None:
        self.update_order_preview()

    def update_order_preview(self) -> None:
        item = self.item_var.get().strip() or "Select an item"
        category = self.category_var.get().strip() or "Category pending"
        quantity = self.quantity_var.get().strip() or "--"
        supplier = self.supplier_var.get().strip() or "Supplier pending"
        priority = self.priority_var.get().strip() or "Priority pending"
        delivery_window = self.delivery_window_var.get().strip() or "Window pending"
        order_code = self.order_code_var.get().strip() or "Order code pending"
        notes = self.notes_var.get().strip() or "No purchasing note added yet."

        self.preview_var.set(
            f"{order_code}\n"
            f"{item} | {category}\n"
            f"Quantity: {quantity} units\n"
            f"Supplier: {supplier}\n"
            f"Priority: {priority} | Delivery: {delivery_window}\n"
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
        draw_inventory_summary_icon(icon)

        text_col = tk.Frame(row, bg=CARD_BACKGROUND)
        text_col.pack(side="left", fill="both", expand=True)

        tk.Label(
            text_col,
            text="Inventory Operations Dashboard",
            font=("Segoe UI", 16, "bold"),
            bg=CARD_BACKGROUND,
            fg=TEXT_PRIMARY,
        ).pack(anchor="w")

        tk.Label(
            text_col,
            text="Your dashboard focuses on stock levels, orders, and restock risk across hospital inventory.",
            font=("Segoe UI", 10),
            bg=CARD_BACKGROUND,
            fg=TEXT_SECONDARY,
            wraplength=840,
            justify="left",
        ).pack(anchor="w", pady=(6, 0))


class InventoryDashboardPage(ScrollablePage):
    def __init__(self, parent: tk.Widget, app: InventoryManagerPortalFrame) -> None:
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
            text="Inventory Manager",
            font=("Segoe UI", 15),
            bg=APP_BACKGROUND,
            fg=TEXT_SECONDARY,
        ).pack(anchor="w", pady=(6, 0))

        summary_card = SummaryCard(self.content)
        summary_card.pack(fill="x", padx=64, pady=12)

        cards = (
            (
                "Inventory",
                "Monitor current stock levels, item categories, and warehouse coverage.",
                "Open inventory",
                draw_inventory_icon,
                self._show_inventory_message,
            ),
            (
                "Orders",
                "Create and review supply orders for medicine, equipment, and hospital essentials.",
                "Place restock order",
                draw_orders_icon,
                lambda: self.app.show_page("place_restock_order"),
            ),
            (
                "Alerts",
                "See items that need replenishment before shortages affect operations.",
                "Open alerts",
                draw_alerts_icon,
                self._show_alerts_message,
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
            command=self.app.destroy,
            cursor="hand2",
        ).pack(anchor="w")

        footer = tk.Frame(self.content, bg=APP_BACKGROUND, height=20)
        footer.pack(fill="x")

    @staticmethod
    def _show_inventory_message() -> None:
        messagebox.showinfo("Inventory", "Inventory monitoring tools can be added here.")

    @staticmethod
    def _show_alerts_message() -> None:
        messagebox.showinfo("Alerts", "Restock alert tools can be added here.")


class RestockOrderPage(ScrollablePage):
    def __init__(self, parent: tk.Widget, app: InventoryManagerPortalFrame) -> None:
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
        self._build_item_section()
        self._build_supplier_section()
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
        draw_orders_icon(icon)

        text_col = tk.Frame(row, bg=CARD_BACKGROUND)
        text_col.pack(side="left", fill="both", expand=True)

        tk.Label(
            text_col,
            text="Place Restock Order",
            font=("Segoe UI", 16, "bold"),
            bg=CARD_BACKGROUND,
            fg=TEXT_PRIMARY,
        ).pack(anchor="w")

        tk.Label(
            text_col,
            text="Create a supply request, confirm the supplier and urgency, and review the order before saving it locally.",
            font=("Segoe UI", 10),
            bg=CARD_BACKGROUND,
            fg=TEXT_SECONDARY,
            wraplength=820,
            justify="left",
        ).pack(anchor="w", pady=(6, 0))

    def _build_item_section(self) -> None:
        section = self._section_card("Item Details", "Select the item, category, and requested quantity", height=168)
        row = tk.Frame(section, bg=CARD_BACKGROUND)
        row.pack(anchor="w")

        item_block = self._labeled_container(row, "Item")
        item_combo = ttk.Combobox(
            item_block,
            textvariable=self.app.item_var,
            values=ITEMS,
            state="readonly",
            style="Portal.TCombobox",
            font=("Segoe UI", 10),
            width=24,
        )
        item_combo.pack(anchor="w", ipadx=4, ipady=3)
        item_block.pack(side="left", padx=(0, 16))

        category_block = self._labeled_container(row, "Category")
        category_combo = ttk.Combobox(
            category_block,
            textvariable=self.app.category_var,
            values=CATEGORIES,
            state="readonly",
            style="Portal.TCombobox",
            font=("Segoe UI", 10),
            width=18,
        )
        category_combo.pack(anchor="w", ipadx=4, ipady=3)
        category_block.pack(side="left", padx=(0, 16))

        self._labeled_entry(row, "Quantity", self.app.quantity_var, width=12).pack(side="left")

    def _build_supplier_section(self) -> None:
        section = self._section_card("Supplier And Delivery", "Choose the supplier, urgency, and delivery target", height=174)
        row = tk.Frame(section, bg=CARD_BACKGROUND)
        row.pack(anchor="w")

        supplier_block = self._labeled_container(row, "Supplier")
        supplier_combo = ttk.Combobox(
            supplier_block,
            textvariable=self.app.supplier_var,
            values=SUPPLIERS,
            state="readonly",
            style="Portal.TCombobox",
            font=("Segoe UI", 10),
            width=24,
        )
        supplier_combo.pack(anchor="w", ipadx=4, ipady=3)
        supplier_block.pack(side="left", padx=(0, 14))

        priority_block = self._labeled_container(row, "Priority")
        priority_combo = ttk.Combobox(
            priority_block,
            textvariable=self.app.priority_var,
            values=PRIORITY_LEVELS,
            state="readonly",
            style="Portal.TCombobox",
            font=("Segoe UI", 10),
            width=14,
        )
        priority_combo.pack(anchor="w", ipadx=4, ipady=3)
        priority_block.pack(side="left", padx=(0, 14))

        delivery_block = self._labeled_container(row, "Delivery Window")
        delivery_combo = ttk.Combobox(
            delivery_block,
            textvariable=self.app.delivery_window_var,
            values=DELIVERY_WINDOWS,
            state="readonly",
            style="Portal.TCombobox",
            font=("Segoe UI", 10),
            width=14,
        )
        delivery_combo.pack(anchor="w", ipadx=4, ipady=3)
        delivery_block.pack(side="left", padx=(0, 14))

        self._labeled_entry(row, "Order Code", self.app.order_code_var, width=12).pack(side="left")

    def _build_notes_section(self) -> None:
        section = self._section_card("Order Notes", "Add a quick purchasing note or warehouse comment", height=140)
        self._make_entry(section, self.app.notes_var, width=86).pack(anchor="w")

    def _build_preview_section(self) -> None:
        section = self._section_card("Order Preview", "Review the order summary before you save it", height=170)
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
            text="Save Order",
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
            command=self.app.clear_order_form,
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
        if self.app.save_order():
            self.app.clear_order_form()


def draw_inventory_summary_icon(canvas: tk.Canvas) -> None:
    canvas.create_rectangle(14, 18, 42, 44, width=3, outline="#111111")
    canvas.create_rectangle(42, 18, 70, 44, width=3, outline="#111111")
    canvas.create_rectangle(28, 44, 56, 68, width=3, outline="#111111")
    canvas.create_line(21, 31, 35, 31, width=2, fill="#111111")
    canvas.create_line(49, 31, 63, 31, width=2, fill="#111111")
    canvas.create_line(35, 56, 49, 56, width=2, fill="#111111")


def draw_inventory_icon(canvas: tk.Canvas) -> None:
    canvas.create_rectangle(18, 22, 44, 46, width=3, outline="#111111")
    canvas.create_rectangle(44, 22, 70, 46, width=3, outline="#111111")
    canvas.create_rectangle(31, 46, 57, 70, width=3, outline="#111111")
    canvas.create_line(82, 20, 98, 20, width=3, fill="#111111", capstyle=tk.ROUND)
    canvas.create_line(90, 12, 90, 28, width=3, fill="#111111", capstyle=tk.ROUND)


def draw_orders_icon(canvas: tk.Canvas) -> None:
    canvas.create_rectangle(18, 18, 64, 60, width=3, outline="#111111")
    canvas.create_line(28, 30, 54, 30, width=3, fill="#111111", capstyle=tk.ROUND)
    canvas.create_line(28, 40, 54, 40, width=3, fill="#111111", capstyle=tk.ROUND)
    canvas.create_line(28, 50, 46, 50, width=3, fill="#111111", capstyle=tk.ROUND)
    canvas.create_line(72, 30, 86, 44, width=4, fill="#111111", capstyle=tk.ROUND)
    canvas.create_line(86, 44, 104, 20, width=4, fill="#111111", capstyle=tk.ROUND)


def draw_alerts_icon(canvas: tk.Canvas) -> None:
    canvas.create_polygon(56, 14, 96, 76, 16, 76, width=3, outline="#111111", fill="")
    canvas.create_line(56, 30, 56, 50, width=4, fill="#111111", capstyle=tk.ROUND)
    canvas.create_oval(53, 58, 59, 64, width=0, fill="#111111")
    canvas.create_line(86, 18, 102, 18, width=3, fill="#111111", capstyle=tk.ROUND)
