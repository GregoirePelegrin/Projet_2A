# External libraries import
from Libraries import LibraryNeuralNetwork as lnn

# Constants

# Class
class GeneticAlgorithm:
    def __init__(self, ni, pc=10, pm=10):
        self.NUMBER_INDIVIDUALS = ni
        self.PROBABILITY_CROSSOVER = pc
        self.PROBABILITY_MUTATION = pm

        self.currentSorted = []
        self.nextGeneration = []
    def __str__(self):
        return "GeneticAlgorithm(ni={}, pc={}, pm={})".format(COEFF_FITNESS, 
            self.NUMBER_INDIVIDUALS, self.PROBABILITY_CROSSOVER, self.PROBABILITY_MUTATION)
    
    def evolve(self, currGen):
        self.currentSorted.clear()
        self.nextGeneration.clear()
        self.sort(currGen)
        # self.variations()
        # self.mutate(self.crossover(self.selection()))
        self.populate()
    def sort(self, currGen):
        # Sort the current gen by descending fitness
        self.currentSorted = sorted(currGen, key=lambda nn:nn.fitness, reverse=True)
    def populate(self):
        for i in range(self.NUMBER_INDIVIDUALS - len(self.nextGeneration)):
            self.nextGeneration.append(lnn.NeuralNetwork())
    
