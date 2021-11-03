import pandas as pd
import Flower


def openFile():
    try:
        d = pd.read_excel('./resources/flowers.xlsx')
    except FileNotFoundError:
        return []
    return d


##################################################
data = openFile()
if len(data) != 0:
    flowersList = []
    for line in range(len(data)):
        f = Flower.Flower(data.loc[line, 'x'], data.loc[line, 'y'])
        flowersList.append(f)
    for flower in flowersList:
        flower.printFlower()
else:
    print("File is empty or does not exist, please place flowers.xlsx in resources directory.")
