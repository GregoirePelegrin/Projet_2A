from random import randint
from random import uniform

import libraryGame as lg

# Constants
PROBABILITY_CROSSOVER = 10
PROBABILITY_MUTATION = 10
COEFF_FITNESS = 1000000000						# Will change

# Functions
def crossover(individuals):						# Swapping weights of the randint()th layer
	for i in range(int(len(individuals) / 2)):
		if randint(0, 100) <= PROBABILITY_CROSSOVER:
			p1 = randint(0, len(individuals)-1)
			p2 = randint(0, len(individuals)-1)
			while p1 == p2:
				p2 = randint(0, len(individuals)-1)
			dim = len(individuals[p1].nn.layers)
			ind_lay = randint(1, dim-1)
			temp_lay = individuals[p1].nn.layers[ind_lay]
			individuals[p1].nn.layers[ind_lay] = individuals[p2].nn.layers[ind_lay]
			individuals[p2].nn.layers[ind_lay] = temp_lay
	return individuals
def evaluate(individuals, best=[]):				# Same as "D:\Scolarite\ENSISA\2A\IA_Opti\Exos\GACardsGroups.py"
	if len(best) == 0:
		best = [individuals[0], fitness(individuals[0])]
	for i in individuals:
		temp = fitness(i)
		if temp < best[1]:
			best = [i, temp]
	return best
def fitness(individual):						# Distance + coeff * nbr_checkpoints
	return individual.totalDistance + COEFF_FITNESS*individual.checkpointPassedCounter
def mutate(individuals):						# Random point => uniform(-1, 1)
	for i in individuals:
		if randint(0, 100) <= PROBABILITY_MUTATION:
			dim = len(i.nn.layers)
			temp_lay = randint(1, dim-1)
			dim = len(i.nn.layers[temp_lay].neurons)
			temp_neu = randint(1, dim-1)
			nn.layers[temp_lay].neurons[temp_neu] = uniform(-1, 1)
	return individuals
def selection(individuals):						# 90% from best, 10% random
	return None