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
    def __init__(self, dimension=0, neuron=None):
        self.id = Neuron.objectCounter
        self.value = 0

        if neuron == None:
            self.populate(dimension)
        else:
            self.bias = neuron.bias
            self.weights = neuron.weights.copy()

        Neuron.objectCounter += 1
    def __str__(self):
        return "Neuron(id={}, value={})".format(self.id, self.value)
    def __repr__(self):
        return "Neuron(id={}\n\tbias={}\n\tweights={})".format(self.id, self.bias, self.weights)

    def evaluate(self, inputs):
        self.value = sigmoid(np.sum(self.weights * inputs) + self.bias)
    def populate(self, size):
        self.bias = uniform(-1, 1)
        self.weights = 2*np.random.rand(size)-1
# TODO: Layer class
# TODO: NeuralNetwork class