import random

pool = "0123456789"

pin_length = int(input("Enter pin length: "))

pin = ""
while len(pin) < pin_length:
    pin += random.choice(pool)
print(pin)
