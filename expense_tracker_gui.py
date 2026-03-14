# Expense Tracker GUI (File Based - No Database)
# Uses: tkinter, messagebox, csv, datetime

import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import datetime

FILE_NAME = "expenses.csv"

class ExpenseTracker:

    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("500x450")

        # Labels
        tk.Label(root, text="Date (YYYY-MM-DD)").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(root, text="Category").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(root, text="Amount").grid(row=2, column=0, padx=10, pady=10)

        # Entry fields
        self.date_entry = tk.Entry(root)
        self.category_entry = tk.Entry(root)
        self.amount_entry = tk.Entry(root)

        self.date_entry.grid(row=0, column=1)
        self.category_entry.grid(row=1, column=1)
        self.amount_entry.grid(row=2, column=1)

        # Buttons
        tk.Button(root, text="Add Expense", command=self.add_expense).grid(row=3, column=0, pady=10)
        tk.Button(root, text="View Expenses", command=self.view_expenses).grid(row=3, column=1)
        tk.Button(root, text="Total Expense", command=self.total_expense).grid(row=4, column=0)

        # Listbox to display data
        self.listbox = tk.Listbox(root, width=60)
        self.listbox.grid(row=5, column=0, columnspan=2, pady=20)

        # Load data when program starts
        self.load_data()


    def add_expense(self):
        date = self.date_entry.get()
        category = self.category_entry.get()
        amount = self.amount_entry.get()

        if date == "" or category == "" or amount == "":
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            float(amount)
        except:
            messagebox.showerror("Error", "Amount must be a number")
            return

        with open(FILE_NAME, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([date, category, amount])

        messagebox.showinfo("Success", "Expense Added")

        self.date_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

        self.view_expenses()


    def view_expenses(self):
        self.listbox.delete(0, tk.END)

        if not os.path.exists(FILE_NAME):
            return

        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                self.listbox.insert(tk.END, f"Date: {row[0]} | Category: {row[1]} | Amount: {row[2]}")


    def total_expense(self):
        total = 0

        if not os.path.exists(FILE_NAME):
            messagebox.showinfo("Total", "No expenses recorded")
            return

        with open(FILE_NAME, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                total += float(row[2])

        messagebox.showinfo("Total Expense", f"Total Expense = {total}")


    def load_data(self):
        if not os.path.exists(FILE_NAME):
            with open(FILE_NAME, "w", newline="") as file:
                pass
        self.view_expenses()


root = tk.Tk()
app = ExpenseTracker(root)
root.mainloop()
