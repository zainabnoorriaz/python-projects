import random
pool = "0123456789"

pin_length = int(input("Enter pin length: "))

pin = ""

while len(pin) < pin_length :
    pin += random.choice(pool)

correct = False
for _ in range (3):
   user_guess = input("Enter your guess: ")
   if user_guess == pin :
    print("correct")
    correct = True
    break

   else :
    print("wrong guess")

if not correct :
  print("Max attempt reached")
