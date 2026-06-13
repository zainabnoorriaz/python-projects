score = 0
questions = [ ["What is the capital of Pakistan?", "Islamabad"],
             ["What is 2 + 2 = ?", '4'],
             ["What language was used in CS50?", "Python"]
             
]
for question in questions :
    print(question[0])
    answer = input("Enter your answer: ")

    if answer.lower() == question[1].lower() :
        print("Correct")
        score += 1
    else :
      print("Incorrect")

print("Total Score is: ", score)
