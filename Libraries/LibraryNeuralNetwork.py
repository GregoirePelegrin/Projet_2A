# External libraries import
from random import uniform
import math
import numpy as np

# Neural Network related constants
NEURAL_NETWORK_SIZE = [5]

class Neuron:
    objectCounter = 0
    def __init__(self, neuron=None):
        self.id = Neuron.objectCounter
        self.value = 0

        if neuron == None:
            self.biaises = np.array([])
            self.weights = np.array([])
            # TODO: Generate random weights and biaises
        else:
            self.biaises = neuron.biaises.copy()
            self.weights = neuron.weights.copy()

        Neuron.objectCounter += 1
    def __str__(self):
        return "Neuron({})".format(self.id)
    def __repr__(self):
        return "Neuron({}\n\t{}\n\t{})".format(self.id, self.biaises, self.weights)