import math
import os

import numpy as np


class MultiKnapsack:

    def __init__(self, target):
        # read and parse input file
        filePath = os.path.join(os.getcwd(), 'problems', 'multiknapsack', 'inputfiles', str(target))
        inputFile = open(filePath, 'r')

        content = inputFile.readlines()
        content = [line.strip('\n') for line in content]
        sacksAndItems = content[0].strip('\t').split('  ')
        numOfKnapsacks = int(sacksAndItems[0])
        numOfItems = int(sacksAndItems[1])

        numOfValuesLines = int(math.ceil(numOfItems / 10))
        values = []
        for line in range(1, numOfValuesLines + 1):
            newValues = [int(val) for val in content[line].replace('\t', ' ').split(' ') if val.isdigit()]
            values = values + newValues

        capacities = [int(capacity) for capacity in content[1 + numOfValuesLines].replace('\t', ' ').split(' ') if
                      capacity.isdigit()]

        knapsackWeightsPerItem = []
        for line in range(numOfValuesLines + 2, (numOfValuesLines * (numOfKnapsacks + 1)) + 2):
            newCapacities = [int(val) for val in content[line].replace('\t', ' ').split(' ') if val.isdigit()]
            knapsackWeightsPerItem = knapsackWeightsPerItem + newCapacities

        knapsackWeightsPerItem = np.reshape(knapsackWeightsPerItem, (numOfKnapsacks, numOfItems))

        self._values = np.array(values)
        self._knapsackWeightsPerItem = knapsackWeightsPerItem
        self._numOfKnapsacks = numOfKnapsacks
        self._numOfItems = numOfItems
        self._capacities = np.array(capacities)
