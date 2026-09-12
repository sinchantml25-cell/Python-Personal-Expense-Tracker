import csv
import os
from datetime import datetime
FILE_NAME = "expenses.csv"


def initialize_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow([
                "Date",
                "Type",
                "Category",
                "Amount",
                "Description"
            ])


def read_transactions():
    if not os.path.exists(FILE_NAME):
        initialize_file()

    try:
     with open(FILE_NAME, newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            return list(reader)
    except (IOError, PermissionError) as e:
        print(f"Error reading file: {e}")
        return []
def write_transactions(rows):
    try:
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=[
                "Date",
                "Type",
                "Category",
                "Amount",
                "Description"
            ])
            writer.writeheader()
            writer.writerows(rows)
    except (IOError, PermissionError) as e:
        print(f"Error writing file: {e}. Your changes may not have been saved.")

def get_valid_date(prompt):
    while True:
        date_str = input(prompt)
        try:
            datetime.strptime(date_str, "%d-%m-%Y")
            return date_str
        except ValueError:
            print("Invalid date. Please use DD-MM-YYYY format (e.g., 05-09-2026).")

def add_transaction():
    print("\n--- Add Transaction ---")

    date = get_valid_date("Enter date (DD-MM-YYYY): ")
    transaction_type = input("Enter type (Income/Expense): ")

    while transaction_type not in ["Income", "Expense"]:
        print("Invalid type. Please enter Income or Expense.")
        transaction_type = input("Enter type (Income/Expense): ")

    category = input("Enter category: ")

    while True:
        try:
            amount = float(input("Enter amount: "))

            if amount <= 0:
                print("Amount must be greater than zero.")
            else:
                break

        except ValueError:
            print("Please enter a valid number.")

    description = input("Enter description: ")

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            date,
            transaction_type,
            category,
            amount,
            description
        ])

    print("Transaction added successfully!")

def view_transactions():
    print("\n--- View Transactions ---")
    rows = read_transactions()

    if not rows:
        print("No transactions found.")
        return

    for index, row in enumerate(rows, start=1):
        print(f"{index}. Date: {row['Date']} | Type: {row['Type']} | Category: {row['Category']} | Amount: {row['Amount']} | Description: {row['Description']}")


def update_transaction():
    print("\n--- Update Transaction ---")
    rows = read_transactions()

    if not rows:
        print("No transactions found to update.")
        return

    view_transactions()

    try:
        row_number = int(input("Enter the transaction number to update: "))
        if row_number < 1 or row_number > len(rows):
            print("Invalid transaction number.")
            return
    except ValueError:
        print("Please enter a valid transaction number.")
        return

    target = rows[row_number - 1]
    print("Choose field to update:")
    print("1. Date")
    print("2. Type")
    print("3. Category")
    print("4. Amount")
    print("5. Description")

    try:
        field_choice = int(input("Enter field number: "))
    except ValueError:
        print("Please enter a valid field number.")
        return

    if field_choice == 1:
        target["Date"] = get_valid_date("Enter new date (DD-MM-YYYY): ")
    elif field_choice == 2:
        transaction_type = input("Enter new type (Income/Expense): ")
        while transaction_type not in ["Income", "Expense"]:
            print("Invalid type. Please enter Income or Expense.")
            transaction_type = input("Enter new type (Income/Expense): ")
        target["Type"] = transaction_type
    elif field_choice == 3:
        target["Category"] = input("Enter new category: ")
    elif field_choice == 4:
        while True:
            try:
                amount = float(input("Enter new amount: "))
                if amount <= 0:
                    print("Amount must be greater than zero.")
                else:
                    target["Amount"] = str(amount)
                    break
            except ValueError:
                print("Please enter a valid number.")
    elif field_choice == 5:
        target["Description"] = input("Enter new description: ")
    else:
        print("Invalid field choice.")
        return

    write_transactions(rows)
    print("Transaction updated successfully!")


