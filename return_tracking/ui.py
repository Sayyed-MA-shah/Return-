import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_NAME = "return_data.db"

import tkinter as tk
from tkinter import ttk

FONT = ("Segoe UI", 11)

class LaptopReturnTrackerUI:
    def __init__(self, root, callbacks):
        self.root = root
        self.callbacks = callbacks
        self.build_ui()

    def build_ui(self):
        self.root.title("Laptop Return Tracker")
        self.root.geometry("1150x650")

        # ---------- Top Navigation ---------- #
        nav_frame = ttk.Frame(self.root)
        nav_frame.pack(fill="x", padx=10, pady=(10, 0))

        ttk.Button(nav_frame, text="Add New Return", command=self.callbacks['show_form']).pack(side="left", padx=(0, 5))
        ttk.Button(nav_frame, text="Returns Table", command=self.callbacks['show_table']).pack(side="left")

        ttk.Label(nav_frame, text="Search by ID:", font=FONT).pack(side="left", padx=(20, 5))
        self.quick_search_entry = ttk.Entry(nav_frame, width=15)
        self.quick_search_entry.pack(side="left")
        ttk.Button(nav_frame, text="Go", command=self.callbacks['quick_search']).pack(side="left", padx=(5, 0))

        # ---------- Main Content Container ---------- #
        self.container = ttk.Frame(self.root)
        self.container.pack(fill="both", expand=True, padx=10, pady=10)

        self.build_form_view()
        self.build_table_view()

        self.show_form()

    def build_form_view(self):
        self.form_frame = ttk.Frame(self.container)

        # Form Fields Grid
        form_grid = ttk.Frame(self.form_frame)
        form_grid.pack(pady=10, fill="x")

        # Row 1
        ttk.Label(form_grid, text="Return ID:", font=FONT).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.brand_cb = ttk.Combobox(form_grid, values=["Dell", "HP", "Lenovo"], font=FONT, state="readonly")
        self.brand_cb.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(form_grid, text="Order No:", font=FONT).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.order_entry = ttk.Entry(form_grid, font=FONT)
        self.order_entry.grid(row=0, column=3, sticky="ew", padx=5, pady=5)

        # Row 2
        ttk.Label(form_grid, text="RAM (GB):", font=FONT).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.ram_entry = ttk.Entry(form_grid, font=FONT)
        self.ram_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(form_grid, text="SSD (GB):", font=FONT).grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.ssd_entry = ttk.Entry(form_grid, font=FONT)
        self.ssd_entry.grid(row=1, column=3, sticky="ew", padx=5, pady=5)

        # Row 3
        ttk.Label(form_grid, text="HDD (GB):", font=FONT).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.hdd_entry = ttk.Entry(form_grid, font=FONT)
        self.hdd_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(form_grid, text="Condition:", font=FONT).grid(row=2, column=2, sticky="w", padx=5, pady=5)
        self.condition_cb = ttk.Combobox(form_grid, values=["Like New", "Good", "Fair", "Poor"], font=FONT, state="readonly")
        self.condition_cb.grid(row=2, column=3, sticky="ew", padx=5, pady=5)

        # Row 4
        ttk.Label(form_grid, text="Status:", font=FONT).grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.status_cb = ttk.Combobox(form_grid, values=["Pending", "Accepted", "Rejected"], font=FONT, state="readonly")
        self.status_cb.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(form_grid, text="Inspector Notes:", font=FONT).grid(row=4, column=0, columnspan=4, sticky="w", padx=5, pady=(15, 0))
        self.notes_text = tk.Text(form_grid, height=3, font=FONT)
        self.notes_text.grid(row=5, column=0, columnspan=4, sticky="ew", padx=5, pady=(0, 10))

        for i in range(4):
            form_grid.columnconfigure(i, weight=1)

        # Form Actions
        actions = ttk.Frame(self.form_frame)
        actions.pack(pady=10)
        ttk.Button(actions, text="Save Return", command=self.callbacks['save']).pack(side="left", padx=5)
        ttk.Button(actions, text="Reset Form", command=self.callbacks['reset']).pack(side="left", padx=5)
        ttk.Button(actions, text="Back to Table View", command=self.callbacks['show_table']).pack(side="left", padx=5)

    def build_table_view(self):
        self.table_frame = ttk.Frame(self.container)

        # Filter/Search Bar
        search_frame = ttk.Frame(self.table_frame)
        search_frame.pack(fill="x", pady=5)

        ttk.Label(search_frame, text="Search by ID:", font=FONT).pack(side="left", padx=5)
        self.search_id_entry = ttk.Entry(search_frame, width=20)
        self.search_id_entry.pack(side="left", padx=5)
        ttk.Button(search_frame, text="Search", command=self.callbacks['search']).pack(side="left", padx=5)

        ttk.Label(search_frame, text="Filter by Condition:", font=FONT).pack(side="left", padx=20)
        self.filter_condition_cb = ttk.Combobox(search_frame, values=["All", "Like New", "Good", "Fair", "Poor"], state="readonly")
        self.filter_condition_cb.current(0)
        self.filter_condition_cb.pack(side="left")
        ttk.Button(search_frame, text="Filter", command=self.callbacks['filter']).pack(side="left", padx=5)

        # Table
        self.tree = ttk.Treeview(self.table_frame, columns=("Return ID", "Brand", "Order No", "RAM", "SSD", "HDD", "Condition", "Status", "Notes"), show="headings")
        self.tree.pack(fill="both", expand=True, pady=10)

        headings = ["Return ID", "Brand", "Order No", "RAM", "SSD", "HDD", "Condition", "Status", "Notes"]
        for col in headings:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        self.tree.bind("<Double-1>", self.callbacks['row_click'])

    def show_form(self):
        self.table_frame.pack_forget()
        self.form_frame.pack(fill="both", expand=True)

    def show_table(self):
        self.form_frame.pack_forget()
        self.table_frame.pack(fill="both", expand=True)



