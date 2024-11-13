# calculator.py

def add_expense(expenses, group_name, name, amount):
    """Adds or updates the expense for each person in the specified group."""
    if name in expenses[group_name]:
        expenses[group_name][name] += amount
    else:
        expenses[group_name][name] = amount


def calculate_balances(expenses):
    total_balance = sum(expenses.values())
    equal_share = total_balance / len(expenses)

    # Calculate balance for each person
    balances = {name: round(amount - equal_share, 2) for name, amount in expenses.items()}

    to_pay = [(name, balance) for name, balance in balances.items() if balance < 0]
    to_receive = [(name, balance) for name, balance in balances.items() if balance > 0]

    payment_instructions = []
    for name_pay, balance_pay in to_pay:
        while balance_pay < 0 and to_receive:
            name_receive, balance_receive = to_receive[0]
            payment = min(abs(balance_pay), balance_receive)
            payment_instructions.append(f"{name_pay} needs to pay {name_receive}: ${payment:.2f}")

            balance_pay += payment
            balance_receive -= payment

            if balance_receive == 0:
                to_receive.pop(0)
            else:
                to_receive[0] = (name_receive, balance_receive)

    return balances, payment_instructions, total_balance

