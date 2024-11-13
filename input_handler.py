from storage import load_expenses, save_expenses, add_expense, update_expense, delete_expense, delete_group, get_group
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
            for group in expenses.keys():
                print(f"- {group}")

            print("\nSelect an action:")
            print("1) Select Group")
            print("2) Create New Group")
            print("3) Delete Group")
            print("4) View Total Balance for Each Group")
            print("5) Reset Program")
            print("6) Exit")

            group_action = input("Enter your choice (1-6): ").strip()

            if group_action == "1":
                if not expenses:
                    print("No groups available. Please create a group first.")
                else:
                    group_name = input("Enter group name to select: ").strip()
                    if group_name in expenses:
                        current_group = group_name
                        print(f"Switched to group '{current_group}'.")
                    else:
                        print(f"Group '{group_name}' does not exist.")

            elif group_action == "2":
                group_name = input("Enter a new group name: ").strip()
                if group_name not in expenses:
                    expenses[group_name] = {}
                    print(f"Group '{group_name}' created.")
                else:
                    print(f"Group '{group_name}' already exists.")

            elif group_action == "3":
                group_name = input("Enter the group name to delete: ").strip()
                delete_group(expenses, group_name)
                print(f"Group '{group_name}' deleted.")

            elif group_action == "4":
                print("\nTotal Balances for Each Group:")
                for group, group_expenses in expenses.items():
                    total_balance = sum(group_expenses.values())
                    print(f"Group '{group}': Total balance is ${total_balance:.2f}")

            elif group_action == "5":
                reset_program()
                expenses = {}  # Clear the in-memory data after reset.
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
            print("2) Update Expense")
            print("3) Delete Expense")
            print("4) Calculate Balances and View Total")
            print("5) View Total Balance")
            print("6) Switch Group")
            print("7) Exit")

            action = input("Enter your choice (1-7): ").strip()

            if action == "1":
                name = input("Enter name: ")
                amount = float(input("Enter amount spent: "))
                add_expense(expenses, current_group, name, amount)
                print(
                    f"Added {name}'s expense of ${amount:.2f} to group '{current_group}'. Total for {name} in group '{current_group}' is now ${expenses[current_group][name]:.2f}")

            elif action == "2":
                name = input("Enter name to update: ")
                if name in expenses[current_group]:
                    amount = float(input(f"Enter new amount for {name}: "))
                    update_expense(expenses, current_group, name, amount)
                else:
                    print(f"No expense found for {name} in group '{current_group}'.")

            elif action == "3":
                name = input("Enter name to delete: ")
                delete_expense(expenses, current_group, name)

            elif action == "4":
                group_expenses = get_group(expenses, current_group)
                if group_expenses:
                    group_balances, payment_instructions, total_balance = calculate_balances(group_expenses)
                    print(f"\nTotal balance for group '{current_group}' is: ${total_balance:.2f}")

                    print("\nInstructions:")
                    for instruction in payment_instructions:
                        print(instruction)

                    print("\nBalances for each person:")
                    for person, balance in group_balances.items():
                        if balance > 0:
                            print(f"{person} should receive ${balance:.2f}")
                        elif balance < 0:
                            print(f"{person} needs to pay ${-balance:.2f}")
                        else:
                            print(f"{person} is settled up.")



                else:
                    print(f"Group '{current_group}' not found or has no expenses.")

            elif action == "5":
                total_balance = sum(expenses[current_group].values())
                print(f"Total balance for group '{current_group}' is ${total_balance:.2f}")

            elif action == "6":
                current_group = None  # Set to None to go back to group selection
                print("Exiting current group.")

            elif action == "7":
                save_expenses(expenses)
                print("Expenses saved. Exiting program.")
                break

            else:
                print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
