class Car :
    def __init__(self, brand, color) :
        self.brand = brand
        self.color = color
        
    def start(self) :
        print(self.color, self.brand,"is starting")

car1 = Car("Toyota", "Red")
car2 = Car("Tesla", "Black")

car1.start()
car2.start()