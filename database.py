import sqlite3
from tkinter import messagebox


class Database:
    def __init__(self):
        self.db_name = 'inventory_system.db'
        self.create_tables()

    def get_connection(self):
        try:
            # Connect to the file
            conn = sqlite3.connect(self.db_name)
            conn.execute("PRAGMA foreign_keys = ON")
            return conn
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Cannot connect to database: {e}")
            return None

    def create_tables(self):
        try:
            conn = self.get_connection()
            if conn is None: return
            cur = conn.cursor()

            # Create Tables
            cur.execute("""CREATE TABLE IF NOT EXISTS users (        
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'cashier'
            )""")

            cur.execute("""CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER NOT NULL,
                reorder_level INTEGER DEFAULT 10,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""")

            cur.execute("""CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                total REAL NOT NULL,
                sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )""")

            # Create Admin
            cur.execute("SELECT * FROM users WHERE username=?", ('admin',))
            if not cur.fetchone():
                cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                            ('admin', 'qwe123', 'admin'))
                conn.commit()

            conn.close()

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error creating tables: {e}")
