class Car :
    def __init__ (self,brand, color, fuel) :
        self.brand = brand
        self.color = color
        self.fuel = fuel

    def start(self) :
         print(f"{self.brand},{self.color} is starting")

    def drive(self) :
        if self.fuel >= 10 :
            self.fuel -= 10
            print(f"{self.brand} is driving. Fuel left: {self.fuel}")
        else :
            print("Not enough fuel to drive")

    def refuel (self, amount) :
        self.fuel = self.fuel + amount
        print (f"Car refueled. fuel is now {self.fuel}")

class ElectricCar(Car) :
    def __init__ (self,brand,color,battery) :
        super().__init__(brand,color,0)
        self.battery = battery
    
    def drive(self):
        if self.battery >= 10:
            self.battery -= 10
            print(f"{self.brand} is driving. Battery Left: {self.battery}")
        else :
            print("Not enough battery")

    def charge(self,amount):
     
        self.battery = self.battery + amount
        if self.battery > 100 :
            self.battery = 100
        print(f"{self.brand} charged. Battery now: {self.battery}")

brand = input("Enter car brand: ")
color = input("Enter car color: ")
fuel = int(input("Enter fuel: "))

car1 = Car(brand,color,fuel)



brand = input("Enter car brand: ")
color = input("Enter car color: ")
battery = int(input("Enter Battery: "))
car2 = ElectricCar(brand,color,battery)


while True :
    print("1. Drive Car")
    print("2. Refuel Car")
    print("3. drive Electric Car")
    print("4. Charge Electric Car")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        car1.drive()

    elif choice == "2" :
        amount = int(input("Enter the fuel amount: "))
        car1.refuel(amount)
    
    elif choice =="3" :
        car2.drive()

    elif choice =="4" :
        amount = int(input("Enter the charge amount: "))
        car2.charge(amount)

    elif choice == "5" :
        print("Exiting program. ")
        break
    