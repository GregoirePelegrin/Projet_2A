import Libraries.LibraryNeuralNetwork as lnn


class Car():
    counter = 0
    def __init__(self, _id=None):
        if _id != None:
            self.id = _id
        else:
            self.id = Car.counter
        self.alive = True
        self.visible = True
        self.selected = False
        self.speed = 10
        self.orientation = 90
        self.x = 350
        self.y = 80
        self.lastX = 0
        self.lastY = 0
        self.totalDistance = 0
        self.totalDistanceLast = 0
        self.nn = lnn.NeuralNetwork()
        self.orientedCarImg = None
        Car.counter += 1
    def __str__(self):
        return "Car({})".format(self.id)

    def reinitialization(self):
        self.alive = True
        self.visible = True
        self.acceleration = 0
        self.orientation = 90
        self.x = 350
        self.y = 80
        self.nn.fitness = 0
        self.totalDistanceLast = self.totalDistance
        self.totalDistance = 0

    def copy(self):
        new_car = Car()
        new_car.nn = self.nn
        new_car.speed = self.speed
        new_car.x = self.x
        new_car.y = self.y
        new_car.orientation = self.orientation
        new_car.selected = self.selected
        new_car.orientedCarImg = self.orientedCarImg
        new_car.totalDistance = self.totalDistance
        new_car.totalDistanceLast = self.totalDistanceLast
        return new_car