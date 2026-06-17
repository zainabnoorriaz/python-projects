import random
pool = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789!@#$%^&*()"

password_length = int(input("Enter password length:"))

password = ""
while (len(password)) < password_length :
    password += random.choice(pool)
print(password)

