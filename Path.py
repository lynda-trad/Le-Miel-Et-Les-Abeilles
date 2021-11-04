import math


def distanceCalculus(coord1, coord2):
    x1 = coord1[0]
    y1 = coord1[1]
    x2 = coord2[0]
    y2 = coord2[1]
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance


class Path:
    def __init__(self):
        self.order = []
        self.length = 0

    def getLength(self):
        return self.length

    def getOrder(self):
        return self.order

    def addFlower(self, flower):
        self.order.append(flower)

    def printPath(self):
        print("Path:")
        for flower in self.order:
            flower.printFlower()

    # Fitness
    def calculateLength(self):
        total = 0
        starting_point = (500, 500)
        if len(self.order) != 0:
            total += distanceCalculus(starting_point, self.order[0].getCoordinates())
        for i in range(len(self.order)):
            if i != len(self.order) - 1:
                total += distanceCalculus(self.order[i].getCoordinates(), self.order[i + 1].getCoordinates())
        self.length = total

    def printFitness(self):
        print("Fitness : ", self.getLength())
