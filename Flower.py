class Flower:
    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.index = index

    def getCoordinates(self):
        return self.x, self.y

    def getIndex(self):
        return self.index

    def printFlower(self):
        print("\nFlower", self.index, ": (", self.x, ",", self.y, ")")