def delete_transaction():
    print("\n--- Delete Transaction ---")
    rows = read_transactions()

    if not rows:
        print("No transactions found to delete.")
        return

    view_transactions()

    try:
        row_number = int(input("Enter the transaction number to delete: "))
        if row_number < 1 or row_number > len(rows):
            print("Invalid transaction number.")
            return
    except ValueError:
        print("Please enter a valid transaction number.")
        return

    del rows[row_number - 1]
    write_transactions(rows)
    print("Transaction deleted successfully!")


def view_summary():
    print("\n--- View Summary ---")
    rows = read_transactions()

    if not rows:
        print("No transactions found.")
        return

    total_income = 0.0
    total_expense = 0.0
    category_totals = {}

    for row in rows:
        try:
            amount = float(row["Amount"])
        except (ValueError, KeyError):
            continue  
        category = row["Category"]
        category_totals[category] = category_totals.get(category, 0.0) + amount

        if row["Type"] == "Income":
            total_income += amount
        elif row["Type"] == "Expense":
            total_expense += amount

    balance = total_income - total_expense

    print(f"Total Income: {total_income:.2f}")
    print(f"Total Expense: {total_expense:.2f}")
    print(f"Balance: {balance:.2f}")
    print("\nCategory totals:")
    for category, total in category_totals.items():
        print(f"- {category}: {total:.2f}")


def generate_report():
    print("\n--- Generate Report ---")
    rows = read_transactions()

    if not rows:
        print("No transactions found to report.")
        return

    print("1. Monthly Report")
    print("2. Category-wise Report")
    report_type = input("Choose report type: ")

    if report_type == "1":
        month = input("Enter month and year (MM-YYYY): ")
        filtered = [row for row in rows if row["Date"][3:] == month]
        title = f"Monthly Report - {month}"
    elif report_type == "2":
        category = input("Enter category: ")
        filtered = [row for row in rows if row["Category"].lower() == category.lower()]
        title = f"Category Report - {category}"
    else:
        print("Invalid choice.")
        return

    if not filtered:
        print("No matching transactions found.")
        return

    total_income = sum(float(r["Amount"]) for r in filtered if r["Type"] == "Income")
    total_expense = sum(float(r["Amount"]) for r in filtered if r["Type"] == "Expense")
    balance = total_income - total_expense

    report_lines = [title, "=" * len(title)]
    report_lines.append(f"Total Income: {total_income:.2f}")
    report_lines.append(f"Total Expense: {total_expense:.2f}")
    report_lines.append(f"Balance: {balance:.2f}")
    report_lines.append("")
    report_lines.append("Transactions:")

    for index, row in enumerate(filtered, start=1):
        report_lines.append(f"{index}. {row['Date']} | {row['Type']} | {row['Category']} | {row['Amount']} | {row['Description']}")

    with open("report.txt", "w") as file:
        file.write("\n".join(report_lines))

    print("Report generated successfully in report.txt")


initialize_file()


print("      *******PYTHON MINI PROJECT********")
print("<=================================================>")
print("        Python Personal Expense Tracker ")
print("<=================================================>")
while True:
    print("1. Add Transaction")
    print("2. View Transactions")
    print("3. Update Transaction")
    print("4. Delete Transaction")
    print("5. View Summary")
    print("6. Generate Report")
    print("7. Exit")

    choice = input("Enter your choice: ")
    if choice == "1":
        add_transaction()
        #print("Add Transaction selected")

    elif choice == "2":
        view_transactions()
        #print("View Transactions selected")

    elif choice == "3":
        update_transaction()
        #print("Update Transaction selected")

    elif choice == "4":
        delete_transaction()
        #print("Delete Transaction selected")

    elif choice == "5":
        view_summary()
        #print("View Summary selected")

    elif choice == "6":
        generate_report()
        #print("Generate Report selected")

    elif choice == "7":
        print("Thank you for using Personal Expense Tracker!")
        break