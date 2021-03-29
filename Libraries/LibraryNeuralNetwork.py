# Libraries import
from random import uniform
import math
import numpy as np

# Constants
NEURAL_NETWORK_SIZE = [3, 5, 5, 5, 3]

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
    def display(self):
        temp = ["Neuron(id={}, value={}".format(self.id, self.value), "\tbias={}".format(self.bias), "\tweights={})".format(self.weights)]
        return temp
    def evaluate(self, inputs):
        self.value = sigmoid(np.sum(self.weights * inputs) + self.bias)
    def populate(self, size):
        if size == 0:
            self.bias = None
            self.weights = []
        else:
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

    def assignValue(self, values):
        for n,v in zip(self.neurons, values):
            n.value = v
    def copy(self, layer):
        for n in layer.neurons:
            self.neurons.append(Neuron(neuron=n))
    def display(self):
        result = ["Layer(id={}".format(self.id)]
        for n in self.neurons:
            for elt in n.display():
                result.append("\t" + elt)
        return result
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

class NeuralNetwork:
    objectCounter = 0
    def __init__(self, neural=None):
        self.fitness = -10
        self.id = NeuralNetwork.objectCounter
        self.layers = []
        self.nbrWeights = 0
        for i in range(1, len(NEURAL_NETWORK_SIZE)):
            self.nbrWeights += NEURAL_NETWORK_SIZE[i-1] * NEURAL_NETWORK_SIZE[i]
        if neural != None:
            self.copy(neural)
        else:
            self.populate()
        NeuralNetwork.objectCounter += 1
    def __str__(self):
        return "NeuralNetwork(id={}, fitness={})".format(self.id, self.fitness)
    def __repr__(self):
        temp = "NeuralNetwork(id={}, fitness={},\n\t".format(self.id, self.fitness)
        for l in self.layers:
            temp += repr(l) + ",\n\t"
        temp += ")"
        return temp
    
    def assignInput(self, values):
        self.layers[0].assignValue(values)
    def copy(self, neural):
        for l in neural.layers:
            self.layers.append(Layer(layer=l))
    def display(self):
        temp = ["NeuralNetwork(id={}".format(self.id)]
        for l in self.layers:
            for elt in l.display():
                temp.append("\t" + elt)
        result = ""
        for elt in temp:
            result += elt + "\n"
        return result
    def evaluate(self, inputs):
        if len(inputs) != NEURAL_NETWORK_SIZE[0]:
            print("NeuralNetwork.evaluate(): Error, inputs dimension mismatch input layer of neural network")
        else:
            self.assignInput(inputs)
            for i in range(1, len(self.layers)):
                self.layers[i].evaluate(self.layers[i-1].getState())
        return self.layers[-1].getState()
    def populate(self):
        self.layers.append(Layer(dimension=(NEURAL_NETWORK_SIZE[0], 0)))
        for i in range(1, len(NEURAL_NETWORK_SIZE)):
            self.layers.append(Layer(dimension=(NEURAL_NETWORK_SIZE[i], NEURAL_NETWORK_SIZE[i-1])))