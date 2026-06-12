contacts = []

def add_contacts () :
    name = input("Enter your name: ")
    email = input("Enter your email")
    contacts.append([name,email])

def view_contacts () :
    for i, contact in enumerate(contacts, start = 1) :
        name = contact[0]
        email = contact[1]
        print(i, name + "|" + email)

def search_contacts ():
    name = input("Enter name to search: ")

    for contact in contacts:
        if contact[0] == name:
            print("Found", contact)
            return
        
    print("Contact not found")

def delete_contact() :
    name = input("Enter a name to delete: ")
    for i, contact in enumerate(contacts):
        if contact[0] == name:
            del contacts[i]
            return
        
    print("Contact not found")

def update_contacts() :
    contact_to_update = int(input("Enter contact to update: "))
    index = contact_to_update - 1
    new_name = input("Enter what name to update with: ")
    new_email = input("Enter email to update with: ")
    if 0 <= index < len(contacts):
     contacts[index] = [new_name,new_email]
    else :
        print("Invalid contact")

print("____list____")
print("1. Add")
print("2. View")
print("3. Search")
print("4. Delete")
print("5. Update")
print("6. Exit")
while(True):
 choice = input("Enter your choice : ")
 if choice == "6":
    break
 elif choice in ['1', '2', '3', '4', '5'] :
  if choice == '1':
    add_contacts()
  elif choice == '2':
    view_contacts()

  elif choice == '3':
    search_contacts()

  elif choice == '4':
    delete_contact()

  elif choice == '5':
    update_contacts() 
  else :
   print("Invalid contact")