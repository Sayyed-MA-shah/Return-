import tkinter as tk
from restock_ui import RestockTrackerUI
import sqlite3
from tkinter import messagebox

class RestockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Restock Paperwork Tracker")
        self.root.geometry("700x500")

        self.ui = RestockTrackerUI(self.root, {
            'save': self.save,
            'reset': self.reset,
            'search': self.search,
            'delete': self.delete,
            'back': lambda: None
        })

        self.conn = self.init_db()
        self.refresh_table()
        self.ui.tree.bind("<Double-1>", self.load_selected)
    
    def init_db(self):
        conn = sqlite3.connect("returns.db")
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS restock (
                order_no TEXT PRIMARY KEY,
                status TEXT
            )
        ''')
        conn.commit()
        return conn

    def save(self):
        order_no, status = self.ui.get_order_info()
        if not order_no or not status:
            messagebox.showwarning("Missing Info", "Order Number and Status are required.")
            return

        c = self.conn.cursor()
        c.execute("SELECT * FROM restock WHERE order_no = ?", (order_no,))
        if c.fetchone():
            update = messagebox.askyesno("Update?", f"Order '{order_no}' exists. Update status?")
            if update:
                c.execute("UPDATE restock SET status = ? WHERE order_no = ?", (status, order_no))
        else:
            c.execute("INSERT INTO restock (order_no, status) VALUES (?, ?)", (order_no, status))

        self.conn.commit()
        self.refresh_table()
        self.ui.clear_fields()

    def delete(self):
        order_no, _ = self.ui.get_order_info()
        if not order_no:
            messagebox.showwarning("Missing Info", "Enter or select an order to delete.")
            return

        confirm = messagebox.askyesno("Confirm", f"Delete order '{order_no}'?")
        if confirm:
            c = self.conn.cursor()
            c.execute("DELETE FROM restock WHERE order_no = ?", (order_no,))
            self.conn.commit()
            self.refresh_table()
            self.ui.clear_fields()

    def search(self):
        keyword = self.ui.get_search_text()
        c = self.conn.cursor()
        c.execute("SELECT order_no, status FROM restock WHERE order_no LIKE ?", (f"%{keyword}%",))
        rows = c.fetchall()
        self.ui.fill_table(rows)

    def reset(self):
        self.ui.clear_fields()
    
    def refresh_table(self):
        c = self.conn.cursor()
        c.execute("SELECT order_no, status FROM restock")
        rows = c.fetchall()
        self.ui.fill_table(rows)

    def load_selected(self, event):
        selected = self.ui.tree.selection()
        if selected:
            values = self.ui.tree.item(selected[0], 'values')
            self.ui.set_order_info(values[0], values[1])

if __name__ == "__main__":
    root = tk.Tk()
    app = RestockApp(root)
    root.mainloop()
