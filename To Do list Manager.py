tasks = []

def add_task() :
 task = input("Enter task to perform: ")
 tasks.append(task)
 save_tasks()

def view_task():
    print("View Tasks")
    for i, task in enumerate(tasks, start=1):
        print(i, task)

def search_task(task) :
 return task in tasks

def update_task():
 task_number = int(input("enter task number to update: "))
 index = task_number - 1
 update_with = input("Enter what to update with? ").rstrip()
 tasks[index] = update_with
 save_tasks()



def delete_task() :
 task_to_remove = int(input("Enter task to remove:  "))
 index = task_to_remove - 1
 del tasks[index]
 save_tasks()

def save_tasks() :
 with open("tasks.txt", "w") as file:
  for task in tasks:
   file.write(task + "\n")

try:
    with open("tasks.txt", "r") as file:
        lines = file.readlines()
        tasks = [line.strip() for line in lines]
except FileNotFoundError:
    tasks = []


while (True) :
 print("------Menu------")
 print("1. Add task")
 print("2. View task")
 print("3. Search task")
 print("4. Delete task")
 print("5. Update task")
 print("6. Exit")

 choice = input("Enter your choice: ").strip()


 if choice == '6':
  break

 elif choice == '1':
   add_task()

 elif choice == '2':
   print("View task")
   view_task()

 elif choice == '3':
   name = input("Enter task to search:")
   result = search_task(name)
   if result:
    print("Found")
   else:
    print("Not Found")
    
 elif choice == '4':
   delete_task()

 elif choice == '5':
   update_task()

 else:
  print("Invalid choice")