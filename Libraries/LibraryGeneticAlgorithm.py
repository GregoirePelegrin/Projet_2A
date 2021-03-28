# Libraries import
from Libraries import LibraryNeuralNetwork as lnn
from random import randint
from random import uniform

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
        self.variations()
        # self.mutate(self.crossover(self.selection()))
        self.populate()
    def sort(self, currGen):
        # Sort the current gen by descending fitness
        self.currentSorted = sorted(currGen, key=lambda nn:nn.fitness, reverse=True)
    def populate(self):
        for i in range(self.NUMBER_INDIVIDUALS - len(self.nextGeneration)):
            self.nextGeneration.append(lnn.NeuralNetwork())
    def variations(self):
        self.nextGeneration.append(self.currentSorted[0])
        for i in range(int(15*self.NUMBER_INDIVIDUALS/40)):
            tempNN = lnn.NeuralNetwork(neural=self.currentSorted[0])
            for j in range(randint(max(5, int(tempNN.nbrWeights/10)), max(15, int(tempNN.nbrWeights/5)))):
                tempLay = randint(1, len(tempNN.layers)-1)
                tempNeu = randint(0, len(tempNN.layers[tempLay].neurons)-1)
                tempWei = randint(0, len(tempNN.layers[tempLay].neurons[tempNeu].weights)-1)
                tempNN.layers[tempLay].neurons[tempNeu].weights[tempWei] += uniform(-0.05, 0.05)
            self.nextGeneration.append(tempNN)
    