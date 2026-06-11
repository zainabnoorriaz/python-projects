students = []
def add_student():
    name = input("What is student name?").rstrip()
    students.append(name)
def view_students():
    print("The students are: ")
    for student in students :
          
     print(student)

def search_student(name):
   return name in students

def delete_student(name):
   if search_student(name):
      students.remove(name)
      return True
   else:
      return False

while(True):
    print("1. Add student")
    print("2. View student")
    print("3. Search student")
    print("4. Delete Student")
    print("5. Exit")
    
    choice = int(input("Enter your choice: "))
    if choice == 5:
        break
    elif choice in [1,2,3,4] :
       if choice == 1:
          add_student()

        
       elif choice == 2:
          view_students()
       elif choice == 3:
          name = input("Enter name to search: ")
          result = search_student(name)
          if result:
             print("Found")
          else :
             print("Not found")
       elif choice == 4 :
          name = input("Enter name to delete: ") 
          if delete_student(name):
             print("Success")
          else :
             print("Not found")
        
    else :
     print("Invalid choice")

