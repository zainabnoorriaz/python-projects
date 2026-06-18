#1
for i in range(6) :
    for j in range (6) :
        print("*", end = " ")
    print()
#2
for i in range(1,6):
    for j in range(1, i+1) :
        print("*", end = " ")
    print()
#3
for i in range(1,6) :
    for j in range(6, i-1, -1):
        print("*", end = " ")
    print()

for i in range(5, 0, -1):
    for j in range (1, i+1):
        print("*", end = " ")
    print()

#4 
for i in range (1,6) :
    for j in range(1, i+1):
        print("*", end = " ")
    print()
for i in range (5,0,-1) :
    for j in range(1, i+1) :
        print("*", end = " ")
    print()

#5
for i in range (1,5):
    for b in range(5 - i):
        print(" ", end = " ")
    for j in range( 2*i-1 ):
        print("*", end = " ")
    print()
for i in range(4,0,-1) :
    for b in range(5-i):
        print(" ", end = " ")
    for j in range (2*i-1): 
        print("*", end = " ")
    print()
                   
#6
import turtle

t = turtle.Turtle()

for i in range(5):
    t.forward(200)
    t.right(144)

turtle.done()