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

		self.fitnessSorted = []
		self.nextGeneration = []
	def __str__(self):
		return "GeneticAlgorithm(cf={}, ni={}, pc={}, pm={})".format(self.COEFF_FITNESS, 
			self.NUMBER_INDIVIDUALS, self.PROBABILITY_CROSSOVER, self.PROBABILITY_MUTATION)

	def evolve(self, individuals):
		self.fitnessSorted.clear()
		self.nextGeneration.clear()

		temp = self.fitness(individuals)
		# 2/ Ajouter les variations des best à la prochaine génération
		self.tweak(self.fitnessSorted[0])
		# 3/ Ajouter les mutations des croisements à la prochaine génération
		self.mutate(self.crossing(self.selection()))
		# 4/ Ajouter le reste (populate) à la prochaine génération
		self.populate()
		# 5/ Attribuer la nouvelle génération aux individus + les reinitialiser
		for individual, neural in zip(individuals, self.nextGeneration):
			individual.nn = neural
			individual.reinitialization()
		# 6/ Renvoie self.fitnessSorted
		return temp
	def fitness(self, individuals):
		# 1/ Calcule la fitness de tout le monde et la stocke dans l'attribut "fitness" des NN
		for individual in individuals:
			individual.nn.fitness = individual.totalDistance + self.COEFF_FITNESS*individual.checkpointPassedCounter
		# 2/ Trie les individus par fitness dans l'attribut "self.fitnessSorted"
		fitnessList = []
		for individual in individuals:
			temp = individual.nn.fitness
			index = 0
			while index < len(self.fitnessSorted) and temp < self.fitnessSorted[index].fitness:
				index += 1
			self.fitnessSorted.insert(index, individual.nn)
			fitnessList.insert(index, individual.nn.fitness)
		# 3/ Ecris le best dans un fichier
		# Not implemented yet, useful?
		return fitnessList

	def crossing(self, selections):
		toCross = selections[:]
		temp_crossing = []
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
				temp_crossing.append(toCross[temp_indPar1])
				temp_crossing.append(toCross[temp_indPar2])

			if len(toCross)%2 != 0:
				del toCross[temp_indPar1]
			else:
				if temp_indPar1 < temp_indPar2:
					del toCross[temp_indPar2]
					del toCross[temp_indPar1]
				else:
					del toCross[temp_indPar1]
					del toCross[temp_indPar2]
		return temp_crossing
	def mutate(self, crossings):
		for neural in crossings:
			if randint(0, 100) < self.PROBABILITY_MUTATION:
				temp_indLay = randint(1, len(neural.layers)-1)
				temp_indNeu = randint(1, len(neural.layers[temp_indLay].neurons)-1)
				temp_indWei = randint(1, len(neural.layers[temp_indLay].neurons[temp_indNeu].weights)-1)
				neural.layers[temp_indLay].neurons[temp_indNeu].weights[temp_indWei] = uniform(-1, 1)
			self.nextGeneration.append(neural)
	def populate(self):
		# Completer la generation suivante avec des nn aleatoires
		for i in range(self.NUMBER_INDIVIDUALS - len(self.nextGeneration)):
			self.nextGeneration.append(lnn.NeuralNetwork(size=lnn.NN_SIZE))
	def selection(self):
		selections = self.fitnessSorted[1:int(6*self.NUMBER_INDIVIDUALS/10)]
		return selections
	def tweak(self, best):
		# Ajouter le best à la prochaine génération
		self.nextGeneration.append(best)
		# Faire des petites variations sur le best et les ajouter à la prochaine génération
		for i in range(int(15*self.NUMBER_INDIVIDUALS/40)-1):
			temp_nn = lnn.NeuralNetwork(neural=best)
			# Ajouter des tweaks ici
			for j in range(randint(5, 25)):
				temp_indLay = randint(1, len(temp_nn.layers)-1)
				temp_indNeu = randint(1, len(temp_nn.layers[temp_indLay].neurons)-1)
				temp_indWei = randint(1, len(temp_nn.layers[temp_indLay].neurons[temp_indNeu].weights)-1)
				temp_nn.layers[temp_indLay].neurons[temp_indNeu].weights[temp_indWei] += uniform(-0.2, 0.2)
			self.nextGeneration.append(temp_nn)
