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
        self._order = []
        self._length = 0

    def getLength(self):
        return self._length

    def getOrder(self):
        return self._order

    def setOrder(self, fList):
        self._order = fList

    # Adds flower object to order list
    def addFlower(self, flower):
        self._order.append(flower)

    # Calculates fitness
    def calculateFitness(self):
        total = 0
        starting_point = (500, 500)
        if len(self._order) != 0:
            total += distanceCalculus(starting_point, self._order[0].getCoordinates())
        for i in range(len(self._order)):
            if i != len(self._order) - 1:
                total += distanceCalculus(self._order[i].getCoordinates(), self._order[i + 1].getCoordinates())
        self._length = total

    # Printing methods
    def printPath(self):
        print("\nPath:")
        for flower in self._order:
            flower.printFlower()
        self.printFitness()

    def printFitness(self):
        print("Fitness : ", self.getLength())

    def printIndex(self):
        indexList = []
        for flower in self._order:
            index = flower.getIndex()
            indexList.append(index)
        return indexList
