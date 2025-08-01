import tkinter as tk
from tkinter import ttk

class RestockTrackerUI:
    def __init__(self, root, callbacks):
        self.root = root
        self.callbacks = callbacks
        self.build_ui()

    def build_ui(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        title = tk.Label(frame, text="Restock Paperwork Tracker", font=("Segoe UI", 16, "bold"))
        title.pack(pady=(0, 20))

        form_frame = tk.Frame(frame)
        form_frame.pack(fill="x")

        tk.Label(form_frame, text="Order Number:", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="e")
        self.order_entry = tk.Entry(form_frame, width=30)
        self.order_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Status:", font=("Segoe UI", 10)).grid(row=0, column=2, sticky="e")
        self.status_combo = ttk.Combobox(form_frame, values=["Paperwork Sent", "Item Sent"], state="readonly")
        self.status_combo.grid(row=0, column=3, padx=5, pady=5)

        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Save", command=self.callbacks['save'], width=12).pack(side="left", padx=5)
        tk.Button(button_frame, text="Reset", command=self.callbacks['reset'], width=12).pack(side="left", padx=5)
        tk.Button(button_frame, text="Delete", command=self.callbacks['delete'], width=12).pack(side="left", padx=5)
        tk.Button(button_frame, text="Back", command=self.callbacks['back'], width=12).pack(side="left", padx=5)

        search_frame = tk.Frame(frame)
        search_frame.pack(pady=(10, 0))

        tk.Label(search_frame, text="Search Order:", font=("Segoe UI", 10)).pack(side="left")
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side="left", padx=5)
        tk.Button(search_frame, text="Search", command=self.callbacks['search']).pack(side="left")

        table_frame = tk.Frame(frame)
        table_frame.pack(fill="both", expand=True, pady=(10, 0))

        self.tree = ttk.Treeview(table_frame, columns=("order_no", "status"), show="headings")
        self.tree.heading("order_no", text="Order Number")
        self.tree.heading("status", text="Status")
        self.tree.column("order_no", width=200)
        self.tree.column("status", width=200)
        self.tree.pack(fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    def get_order_info(self):
        return self.order_entry.get().strip(), self.status_combo.get().strip()

    def set_order_info(self, order, status):
        self.order_entry.delete(0, tk.END)
        self.order_entry.insert(0, order)
        self.status_combo.set(status)

    def clear_fields(self):
        self.order_entry.delete(0, tk.END)
        self.status_combo.set("")

    def get_search_text(self):
        return self.search_entry.get().strip()

    def fill_table(self, rows):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in rows:
            self.tree.insert("", "end", values=row)
