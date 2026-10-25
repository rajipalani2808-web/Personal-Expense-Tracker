
import json
import os
from datetime import date

# Store the JSON file in the same folder as this program
FOLDER = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(FOLDER, "expenses.json")

CATEGORIES = [
    "Food",
    "Travel",
    "Shopping",
    "Education",
    "Bills",
    "Health",
    "Salary",
    "Other"
]


def load_transactions():
    """Load saved transactions from the JSON file."""
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read saved data. Starting with an empty list.")
        return []


def save_transactions(transactions):
    """Save transactions to the JSON file."""
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(transactions, file, indent=4)


def get_amount():
    """Accept only a positive amount."""
    while True:
        try:
            amount = float(input("Enter amount (Rs.): "))

            if amount > 0 and amount != float("inf"):
                return round(amount, 2)

            print("Amount must be greater than zero.")
        except ValueError:
            print("Please enter a valid number.")


def get_date():
    """Accept a date in YYYY-MM-DD format."""
    while True:
        entered_date = input(
            f"Enter date (YYYY-MM-DD) or press Enter for today "
            f"[{date.today()}]: "
        ).strip()

        if entered_date == "":
            return str(date.today())

        try:
            return str(date.fromisoformat(entered_date))
        except ValueError:
            print("Invalid date. Example: 2026-10-24")


def add_transaction(transactions):
    """Add a new income or expense."""
    print("\n1. Income")
    print("2. Expense")

    choice = input("Choose transaction type: ").strip()

    if choice == "1":
        transaction_type = "Income"
    elif choice == "2":
        transaction_type = "Expense"
    else:
        print("Invalid transaction type.")
        return

    amount = get_amount()

    print("\nAvailable categories:")
    for number, category in enumerate(CATEGORIES, start=1):
        print(f"{number}. {category}")

    while True:
        try:
            category_number = int(input("Choose category number: "))

            if 1 <= category_number <= len(CATEGORIES):
                category = CATEGORIES[category_number - 1]
                break

            print("Choose a number from the list.")
        except ValueError:
            print("Please enter a valid category number.")

    description = input("Enter description: ").strip()
    transaction_date = get_date()

    transaction = {
        "id": max(
            (t.get("id", 0) for t in transactions
             if isinstance(t.get("id"), int)),
            default=0
        ) + 1,
        "type": transaction_type,
        "amount": amount,
        "category": category,
        "description": description,
        "date": transaction_date
    }

    transactions.append(transaction)
    save_transactions(transactions)
    print("Transaction saved successfully!")


def view_transactions(transactions):
    """Display every saved transaction."""
    if not transactions:
        print("\nNo transactions found.")
        return

    print("\n========== ALL TRANSACTIONS ==========")

    for item in transactions:
        print(f"\nID: {item['id']}")
        print(f"Date: {item['date']}")
        print(f"Type: {item['type']}")
        print(f"Category: {item['category']}")
        print(f"Description: {item['description']}")
        print(f"Amount: Rs. {item['amount']:.2f}")


def show_summary(transactions):
    """Calculate income, expenses, and balance."""
    total_income = sum(
        item["amount"] for item in transactions
        if item["type"] == "Income"
    )

    total_expenses = sum(
        item["amount"] for item in transactions
        if item["type"] == "Expense"
    )

    balance = total_income - total_expenses

    print("\n========== FINANCIAL SUMMARY ==========")
    print(f"Total Income:   Rs. {total_income:.2f}")
    print(f"Total Expenses: Rs. {total_expenses:.2f}")
    print(f"Remaining Balance: Rs. {balance:.2f}")


def search_category(transactions):
    """Search transactions by category."""
    category = input(
        "Enter category to search (e.g. Food): "
    ).strip().lower()

    matches = [
        item for item in transactions
        if item["category"].lower() == category
    ]

    if not matches:
        print("No transactions found in this category.")
        return

    print(f"\nTransactions in {matches[0]['category']}:")

    for item in matches:
        print(
            f"ID: {item['id']} | {item['date']} | "
            f"{item['type']} | Rs. {item['amount']:.2f} | "
            f"{item['description']}"
        )


def main():
    transactions = load_transactions()

    while True:
        print("\n===================================")
        print("     PERSONAL EXPENSE TRACKER")
        print("===================================")
        print("1. Add Income or Expense")
        print("2. View All Transactions")
        print("3. View Financial Summary")
        print("4. Search by Category")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_transaction(transactions)
        elif choice == "2":
            view_transactions(transactions)
        elif choice == "3":
            show_summary(transactions)
        elif choice == "4":
            search_category(transactions)
        elif choice == "5":
            print("Your transactions are saved. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
