import pandas as pd
import random
import Flower
import Path
import graphPrinting

POPULATION_COUNT = 100
GENERATION_COUNT_MAX = 2000
STARTING_POS = (500, 500)
FLOWERS_NUMBER = 50
MUTATION_RATE = 0.05


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
    fitList = {}
    i = 0
    for individual in population:
        individual.calculateFitness()
        fitList[i] = individual.getLength()
        i += 1
    return fitList


# Sorts fitness list by shortest
def sortFitnesses(fitnesses):
    fitList = sorted(fitnesses.items(), key=lambda x: x[1])
    return dict(fitList)


# Sorts population by shortest fitness
def sortPopulation(population):
    fitDic = fitness(population)
    fitDic = sortFitnesses(fitDic)
    sortedPopulation = []
    for key in fitDic.keys():
        sortedPopulation.append(population[int(key)])
    population = sortedPopulation
    return population


# Removes duplicates from genome
def removeDuplicate(cross):
    indexList = []
    order = cross.getOrder()
    for i in range(FLOWERS_NUMBER):
        count = 0
        for j in range(len(order)):
            flower = order[j]
            if flower.getIndex() == i:
                count += 1
                if count > 1:
                    indexList.append(j)
    indexList.sort(reverse=True)
    for j in indexList:
        order.pop(j)
    cross.setOrder(order)
    return cross


# Adds missing flowers
def addMissingFlowers(cross, flowList):
    indexList = []
    for flower in cross.getOrder():
        index = flower.getIndex()
        indexList.append(index)
    for i in range(FLOWERS_NUMBER):
        if i not in indexList:
            missingFlower = getFlowerById(flowList, i)
            cross.addFlower(missingFlower)


# Crosses first half and last half of two genomes ; returns new genome
def crossing(first_half, last_half, half, flowList):
    cross = Path.Path()
    for i in range(half):
        cross.addFlower(first_half[i])
    for i in range(half, FLOWERS_NUMBER - 1):
        cross.addFlower(last_half[i])
    removeDuplicate(cross)
    addMissingFlowers(cross, flowList)
    cross.calculateFitness()
    return cross


# Creates 2 children with gen's best bees couples
def crossover(population, bestL, flowList):
    half = int(FLOWERS_NUMBER / 2) - 1
    orders = []
    for best in bestL:
        orders.append(best.getOrder())
    for i in range(len(bestL) - 3):
        population.append(crossing(orders[i], orders[i + 2], half, flowList))
        population.append(crossing(orders[i + 2], orders[i], half, flowList))
    return population


def flowersSwitch(individual):
    pos1 = random.randint(0, FLOWERS_NUMBER - 2)
    pos2 = random.randint(0, FLOWERS_NUMBER - 2)
    while pos2 == pos1:
        pos2 = random.randint(0, FLOWERS_NUMBER - 2)
    path = individual.getOrder()
    first_flower = path[pos1]
    second_flower = path[pos2]
    if pos2 > pos1:
        path.pop(pos2)
        path.pop(pos1)
    else:
        path.pop(pos1)
        path.pop(pos2)
    path.insert(pos1, second_flower)
    path.insert(pos2, first_flower)
    individual.setOrder(path)
    return individual


# 2 flowers switch places in every path of the population
def mutation(population):
    for i in range(20, POPULATION_COUNT - 2):
        individual = population[i]
        population[i] = flowersSwitch(individual)
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
        individual.calculateFitness()
        population.append(individual)
    return population


# Generates first generation
def generateFirstGeneration(fList):
    first = []
    first = generatePopulation(first, fList, POPULATION_COUNT - len(first))
    first = sortPopulation(first)
    return first


# Generates a new generation with previous one
def generateNewGeneration(previous, flowList, previousAverage):
    new = previous
    bestList = []
    if abs(previousAverage - calculateAverage(new)) <= 500:
        new = mutation(new)
    new = sortPopulation(new)
    for i in range(20):
        bestList.append(new[i])
    new = crossover(new, bestList, flowList)
    new = sortPopulation(new)
    new = removingWorst(new)
    return new


# Generates GENERATION_COUNT_MAX generations and returns the last one
def cycle(fList, graph, nodePos, flowList):
    averageList = []
    bestBees = []
    # First generation
    firstPopulation = generateFirstGeneration(fList)
    previousGen = firstPopulation
    newGeneration = []
    averageList.append(calculateAverage(previousGen))
    # graphPrinting.printGraph(graph, nodePos, fList, 1, previousGen[0])

    # New generation
    for i in range(2, GENERATION_COUNT_MAX + 1):
        previousAverage = 0
        if len(averageList) >= 2:
            previousAverage = averageList[-1]
        newGeneration = generateNewGeneration(previousGen, flowList, previousAverage)
        averageList.append(calculateAverage(newGeneration))
        bestBees.append(newGeneration[0].getLength())
        """
        bestBee = newGeneration[0]
        graphPrinting.printGraph(graph, nodePos, fList, i, bestBee)
        """
        if i % 500 == 0:
            print("GENERATION", i, "REACHED\n")
        if i != GENERATION_COUNT_MAX:
            previousGen = newGeneration
            newGeneration = []
    return newGeneration, averageList, bestBees  # last gen


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

print("-- GENERATING --\nPlease bee patient !")
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
last_generation, averageL, bestBees = cycle(flowersList, G, pos, flowersList)
best_path = last_generation[0]
printPopulation(last_generation, GENERATION_COUNT_MAX)
print("\nBEST PATH OF LAST GENERATION : ")
best_path.printPath()
print("LENGTH", len(last_generation))
# Generates graph showing averageL of each generation compared to the others
best = best_path.getLength()
graphPrinting.printEvolutionGraph(averageL, str(best), 'average')
graphPrinting.printEvolutionGraph(bestBees, str(bestBees[-1]), 'bees')
