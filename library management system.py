books = []

def add_book() :
    book_title = input("Enter the title of the book: ")
    book_id = int(input("Enter book id: "))
    author = input("Enter the author of the book:" )

    book = {
        "title" : book_title,
        "id" : book_id,
        "author" : author,
        "status" : "Available"
    }
    books.append(book)
    print("Book added successfully")

def view_book() :
    if not books :
        print("No books available")
    else :
       for i, book in enumerate(books, start = 1) :
         print(i, book['title'], book['id'], book['author'], book['status'])

def delete_book ():
   found = False
   book_to_delete = int(input("Enter the book id to delete:"))
   
   for book in books:
      if book_to_delete == book['id'] :
       books.remove(book)
       found = True
       break
   if found == False:
      print("Not Found")
      
def update_book():
   found = False
   book_to_update = int(input("Enter the book id to update: "))
   for book in books :
     if book_to_update == book['id'] :
        update = input("Enter what to update:")
        update_with = input("Enter what to update with:")
        book[update] = update_with
        found = True
        break
   if not found :
      print("Not Found")
    
def total_books():
   print("Total books are:", len(books))


print("_____MENU_____")

while(True) :

 print("1. Add Book")
 print("2. View Book")
 print("3. Delete Book")
 print("4. Update Book ")
 print("5. Total Books")
 print("6. Exit")

 choice = int(input("Enter your choice: "))
 if choice == 6:
    break
 elif choice in [1,2,3,4,5] :
   if choice == 1:
      add_book()
   elif choice ==2:
      view_book()
   elif choice ==3:
      delete_book() 
   elif choice == 4:
      update_book()
   elif choice == 5:
      total_books()
   else :
    print("Choice not found")

