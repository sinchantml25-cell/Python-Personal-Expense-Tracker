import csv
import os
import tempfile
import unittest
from unittest.mock import patch

import main


class ExpenseTrackerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = os.path.join(self.temp_dir.name, "expenses.csv")
        self.report_path = os.path.join(self.temp_dir.name, "report.txt")
        main.FILE_NAME = self.file_path
        main.REPORT_FILE = self.report_path
        main.initialize_file(self.file_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_initialize_file_creates_header(self):
        with open(self.file_path, newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader)
        self.assertEqual(header, main.CSV_COLUMNS)

    def test_read_transactions_repair_malformed_rows(self):
        with open(self.file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["10-12-2026", "Expense", "Food", "250.00", "Dinner"])
            writer.writerow(["12-04-26", "Income", "80000", "80000.0", ""])

        rows = main.read_transactions(self.file_path)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["Type"], "Expense")
        self.assertEqual(rows[1]["Date"], "12-04-2026")
        self.assertEqual(rows[1]["Category"], "80000")

    def test_generate_report_monthly_report(self):
        rows = [
            {"Date": "05-12-2026", "Type": "Income", "Category": "Salary", "Amount": "5000.00", "Description": "salary"},
            {"Date": "07-12-2026", "Type": "Expense", "Category": "Food", "Amount": "1200.00", "Description": "lunch"},
            {"Date": "10-11-2026", "Type": "Expense", "Category": "Travel", "Amount": "300.00", "Description": "train"},
        ]
        main.write_transactions(rows, self.file_path)

        with patch("builtins.input", side_effect=["1", "12-2026"]):
            main.generate_report()

        with open(self.report_path, "r", encoding="utf-8") as file:
            content = file.read()

        self.assertIn("Monthly Report - 12-2026", content)
        self.assertIn("Total Income: 5000.00", content)
        self.assertIn("Total Expense: 1200.00", content)
        self.assertNotIn("Travel", content)

    def test_invalid_and_empty_inputs_are_handled(self):
        with self.assertRaises(ValueError):
            main.format_amount("-10")

        self.assertEqual(main.normalize_transaction_type("expense"), "Expense")
        self.assertEqual(main.normalize_transaction_type("INCOME"), "Income")
        self.assertEqual(main.clean_text("   Hello   "), "Hello")
        self.assertEqual(main.clean_text("   ", "Default"), "Default")


if __name__ == "__main__":
    unittest.main()
