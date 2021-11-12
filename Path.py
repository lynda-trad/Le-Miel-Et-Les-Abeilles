import math


# Calculates distance between two points
def distanceCalculus(coord1, coord2):
    x1 = coord1[0]
    y1 = coord1[1]
    x2 = coord2[0]
    y2 = coord2[1]
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return int(distance)


class Path:
    def __init__(self):
        self.__order = []
        self.__length = 0

    def getLength(self):
        return self.__length

    def getOrder(self):
        return self.__order

    def setOrder(self, fList):
        self.__order = fList

    # Adds flower object to order list
    def addFlower(self, flower):
        self.__order.append(flower)

    # Calculates fitness
    def calculateFitness(self):
        total = 0
        starting_point = (500, 500)
        if len(self.__order) != 0:
            total += distanceCalculus(starting_point, self.__order[0].getCoordinates())
        for i in range(len(self.__order)):
            if i != len(self.__order) - 1:
                total += distanceCalculus(self.__order[i].getCoordinates(), self.__order[i + 1].getCoordinates())
        self.__length = total

    # Printing methods
    def printPath(self):
        print("\nPath:")
        for flower in self.__order:
            flower.printFlower()
        self.printFitness()

    def printFitness(self):
        print("Fitness : ", self.getLength())

    def printIndex(self):
        indexList = []
        for flower in self.__order:
            index = flower.getIndex()
            indexList.append(index)
        return indexList
