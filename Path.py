import math


class Path:
    def __init__(self):
        self.order = []
        self.length = 0

    def addFlower(self, flower):
        self.order.append(flower)

    def distanceCalculus(self, coord1, coord2):
        x1 = coord1[0]
        y1 = coord1[1]
        x2 = coord2[0]
        y2 = coord2[1]
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        self.length += distance
