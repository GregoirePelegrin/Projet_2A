import LibraryNeuralNetwork.py as lnn

class Car():
    def __init__(self):
        self.acceleration = 0
        self.orientation = 90
        self.x = 350
        self.y = 150
        self.distance = 0
        self.nn = lnn.NeuralNetwork(size=[2,5,5,4])
