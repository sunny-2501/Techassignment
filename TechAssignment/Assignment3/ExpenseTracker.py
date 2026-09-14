import json
from pathlib import Path
from datetime import datetime, date
from decimal import Decimal, InvalidOperation

DATA_FILE = Path(__file__).resolve().with_name("expenses.json")


def load_expenses():
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            expenses = json.load(file)

        if not isinstance(expenses, list):
            raise ValueError("Invalid expense data.")

        seen_ids = set()

        for expense in expenses:
            if not isinstance(expense, dict):
                raise ValueError("Invalid expense record.")

            if (
                type(expense.get("id")) is not int
                or expense["id"] <= 0
                or expense["id"] in seen_ids
                or type(expense.get("amount_paise")) is not int
                or expense["amount_paise"] <= 0
                or not isinstance(expense.get("category"), str)
                or not expense["category"].strip()
                or not isinstance(expense.get("description"), str)
                or not isinstance(expense.get("date"), str)
            ):
                raise ValueError("Invalid expense fields.")

            parsed = date.fromisoformat(expense["date"])
            if parsed.isoformat() != expense["date"]:
                raise ValueError("Invalid date format.")

            seen_ids.add(expense["id"])

        return expenses

    except (OSError, ValueError) as error:
        raise SystemExit(
            f"Cannot load expenses.json: {error}\n"
            "Check the file before restarting."
        )


def save_expenses(expenses):
    temporary_file = DATA_FILE.with_suffix(".tmp")

    with temporary_file.open("w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=4)

    temporary_file.replace(DATA_FILE)


def money(paise):
    return f"Rs. {Decimal(paise) / 100:,.2f}"


def read_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


def read_amount():
    while True:
        raw = input("Amount in rupees: ").strip()

        try:
            amount = Decimal(raw)

            if not amount.is_finite() or amount <= 0:
                print("Enter a positive, finite amount.")
                continue

            # Practical upper limit for this assignment.
            if amount > Decimal("1000000000"):
                print("Amount is too large.")
                continue

            paise = amount * 100

            if paise != paise.to_integral_value():
                print("Use a maximum of two decimal places.")
                continue

            return int(paise)

        except InvalidOperation:
            print("Enter a valid amount, such as 150 or 150.50.")


def read_date():
    while True:
        value = input(
            "Date YYYY-MM-DD (Enter for today): "
        ).strip()

        if not value:
            return date.today().isoformat()

        try:
            parsed = datetime.strptime(value, "%Y-%m-%d").date()

            if parsed.isoformat() != value:
                raise ValueError

            return value

        except ValueError:
            print("Enter a valid date in YYYY-MM-DD format.")


def add_expense(expenses):
    expense_date = read_date()
    category = read_text(
        "Category (Food/Travel/Books/etc.): "
    ).title()
    amount = read_amount()
    description = input("Description (optional): ").strip()

    expense_id = max(
        (expense["id"] for expense in expenses), default=0
    ) + 1

    expenses.append({
        "id": expense_id,
        "date": expense_date,
        "category": category,
        "amount_paise": amount,
        "description": description,
    })

    save_expenses(expenses)
    print(f"Expense added. ID: {expense_id}")


def view_expenses(expenses):
    if not expenses:
        print("No expenses recorded.")
        return

    for expense in sorted(
        expenses, key=lambda item: (item["date"], item["id"])
    ):
        print(
            f"\nID: {expense['id']} | Date: {expense['date']}\n"
            f"Category: {expense['category']}\n"
            f"Amount: {money(expense['amount_paise'])}\n"
            f"Description: {expense['description'] or '-'}"
        )

    total = sum(item["amount_paise"] for item in expenses)
    print(f"\nTotal spending: {money(total)}")


def category_summary(expenses):
    if not expenses:
        print("No expenses recorded.")
        return

    totals = {}

    for expense in expenses:
        category = expense["category"]
        totals[category] = (
            totals.get(category, 0) + expense["amount_paise"]
        )

    print("\nCATEGORY-WISE SPENDING")

    for category, amount in sorted(
        totals.items(), key=lambda item: (-item[1], item[0])
    ):
        print(f"{category}: {money(amount)}")

    print(f"Total: {money(sum(totals.values()))}")


def monthly_summary(expenses):
    if not expenses:
        print("No expenses recorded.")
        return

    totals = {}

    for expense in expenses:
        month = expense["date"][:7]
        totals[month] = (
            totals.get(month, 0) + expense["amount_paise"]
        )

    print("\nMONTH-WISE SPENDING")

    for month, amount in sorted(totals.items()):
        print(f"{month}: {money(amount)}")

    print(f"Total: {money(sum(totals.values()))}")


def delete_expense(expenses):
    try:
        expense_id = int(input("Expense ID to delete: "))
    except ValueError:
        print("Enter a valid integer ID.")
        return

    for index, expense in enumerate(expenses):
        if expense["id"] == expense_id:
            confirmation = input(
                f"Delete {expense['category']} expense of "
                f"{money(expense['amount_paise'])}? (y/n): "
            ).strip().lower()

            if confirmation == "y":
                expenses.pop(index)
                save_expenses(expenses)
                print("Expense deleted.")
            else:
                print("Deletion cancelled.")

            return

    print("Expense ID not found.")


def main():
    expenses = load_expenses()

    actions = {
        "1": add_expense,
        "2": view_expenses,
        "3": category_summary,
        "4": monthly_summary,
        "5": delete_expense,
    }

    while True:
        print("\nPERSONAL EXPENSE TRACKER")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Category-wise spending")
        print("4. Monthly spending")
        print("5. Delete expense")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "6":
            print("Program closed.")
            break

        action = actions.get(choice)

        if action:
            action(expenses)
        else:
            print("Invalid choice. Select 1–6.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram closed.")
    except OSError as error:
        print(f"\nCould not save data: {error}")
        print("The latest change may not have been saved.")