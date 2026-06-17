import random 
rounds = int(input("How many rounds do you want to play? "))

user_score = 0
computer_score = 0
for i in range (rounds) :

    print(f"\nRound {i+1}")
    user_roll = random.randint(1,6)
    computer_roll = random.randint(1,6)

    print("User rolled:", user_roll)
    print("Computer rolled:", computer_roll)

    if user_roll > computer_roll:
        user_score += 1
        print("User wins this round")
    elif computer_roll > user_roll :
        computer_score += 1
        print("computer wins this round")
    else :
        print("Tie")
print("\nFINAL RESULT")

if user_score > computer_score :
    print("User wins")
elif user_score == computer_score:
    print("This is tie")

else :
    print("Computer wins")
