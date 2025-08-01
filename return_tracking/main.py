import tkinter as tk
from tkinter import messagebox
import sqlite3
from ui import LaptopReturnTrackerUI


class ReturnApp:
    def __init__(self):
        self.root = tk.Tk()
        self.ui = LaptopReturnTrackerUI(self.root, {
            'save': self.save_return,
            'reset': self.reset_form,
            'search': self.search_by_id,
            'filter': self.filter_by_condition,
            'row_click': self.row_click,
            'show_form': self.ui_show_form,
            'show_table': self.ui_show_table,
            'quick_search': self.quick_search,
            'delete': self.delete
        })

        self.setup_database()
        self.refresh_table()

    def setup_database(self):
        self.conn = sqlite3.connect("returns.db")
        self.c = self.conn.cursor()
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS returns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                return_id TEXT,
                brand TEXT,
                order_number TEXT,
                ram INTEGER,
                ssd INTEGER,
                hdd INTEGER,
                condition TEXT,
                status TEXT,
                inspector_comment TEXT
            )
        ''')
        self.conn.commit()

    def generate_return_id(self, brand):
        prefix = brand[0].upper() + "R"
        self.c.execute("SELECT COUNT(*) FROM returns WHERE brand = ?", (brand,))
        count = self.c.fetchone()[0] + 1
        return f"{prefix}-{str(count).zfill(3)}"

    def save_return(self):
        brand = self.ui.brand_cb.get()
        order = self.ui.order_entry.get()
        ram = self.ui.ram_entry.get()
        ssd = self.ui.ssd_entry.get()
        hdd = self.ui.hdd_entry.get()
        cond = self.ui.condition_cb.get()
        stat = self.ui.status_cb.get()
        notes = self.ui.notes_text.get("1.0", tk.END).strip()

        if not brand or not order:
            messagebox.showwarning("Missing Info", "Brand and Order Number are required.")
            return

        return_id = self.generate_return_id(brand)

        self.c.execute("""
            INSERT INTO returns (return_id, brand, order_number, ram, ssd, hdd, condition, status, inspector_comment)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (return_id, brand, order, ram, ssd, hdd, cond, stat, notes))
        self.conn.commit()

        messagebox.showinfo("Saved", f"Return {return_id} saved successfully.")
        self.reset_form()
        self.refresh_table()
    

    def reset_form(self):
        self.ui.brand_cb.set("")
        self.ui.order_entry.delete(0, tk.END)
        self.ui.ram_entry.delete(0, tk.END)
        self.ui.ssd_entry.delete(0, tk.END)
        self.ui.hdd_entry.delete(0, tk.END)
        self.ui.condition_cb.set("")
        self.ui.status_cb.set("")
        self.ui.notes_text.delete("1.0", tk.END)

    def refresh_table(self, condition_filter=None):
        for row in self.ui.tree.get_children():
            self.ui.tree.delete(row)

        query = "SELECT return_id, brand, order_number, ram, ssd, hdd, condition, status, inspector_comment FROM returns"
        params = ()
        if condition_filter and condition_filter != "All":
            query += " WHERE condition = ?"
            params = (condition_filter,)

        for row in self.c.execute(query, params):
            self.ui.tree.insert("", tk.END, values=row)

    def delete(self):
        selected = self.ui.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a return to delete.")
            return

        return_id = self.ui.tree.item(selected[0], 'values')[0]
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete return {return_id}?")
        if confirm:
            self.c.execute("DELETE FROM returns WHERE return_id = ?", (return_id,))
            self.conn.commit()
            self.refresh_table()
            messagebox.showinfo("Deleted", f"Return {return_id} deleted successfully.")

    def search_by_id(self):
        return_id = self.ui.search_id_entry.get()
        if not return_id:
            return
        self.ui.tree.delete(*self.ui.tree.get_children())
        for row in self.c.execute("SELECT return_id, brand, order_number, ram, ssd, hdd, condition, status, inspector_comment FROM returns WHERE return_id = ?", (return_id,)):
            self.ui.tree.insert("", tk.END, values=row)

    def filter_by_condition(self):
        selected = self.ui.filter_condition_cb.get()
        self.refresh_table(condition_filter=selected)

    def quick_search(self):
        return_id = self.ui.quick_search_entry.get()
        self.ui_show_table()
        self.ui.tree.delete(*self.ui.tree.get_children())
        for row in self.c.execute("SELECT return_id, brand, order_number, ram, ssd, hdd, condition, status, inspector_comment FROM returns WHERE return_id = ?", (return_id,)):
            self.ui.tree.insert("", tk.END, values=row)

    def row_click(self, event):
        selected = self.ui.tree.focus()
        if not selected:
            return
        values = self.ui.tree.item(selected)['values']
        self.ui_show_form()

        self.ui.brand_cb.set(values[1])
        self.ui.order_entry.delete(0, tk.END)
        self.ui.order_entry.insert(0, values[2])
        self.ui.ram_entry.delete(0, tk.END)
        self.ui.ram_entry.insert(0, values[3])
        self.ui.ssd_entry.delete(0, tk.END)
        self.ui.ssd_entry.insert(0, values[4])
        self.ui.hdd_entry.delete(0, tk.END)
        self.ui.hdd_entry.insert(0, values[5])
        self.ui.condition_cb.set(values[6])
        self.ui.status_cb.set(values[7])
        self.ui.notes_text.delete("1.0", tk.END)
        self.ui.notes_text.insert("1.0", values[8])

    def ui_show_form(self):
        self.ui.show_form()

    def ui_show_table(self):
        self.ui.show_table()
        self.refresh_table()

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = ReturnApp()
    app.run()
