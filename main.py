import pandas as pd
import math


def openFile():
    try:
        d = pd.read_excel('./resources/flowers.xlsx')
    except FileNotFoundError:
        return []
    return d


def distanceCalculus(coordx1, coordx2):
    x1 = coordx1[0]
    y1 = coordx1[1]
    x2 = coordx2[0]
    y2 = coordx2[1]
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


##################################################
data = openFile()
if len(data) != 0:
    flowersList = []
    for line in range(len(data)):
        flowersList.append((data.loc[line, 'x'], data.loc[line, 'y']))
    for flower in flowersList:
        print(flower)
else:
    print("File is empty or does not exist, please place flowers.xlsx in resources directory.")
