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
        self.order = []
        self.length = 0

    def getLength(self):
        return self.length

    def getOrder(self):
        return self.order

    def setOrder(self, fList):
        self.order = fList

    # Adds flower object to order list
    def addFlower(self, flower):
        self.order.append(flower)

    # Printing methods
    def printPath(self):
        print("\nPath:")
        for flower in self.order:
            flower.printFlower()
        self.printFitness()

    def printFitness(self):
        print("Fitness : ", self.getLength())

    # Calculates fitness
    def calculateLength(self):
        total = 0
        starting_point = (500, 500)
        if len(self.order) != 0:
            total += distanceCalculus(starting_point, self.order[0].getCoordinates())
        for i in range(len(self.order)):
            if i != len(self.order) - 1:
                total += distanceCalculus(self.order[i].getCoordinates(), self.order[i + 1].getCoordinates())
        self.length = total
