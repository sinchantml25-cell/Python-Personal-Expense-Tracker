import csv
import os
from datetime import datetime

FILE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expenses.csv")
REPORT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "report.txt")
CSV_COLUMNS = ["Date", "Type", "Category", "Amount", "Description"]
VALID_TYPES = {"income": "Income", "expense": "Expense"}


def initialize_file(file_path=None):
    if file_path is None:
        file_path = FILE_NAME
    if not os.path.exists(file_path):
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_COLUMNS)
            writer.writeheader()


def clean_text(value, default=""):
    if value is None:
        return default
    text = str(value).strip()
    return text if text else default


def format_amount(value):
    amount = float(str(value).strip())
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    return f"{amount:.2f}"


def parse_date(date_value):
    value = clean_text(date_value)
    if not value:
        raise ValueError("Date is required.")

    for fmt in ("%d-%m-%Y", "%d-%m-%y", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue

    raise ValueError("Date must be in DD-MM-YYYY, DD-MM-YY, or YYYY-MM-DD format.")


def format_date(date_value):
    return parse_date(date_value).strftime("%d-%m-%Y")


def normalize_transaction_type(value):
    type_value = clean_text(value)
    if not type_value:
        raise ValueError("Transaction type is required.")
    normalized = type_value.lower()
    if normalized not in VALID_TYPES:
        raise ValueError("Type must be Income or Expense.")
    return VALID_TYPES[normalized]


def normalize_transaction_row(row):
    if row is None:
        return None

    if not isinstance(row, dict):
        row = {key: value for key, value in zip(CSV_COLUMNS, row[:5])}

    required_keys = set(CSV_COLUMNS)
    if not required_keys.issubset(row.keys()):
        row = {key: row.get(key, "") for key in CSV_COLUMNS}

    date_value = format_date(row.get("Date", ""))
    type_value = normalize_transaction_type(row.get("Type", ""))
    category_value = clean_text(row.get("Category"), "Uncategorized")
    amount_value = format_amount(row.get("Amount", ""))
    description_value = clean_text(row.get("Description"), "No description")

    return {
        "Date": date_value,
        "Type": type_value,
        "Category": category_value,
        "Amount": amount_value,
        "Description": description_value,
    }


def repair_file(file_path=None):
    if file_path is None:
        file_path = FILE_NAME
    if not os.path.exists(file_path):
        initialize_file(file_path)
        return

    try:
        with open(file_path, "r", newline="", encoding="utf-8-sig") as file:
            rows = list(csv.reader(file))
    except (OSError, csv.Error):
        initialize_file(file_path)
        return

    if not rows:
        initialize_file(file_path)
        return

    header = [cell.strip() for cell in rows[0]]
    if header == CSV_COLUMNS:
        return

    cleaned_rows = []
    for row in rows:
        if not row or all(clean_text(cell) == "" for cell in row):
            continue
        while len(row) < 5:
            row.append("")
        row = row[:5]
        try:
            cleaned_rows.append(normalize_transaction_row(row))
        except ValueError:
            continue

    write_transactions(cleaned_rows, file_path)


def read_transactions(file_path=None):
    if file_path is None:
        file_path = FILE_NAME
    repair_file(file_path)

    try:
        with open(file_path, newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            rows = []
            for row in reader:
                if row is None or all(clean_text(value) == "" for value in row.values()):
                    continue
                try:
                    rows.append(normalize_transaction_row(row))
                except ValueError:
                    continue
            return rows
    except (IOError, PermissionError, csv.Error) as exc:
        print(f"Error reading file: {exc}")
        return []


def write_transactions(rows, file_path=None):
    if file_path is None:
        file_path = FILE_NAME
    try:
        normalized_rows = []
        for row in rows:
            try:
                normalized_rows.append(normalize_transaction_row(row))
            except ValueError:
                continue

        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_COLUMNS)
            writer.writeheader()
            writer.writerows(normalized_rows)
    except (IOError, PermissionError, csv.Error) as exc:
        print(f"Error writing file: {exc}. Your changes may not have been saved.")


def get_valid_date(prompt):
    while True:
        date_str = input(prompt).strip()
        try:
            return format_date(date_str)
        except ValueError:
            print("Invalid date. Please use DD-MM-YYYY or YYYY-MM-DD format.")


def prompt_for_type(prompt):
    while True:
        transaction_type = input(prompt).strip()
        try:
            return normalize_transaction_type(transaction_type)
        except ValueError:
            print("Invalid type. Please enter Income or Expense.")


def prompt_for_amount(prompt):
    while True:
        value = input(prompt).strip()
        try:
            return format_amount(value)
        except ValueError:
            print("Please enter a valid positive amount.")


def add_transaction():
    print("\n--- Add Transaction ---")
    date = get_valid_date("Enter date (DD-MM-YYYY): ")
    transaction_type = prompt_for_type("Enter type (Income/Expense): ")
    category = clean_text(input("Enter category: "), "Uncategorized")
    amount = prompt_for_amount("Enter amount: ")
    description = clean_text(input("Enter description: "), "No description")

    rows = read_transactions()
    rows.append({
        "Date": date,
        "Type": transaction_type,
        "Category": category,
        "Amount": amount,
        "Description": description,
    })
    write_transactions(rows)
    print("Transaction added successfully!")


def print_transaction_table(rows):
    if not rows:
        print("No transactions found.")
        return

    print(f"{'#':<4} {'Date':<12} {'Type':<8} {'Category':<15} {'Amount':>10} {'Description'}")
    print("-" * 80)
    for index, row in enumerate(rows, start=1):
        print(
            f"{index:<4} {row['Date']:<12} {row['Type']:<8} {row['Category']:<15} {float(row['Amount']):>10.2f} {row['Description']}"
        )


def view_transactions():
    print("\n--- View Transactions ---")
    rows = read_transactions()
    print_transaction_table(rows)


def update_transaction():
    print("\n--- Update Transaction ---")
    rows = read_transactions()
    if not rows:
        print("No transactions found to update.")
        return

    print_transaction_table(rows)

    try:
        row_number = int(input("Enter the transaction number to update: ").strip())
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
        field_choice = int(input("Enter field number: ").strip())
    except ValueError:
        print("Please enter a valid field number.")
        return

    if field_choice == 1:
        target["Date"] = get_valid_date("Enter new date (DD-MM-YYYY): ")
    elif field_choice == 2:
        target["Type"] = prompt_for_type("Enter new type (Income/Expense): ")
    elif field_choice == 3:
        target["Category"] = clean_text(input("Enter new category: "), "Uncategorized")
    elif field_choice == 4:
        target["Amount"] = prompt_for_amount("Enter new amount: ")
    elif field_choice == 5:
        target["Description"] = clean_text(input("Enter new description: "), "No description")
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

    print_transaction_table(rows)

    try:
        row_number = int(input("Enter the transaction number to delete: ").strip())
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
        except (TypeError, ValueError):
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
    for category, total in sorted(category_totals.items()):
        print(f"- {category}: {total:.2f}")


def generate_report():
    print("\n--- Generate Report ---")
    rows = read_transactions()
    if not rows:
        print("No transactions found to report.")
        return

    print("1. Monthly Report")
    print("2. Category-wise Report")
    report_type = input("Choose report type: ").strip()

    try:
        if report_type == "1":
            month = input("Enter month and year (MM-YYYY): ").strip()
            datetime.strptime(month, "%m-%Y")
            filtered = [row for row in rows if row["Date"][3:] == month]
            title = f"Monthly Report - {month}"
        elif report_type == "2":
            category = clean_text(input("Enter category: "), "Uncategorized")
            filtered = [row for row in rows if row["Category"].lower() == category.lower()]
            title = f"Category Report - {category}"
        else:
            print("Invalid choice.")
            return
    except ValueError:
        print("Invalid month format. Please use MM-YYYY.")
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

    with open(REPORT_FILE, "w", encoding="utf-8") as file:
        file.write("\n".join(report_lines))

    print(f"Report generated successfully in {os.path.basename(REPORT_FILE)}")


def display_menu():
    print("\n=================================")
    print("       PERSONAL EXPENSE TRACKER")
    print("=================================")
    print("1. Add Transaction")
    print("2. View Transactions")
    print("3. Update Transaction")
    print("4. Delete Transaction")
    print("5. View Summary")
    print("6. Generate Report")
    print("7. Exit")


def run_app():
    initialize_file()
    print("\nWelcome to the Personal Expense Tracker!")

    while True:
        display_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            update_transaction()
        elif choice == "4":
            delete_transaction()
        elif choice == "5":
            view_summary()
        elif choice == "6":
            generate_report()
        elif choice == "7":
            print("Thank you for using Personal Expense Tracker!")
            break
        else:
            print("Invalid choice. Please select a number between 1 and 7.")


if __name__ == "__main__":
    run_app()