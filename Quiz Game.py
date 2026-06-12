score = 0
question_1 = input("What is the capital of Pakistan?")
if question_1 == "Islamabad" :
    print("Correct")
    score += 1
    
else :
    print("Incorrect")

question_2 = int(input("What is 2 + 2 = ?"))
if question_2 == 4 :
    print("Correct")
    score +=1
else :
    print("Incorrect")

question_3 = input("What language us used in CS50?")
if question_3 == "Python" :
    print("Correct")
    score +=1
else :
    print("Incorrect")

print("Final Score is: ", score)



