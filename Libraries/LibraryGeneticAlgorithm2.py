from random import randint
from random import uniform

from Libraries import LibraryGame as lg
from Libraries import LibraryNeuralNetwork as lnn

class GeneticAlgorithm():
	def __init__(self, cf=1000000, ni=10, pc=10, pm=10):
		self.COEFF_FITNESS = cf
		self.NUMBER_INDIVIDUALS = ni
		self.PROBABILITY_CROSSOVER = pc
		self.PROBABILITY_MUTATION = pm

		self.bestNeural = None
		self.rankingNeural = []
		self.nextGen = []

		if self.NUMBER_INDIVIDUALS%10 != 0:
			print("Error on the number of elts per generation, must be a \
				>10 and a multiple of 10! (You've input {})".format(
				self.NUMBER_INDIVIDUALS))
	def __str__(self):
		return "GeneticAlgorithm(cf={}, ni={}, pc={}, pm={})".format(self.COEFF_FITNESS, 
			self.NUMBER_INDIVIDUALS, self.PROBABILITY_CROSSOVER, self.PROBABILITY_MUTATION)

	def evaluate(self, individuals):
		self.rankingNeural.clear()
		self.rankingNeural.append(individuals[0].nn)
		best, mean = individuals[0].nn.fitness, 0
		for individual in individuals:
			temp = individual.nn.fitness
			index = 0
			while index < len(self.rankingNeural) and temp < self.rankingNeural[index].fitness:
				index += 1
			self.rankingNeural.insert(index, individual.nn)
			mean += temp
		best = self.rankingNeural[0].fitness
		counter = 0
		for individual in individuals:
			if individual.nn.fitness == best:
				counter += 1
		mean /= len(individuals)
		return best, mean, self.rankingNeural[0], counter
	def evolve(self, individuals):
		self.nextGen.clear()
		self.nextGen.append(lnn.NeuralNetwork(neural=self.rankingNeural[0]))
		# Next gen generation
		self.crossing(self.selection())
		self.mutate()
		self.populate()
		# Next gen attribution + Reinitialisation of cars
		for individual, neural in zip(individuals, self.nextGen):
			individual.nn = neural
			individual.reinitialization()
		return individuals
	def fitness(self, individuals):
		for individual in individuals:
			individual.nn.fitness = individual.totalDistance + self.COEFF_FITNESS*individual.checkpointPassedCounter

	def crossing(self, individuals):
		toCross = individuals[:]
		while len(toCross) > 0:
			temp_indPar1 = randint(0, len(toCross)-1)
			temp_indPar2 = randint(0, len(toCross)-1)
			while temp_indPar1 == temp_indPar2:
				temp_indPar2 = randint(0, len(toCross)-1)

			if randint(0, 100) < self.PROBABILITY_CROSSOVER:
				temp_indLay = randint(1, len(toCross[temp_indPar1].layers)-1)
				temp_lay = toCross[temp_indPar1].layers[temp_indLay]
				toCross[temp_indPar1].layers[temp_indLay] = toCross[temp_indPar2].layers[temp_indLay]
				toCross[temp_indPar2].layers[temp_indLay] = temp_lay
			else:
				self.nextGen.append(toCross[temp_indPar1])
				self.nextGen.append(toCross[temp_indPar2])

			if len(toCross)%2 != 0:
				del toCross[temp_indPar1]
			else:
				if temp_indPar1 < temp_indPar2:
					del toCross[temp_indPar2]
					del toCross[temp_indPar1]
				else:
					del toCross[temp_indPar1]
					del toCross[temp_indPar2]
	def mutate(self):
		for neural in self.nextGen:
			if randint(0, 100) < self.PROBABILITY_MUTATION:
				temp_indLay = randint(1, len(neural.layers)-1)
				temp_indNeu = randint(1, len(neural.layers[temp_indLay].neurons)-1)
				temp_indWei = randint(1, len(neural.layers[temp_indLay].neurons[temp_indNeu].weights)-1)
				neural.layers[temp_indLay].neurons[temp_indNeu].weights[temp_indWei] = uniform(-1, 1)
		return None
	def populate(self):
		while len(self.nextGen) < self.NUMBER_INDIVIDUALS:
			self.nextGen.append(lnn.NeuralNetwork(size=[4,16,32,16,4]))
	def selection(self):
		temp_selec = []
		for i in range(1,int(8*self.NUMBER_INDIVIDUALS/10)):
			temp_selec.append(self.rankingNeural[i])
		return temp_selec
