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
