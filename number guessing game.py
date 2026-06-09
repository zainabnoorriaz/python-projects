secret_number = 7
while(True) :
    guess = int(input("Enter your guess: "))
    if guess > secret_number:
        print("Too High")
    elif guess < secret_number:
        print("Too Low")
    else :
        print("Correct guess")
        break
