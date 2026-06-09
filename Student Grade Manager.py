name = input("Enter your name: ")
sub1 = int(input("Enter your marks in English: "))
sub2 = int(input("Enter your marks in Math: "))
sub3 = int(input("Enter your marks in Science: "))

total_marks = sub1+sub2+sub3
print("Total marks: ", total_marks)
avg_marks = total_marks/3
print("Average marks: ", avg_marks)

if avg_marks >= 90 :
   grade = "A"
elif avg_marks >= 80:
    grade = "B"
elif avg_marks >= 70 :
    grade = "C"
elif avg_marks >= 60:
    grade = "D"
else :
   grade = "F"

print("______Report______")

print(f"Name is: {name}\n total marks are: {total_marks}\n average marks : {avg_marks:.2f}\n grade is {grade}")


    