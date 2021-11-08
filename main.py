import pandas as pd
import random
import Flower
import Path
import graphPrinting

POPULATION_COUNT = 100
GENERATION_COUNT_MAX = 500
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
def crossing(first_half, last_half, half, flowList):
    cross = Path.Path()
    for i in range(half):
        cross.addFlower(first_half[i])
    for i in range(half, FLOWERS_NUMBER - 1):
        cross.addFlower(last_half[i])
    # Removes duplicates
    cross.setOrder(list(dict.fromkeys(cross.getOrder())))
    # Adds missing flowers
    indexList = []
    for flower in cross.getOrder():
        indexList.append(flower.getIndex())
    for i in range(50):
        if i not in indexList:
            missingFlower = getFlowerById(flowList, i)
            cross.addFlower(missingFlower)
    cross.calculateLength()
    return cross


def crossover(population, bestL, flowList):
    half = int(FLOWERS_NUMBER / 2) - 1
    orders = []
    for best in bestL:
        orders.append(best.getOrder())
    for i in range(len(bestL) - 3):
        population.append(crossing(orders[i], orders[i + 2], half, flowList))
    return population


"""
def crossover(population, bestL):
    half = int(FLOWERS_NUMBER / 2) - 1
    orders = []
    for best in bestL:
        orders.append(best.getOrder())
    for i in range(len(bestL) - 1):
        for j in range(len(bestL) - 1):  # each best will reproduce with another best twice
            if i != j:
                cross = Path.Path()
                fList = list(set(orders[i] + orders[j]))
                cross.setOrder(fList)
                population.append(cross)
                # population.append(crossing(orders[i], orders[j], half))
    return population
"""


# 2 flowers switch places in every path of the population
def mutation(population):
    for i in range(20, POPULATION_COUNT - 2):
        individual = population[i]
        pos1 = random.randint(0, FLOWERS_NUMBER - 2)
        pos2 = random.randint(0, FLOWERS_NUMBER - 2)
        while pos2 == pos1:
            pos2 = random.randint(0, FLOWERS_NUMBER - 2)
        path = individual.getOrder()
        first_flower = path[pos1]
        second_flower = path[pos2]
        path.pop(pos1)
        path.pop(pos2)
        path.insert(pos1, second_flower)
        path.insert(pos2, first_flower)
    return population


# Removes worst individuals to reach max number of individuals
def removingWorst(new):
    i = len(new) - 1
    while i != POPULATION_COUNT - 1:
        new.pop(i)
        i -= 1
    return new


# Generates random individuals for the very first generation
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
    first = generatePopulation(first, fList, POPULATION_COUNT - len(first))
    fitnessDic = fitness(first)
    fitnessDic = sortFitnesses(fitnessDic)
    first = sortPopulation(fitnessDic, first)
    return first


# Generates a new generation with previous one
def generateNewGeneration(previous, flowList):
    new = previous
    bestList = []
    for i in range(20):
        bestList.append(new[i])

    new = mutation(new)  # 6 ) last 80 members will be mutated
    new = crossover(new, bestList, flowList)  # 4 ) 400 children are generated

    # Sorting population
    new_fitnessDic = fitness(new)  # 2 )
    new_fitnessDic = sortFitnesses(new_fitnessDic)
    new = sortPopulation(new_fitnessDic, new)

    # Removing excess worst individuals
    new = removingWorst(new)
    return new


# Generates GENERATION_COUNT_MAX generations and returns the last one
def cycle(fList, graph, nodePos, flowList):
    averageList = []
    # First generation
    firstPopulation = generateFirstGeneration(fList)
    previousGen = firstPopulation
    newGeneration = []
    averageList.append(calculateAverage(previousGen))
    graphPrinting.printGraph(graph, nodePos, fList, 1, previousGen[0])

    # New generation
    for i in range(2, GENERATION_COUNT_MAX + 1):
        newGeneration = generateNewGeneration(previousGen, flowList)
        # Calculates average length of generation's bees
        averageList.append(calculateAverage(newGeneration))
        # Printing best bee of this generation
        bestBee = newGeneration[0]
        graphPrinting.printGraph(graph, nodePos, fList, i, bestBee)
        if i != GENERATION_COUNT_MAX:
            previousGen = newGeneration
            newGeneration = []
    return newGeneration, averageList  # last gen


# Prints fitness of each individual of a population
def printPopulation(population, i):
    print("\nGeneration", i)
    for individual in population:
        individual.printFitness()


# Calculates average path length of a population
def calculateAverage(population):
    total = 0
    for individual in population:
        total += individual.getLength()
    average = total / POPULATION_COUNT
    return average


##################################################
data = openFile()
if len(data) == 0:
    print("File is empty or does not exist, please place flowers.xlsx in resources directory.")
    quit()
flowersList = initFlowersList(data)

# NetworkX Graph init
G, pos = graphPrinting.initPrintingGraph(flowersList)

print("-- GENERATIONS --\nPlease be patient !")
print('''
              \     /
          \    o ^ o    /
            \ (     ) /
 ____________(%%%%%%%)____________
(     /   /  )%%%%%%%(  \   \     )
(___/___/__/           \__\___\___)
   (     /  /(%%%%%%%)\  \     )
    (__/___/ (%%%%%%%) \___\__)
            /(       )\\
          /   (%%%%%)   \\
               (%%%)
                 !
''')
last_generation, averageL = cycle(flowersList, G, pos, flowersList)
best_path = last_generation[0]
printPopulation(last_generation, GENERATION_COUNT_MAX)
print("\nBEST PATH OF LAST GENERATION : ")
best_path.printPath()
print("LENGTH", len(last_generation))

# Generates graph showing averageL of each generation compared to the others
graphPrinting.printAverageGraph(averageL)
