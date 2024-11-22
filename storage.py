import json
import os


def load_expenses():
    """Loads expenses from the JSON file."""
    if os.path.exists("expenses.json"):
        with open("expenses.json", "r") as file:
            return json.load(file)
    return {}


def save_expenses(expenses):
    """Saves expenses to the JSON file."""
    with open("expenses.json", "w") as file:
        json.dump(expenses, file, indent=4)


def add_expense_item(expenses, group_name, person, description, amount):
    """Adds an expense item for a specific person in the group."""
    if group_name not in expenses:
        expenses[group_name] = {"members": [], "expenses": {}}

    if person not in expenses[group_name]["expenses"]:
        expenses[group_name]["expenses"][person] = []

    expenses[group_name]["expenses"][person].append({"description": description, "amount": amount})
    save_expenses(expenses)


def delete_expense_item(expenses, group_name, person, index):
    """Deletes a specific expense item for a person in the group."""
    if group_name in expenses and person in expenses[group_name]["expenses"]:
        try:
            expenses[group_name]["expenses"][person].pop(index)
            if not expenses[group_name]["expenses"][person]:  # Remove the person if no expenses left
                del expenses[group_name]["expenses"][person]
            save_expenses(expenses)
        except IndexError:
            print(f"Invalid index. {person} has no expense at index {index}.")


def delete_group(expenses, group_name):
    """Deletes an entire group."""
    if group_name in expenses:
        del expenses[group_name]
        save_expenses(expenses)


def get_group(expenses, group_name):
    """Returns the expenses for a specific group."""
    return expenses.get(group_name, {})


def create_group(expenses, group_name, members):
    """Creates a new group with a list of members."""
    if group_name in expenses:
        raise ValueError(f"Group '{group_name}' already exists.")
    # Validate and clean member list
    members = [member.strip() for member in members if member.strip()]
    if not members:
        raise ValueError("Cannot create a group without valid members.")
    expenses[group_name] = {"members": members, "expenses": {}}
    save_expenses(expenses)


def add_group_member(expenses, group_name, member_name):
    """Adds a new member to the specified group."""
    if group_name not in expenses:
        raise ValueError(f"Group '{group_name}' does not exist.")
    if not member_name or member_name.strip() == "":
        raise ValueError("Invalid member name. Member name cannot be empty.")
    if "," in member_name:
        raise ValueError("Member name cannot contain commas.")
    if member_name in expenses[group_name]["members"]:
        raise ValueError(f"Member '{member_name}' is already in the group.")
    expenses[group_name]["members"].append(member_name.strip())
    save_expenses(expenses)


def remove_group_member(expenses, group_name, member_name):
    """Removes a member from the specified group."""
    if group_name not in expenses:
        raise ValueError(f"Group '{group_name}' does not exist.")
    if member_name not in expenses[group_name]["members"]:
        raise ValueError(f"Member '{member_name}' is not in the group.")
    expenses[group_name]["members"].remove(member_name)
    # Optionally, remove all expenses associated with the member
    if member_name in expenses[group_name]["expenses"]:
        del expenses[group_name]["expenses"][member_name]
    save_expenses(expenses)
