expenses = []

def add_expense() :
    name = input("Enter item name :")
    price = int(input("Enter the price of the item: "))
    category = input("Enter the category of the item: ")
    expenses.append([name,price,category])

    with open("expense.csv", "a") as file:
        file.write(name + "," + str(price) + "," + category + "\n")

def view_expense() :
    for i, expense in enumerate (expenses, start = 1) :
        print(i, expense[0],"-" ,expense[1], "-", expense[2] + "\n")

def total_expense() :
    total = 0
    for expense in expenses :
        total += expense[1]
    return total
def category_total():
    totals = {}

    for expense in expenses:
        name = expense[0]
        price = expense[1]
        category = expense[2]

        if category in totals:
            totals[category] += price
        else:
            totals[category] = price

    for category, total in totals.items():
        print(category, ":", total)

def load_expense () :
    
    try:
        with open("expense.csv", "r") as file:
          for line in file :
            name, price, category = line.strip().split(",")
            expenses.append([name, int(price), category])
    except FileNotFoundError:
        pass

def update_expense():
    expense_number = int(input("Enter expense number to update: "))
    index = expense_number - 1

    new_name = input("Enter new item: ")
    new_price = int(input("Enter new price of item: "))
    new_category = input("Enter new category of item: ")

    expenses[index] = [new_name, new_price, new_category]
    with open ("expense.csv", "w") as file:
        for expense in expenses:
            file.write(expense[0] + "," + str(expense[1]) + "," + expense[2] + "\n")
        
def delete_expense() :
    item_to_delete = int(input("Enter the item to delete: "))
    index = item_to_delete - 1
    expenses.pop(index)

    with open ("expense.csv", "w") as file:
        for expense in expenses:
            file.write(expense[0] + "," + str(expense[1]) + "," + expense[2]+ "\n")



print("______MENU________")
print("1. Add Expenses")
print("2. View Expenses")
print("3. Total Expense")
print("4. Category total")
print("5. Update Expense")
print("6. Delete Expense")
print("7. Exit")
load_expense()
while (True) :
    choice = int(input("Enter your choice: "))
    if choice == 7:
        break
    elif choice == 1:
        add_expense()

    elif choice == 2:
        view_expense()
    elif choice == 3:
        print("Total expense is: ", total_expense())
    elif choice == 4:
        category_total() 
    elif choice == 5:
        update_expense()
    elif choice == 6:
        delete_expense()
    else :
        print("Invalid Choice")