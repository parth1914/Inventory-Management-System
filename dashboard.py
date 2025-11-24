import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3

class DashboardWindow:
    def __init__(self, root, db, user_id, username, role):
        self.root = root
        self.db = db
        self.user_id = user_id

        self.root.title(f"Inventory Dashboard - {username} ({role})")
        self.root.geometry("1000x600")

        self.create_ui()
        self.load_data()

    def create_ui(self):
        top_frame = tk.Frame(self.root, pady=10)
        top_frame.pack(fill=tk.X)

        tk.Label(top_frame, text="Add New Product", font=("Arial", 12, "bold")).pack()

        input_frame = tk.Frame(top_frame)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Name:").grid(row=0, column=0, padx=5)
        self.ent_name = tk.Entry(input_frame, width=20)
        self.ent_name.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Price:").grid(row=0, column=2, padx=5)
        self.ent_price = tk.Entry(input_frame, width=10)
        self.ent_price.grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Stock:").grid(row=0, column=4, padx=5)
        self.ent_stock = tk.Entry(input_frame, width=10)
        self.ent_stock.grid(row=0, column=5, padx=5)

        tk.Label(input_frame, text="Reorder:").grid(row=0, column=6, padx=5)
        self.ent_reorder = tk.Entry(input_frame, width=10)
        self.ent_reorder.insert(0, "10")
        self.ent_reorder.grid(row=0, column=7, padx=5)

        tk.Button(input_frame, text="Add Product", command=self.add_product, bg="green", fg="white",
                  font=("Arial", 10, "bold")).grid(row=0, column=8, padx=10)

        middle_frame = tk.Frame(self.root)
        middle_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(middle_frame, text="Product Inventory", font=("Arial", 12, "bold")).pack(anchor="w")

        tree_frame = tk.Frame(middle_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        scrollbar = tk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(tree_frame, columns=("id", "name", "price", "stock", "reorder"),
                                 show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)

        cols = ["id", "name", "price", "stock", "reorder"]
        headings = ["ID", "Product Name", "Price", "Stock", "Reorder Level"]
        for col, h in zip(cols, headings):
            self.tree.heading(col, text=h)
            self.tree.column(col, width=100)
        self.tree.column("name", width=250)
        self.tree.pack(fill=tk.BOTH, expand=True)

        bottom_frame = tk.Frame(self.root, pady=10)
        bottom_frame.pack(fill=tk.X)

        btn_frame = tk.Frame(bottom_frame)
        btn_frame.pack()

        tk.Button(btn_frame, text="Sell Selected", command=self.sell_item, bg="lightblue", fg="white",
                  font=("Arial", 11, "bold"), width=20).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Delete Product", command=self.delete_product, bg="orange", fg="white",
                  font=("Arial", 11, "bold"), width=15).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="View Sales History", command=self.view_sales, bg="purple", fg="white",
                  font=("Arial", 11, "bold"), width=20).grid(row=0, column=2, padx=10)
        tk.Button(btn_frame, text="Refresh", command=self.load_data, bg="grey", fg="white",
                  font=("Arial", 11, "bold"), width=10).grid(row=0, column=3, padx=10)

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = self.db.get_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SELECT id, name, price, stock, reorder_level FROM products ORDER BY id")
                rows = cur.fetchall()

                for row in rows:
                    pid, name, price, stock, reorder = row
                    self.tree.insert("", tk.END, values=(pid, name, f"{price:.2f}", stock, reorder))
            finally:
                conn.close()

    def add_product(self):
        try:
            n = self.ent_name.get().strip()
            p = float(self.ent_price.get())
            s = int(self.ent_stock.get())
            r = int(self.ent_reorder.get())

            if not n:
                messagebox.showerror("Error", "Name required")
                return

            conn = self.db.get_connection()
            if conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO products (name, price, stock, reorder_level) VALUES (?, ?, ?, ?)",
                            (n, p, s, r))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Product Added")
                self.load_data()
                self.ent_name.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Price/Stock must be numbers")

    def sell_item(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select product first")
            return

        item = self.tree.item(sel)['values']

        try:
            pid = item[0]
            name = item[1]
            price = float(str(item[2]).replace(',', ''))
            stock = int(item[3])
        except:
            messagebox.showerror("Error", "Error reading row data")
            return

        if stock <= 0:
            messagebox.showerror("Error", "Out of Stock")
            return

        qty_win = tk.Toplevel(self.root)
        qty_win.title("Qty")
        qty_win.geometry("250x150")

        tk.Label(qty_win, text=f"Sell {name}").pack(pady=10)
        tk.Label(qty_win, text="Quantity:").pack()
        qty_ent = tk.Entry(qty_win)
        qty_ent.pack()

        def confirm_sale():
            try:
                q = int(qty_ent.get())
                if q <= 0 or q > stock:
                    messagebox.showerror("Error", "Invalid Quantity")
                    return

                total = price * q
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                conn = self.db.get_connection()
                if conn:
                    cur = conn.cursor()
                    cur.execute("UPDATE products SET stock=? WHERE id=?", (stock - q, pid))
                    cur.execute(
                        "INSERT INTO sales (product_name, quantity, unit_price, total, user_id,sale_date) VALUES (?, ?, ?, ?, ?, ?)",
                        (name, q, price, total, self.user_id, current_time))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Sold", f"Total: {total}")
                    self.load_data()
                    qty_win.destroy()
            except ValueError:
                messagebox.showerror("Error", "Number required")

        tk.Button(qty_win, text="Confirm", command=confirm_sale, bg="green", fg="white").pack(pady=10)

    def delete_product(self):
        sel = self.tree.selection()
        if sel and messagebox.askyesno("Delete", "Are you sure?"):
            pid = self.tree.item(sel)['values'][0]
            conn = self.db.get_connection()
            if conn:
                conn.cursor().execute("DELETE FROM products WHERE id=?", (pid,))
                conn.commit()
                conn.close()
                self.load_data()

    def view_sales(self):
        win = tk.Toplevel(self.root)
        win.title("Sales History")
        win.geometry("600x400")

        tree = ttk.Treeview(win, columns=("id", "name", "qty", "total", "date"), show="headings")
        for c in ["id", "name", "qty", "total", "date"]:
            tree.heading(c, text=c.upper())
            tree.column(c, width=100)
        tree.pack(fill=tk.BOTH, expand=True)

        conn = self.db.get_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT id, product_name, quantity, total, sale_date FROM sales ORDER BY sale_date DESC")
            for row in cur.fetchall(): tree.insert("", tk.END, values=row)
            conn.close()
