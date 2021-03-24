
class Car():
    counter = 0
    def __init__(self, _id=None):
        if _id != None:
            self.id = _id
        else:
            self.id = Car.counter
        self.alive = True
        self.speed = 10
        self.orientation = 90
        self.x = 350
        self.y = 80
        self.lastX = 0
        self.lastY = 0
        self.totalDistance = 0
        self.nn = None
        self.nextCheckpoint = 2
        self.orientedCarImg = None
        self.checkpointPassedCounter = 0
        Car.counter += 1
    def __str__(self):
        return "Car({})".format(self.id)

    def reinitialization(self):
        self.alive = True
        self.acceleration = 0
        self.orientation = 80
        self.x = 350
        self.y = 90
        self.nn.fitness = 0
        self.totalDistance = 0
        self.nextCheckpoint = 2
        self.checkpointPassedCounter = 0

    def copy(self):
        new_car = Car()
        new_car.nn = self.nn
        new_car.orientedCarImg = self.orientedCarImg
        return new_car