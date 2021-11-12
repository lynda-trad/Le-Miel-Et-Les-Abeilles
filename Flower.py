class Flower:
    def __init__(self, x, y, index):
        self.__x = x
        self.__y = y
        self.__index = index

    def getCoordinates(self):
        return self.__x, self.__y

    def getIndex(self):
        return self.__index

    def printFlower(self):
        print("Flower", self.__index, ": (", self.__x, ",", self.__y, ")")
