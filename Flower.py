class Flower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False

    def setVisited(self, visited):
        self.visited = visited

    def printFlower(self):
        print("\nFlower:", "\nx:", self.x, "\ny:", self.y, "\nvisited:", self.visited)
