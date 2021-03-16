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

		# 1/ self.fitness(individuals)
		# 2/ Ajouter les variations des best à la prochaine génération
		# 3/ Ajouter les mutations des croisements à la prochaine génération
		# 4/ Ajouter le reste (populate) à la prochaine génération
		# 5/ Attribuer la nouvelle génération aux individus
		# 6/ Renvoie self.fitnessSorted
	def fitness(self, individuals):
		# 1/ Calcule la fitness de tout le monde et la stocke dans l'attribut "fitness" des NN
		# 2/ Trie les individus par fitness dans l'attribut "self.fitnessSorted"
		# 3/ Ecris le best dans un fichier

	def crossing(self, selections):
		crossings = []
		return crossings
	def mutate(self, crossings):
		mutations = []
		return mutations
	def populate(self, n):
		# Ajouter des randoms à la génération suivante
		return None
	def selection(self, individuals):
		selections = []
		return selections
	def tweak(self, best):
		variations = []
		# Ajouter le best à la prochaine génération
		# Faire des petites variations sur le best et les ajouter à la prochaine génération

