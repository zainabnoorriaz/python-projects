while(True):
    print(" 1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Exit") 
    
    choice = int(input("Enter your choice: "))
    if choice == 5:
      break

    elif choice in [1,2,3,4]:
      
       a = int(input("Enter number 1:"))
       b= int(input("Enter number 2: "))


    

       if choice == 1 :
         result = a + b 
         print(result)
       elif choice == 2 :
          result = a - b 
          print(result)
       elif choice == 3 :
         result = a * b
         print(result)
       elif choice == 4:
         result = a/b 
         print(result)
    
    else :
      print("Invalid choice")