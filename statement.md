## Problem Statement
I noticed that a lot of small local shops still use notebooks or loose paper to write down their stock and sales. This is risky because pages can get lost, and it's easy to make math mistakes when calculating bills in a rush. They need a digital way to handle this that is free and doesn't require the internet.

## Scope of the Project
I built this desktop application to solve that problem. It helps a shopkeeper move from paper to a computer.
Specifically, the project handles:
1.  **Storing Data:** Keeping a digital list of all products and their prices.
2.  **Calculations:** Automatically doing the math for sales so there are no errors.
3.  **Records:** Saving a history of every sale made, which is hard to maintain.

## Target Users
* **Shop Owners:** Who need to see what items are low in quantity and check past sales made.
* **Cashiers:** Who can bill items without using calculators.

## High-Level Features
* **Login Protection:** You have to sign in with a username and password to access the billing system.
* **Stock Management:** Used to add new items or delete old ones.
* **Billing System:** You can just select the item and quantity, and it can calculate the total.
* **History Record:** A table that shows exactly when the item was sold by showing Date and Time.
* **Offline Database:** It uses a local file (`.db`) so it works on any computer without Wi-Fi.
