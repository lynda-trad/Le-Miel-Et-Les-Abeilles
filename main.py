import pandas as pd
import numpy as np
import random
import Flower
import Path

POPULATION_COUNT = 100
GENERATION_COUNT_MAX = 100
STARTING_POS = (500, 500)
FLOWERS_NUMBER = 50


# Opens excel file and returns dataframe
def openFile():
    try:
        d = pd.read_excel('./resources/flowers.xlsx')
    except FileNotFoundError:
        return []
    return d


# Returns flower list by parsing dataframe
def initFlowersList(d):
    fList = []
    i = 0
    for line in range(len(d)):
        f = Flower.Flower(d.loc[line, 'x'], d.loc[line, 'y'], i)
        fList.append(f)
        i += 1
    return fList


# Returns flower when given its ID
def getFlowerById(flowList, index):
    for flower in flowList:
        if flower.getIndex() == index:
            return flower


# Returns list of individuals' fitness in a population
def fitness(population):
    fitnesses = {}
    i = 0
    for individual in population:
        individual.calculateLength()
        fitnesses[i] = individual.getLength()
        i += 1
    return fitnesses


# Sorts fitness list by shortest
def sortFitnesses(fitnesses):
    fitList = sorted(fitnesses.items(), key=lambda x: x[1])
    return dict(fitList)


# Sorts population by shortest fitness
def sortPopulation(fitnesses, population):
    sortedPopulation = []
    for key in fitnesses.keys():
        sortedPopulation.append(population[int(key)])
    population = sortedPopulation
    return population


# Crosses first half and last half of two genomes ; returns new genome
def crossing(first_half, last_half, half):
    cross = Path.Path()
    for i in range(half):
        cross.addFlower(first_half[i])
    for i in range(half, FLOWERS_NUMBER):
        cross.addFlower(last_half[i])
    cross.calculateLength()
    return cross


def crossover(population, bestL):
    half = int(FLOWERS_NUMBER / 2) - 1
    orders = []
    for best in bestL:
        orders.append(best.getOrder())
    for i in range(len(bestL) - 1):
        population.append(crossing(orders[i], orders[i + 1], half))
    return population


# 2 flowers switch places in every path of the population
def mutation(population):
    for i in range(19, POPULATION_COUNT - 1):
        individual = population[i]
        pos1 = random.randint(0, FLOWERS_NUMBER - 1)
        pos2 = 0
        while pos2 == pos1:
            pos2 = random.randint(0, FLOWERS_NUMBER - 1)
        path = individual.getOrder()
        first = path[pos1]
        second = path[pos2]
        path.pop(pos1)
        path.pop(pos2)
        path.insert(pos1, second)
        path.insert(pos2, first)
    return population


def removingWorst(new):
    i = len(new) - 1
    while i != 99:
        new.pop(i)
        i -= 1
    return new


# Generates individuals in a population
def generatePopulation(population, flowList, count):
    for pop in range(count):
        individual = Path.Path()
        indexList = random.sample(range(len(flowList)), len(flowList))
        for index in indexList:
            individual.addFlower(getFlowerById(flowList, index))
        individual.calculateLength()
        population.append(individual)
    return population


# Generates first generation
def generateFirstGeneration(fList):
    first = []
    first = generatePopulation(first, fList, POPULATION_COUNT - len(first))  # 1 )
    fitnessDic = fitness(first)  # 2 )
    fitnessDic = sortFitnesses(fitnessDic)
    first = sortPopulation(fitnessDic, first)
    return first


# Generates a new generation with previous one
def generateNewGeneration(previous, new):
    new = previous
    bestList = []
    for i in range(20):
        bestList.append(new[i])

    new = mutation(new)  # 6 ) 80 other members

    new = crossover(new, bestList)  # 4 ) added 2 children per couple so 20

    # Sorting population
    new_fitnessDic = fitness(new)  # 2 )
    new_fitnessDic = sortFitnesses(new_fitnessDic)
    new = sortPopulation(new_fitnessDic, new)

    # Removing excess worst individuals
    new = removingWorst(new)
    return new


# Generates GENERATION_COUNT_MAX generations and returns the last one
def cycle(fList):
    # First generation
    firstPopulation = generateFirstGeneration(fList)
    previousGen = firstPopulation
    newGeneration = []
    # printPopulation(previousGen, 1)

    # New generation
    for i in range(2, GENERATION_COUNT_MAX + 1):
        newGeneration = generateNewGeneration(previousGen, newGeneration)
        printPopulation(newGeneration, i)
        if i != GENERATION_COUNT_MAX:
            previousGen = newGeneration
            newGeneration = []
    return newGeneration  # last generation


def printPopulation(population, i):
    print("\nGeneration", i)
    for individual in population:
        individual.printFitness()


##################################################
data = openFile()
if len(data) == 0:
    print("File is empty or does not exist, please place flowers.xlsx in resources directory.")
    quit()
flowersList = initFlowersList(data)

last_generation = cycle(flowersList)
best_path = last_generation[0]  # or is it ?
printPopulation(last_generation, GENERATION_COUNT_MAX)
print("\nBEST PATH OF LAST GENERATION : ")
best_path.printPath()
print("LENGTH", len(last_generation))
"""
New AG : 
FIRST GENERATION : start with POPULATION_COUNT = 100 random paths
Calculate fitness and sort the population by shortest path

NEW GENERATIONS :
1 ) append all from previous gen
2 ) 80 last will have mutations
3 ) first 20 from previous best will generate children
- we end up with 120 individuals so we have to :
4 ) sort the population
5 ) last 20 are the worst, we remove them to end up with POPULATION_COUNT = 100 individuals

Previous AG :
1 ) take first best from previous gen and add it to new generation
2 ) cross over first 3 of previous gen, half from first, half from second -> new generation has 6 members
3 ) add (POPULATION_COUNT - new gen length) new members by generating them randomly
4 ) add mutation to genes -> 2 flowers will be switched in [ every path or just the cross overs ? ] 
5 ) calculate fitness
6 ) sort by shortest path

repeat new generations for 100 tries and look if its good enough 
"""
