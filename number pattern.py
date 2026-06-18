for i in range (1, 6) :
    for j in range (1, i + 1) :
        print(j, end = " ")
    print()


for i in range (5,0,-1) :
    for j in range (1, i+1) :
        print(j, end = " ")
    print()


for i in range (1,6) :
    for j in range (5,i-1,-1) :
        print(j, end = " ")
    print()

#pyramid 
for i in range(1,6) :
    for b in range(5 - i):
        print(" ", end = " ")
    for j in range(1, i+1):
        print(j, end=" ")
    for j in range (i - 1, 0, -1):
        print(j, end = " ")
    print()