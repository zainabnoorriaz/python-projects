while(True) :

    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Exit")

    choice = int(input("Enter your choice: "))
    if choice == 5:
        break
    elif choice in [1,2,3,4] :
      a = int(input("Enter value of a: "))
      b = int(input("Enter value of b: "))

      if choice == 1:
         result = a + b
         print("Sum is:", result)

      elif choice == 2:
         result = a - b
         print ("Difference is:", result)
      elif choice == 3:
         result = a * b
         print("Product is:", result)
      elif choice == 4:
         result = a / b
         print("Division is:", result)
    else :
       print("Invalid choice")
    
