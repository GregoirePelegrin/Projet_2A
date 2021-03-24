# External libraries import
from random import uniform
import math
import numpy as np

# Constants
NEURAL_NETWORK_SIZE = [5]

# Activation functions
def identity(x):
    return x
def relu(x):
    return max(0, x)
def sigmoid(x):
    return 1/(1+math.exp(-x))

# Classes
class Neuron:
    objectCounter = 0
    def __init__(self, dimension=None, neuron=None):
        self.id = Neuron.objectCounter
        self.value = 0
        if dimension != None:
            self.populate(dimension)
        elif neuron != None:
            self.copy(neuron)
        else:
            print("Neuron.__init__(): Error, must specify dimension or neuron")
        Neuron.objectCounter += 1
    def __str__(self):
        return "Neuron(id={}, value={})".format(self.id, self.value)
    def __repr__(self):
        return "Neuron(id={}\n\tbias={}\n\tweights={})".format(self.id, self.bias, self.weights)

    def copy(self, neuron):
        self.bias = neuron.bias
        self.weights = neuron.weights.copy()
    def evaluate(self, inputs):
        self.value = sigmoid(np.sum(self.weights * inputs) + self.bias)
    def populate(self, size):
        self.bias = uniform(-1, 1)
        self.weights = 2*np.random.rand(size)-1

class Layer:
    objectCounter = 0
    def __init__(self, dimension=None, layer=None):
        self.id = Layer.objectCounter
        self.neurons = []
        if dimension != None:
            self.populate(dimension)
        elif layer != None:
            self.copy(layer)
        else:
            print("Layer.__init__(): Error, must specify dimension or layer")
        Layer.objectCounter += 1
    def __str__(self):
        return "Layer(id={})".format(self.id)
    def __repr__(self):
        temp = "Layer(id={},\n\t".format(self.id)
        for n in self.neurons:
            temp += repr(n) + ",\n\t"
        temp += ")"
        return temp

    def copy(self, layer):
        for n in layer.neurons:
            self.neurons.append(Neuron(neuron=n))
    def evaluate(self, inputs):
        for n in self.neurons:
            n.evaluate(inputs)
    def getState(self):
        temp = np.array([])
        for n in self.neurons:
            temp = np.append(temp, [n.value])
        return temp
    def populate(self, dimension):
        for i in range(dimension[0]):
            self.neurons.append(Neuron(dimension=dimension[1]))
# TODO: NeuralNetwork class