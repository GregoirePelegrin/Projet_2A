# External libraries import
from random import uniform
import math
import numpy as np

# Constants
NEURAL_NETWORK_SIZE = [5]

# Activation functions
def relu(x):
    return max(0, x)
def sigmoid(x):
    return 1/(1+math.exp(-x))

# Classes
class Neuron:
    objectCounter = 0
    def __init__(self, neuron=None):
        self.id = Neuron.objectCounter
        self.value = 0
        if neuron != None:
            self.copy(neuron)
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
    def initialWeighing(self, size):
        self.bias = uniform(-1, 1)
        self.weights = 2*np.random.rand(size)-1

# TODO: Tests !
class Layer:
    objectCounter = 0
    def __init__(self, dimension=0, layer=None):
        self.id = Layer.objectCounter
        self.neurons = []
        if layer != None:
            self.populate(dimension)
        else:
            self.copy(layer)
        Layer.objectCounter += 1
    def __str__(self):
        return "Layer(id={})".format(self.id)
    def __repr__(self):
        temp = "Layer(id={}\n\t".format(self.id)
        for n in self.neurons:
            temp += repr(n) + "\n\t"
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
    def populate(self, size):
        for i in range(size):
            self.neurons.append(Neuron())
    def initialWeighing(self, size):
        for n in self.neurons:
            n.initialWeighing(size)
# TODO: NeuralNetwork class