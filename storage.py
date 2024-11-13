# storage.py

import json
import os

DATA_FILE = "expenses.json"

# Load all groups from the data file if it exists
def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}

# Save all groups to the data file
def save_expenses(expenses):
    with open(DATA_FILE, "w") as file:
        json.dump(expenses, file)

# Add or update an expense for a person within a specific group
def add_expense(expenses, group_name, name, amount):
    if group_name not in expenses:
        expenses[group_name] = {}
    if name in expenses[group_name]:
        expenses[group_name][name] += amount
    else:
        expenses[group_name][name] = amount

# Update a specific expense in a group
def update_expense(expenses, group_name, name, amount):
    if group_name in expenses and name in expenses[group_name]:
        expenses[group_name][name] = amount
        print(f"Updated {name}'s expense to ${amount:.2f} in group '{group_name}'.")
    else:
        print(f"No expense found for {name} in group '{group_name}'.")

# Delete an expense for a person in a group
def delete_expense(expenses, group_name, name):
    if group_name in expenses and name in expenses[group_name]:
        del expenses[group_name][name]
        print(f"Deleted expense for {name} in group '{group_name}'.")
    else:
        print(f"No expense found for {name} in group '{group_name}'.")

# Delete an entire group
def delete_group(expenses, group_name):
    if group_name in expenses:
        del expenses[group_name]
        print(f"Deleted group '{group_name}'.")
    else:
        print(f"No group found with the name '{group_name}'.")

# Retrieve a specific group's expenses
def get_group(expenses, group_name):
    return expenses.get(group_name, {})
