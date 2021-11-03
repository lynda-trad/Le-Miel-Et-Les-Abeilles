class Flower:
    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.index = index
        self.visited = False

    def setVisited(self, visited):
        self.visited = visited

    def printFlower(self):
        print("\nFlower:", "\nx:", self.x, "\ny:", self.y, "\nIndex:", self.index, "\nvisited:", self.visited)

    def getCoordinates(self):
        return self.x, self.y

    def getIndex(self):
        return self.index
