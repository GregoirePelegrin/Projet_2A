import Libraries.LibraryNeuralNetwork as lnn

class Car():
    def __init__(self, id):
        self.id = id
        self.alive = True
        self.acceleration = 0
        self.orientation = 90
        self.x = 350
        self.y = 150
        self.totalDistance = 0
        self.nn = lnn.NeuralNetwork(size=[2,5,5,4])
        self.nextCheckpoint = 2
        self.orientedCarImg = None
        self.checkpointPassedCounter = 0