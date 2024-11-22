def calculate_balances(expenses, members):
    """
    Calculates the balances for each group member based on expenses.

    :param expenses: Dictionary of expenses where keys are names and values are lists of expense items.
    :param members: List of group members.
    :return: A tuple of (balances, payment instructions, total balance).
    """
    balances = {member: 0 for member in members}
    total_balance = 0

    # Calculate balances
    for person, person_expenses in expenses.items():
        for expense in person_expenses:
            balances[person] += expense["amount"]
            total_balance += expense["amount"]

    # Equal share of expenses
    equal_share = total_balance / len(members)

    # Adjust balances
    for member in balances:
        balances[member] -= equal_share

    # Create payment instructions
    creditors = {k: v for k, v in balances.items() if v > 0}
    debtors = {k: -v for k, v in balances.items() if v < 0}

    payment_instructions = []
    while debtors:
        # Get a debtor and their debt
        debtor, debt = next(iter(debtors.items()))

        if not creditors:
            break  # No more creditors to pay

        # Get a creditor and their credit
        creditor, credit = next(iter(creditors.items()))

        # Determine payment amount
        payment = min(debt, credit)
        payment_instructions.append(f"{debtor} pays ${payment:.2f} to {creditor}")

        # Update balances
        debt -= payment
        credit -= payment

        # Update debtors and creditors
        if debt == 0:
            del debtors[debtor]
        else:
            debtors[debtor] = debt

        if credit == 0:
            del creditors[creditor]
        else:
            creditors[creditor] = credit

    return balances, payment_instructions, total_balance

