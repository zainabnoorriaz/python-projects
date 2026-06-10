print("1. Add")
print("2.subtract")

choice = int(input("Enter your choice"))

a = int(input("enter a:"))
b = int(input("Enter b:"))

if choice == 1:
    result = a + b
    print(result)

elif choice == 2:
    result = a - b
    print(result)