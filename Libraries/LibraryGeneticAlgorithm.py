from random import randint
from random import uniform

import Libraries.LibraryGame as lg

class GeneticAlgorithm():
	def __init__(self, cf=1000000, ni=10, pc=10, pm=10):
		self.COEFF_FITNESS = cf
		self.NUMBER_INDIVIDUALS = ni
		self.PROBABILITY_CROSSOVER = pc
		self.PROBABILITY_MUTATION = pm

		self.nextGen = []

		if self.NUMBER_INDIVIDUALS%10 != 0:
			print("Error on the number of elts per generation, must be a >10 and a multiple of 10! (You've input {})".format(
				self.NUMBER_INDIVIDUALS))
	def __str__(self):
		return "GeneticAlgorithm(cf={}, ni={}, pc={}, pm={})".format(self.COEFF_FITNESS, 
			self.NUMBER_INDIVIDUALS, self.PROBABILITY_CROSSOVER, self.PROBABILITY_MUTATION)

	def evolve(self, individuals):
		currentGen = individuals[:]
		self.crossover(self.selection(currentGen))
		self.mutate()
		self.populate()
		return self.nextGen

	def crossover(self, individuals):
		while len(individuals) != 0:
			r1 = randint(0, len(individuals)-1)
			r2 = randint(0, len(individuals)-1)
			while r1 == r2:
				r2 = randint(0, len(individuals)-1)
			p1 = individuals[r1]
			p2 = individuals[r2]
			if len(individuals)%2 != 0:
				if self.fitness(individuals[r1]) > self.fitness(individuals[r2]):
					del individuals[r2]
				else:
					del individuals[r1]
			else:
				if r2 > r1:
					del individuals[r2]
					del individuals[r1]
				else:
					del individuals[r1]
					del individuals[r2]
			if randint(0, 100) >= self.PROBABILITY_CROSSOVER:
				self.nextGen.append(p1)
				self.nextGen.append(p2)
			else:
				dim = len(p1.nn.layers)
				ind_lay = randint(1, dim-1)
				temp_lay = p1.nn.layers[ind_lay]
				p1.nn.layers[ind_lay] = p2.nn.layers[ind_lay]
				p2.nn.layers[ind_lay] = temp_lay
				self.nextGen.append(p1)
				self.nextGen.append(p2)
	def fitness(self, individual):
		return individual.totalDistance + self.COEFF_FITNESS*individual.checkpointPassedCounter
	def mutate(self):
		for individual in self.nextGen:
			if randint(0, 100) < self.PROBABILITY_MUTATION:
				lay = randint(1, len(individual.nn.layers)-1)
				neu = randint(0, len(individual.nn.layers[lay].neurons)-1)
				wei = randint(0, len(individual.nn.layers[lay].neurons[neu].weights)-1)
				individual.nn.layers[lay].neurons[neu].weights[wei] += uniform(-0.005, 0.005)
	def populate(self):
		for i in range(int(self.NUMBER_INDIVIDUALS / 10)):
			self.nextGen.append(lg.Car)
	def selection(self, individuals):
		currentGen = individuals[:]
		sortedList = []
		toCross = []
		for index, individual in enumerate(individuals):
			sortedList.append([index, self.fitness(individual)])
		sortedList = sorted(sortedList, key=lambda fit: fit[1])
		for i in range(self.NUMBER_INDIVIDUALS):
			currentGen.append(individuals[sortedList[i][0]])
		index = 0
		while index < self.NUMBER_INDIVIDUALS/5:
			index += 1
			self.nextGen.append(currentGen[0])
			toCross.append(currentGen[0])
			del currentGen[0]
		for i in range(int(7*self.NUMBER_INDIVIDUALS/10)):
			r = randint(0, len(currentGen)-1)
			toCross.append(currentGen[r])
			del currentGen[r]
		return toCross