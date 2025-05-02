from datetime import datetime
import json

DATA_FILE = "data.json"

def add_monthly_expense():
    monthly_expense = input("What kind of monthly expense is this? (loan or bill): ").lower()

    if monthly_expense == "loan":
        name = input("Enter name of loan (e.g., Car Loan, Student Loan): ")
        amount = float(input("Enter monthly payment amount: "))
        due_date = input("Enter due date: ")
        apr = float(input("Enter APR (e.g., 6 for 6%): "))
        remaining = float(input("Enter current remaining balance: "))
        monthly_payment = float(input("Enter expected monthly payment: "))

        expense = {
            "monthly_expense": monthly_expense,
            "name": name,
            "amount": amount,
            "due_date": due_date,
            "apr": apr,
            "remaining_balance": remaining,
            "monthly_payment": monthly_payment
        }

    elif monthly_expense == "bill":
        name = input("Enter name of bill (e.g., Rent, Car Insurance, Internet): ")
        amount = float(input("Enter monthly amount: "))
        due_date = input("Enter due date: ")

        if name.lower() in ["car insurance", "auto insurance"]:
            print("Auto/Car Insurance will be treated as a 6-month fixed-term policy.")
            start_input = input("When did your policy begin? (MM-YYYY): ")

            try:
                start_date = datetime.strptime(start_input, "%m-%Y")
                today = datetime.today()
                months_passed = (today.year - start_date.year) * 12 + today.month - start_date.month
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
            "remaining_balance": remaining
        }

    else:
        print("Invalid expense type entered.")
        return

    try:
        with open(DATA_FILE, 'r') as file:
            expenses = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        expenses = []

    expenses.append(expense)

    with open(DATA_FILE, 'w') as file:
        json.dump(expenses, file, indent=4)


add_monthly_expense()

def view_expenses():

    try:
        with open(DATA_FILE, 'r') as file:
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

def main():
    while True:
        print("\n Monthly Expense Tracker")
        print("1. Add a new expense")
        print("2. View all expenses")
        print("3. Exit")

        choice = input("Choose an option (1, 2, or 3): ").strip()

        if choice == "1":
            add_monthly_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
