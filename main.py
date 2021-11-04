import pandas as pd
import numpy as np
import random
import Flower
import Path

POPULATION_COUNT = 10
GENERATION_COUNT_MAX = 100
STARTING_POS = (500, 500)
FLOWERS_NUMBER = 50


def openFile():
    try:
        d = pd.read_excel('./resources/flowers.xlsx')
    except FileNotFoundError:
        return []
    return d


def getFlowerById(flowList, index):
    for flower in flowList:
        if flower.getIndex() == index:
            return flower


def generatePopulation(population, flowList, count):
    for pop in range(count):
        individual = Path.Path()
        indexList = random.sample(range(len(flowList)), len(flowList))
        for index in indexList:
            individual.addFlower(getFlowerById(flowList, index))
        individual.calculateLength()
        population.append(individual)
    return population


def fitness(population):
    fitnesses = {}
    i = 0
    for individual in population:
        individual.calculateLength()
        fitnesses[i] = individual.getLength()
        i += 1
    return fitnesses


def sortFitnesses(fitnesses):
    fitList = sorted(fitnesses.items(), key=lambda x: x[1])
    return dict(fitList)


def sortPopulation(fitnesses, population):
    sortedPopulation = []
    for key in fitnesses.keys():
        sortedPopulation.append(population[int(key)])
    population = sortedPopulation
    return population


def crossing(first_half, last_half, half):
    cross = Path.Path()
    for i in range(half):
        cross.addFlower(first_half[i])
    for i in range(half, FLOWERS_NUMBER):
        cross.addFlower(last_half[i])
    cross.calculateLength()
    return cross


def crossover(population, first_best, second_best, third_best):
    half = int(FLOWERS_NUMBER / 2) - 1
    first_order = first_best.getOrder()
    second_order = second_best.getOrder()
    third_order = third_best.getOrder()
    population.append(crossing(first_order, second_order, half))
    population.append(crossing(first_order, third_order, half))
    population.append(crossing(second_order, first_order, half))
    population.append(crossing(second_order, third_order, half))
    population.append(crossing(third_order, first_order, half))
    population.append(crossing(third_order, second_order, half))
    return population


def printPopulation(population):
    for individual in population:
        individual.printFitness()


# 2 flowers switch places in every path of the population
def mutation(population):
    for individual in population:
        pos = random.randint(0, len(population) - 1)
        path = individual.getOrder()
        first = path[pos]
        second = path[pos + 1]
        path.pop(pos)
        path.pop(pos + 1)
        path.insert(pos, second)
        path.insert(pos + 1, first)
    return population


##################################################
data = openFile()
if len(data) == 0:
    print("File is empty or does not exist, please place flowers.xlsx in resources directory.")
    quit()

flowersList = []
i = 0
for line in range(len(data)):
    f = Flower.Flower(data.loc[line, 'x'], data.loc[line, 'y'], i)
    flowersList.append(f)
    i += 1

firstPopulation = []
firstPopulation = generatePopulation(firstPopulation, flowersList, POPULATION_COUNT)  # 1 )

fitnessDic = fitness(firstPopulation)  # 2 )
fitnessDic = sortFitnesses(fitnessDic)
firstPopulation = sortPopulation(fitnessDic, firstPopulation)

newGeneration = []
first_best = firstPopulation[0]
second_best = firstPopulation[1]
third_best = firstPopulation[2]
newGeneration.append(first_best)  # 3 )

newGeneration = crossover(newGeneration, first_best, second_best, third_best)  # 4 )
newGeneration = generatePopulation(newGeneration, flowersList, POPULATION_COUNT - len(newGeneration))  # 5 )

newGeneration = mutation(newGeneration)  # 6 )

""" Incidence Matrix 
# chemin hamiltonien minimal
# Permutation encoding ? Chromosome == order of flowers ?
matrix = np.zeros((len(data), len(data)))
for f1 in flowersList:
    for f2 in flowersList:
        matrix[f1.getIndex(), f2.getIndex()] = Path.distanceCalculus(f1.getCoordinates(), f2.getCoordinates())
"""

"""
    individual = random path
    gene == flower
1 ) generate population -> start with 10 random paths
2 ) calculate fitness and sort the population by shortest path
3 ) takes first best from the list and add it to new generation
4 ) cross over first 3, half from first, half from second -> new generation has 6 members
5 ) add 10 - new gen length new members by generating them randomly
6 ) add mutation to genes -> 2 flowers will be switched in every path
7 ) start again from 2
8 ) continue for 100 tries and look if its good enough
9 ) how do we know its good enough ? new generation can be worse than the previous one...   
"""
