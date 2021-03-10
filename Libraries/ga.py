from random import randint
from random import uniform

import Libraries.LibraryGame as lg

def select(population):
    index1 = index2 = 0
    best1 = best2 = 0
    for i in range(len(population)):
        if population[i].totalDistance > best2 :
            if population[i].totalDistance > best1 :
                best1, best2 = population[i].totalDistance, best1
                index1, index2 = i, index1
            else :
                best2 = population[i].totalDistance
                index2 = i
    return index1,index2

def cross(ind1, ind2):
    if randint(0, 100) <= 20:
        dim = len(ind1.nn.layers)
        layer = randint(1, dim-1)
        # Swap random layer
        tmp = ind1.nn.layers[layer]
        ind1.nn.layers[layer] = ind2.nn.layers[layer]
        ind2.nn.layers[layer] = tmp

def mutate(ind):
    if randint(0, 100) <= 20:
        layer = randint(1, len(ind.nn.layers)-1)
        neuron = randint(0, len(ind.nn.layers[layer].neurons)-1)
        weight = randint(0, len(ind.nn.layers[layer].neurons[neuron].weights)-1)
        ind.nn.layers[layer].neurons[neuron].weights[weight] += uniform(-0.005, 0.005)

def step(population, size):

    nextPopulation = []
    for i in range(int(len(population)/4)):
        best1, best2 = select(population)
        nextPopulation.append(population[best1])
        nextPopulation.append(population[best2])
        # Cross
        cross(population[best1], population[best2])
        nextPopulation.append(population[best1])
        nextPopulation.append(population[best2])
        # Mutate
        mutate(nextPopulation[randint(0, len(nextPopulation)-1)])
        # Remove 2 bests from current population
        del population[max(best1, best2)]
        del population[min(best1, best2)]


    while len(nextPopulation) < size :
        index = randint(0, len(population)-1)
        nextPopulation.append(population[index])
        del population[index]

    for car in nextPopulation:
        car.alive = True
        car.acceleration = 0
        car.orientation = 90
        car.x = 350
        car.y = 150
        car.totalDistance = 0
        car.nextCheckpoint = 2
        car.checkpointPassedCounter = 0
    return nextPopulation