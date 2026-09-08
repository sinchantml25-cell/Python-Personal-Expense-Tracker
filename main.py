print("      *******PYTHON MINI PROJECT********")
print("        Python Personal Expense Tracker")

transactions = []

while True:
    print("\n1. Add Transaction\n2. View Transactions\n3. Update Transaction")
    print("4. Delete Transaction\n5. View Summary\n6. Generate Report\n7. Exit")
    choice = input("Enter your choice: ").strip()

    if choice == "1":
        try:
            amount = float(input("Amount: "))
            description = input("Description: ").strip()
            category = input("Category: ").strip() or "Other"
            transactions.append({"amount": amount, "description": description,
                                 "category": category})
            print("Transaction added.")
        except ValueError:
            print("Amount must be a number.")
    elif choice == "2":
        if not transactions:
            print("No transactions found.")
        for number, transaction in enumerate(transactions, 1):
            print(f"{number}. {transaction['description']} - "
                  f"${transaction['amount']:.2f} ({transaction['category']})")
    elif choice in ("3", "4"):
        if not transactions:
            print("No transactions found.")
            continue
        try:
            number = int(input("Transaction number: ")) - 1
            transaction = transactions[number]
            if choice == "4":
                transactions.pop(number)
                print("Transaction deleted.")
            else:
                transaction["description"] = input("New description: ").strip()
                transaction["category"] = input("New category: ").strip() or "Other"
                transaction["amount"] = float(input("New amount: "))
                print("Transaction updated.")
        except (ValueError, IndexError):
            print("Invalid transaction number or amount.")
    elif choice in ("5", "6"):
        total = sum(item["amount"] for item in transactions)
        print(f"Total expenses: ${total:.2f}")
        if choice == "6":
            print(f"Report contains {len(transactions)} transaction(s).")
    elif choice == "7":
        print("Thank you for using Personal Expense Tracker!")
        break
    else:
        print("Invalid choice.")
