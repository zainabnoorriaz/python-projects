questions = [
    {
    "question" : "What is the capital of Pakistan?",
    "options" : ["Lahore", "Karachi", "Islamabad","Multan"],
    "answer" : "C"
    },
    {
     "question" : "What is 2 + 2?" ,
     "options" :['2' , '4', '6', '8'],
     "answer": "B"
    }
]
score = 0
for question in questions :
    print(question['question'])

    letters= ["A", "B", "C", "D"]

    for i, option in enumerate(question['options']):
        print(letters[i], option)
    while(True) :
      user_input= input("Enter your answer:")


      if user_input == question['answer'] :
         print("Correct!")
         score += 1
         break
      else :
        print("Incorrect")
print("Score is:", score)