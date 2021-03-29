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
        score = []
        for nn in self.currentSorted:
            score.append(nn.fitness)
        self.variations()
        self.mutate(self.crossover(self.selection()))
        self.populate()
        return score

    def crossover(self, selected):
        crossed = []
        if len(selected)%2 != 0:
            r = randint(0, len(selected)-1)
            crossed.append(lnn.NeuralNetwork(neural=selected[r]))
            del selected[r]
        while len(selected) > 0:
            indPar1 = randint(0, len(selected)-1)
            indPar2 = randint(0, len(selected)-1)
            while indPar1 == indPar2:
                indPar2 = randint(0, len(selected)-1)
            p1 = lnn.NeuralNetwork(neural=selected[indPar1])
            p2 = lnn.NeuralNetwork(neural=selected[indPar2])
            if randint(0, 100) < self.PROBABILITY_CROSSOVER:
                tempIndLay = randint(0, len(p1.layers)-1)
                tempLay = lnn.Layer(layer=p1.layers[tempIndLay])
                p1.layers[tempIndLay] = lnn.Layer(layer=p2.layers[tempIndLay])
                p2.layers[tempIndLay] = tempLay
            crossed.append(p1)
            crossed.append(p2)
            del selected[max(indPar1, indPar2)]
            del selected[min(indPar1, indPar2)]
        return crossed
    def mutate(self, crossed):
        for nn in crossed:
            if randint(0, 100) < self.PROBABILITY_MUTATION:
                tempLay = randint(1, len(nn.layers)-1)
                tempNeu = randint(0, len(nn.layers[tempLay].neurons)-1)
                tempWei = randint(0, len(nn.layers[tempLay].neurons[tempNeu].weights)-1)
                nn.layers[tempLay].neurons[tempNeu].weights[tempWei] = uniform(-1, 1)
            self.nextGeneration.append(nn)
    def populate(self):
        for i in range(self.NUMBER_INDIVIDUALS - len(self.nextGeneration)):
            self.nextGeneration.append(lnn.NeuralNetwork())
    def sort(self, currGen):
        # Sort the current gen by descending fitness
        self.currentSorted = sorted(currGen, key=lambda nn:nn.fitness, reverse=True)
    def selection(self):
        selected = []
        for nn in self.currentSorted[1:int(self.NUMBER_INDIVIDUALS/2)]:
            selected.append(lnn.NeuralNetwork(neural=nn))
        temp = []
        for i in range(int(self.NUMBER_INDIVIDUALS/10)):
            r = randint(int(self.NUMBER_INDIVIDUALS/2), len(self.currentSorted)-1)
            while r in temp:
                r = randint(int(self.NUMBER_INDIVIDUALS/2), len(self.currentSorted)-1)
            temp.append(r)
            selected.append(lnn.NeuralNetwork(neural=self.currentSorted[r]))
        return selected
    def variations(self):
        self.nextGeneration.append(lnn.NeuralNetwork(neural=self.currentSorted[0]))
        for i in range(int(15*self.NUMBER_INDIVIDUALS/40)):
            tempNN = lnn.NeuralNetwork(neural=self.currentSorted[0])
            for j in range(randint(max(5, int(tempNN.nbrWeights/10)), max(15, int(tempNN.nbrWeights/5)))):
                tempLay = randint(1, len(tempNN.layers)-1)
                tempNeu = randint(0, len(tempNN.layers[tempLay].neurons)-1)
                tempWei = randint(0, len(tempNN.layers[tempLay].neurons[tempNeu].weights)-1)
                tempNN.layers[tempLay].neurons[tempNeu].weights[tempWei] += uniform(-0.3, 0.3)
                if tempNN.layers[tempLay].neurons[tempNeu].weights[tempWei] > 0:
                    tempNN.layers[tempLay].neurons[tempNeu].weights[tempWei] = min(1, tempNN.layers[tempLay].neurons[tempNeu].weights[tempWei])
                else:
                    tempNN.layers[tempLay].neurons[tempNeu].weights[tempWei] = max(-1, tempNN.layers[tempLay].neurons[tempNeu].weights[tempWei])
            self.nextGeneration.append(tempNN)
    