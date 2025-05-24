from datetime import datetime
import json

DATA_FILE = "data.json"


def main():
    while True:
        print("\n Monthly Expense Tracker")
        print("1. Add a new expense")
        print("2. View all expenses")
        print("3. Exit")

        choice = input()

        if choice == "1":
            add_monthly_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Please make a selection. ")


def add_monthly_expense():
    monthly_expense = input(
        "What kind of monthly expense would you like to add? (loan or bill): "
    ).lower()

    if monthly_expense == "loan":
        name = input("Enter name of loan (e.g., Car Loan, Student Loan, etc.): ")

        while True:
            try:
                amount = float(input("Enter monthly payment amount: "))
                break
            except ValueError:
                print("Enter a valid number(s). ")

        while True:
            due_date = input("Enter due date (MM/DD/YYYY or MMDDYYYY): ").strip()

            # Try both formats
            for fmt in ("%m/%d/%Y", "%m%d%Y"):
                try:
                    parsed = datetime.strptime(due_date, fmt)
                    due_date = parsed.strftime("%m/%d/%Y")  # Consistent output format
                    break  # Exit loop if valid
                except ValueError:
                    continue  # Try next format

            else:
                print("Invalid date. Please enter in MM/DD/YYYY or MMDDYYYY format.")
                continue  # Restart the input loop

            break  # Only break when we have a valid date

        while True:
            try:
                apr = float(input("Enter APR (e.g., 6 for 6%): "))
                break
            except ValueError:
                print("Enter a valid number(s). ")

        while True:
            try:
                remaining = float(input("Enter current remaining balance: "))
                break
            except ValueError:
                print("Enter a valid number.")

        while True:
            try:
                monthly_payment = float(input("Enter expected monthly payment: "))
                break
            except ValueError:
                print("Enter a valid number.")

        expense = {
            "monthly_expense": monthly_expense,
            "name": name,
            "amount": amount,
            "due_date": due_date,
            "apr": apr,
            "remaining_balance": remaining,
            "monthly_payment": monthly_payment,
        }

    elif monthly_expense == "bill":
        name = input("Enter name of bill (e.g., Rent, Car Insurance, Internet): ")

        while True:
            try:
                amount = float(input("Enter monthly amount: "))
                break
            except ValueError:
                print("Enter a valid number.")

        while True:
            due_date = input("Enter due date (MM/DD/YYYY or MMDDYYYY): ").strip()

            for fmt in ("%m/%d/%Y", "%m%d%Y"):
                try:
                    parsed = datetime.strptime(due_date, fmt)
                    due_date = parsed.strftime("%m/%d/%Y")

                    break
                except ValueError:
                    continue

            else:
                print("Invalid date. Please enter in MM/DD/YYYY format.")
                continue
            break

        if name.lower() in ["car insurance", "auto insurance"]:
            print("Auto/Car Insurance will be treated as a 6-month fixed-term policy.")
            start_input = input("When did your policy begin? (MM-YYYY): ")

            try:
                start_date = datetime.strptime(start_input, "%m-%Y")
                today = datetime.today()
                months_passed = (
                    (today.year - start_date.year) * 12 + today.month - start_date.month
                )
                months_remaining = max(6 - months_passed, 0)
                remaining = amount * months_remaining
            except ValueError:
                print("Invalid format. Assuming full 6 months remaining.")
                remaining = amount * 6
        else:
            remaining = "Until canceled"

        expense = {
            "monthly_expense": monthly_expense,
            "name": name,
            "amount": amount,
            "due_date": due_date,
            "remaining_balance": remaining,
        }

    else:
        print("Invalid expense type entered.")
        return

    try:
        with open(DATA_FILE, "r") as file:
            expenses = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        expenses = []

    expenses.append(expense)

    with open(DATA_FILE, "w") as file:
        json.dump(expenses, file, indent=4)


def view_expenses():

    try:
        with open(DATA_FILE, "r") as file:
            expenses = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        expenses = []

    if not expenses:
        print("There are no saved monthly expenses.")
        return
    else:
        print("\n--- Saved Monthly Expenses ---")
        for index, expense in enumerate(expenses, 1):
            name = expense.get("name")
            amount = expense.get("amount")
            due = expense.get("due_date")
            balance = expense.get("remaining_balance", "N/A")
            print(f"{index}. {name} - ${amount:.2f} (Due: {due}, Remaining: {balance})")
        print("--------------------")


if __name__ == "__main__":
    main()
