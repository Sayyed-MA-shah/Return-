import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_NAME = "return_data.db"

from ui import launch_app
import sqlite3

def init_db():
    conn = sqlite3.connect("return_data.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS returns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            return_id TEXT UNIQUE,
            brand TEXT,
            order_number TEXT,
            ram TEXT,
            ssd TEXT,
            hdd TEXT,
            condition TEXT,
            status TEXT,
            inspector_comment TEXT
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    launch_app()

# === ID Generator ===
def generate_return_id(brand_code):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM returns WHERE return_id LIKE ?", (brand_code + '%',))
    count = c.fetchone()[0] + 1
    conn.close()
    return f"{brand_code}-{count:03d}"

# === Save Record ===
def save_data():
    brand = brand_var.get()
    brand_code = brand_codes.get(brand, "XX")
    return_id = generate_return_id(brand_code)
    order_number = order_entry.get()
    ram = ram_entry.get()
    ssd = ssd_entry.get()
    hdd = hdd_entry.get()
    condition = condition_var.get()
    status = status_var.get()
    inspector_comment = comment_entry.get()

    if not order_number:
        messagebox.showwarning("Missing Data", "Order number is required.")
        return

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO returns (return_id, brand, order_number, ram, ssd, hdd, condition, status, inspector_comment)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (return_id, brand, order_number, ram, ssd, hdd, condition, status, inspector_comment))
        conn.commit()
        return_id_var.set(return_id)
        messagebox.showinfo("Success", f"Return added with ID: {return_id}")
        clear_form(keep_return_id=True)
        show_all_returns()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Duplicate return ID.")
    finally:
        conn.close()

# === Search By Return ID ===
def search_by_return_id():
    search_id = search_entry.get()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM returns WHERE return_id = ?", (search_id,))
    result = c.fetchone()
    conn.close()

    table.delete(*table.get_children())
    if result:
        table.insert("", "end", values=result[1:])
    else:
        messagebox.showerror("Not Found", "Return ID not found.")

# === Search By Condition ===
def search_by_condition():
    selected_condition = filter_condition_var.get()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM returns WHERE condition = ?", (selected_condition,))
    results = c.fetchall()
    conn.close()

    table.delete(*table.get_children())
    for row in results:
        table.insert("", "end", values=row[1:])

# === Show All ===
def show_all_returns():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM returns")
    results = c.fetchall()
    conn.close()

    table.delete(*table.get_children())
    for row in results:
        table.insert("", "end", values=row[1:])

# === Clear Form ===
def clear_form(keep_return_id=False):
    if not keep_return_id:
        return_id_var.set("")
    order_entry.delete(0, tk.END)
    ram_entry.delete(0, tk.END)
    ssd_entry.delete(0, tk.END)
    hdd_entry.delete(0, tk.END)
    condition_var.set("Good")
    status_var.set("Pending")
    comment_entry.delete(0, tk.END)

# === GUI ===
init_db()
root = tk.Tk()
root.title("Laptop Return Tracker")
root.geometry("1000x600")

brand_codes = {"Dell": "DR", "HP": "HR", "Lenovo": "LR"}

# === Form Section ===
frame_form = ttk.Frame(root)
frame_form.pack(padx=10, pady=10, anchor="nw")

brand_var = tk.StringVar(value="Dell")
condition_var = tk.StringVar(value="Good")
status_var = tk.StringVar(value="Pending")
return_id_var = tk.StringVar()

ttk.Label(frame_form, text="Brand:").grid(row=0, column=0, sticky="w")
ttk.Combobox(frame_form, textvariable=brand_var, values=list(brand_codes.keys()), state="readonly").grid(row=0, column=1)

ttk.Label(frame_form, text="Return ID:").grid(row=0, column=2, sticky="w", padx=(20, 0))
ttk.Entry(frame_form, textvariable=return_id_var, state="readonly").grid(row=0, column=3)

ttk.Label(frame_form, text="Order Number:").grid(row=1, column=0, sticky="w")
order_entry = ttk.Entry(frame_form)
order_entry.grid(row=1, column=1)

ttk.Label(frame_form, text="RAM:").grid(row=1, column=2, sticky="w", padx=(20, 0))
ram_entry = ttk.Entry(frame_form)
ram_entry.grid(row=1, column=3)

ttk.Label(frame_form, text="SSD:").grid(row=2, column=0, sticky="w")
ssd_entry = ttk.Entry(frame_form)
ssd_entry.grid(row=2, column=1)

ttk.Label(frame_form, text="HDD:").grid(row=2, column=2, sticky="w", padx=(20, 0))
hdd_entry = ttk.Entry(frame_form)
hdd_entry.grid(row=2, column=3)

ttk.Label(frame_form, text="Condition:").grid(row=3, column=0, sticky="w")
ttk.Combobox(frame_form, textvariable=condition_var, values=["Like New", "Good", "Fair", "Damaged"], state="readonly").grid(row=3, column=1)

ttk.Label(frame_form, text="Status:").grid(row=3, column=2, sticky="w", padx=(20, 0))
ttk.Combobox(frame_form, textvariable=status_var, values=["Pending", "Accepted", "Rejected", "Resolved"], state="readonly").grid(row=3, column=3)

ttk.Label(frame_form, text="Inspector Comment:").grid(row=4, column=0, sticky="w")
comment_entry = ttk.Entry(frame_form, width=60)
comment_entry.grid(row=4, column=1, columnspan=3, sticky="ew")

# Buttons
ttk.Button(frame_form, text="Add Return", command=save_data).grid(row=5, column=0, pady=10)
ttk.Button(frame_form, text="Clear Form", command=clear_form).grid(row=5, column=1)
ttk.Button(frame_form, text="Show All Returns", command=show_all_returns).grid(row=5, column=2)

# === Search Section ===
frame_search = ttk.LabelFrame(root, text="Search")
frame_search.pack(padx=10, pady=5, fill="x")

ttk.Label(frame_search, text="By Return ID:").grid(row=0, column=0, padx=5, pady=5)
search_entry = ttk.Entry(frame_search)
search_entry.grid(row=0, column=1, padx=5)
ttk.Button(frame_search, text="Search", command=search_by_return_id).grid(row=0, column=2, padx=5)

ttk.Label(frame_search, text="By Condition:").grid(row=0, column=3, padx=15)
filter_condition_var = tk.StringVar(value="Good")
ttk.Combobox(frame_search, textvariable=filter_condition_var, values=["Like New", "Good", "Fair", "Damaged"], state="readonly").grid(row=0, column=4)
ttk.Button(frame_search, text="Filter", command=search_by_condition).grid(row=0, column=5, padx=5)

# === Table Section ===
table = ttk.Treeview(root, columns=("return_id", "brand", "order_number", "ram", "ssd", "hdd", "condition", "status", "comment"), show="headings", height=12)
for col in table["columns"]:
    table.heading(col, text=col.replace("_", " ").title())
    table.column(col, width=110, anchor="center")
table.pack(padx=10, pady=10, fill="both", expand=True)

# Start with all data
show_all_returns()

root.mainloop()

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
