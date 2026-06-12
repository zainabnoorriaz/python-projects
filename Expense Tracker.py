expenses = []

def add_expense() :
    name = input("Enter item name :")
    price = int(input("Enter the price of the item: "))
    expenses.append([name,price])

    with open("expense.csv", "a") as file:
        file.write(name + "," + str(price) + "\n")

def view_expense() :
    for i, expense in enumerate (expenses, start = 1) :
        print(i, expense[0],"-" ,expense[1])

def total_expense() :
    total = 0
    for expense in expenses :
        total += expense[1]
    return total

def load_expense () :
    with open("expense.csv", "r") as file:
        for line in file :
            name, price = line.strip().split(",")
            expenses.append([name, int(price)])

print("______MENU________")
print("1. Add Expenses")
print("2. View Expenses")
print("3. Total Expense")
print("4. Exit")

while (True) :
    choice = int(input("Enter your choice: "))
    if choice == 4:
        break
    elif choice == 1:
        add_expense()

    elif choice == 2:
        view_expense()
    elif choice == 3:
        print("Total expense is, ", total_expense())
    else :
        print("Invalid Choice")