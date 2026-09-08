Personal Expense Tracker

📌 Project Overview

The Personal Expense Tracker is a Python-based mini project designed
to help users record, organize, and monitor their daily income and
expenses.

The application provides a simple menu-driven interface where users
can manage their financial transactions and view useful summaries of
their spending and income.

The project uses file handling to store financial records so that
the data can be maintained even after the program is closed.

🎯 Aim

To develop a simple Python-based Personal Expense Tracker that allows
users to:

Add financial transactions

View saved transactions

Update existing transactions

Delete transactions

Calculate total income

Calculate total expenses

Calculate current balance

Generate monthly and category-wise expense reports

Store financial records safely using file handling

✨ Features

1. Add Transaction

Users can add a new transaction by entering:

Date

Type --- Income or Expense

Category

Amount

The program validates the entered information before saving it.

2. View Transactions

Displays all recorded income and expense transactions in an organized
format.

3. Update Transaction

Allows users to modify the details of an existing transaction.

4. Delete Transaction

Allows users to remove an unwanted transaction from the records.

5. Financial Summary

The application calculates:

Total Income

Total Expenses

Current Balance

Balance = Total Income - Total Expenses

6. Expense Reports

Users can generate reports such as:

Monthly expense report

Category-wise expense report

These reports help users understand where their money is being spent.

7. Data Storage

Financial records are stored using a file such as expenses.csv.

🛠️ Technologies Used

Python 3

CSV File Handling

Python Functions

Conditional Statements

Loops

Lists / Dictionaries

Exception Handling

Date Validation

📁 Project Structure

Personal-Expense-Tracker/
│
├── main.py
├── expenses.csv
└── README.md

Files Description

File                   Description

expense_tracker.py   Main Python program
expenses.csv         Stores income and expense records
README.md            Project documentation

📋 Transaction Format

The CSV file stores records using the following columns:

Date, Type, Category, Amount

Example:

2026-09-01,Income,Salary,25000
2026-09-02,Expense,Food,300
2026-09-03,Expense,Transport,150
2026-09-04,Expense,Shopping,1000

🧭 Main Menu

The application provides a menu similar to:

=================================
      PERSONAL EXPENSE TRACKER
=================================

1. Add Transaction
2. View Transactions
3. Update Transaction
4. Delete Transaction
5. Reports
6. Exit

Enter your choice:

The user selects an option, performs the required operation, and then
returns to the main menu.

🔄 Basic Working

Start the program.

Check whether expenses.csv exists.

If the file does not exist, create it with the required headings.

Display the main menu.

Ask the user to select an option.

Perform the selected operation.

Validate user input wherever required.

Save changes to the CSV file.

Display the result to the user.

Return to the main menu.

Continue until the user selects Exit.

✅ Input Validation

The program checks that:

Date is entered in the correct format.

Transaction type is either Income or Expense.

Amount is a positive number.

Required information is not left empty.

Menu choice is a valid option.

If invalid data is entered, the program displays an error message and
asks the user to enter the information again.

📊 Example

Suppose the user enters:

Income:
Salary = ₹25,000

Expenses:
Food = ₹2,000
Transport = ₹1,000
Shopping = ₹3,000

Then:

Total Income   : ₹25,000
Total Expenses : ₹6,000
Current Balance: ₹19,000

🚀 How to Run

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
