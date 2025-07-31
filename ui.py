import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_NAME = "return_data.db"

# def launch_app():
#     # ==== Style ====
#     FONT = ("Segoe UI", 11)
#     HEADING_FONT = ("Segoe UI", 11, "bold")

#     # ==== Main Window ====
#     root = tk.Tk()
#     root.title("Laptop Return Tracker")
#     root.geometry("1000x600")

#     brand_codes = {"Dell": "DR", "HP": "HR", "Lenovo": "LR"}

#     # ==== DB Helper ====
#     def generate_return_id(brand_code):
#         conn = sqlite3.connect(DB_NAME)
#         c = conn.cursor()
#         c.execute("SELECT COUNT(*) FROM returns WHERE return_id LIKE ?", (brand_code + '%',))
#         count = c.fetchone()[0] + 1
#         conn.close()
#         return f"{brand_code}-{count:03d}"

#     def save_data():
#         brand = brand_var.get()
#         brand_code = brand_codes.get(brand, "XX")
#         return_id = generate_return_id(brand_code)
#         order_number = order_entry.get()
#         ram = ram_entry.get()
#         ssd = ssd_entry.get()
#         hdd = hdd_entry.get()
#         condition = condition_var.get()
#         status = status_var.get()
#         inspector_comment = comment_entry.get()

#         if not order_number:
#             messagebox.showwarning("Missing Data", "Order number is required.")
#             return

#         conn = sqlite3.connect(DB_NAME)
#         c = conn.cursor()
#         try:
#             c.execute('''
#                 INSERT INTO returns (return_id, brand, order_number, ram, ssd, hdd, condition, status, inspector_comment)
#                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
#             ''', (return_id, brand, order_number, ram, ssd, hdd, condition, status, inspector_comment))
#             conn.commit()
#             return_id_var.set(return_id)
#             messagebox.showinfo("Success", f"Return added with ID: {return_id}")
#             clear_form(keep_return_id=True)
#             show_all_returns()
#         except sqlite3.IntegrityError:
#             messagebox.showerror("Error", "Duplicate return ID.")
#         finally:
#             conn.close()

#     def search_by_return_id():
#         search_id = search_entry.get()
#         conn = sqlite3.connect(DB_NAME)
#         c = conn.cursor()
#         c.execute("SELECT * FROM returns WHERE return_id = ?", (search_id,))
#         result = c.fetchone()
#         conn.close()

#         table.delete(*table.get_children())
#         if result:
#             table.insert("", "end", values=result[1:])
#         else:
#             messagebox.showerror("Not Found", "Return ID not found.")

#     def search_by_condition():
#         selected_condition = filter_condition_var.get()
#         conn = sqlite3.connect(DB_NAME)
#         c = conn.cursor()
#         c.execute("SELECT * FROM returns WHERE condition = ?", (selected_condition,))
#         results = c.fetchall()
#         conn.close()

#         table.delete(*table.get_children())
#         for row in results:
#             table.insert("", "end", values=row[1:])

#     def show_all_returns():
#         conn = sqlite3.connect(DB_NAME)
#         c = conn.cursor()
#         c.execute("SELECT * FROM returns")
#         results = c.fetchall()
#         conn.close()

#         table.delete(*table.get_children())
#         for row in results:
#             table.insert("", "end", values=row[1:])

#     def clear_form(keep_return_id=False):
#         if not keep_return_id:
#             return_id_var.set("")
#         order_entry.delete(0, tk.END)
#         ram_entry.delete(0, tk.END)
#         ssd_entry.delete(0, tk.END)
#         hdd_entry.delete(0, tk.END)
#         condition_var.set("Good")
#         status_var.set("Pending")
#         comment_entry.delete(0, tk.END)

#     # ==== Variables ====
#     brand_var = tk.StringVar(value="Dell")
#     condition_var = tk.StringVar(value="Good")
#     status_var = tk.StringVar(value="Pending")
#     return_id_var = tk.StringVar()
#     filter_condition_var = tk.StringVar(value="Good")

#     # ==== Treeview Style ====
#     style = ttk.Style()
#     style.configure("Treeview.Heading", font=HEADING_FONT)
#     style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)

#     # ==== Form Frame ====
#     frame_form = ttk.Frame(root)
#     frame_form.pack(padx=10, pady=10, anchor="nw", fill="x")

#     def form_label(row, text):
#         return ttk.Label(frame_form, text=text + ":", font=FONT).grid(row=row, column=0, sticky="w", padx=10, pady=5)

#     form_label(0, "Brand")
#     ttk.Combobox(frame_form, textvariable=brand_var, values=list(brand_codes.keys()), state="readonly", font=FONT).grid(row=0, column=1, padx=10)

#     form_label(0, "Return ID")
#     ttk.Entry(frame_form, textvariable=return_id_var, font=FONT, state="readonly", width=30).grid(row=0, column=3, padx=10)

#     form_label(1, "Order Number")
#     order_entry = ttk.Entry(frame_form, font=FONT, width=30)
#     order_entry.grid(row=1, column=1, padx=10)

#     form_label(1, "RAM")
#     ram_entry = ttk.Entry(frame_form, font=FONT, width=30)
#     ram_entry.grid(row=1, column=3, padx=10)

#     form_label(2, "SSD")
#     ssd_entry = ttk.Entry(frame_form, font=FONT, width=30)
#     ssd_entry.grid(row=2, column=1, padx=10)

#     form_label(2, "HDD")
#     hdd_entry = ttk.Entry(frame_form, font=FONT, width=30)
#     hdd_entry.grid(row=2, column=3, padx=10)

#     form_label(3, "Condition")
#     ttk.Combobox(frame_form, textvariable=condition_var, values=["Like New", "Good", "Fair", "Damaged"], state="readonly", font=FONT).grid(row=3, column=1, padx=10)

#     form_label(3, "Status")
#     ttk.Combobox(frame_form, textvariable=status_var, values=["Pending", "Accepted", "Rejected", "Resolved"], state="readonly", font=FONT).grid(row=3, column=3, padx=10)

#     form_label(4, "Inspector Comment")
#     comment_entry = ttk.Entry(frame_form, font=FONT, width=65)
#     comment_entry.grid(row=4, column=1, columnspan=3, padx=10)

#     # ==== Form Buttons ====
#     ttk.Button(frame_form, text="Add Return", command=save_data).grid(row=5, column=0, padx=10, pady=10)
#     ttk.Button(frame_form, text="Clear Form", command=clear_form).grid(row=5, column=1, padx=10)
#     ttk.Button(frame_form, text="Show All Returns", command=show_all_returns).grid(row=5, column=2, padx=10)

#     # ==== Search Frame ====
#     frame_search = ttk.LabelFrame(root, text="Search")
#     frame_search.pack(fill="x", padx=10, pady=5)

#     ttk.Label(frame_search, text="By Return ID:", font=FONT).grid(row=0, column=0, padx=5, pady=5)
#     search_entry = ttk.Entry(frame_search, font=FONT)
#     search_entry.grid(row=0, column=1, padx=5)
#     ttk.Button(frame_search, text="Search", command=search_by_return_id).grid(row=0, column=2, padx=5)

#     ttk.Label(frame_search, text="By Condition:", font=FONT).grid(row=0, column=3, padx=15)
#     ttk.Combobox(frame_search, textvariable=filter_condition_var, values=["Like New", "Good", "Fair", "Damaged"], state="readonly", font=FONT).grid(row=0, column=4)
#     ttk.Button(frame_search, text="Filter", command=search_by_condition).grid(row=0, column=5, padx=5)
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



