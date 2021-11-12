class Flower:
    def __init__(self, x, y, index):
        self._x = x
        self._y = y
        self._index = index

    def getCoordinates(self):
        return self._x, self._y

    def getIndex(self):
        return self._index

    def printFlower(self):
        print("Flower", self.index, ": (", self.x, ",", self.y, ")")
