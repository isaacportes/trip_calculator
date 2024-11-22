from storage import (
    load_expenses,
    save_expenses,
    add_expense_item,
    delete_expense_item,
    delete_group,
    get_group,
    create_group,
    add_group_member,
    remove_group_member
)
from calculator import calculate_balances
import os


def reset_program():
    """Resets the program by deleting the expenses.json file."""
    if os.path.exists("expenses.json"):
        os.remove("expenses.json")
        print("Program reset. All data has been cleared.")
    else:
        print("No data to reset.")


def main():
    expenses = load_expenses()
    current_group = None  # Track the active group

    while True:
        # Group selection or creation
        if not current_group:
            print("\nAvailable Groups:")
            for group, data in expenses.items():
                print(f"- {group} (Members: {', '.join(data['members'])})")

            print("\nSelect an action:")
            print("1) Select Group")
            print("2) Create New Group")
            print("3) Delete Group")
            print("4) View Total Balance for Each Group")
            print("5) Reset Program")
            print("6) Exit")

            group_action = input("Enter your choice (1-6): ").strip()

            if group_action == "1":
                group_name = input("Enter group name to select: ").strip()
                if group_name in expenses:
                    current_group = group_name
                    print(f"Switched to group '{current_group}'.")
                else:
                    print(f"Group '{group_name}' does not exist.")

            elif group_action == "2":
                group_name = input("Enter a new group name: ").strip()
                if group_name in expenses:
                    print(f"Group '{group_name}' already exists.")
                else:
                    members = input("Enter group members (comma-separated): ").strip().split(",")
                    members = [member.strip() for member in members if member.strip()]
                    try:
                        create_group(expenses, group_name, members)
                        print(f"Group '{group_name}' created with members: {', '.join(members)}")
                    except ValueError as e:
                        print(e)

            elif group_action == "3":
                group_name = input("Enter the group name to delete: ").strip()
                delete_group(expenses, group_name)
                print(f"Group '{group_name}' deleted.")

            elif group_action == "4":
                print("\nTotal Balances for Each Group:")
                for group, data in expenses.items():
                    total_balance = sum(
                        sum(item["amount"] for item in person_expenses)
                        for person_expenses in data["expenses"].values()
                    )
                    print(f"Group '{group}': Total balance is ${total_balance:.2f}")

            elif group_action == "5":
                reset_program()
                expenses = {}
                current_group = None

            elif group_action == "6":
                save_expenses(expenses)
                print("Expenses saved. Exiting program.")
                break

            else:
                print("Invalid choice. Please enter a number from 1 to 6.")

        # Actions within the selected group
        else:
            print(f"\nYou are in group '{current_group}'. Choose an action:")
            print("1) Add Expense")
            print("2) Remove Specific Expense")
            print("3) Add New Member")
            print("4) Remove Member")
            print("5) Calculate Balances and View Total")
            print("6) Switch Group")
            print("7) Exit")

            action = input("Enter your choice (1-7): ").strip()

            if action == "1":
                name = input("Enter name: ")
                description = input("Enter description of expense: ")
                amount = float(input("Enter amount spent: "))
                add_expense_item(expenses, current_group, name, description, amount)
                print(f"Added ${amount:.2f} expense for {name} in group '{current_group}'.")

            elif action == "2":
                name = input("Enter name: ")
                if name in expenses[current_group]["expenses"]:
                    print(f"Expenses for {name}: {expenses[current_group]['expenses'][name]}")
                    index = int(input("Enter the index of the expense to remove (starting at 0): "))
                    delete_expense_item(expenses, current_group, name, index)
                else:
                    print(f"No expenses found for {name} in group '{current_group}'.")

            elif action == "3":
                member_name = input("Enter the name of the new member: ").strip()
                try:
                    add_group_member(expenses, current_group, member_name)
                    print(f"Added {member_name} to group '{current_group}'.")
                except ValueError as e:
                    print(e)

            elif action == "4":
                member_name = input("Enter the name of the member to remove: ").strip()
                try:
                    remove_group_member(expenses, current_group, member_name)
                    print(f"Removed {member_name} from group '{current_group}'.")
                except ValueError as e:
                    print(e)


            elif action == "5":
                group_data = get_group(expenses, current_group)
                if group_data:
                    group_expenses = group_data["expenses"]
                    members = group_data["members"]
                    group_balances, payment_instructions, total_balance = calculate_balances(
                        group_expenses, members
                    )
                    print(f"\nTotal balance for group '{current_group}' is: ${total_balance:.2f}")
                    print("\nBalances for each person:")
                    for person, balance in group_balances.items():
                        if balance > 0:
                            print(f"{person} should receive ${balance:.2f}")
                        elif balance < 0:
                            print(f"{person} needs to pay ${-balance:.2f}")
                        else:
                            print(f"{person} is settled.")
                    print("\nPayment Instructions:")

                    for instruction in payment_instructions:
                        print(instruction)

                else:

                    print(f"No expenses recorded yet for group '{current_group}'.")

            elif action == "6":
                current_group = None

            elif action == "7":
                save_expenses(expenses)
                print("Expenses saved. Exiting program.")
                break

            else:
                print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
