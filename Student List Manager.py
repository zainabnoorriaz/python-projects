students = []

while(True):
    print("1. Add student")
    print("2. View student")
    print("3. Exit")
    
    choice = int(input("Enter your choice: "))
    if choice == 3:
        break
    elif choice in [1,2] :
       if choice == 1:

        name = input("What is student name?")
        students.append(name)
        
       elif choice == 2:
        print("The students are: ")
        for student in students :
          
         print(student)
    else :
     print("Invalid choice")




