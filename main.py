import tkinter as tk
from database import Database
from login import LoginWindow
from dashboard import DashboardWindow

if __name__ == "__main__":
    # Initialize the database
    db = Database()

    # Initialize the main window
    root = tk.Tk()


    # Function to handle what happens when login is successful
    def show_dashboard(uid, uname, role):
        # Clear the login screen
        for w in root.winfo_children():
            w.destroy()
        # Open the dashboard
        DashboardWindow(root, db, uid, uname, role)


    # Start with the Login Window
    LoginWindow(root, db, show_dashboard)

    # Run the app
    root.mainloop()
