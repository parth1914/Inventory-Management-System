import tkinter as tk
from tkinter import messagebox
import sqlite3

class LoginWindow:
    def __init__(self, root, db, on_login_success):
        self.root = root
        self.db = db
        self.on_login_success = on_login_success

        self.root.title("Inventory System - Login")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.create_ui()

    def create_ui(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (300 // 2)
        self.root.geometry(f'400x300+{x}+{y}')

        tk.Label(self.root, text="Inventory Management System", font=("Arial", 16, "bold"), fg="black").pack(pady=20)

        login_frame = tk.Frame(self.root)
        login_frame.pack(pady=20)

        tk.Label(login_frame, text="Username:", font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=10)
        self.user_entry = tk.Entry(login_frame, font=("Arial", 11), width=20)
        self.user_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(login_frame, text="Password:", font=("Arial", 11)).grid(row=1, column=0, padx=10, pady=10)
        self.pass_entry = tk.Entry(login_frame, show="*", font=("Arial", 11), width=20)
        self.pass_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Login", command=self.login_action, font=("Arial", 12, "bold"), bg="olive",
                  fg="white", width=15).pack(pady=20)
        tk.Label(self.root, text="Default: admin / qwe123", font=("Arial", 10, "bold"), fg="gray").pack()

    def login_action(self):
        u = self.user_entry.get().strip()
        p = self.pass_entry.get().strip()

        conn = self.db.get_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SELECT id, username, role FROM users WHERE username=? AND password=?", (u, p))
                user = cur.fetchone()
                conn.close()

                if user:
                    messagebox.showinfo("Success", f"Welcome, {user[1]}!")
                    self.on_login_success(user[0], user[1], user[2])
                else:
                    messagebox.showerror("Error", "Invalid Login")
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"DB Error: {e}")
