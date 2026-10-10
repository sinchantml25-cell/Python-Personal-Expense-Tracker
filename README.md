# Personal Expense Tracker

A simple Python-based expense tracking application that stores income and expense records in a CSV file, supports common financial operations, and generates useful summaries and reports.

## Overview

The Personal Expense Tracker helps users:

- Add income and expense transactions
- View all stored transactions in a clean table
- Update or remove any transaction
- Check total income, total expense, and current balance
- Generate monthly or category-based financial reports
- Keep data stored persistently in a local CSV file

## Features

- Date validation for `DD-MM-YYYY` and `YYYY-MM-DD`
- Strict validation for `Income` and `Expense` types
- Positive amount enforcement
- Blank-field fallback handling (`Uncategorized`, `No description`)
- File repair for malformed CSV entries
- Friendly terminal-based menu and output formatting
- Report generation saved to `report.txt`

## Project structure

- `main.py` — application logic and menu-driven interface
- `expenses.csv` — transaction storage
- `report.txt` — generated report output
- `test_expense_tracker.py` — automated validation tests
- `README.md` — project documentation

## Data format

The CSV file is stored with the following columns:

```csv
Date,Type,Category,Amount,Description
```

Example:

```csv
05-09-2026,Income,Salary,50000.00,Monthly salary
07-09-2026,Expense,Food,250.00,Groceries
```

## How to run

From the project folder:

```bash
python main.py
```

## Menu options

1. Add Transaction
2. View Transactions
3. Update Transaction
4. Delete Transaction
5. View Summary
6. Generate Report
7. Exit

## Input validation and edge cases handled

The project now checks for and handles:

- invalid dates
- wrong transaction types
- negative or zero amounts
- blank category or description entries
- missing or malformed CSV content
- no-record scenarios
- invalid menu choices
- month and report filtering errors

## Testing

The project includes unit tests covering key scenarios, including:

- valid CSV creation
- malformed file repair
- monthly report generation
- positive amount validation
- common input normalization

Run the tests with:

```bash
python -m unittest -v
```

## Example workflow

1. Start the program.
2. Add transactions for income and expenses.
3. View the transaction list.
4. Check the summary to see total income, expense, and balance.
5. Generate a monthly or category report for a specific period.

## Notes

This project is designed as a practical beginner-friendly finance tracker and can be extended later with features such as monthly budgets, data filtering, charts, or a GUI version.

Step 1: Install Python

Make sure Python 3 is installed on your computer.

Check the installation using:

python --version

Step 2: Open the Project Folder

Open the project folder in VS Code, PyCharm, or another
Python-supported editor.

Step 3: Run the Program

Use:

python expense_tracker.py

🔮 Future Improvements

The project can be improved further by adding:

Login and user authentication

Graphs and charts

Budget limits

Savings goals

Export reports to PDF or Excel

SQLite/MySQL database support

Better graphical user interface

Search and filter transactions

Automatic monthly summaries

👨‍💻 Project Information

Project Name: Personal Expense Tracker
Language: Python
Project Type: Mini Project
Interface: Menu-driven console application
Data Storage: CSV file / File Handling

📚 Learning Outcomes

Through this project, we learn how to:

Work with Python functions

Use loops and conditional statements

Handle user input

Validate data

Read and write CSV files

Perform calculations on financial data

Organize a Python project

Build a practical real-world application

📄 License

This project is created for educational and academic purposes.
