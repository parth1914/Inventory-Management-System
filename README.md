# Inventory Management System

## Overview of the Project
I created this project to help manage shop inventory easily without relying on paper records. It is a simple desktop application that lets users add products, process sales, and view transaction history. The app runs entirely offline and saves data automatically to a local database, making it lightweight and easy to use.

## Features
* **Login System:** Separate access for Admins and Cashiers to ensure security.
* **Inventory Management:** Add new products, check current stock levels, and delete old items.
* **Billing & Sales:** Automatically calculates total costs and deducts quantity from stock immediately.
* **Sales History:** Keeps a permanent log of every sale with the exact date and time.
* **Auto-Save:** All data is saved instantly to the local `inventory_system.db` file.

## Technologies/Tools Used
* **Python:** The core programming language for the logic.
* **Tkinter:** Standard Python library used for the Graphical User Interface (GUI).
* **SQLite:** A serverless database used to store user and product data.
* **PyInstaller:** The tool used to compile the Python script into a standalone `.exe` file.

## Steps to Install & Run the Project
You do not need to install Python to run this application.

1.  **Download the Files:** Download `invtmgmtsys.exe` and `inventory_system.db` from this repository.
2.  **Keep them together:** Place both files in the same folder (e.g., a folder on your Desktop).
3.  **Run:** Double-click `invtmgmtsys.exe`.
    * *Note: If Windows shows a "Protected your PC" warning, click "More Info" -> "Run Anyway".* *

## Instructions for Testing
Follow these steps to verify the project works:
1.  **Login:** Use Username: `admin` and Password: `qwe123`.
2.  **Add Stock:** Go to the "Add New Product" section. Enter Name: `Test Pen`, Price: `10`, Stock: `50`. Click "Add Product".
3.  **Sell Stock:** Select `Test Pen` from the list. Click "Sell Selected". Enter Quantity `5` and confirm.
4.  **Verify:** Check that the stock count dropped to `45`. Then, click "View Sales History" to see the transaction log.

## How to Reset the App
If you want to clear all data and start fresh:
1. Close the application.
2. Delete the `inventory_system.db` file.
3. Run the app again. It will automatically create a brand new database.

## Screenshots
*(Please see the "Screenshots" folder in this repository for visual references of the Login Screen, Dashboard, and Sales History)*
  
