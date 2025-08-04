import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from return_tracking.ui import LaptopReturnTrackerUI

class RestockTrackerUI:
    def __init__(self, root, callbacks):
        self.root = root
        self.callbacks = callbacks
        self.build_ui()

    def build_ui(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        title = tk.Label(frame, text="Restock Paperwork Tracker", font=("Segoe UI", 16, "bold"))
        title.pack(pady=10)

        form = tk.Frame(frame)
        form.pack(pady=10)

        tk.Label(form, text="Order Number:").grid(row=0, column=0, sticky="e")
        self.order_entry = tk.Entry(form)
        self.order_entry.grid(row=0, column=1, padx=5)

        tk.Label(form, text="Status:").grid(row=1, column=0, sticky="e")
        self.status_var = tk.StringVar()
        self.status_combo = ttk.Combobox(form, textvariable=self.status_var, values=["Paperwork Sent", "Item Received", "Item Dispatched"], state="readonly")
        self.status_combo.grid(row=1, column=1, padx=5)

        button_frame = tk.Frame(frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Save", command=self.callbacks['save']).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Reset", command=self.callbacks['reset']).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete", command=self.callbacks['delete']).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Back", command=self.callbacks['back']).pack(side="left", padx=5)

        search_frame = tk.Frame(frame)
        search_frame.pack(pady=5)

        tk.Label(search_frame, text="Search Order:").pack(side="left")
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side="left", padx=5)
        ttk.Button(search_frame, text="Search", command=self.callbacks['search']).pack(side="left", padx=5)

        self.tree = ttk.Treeview(frame, columns=("Order No", "Status"), show="headings")
        self.tree.heading("Order No", text="Order No")
        self.tree.heading("Status", text="Status")
        self.tree.pack(fill="both", expand=True, pady=10)

    def get_order_info(self):
        return self.order_entry.get().strip(), self.status_var.get().strip()

    def set_order_info(self, order, status):
        self.order_entry.delete(0, tk.END)
        self.order_entry.insert(0, order)
        self.status_var.set(status)

    def clear_fields(self):
        self.order_entry.delete(0, tk.END)
        self.status_var.set("")

    def get_search_text(self):
        return self.search_entry.get().strip()

    def fill_table(self, rows):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in rows:
            self.tree.insert("", "end", values=row)

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Return & Restock Tracker")
        self.root.geometry("900x600")

        self.conn = sqlite3.connect("returns.db")
        self.init_db()
        self.menu_screen()

    def init_db(self):
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS restock (
                order_no TEXT PRIMARY KEY,
                status TEXT
            )
        ''')
        self.conn.commit()

    def menu_screen(self):
        self.clear_window()

        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="Select an Option", font=("Segoe UI", 16)).pack(pady=20)

        tk.Button(frame, text="Return Tracking System", width=30, height=2,
                  command=self.show_return_tracker).pack(pady=10)

        tk.Button(frame, text="You are gay!", width=30, height=2,
                  command=self.show_restock_tracker).pack(pady=10)

    def show_return_tracker(self):
     self.clear_window()
     self.return_ui = LaptopReturnTrackerUI(self.root, {
        'back': self.menu_screen,
        'show_form': lambda: None,
        'show_table': lambda: None,
        'save': lambda *args, **kwargs: None,
        'reset': lambda: None,
        'search': lambda *args, **kwargs: None,
        'filter': lambda: None
    })


    def show_restock_tracker(self):
        self.clear_window()
        self.restock_ui = RestockTrackerUI(self.root, {
            'save': self.save_restock,
            'reset': self.reset_restock,
            'search': self.search_restock,
            'delete': self.delete_restock,
            'back': self.menu_screen
        })
        self.refresh_restock_table()
        self.restock_ui.tree.bind("<Double-1>", self.load_restock_entry)

    def save_restock(self):
        order, status = self.restock_ui.get_order_info()
        if not order or not status:
            messagebox.showwarning("Missing Info", "Order Number and Status are required.")
            return

        c = self.conn.cursor()
        c.execute("SELECT * FROM restock WHERE order_no = ?", (order,))
        existing = c.fetchone()

        if existing:
            update = messagebox.askyesno("Update?", f"Order {order} exists. Update status?")
            if update:
                c.execute("UPDATE restock SET status = ? WHERE order_no = ?", (status, order))
        else:
            c.execute("INSERT INTO restock (order_no, status) VALUES (?, ?)", (order, status))

        self.conn.commit()
        self.refresh_restock_table()
        self.restock_ui.clear_fields()

    def delete_restock(self):
        order, _ = self.restock_ui.get_order_info()
        if not order:
            messagebox.showwarning("Missing Info", "Select or enter Order Number to delete.")
            return

        confirm = messagebox.askyesno("Delete Confirmation", f"Delete order {order}?")
        if confirm:
            c = self.conn.cursor()
            c.execute("DELETE FROM restock WHERE order_no = ?", (order,))
            self.conn.commit()
            self.refresh_restock_table()
            self.restock_ui.clear_fields()

    def search_restock(self):
        keyword = self.restock_ui.get_search_text()
        c = self.conn.cursor()
        c.execute("SELECT order_no, status FROM restock WHERE order_no LIKE ?", (f"%{keyword}%",))
        rows = c.fetchall()
        self.restock_ui.fill_table(rows)

    def refresh_restock_table(self):
        c = self.conn.cursor()
        c.execute("SELECT order_no, status FROM restock")
        rows = c.fetchall()
        self.restock_ui.fill_table(rows)

    def load_restock_entry(self, event):
        selected = self.restock_ui.tree.selection()
        if selected:
            values = self.restock_ui.tree.item(selected[0], 'values')
            self.restock_ui.set_order_info(values[0], values[1])

    def reset_restock(self):
        self.restock_ui.clear_fields()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
