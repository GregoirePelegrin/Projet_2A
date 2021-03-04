from random import uniform
import math

# Activation functions
def relu(x):
	return max(0, x)
def sigmoid(x):
	return 1/(1+math.exp(-x))

# Neuron class
class Neuron():
	def __init__(self, weigths=[]):
		self.value = 0
		self.weights = weigths							# These are the input weights for this neuron
	def __str__(self):
		return "Neuron({})".format(self.value)
	def __repr__(self):
		return "{}".format(self.weights)
	def evaluate(self, inputs):
		temp = 0
		for i,w in zip(inputs, self.weights):
			temp += w*i 								# n*True = n
		self.value = sigmoid(temp)
	def populate(self, pop):
		self.weights = []
		for i in range(pop):
			self.weights.append(uniform(-1, 1))
# Layer class
class Layer():
	def __init__(self, size=0, weights=[]):
		self.neurons = []
		self.size = 0
		if size == 0 and len(weights) == 0:
			print("Error, please input a size OR an array of weights")
			return None
		elif size != 0:
			self.size = size
			self.neurons = []
			for i in range(self.size):
				self.neurons.append(Neuron())
		else:
			self.size = len(weights)
			self.neurons = []
			for w in weights:
				self.neurons.append(Neuron(w))
	def __str__(self):
		temp = []
		for n in self.neurons:
			temp.append(n.value)
		return "Layer({})".format(temp)
	def __repr__(self):
		temp = ""
		for n in self.neurons:
			temp += n.__repr__() + "\n"
		return temp
	def assign(self, values):
		for n,v in zip(self.neurons, values):
			n.value = v
	def evaluate(self, inputs):
		for n in self.neurons:
			n.evaluate(inputs)
	def getState(self):
		temp = []
		for n in self.neurons:
			temp.append(n.value)
		return temp
	def populate(self, pop):
		for n in self.neurons:
			n.populate(pop)
# NeuralNetwork class
class NeuralNetwork():
	def __init__(self, size=[], weights=[]):
		""" size must be a [int]: len(size) = nbrHiddenLayers+2 (i/o), size[n] being the nbr of Neurons on the nth layer
			weights must be a [[[int]]]: len(weights) = nbrHiddenLayers+1, weights[n] being the weights of the nth layer"""
		if len(size) == 0 and len(weights) == 0:
			print("Error, please input a pair of size OR an array of weights")
			return None
		self.layers = []
		self.size = []
		if len(size) != 0:
			self.size = size
			for i in range(len(self.size)):
				self.layers.append(Layer(self.size[i]))
				if i != 0:
					self.layers[i].populate(self.size[i-1])
		else:
			self.size = len(weights)
			for i,w in enumerate(weights):
				self.layers.append(Layer(w))
				if i != 0:
					self.layers[i].populate(len(weights[i-1]))
	def __str__(self):
		temp = "NeuralNetwork:\n"
		for l in self.layers:
			temp += "\t" + str(l) + "\n"
		return temp
	def __repr__(self):
		temp = ""
		for l in self.layers:
			temp += l.__repr__() + "\n"
		return temp
	def evaluate(self, inputs):
		self.layers[0].assign(inputs)
		for i in range(1, len(self.layers)):
			self.layers[i].evaluate(self.layers[i-1].getState())
		return self.layers[-1].getState()