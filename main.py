import pandas as pd
import numpy as np
import Flower
import Path

POPULATION_COUNT = 100
GENERATION_COUNT_MAX = 100000
STARTING_POS = (500, 500)
CHANCE_TO_MUTATE = 0.1


def openFile():
    try:
        d = pd.read_excel('./resources/flowers.xlsx')
    except FileNotFoundError:
        return []
    return d


##################################################
data = openFile()
if len(data) == 0:
    print("File is empty or does not exist, please place flowers.xlsx in resources directory.")
    quit()

flowersList = []
i = 0
for line in range(len(data)):
    f = Flower.Flower(data.loc[line, 'x'], data.loc[line, 'y'], i)
    flowersList.append(f)
    i += 1

""" Incidence Matrix 
# chemin hamiltonien minimal
# Permutation encoding ? Chromosome == order of flowers ?
matrix = np.zeros((len(data), len(data)))
for f1 in flowersList:
    for f2 in flowersList:
        matrix[f1.getIndex(), f2.getIndex()] = Path.distanceCalculus(f1.getCoordinates(), f2.getCoordinates())
"""
