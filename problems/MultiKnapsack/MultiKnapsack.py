import math
import os

import numpy as np

from problems.Problem import Problem


class MultiKnapsack(Problem):

    def __init__(self, target, values=None, knapsackWeightsPerItem=None, numOfKnapsacks=None, numOfItems=None,
                 capacities=None, optimal=None, initFromFile=True):
        super().__init__(target)
        self._values = values
        self._knapsackWeightsPerItem = knapsackWeightsPerItem
        self._numOfKnapsacks = numOfKnapsacks
        self._numOfItems = numOfItems
        self._capacities = capacities
        self._optimalVal = optimal

        if initFromFile:
            self._initFromFile(target)

        self._densities = np.array(self.getDensitiesSum())

    def _initFromFile(self, target):
        super().__init__(target)
        # read and parse input file
        filePath = os.path.join(os.getcwd(), 'problems', 'MultiKnapsack', 'inputfiles', str(target))
        inputFile = open(filePath, 'r')

        lineNum = 0

        content = inputFile.readlines()
        content = [line.strip('\n') for line in content]
        sacksAndItems = content[lineNum].strip('\t').split('  ')
        numOfKnapsacks = int(sacksAndItems[0])
        numOfItems = int(sacksAndItems[1])

        lineNum += 1

        numOfValuesLines = int(math.ceil(numOfItems / 10))
        values = []
        for line in range(lineNum, numOfValuesLines + lineNum):
            newValues = [int(val) for val in content[line].replace('\t', ' ').split(' ') if val.isdigit()]
            values = values + newValues

        lineNum += numOfValuesLines

        numOfCapacitiesLines = int(math.ceil(numOfKnapsacks / 10))
        capacities = []
        for line in range(lineNum, lineNum + numOfCapacitiesLines):
            newCapacities = [int(capacity) for capacity in content[1 + numOfValuesLines].replace('\t', ' ').split(' ')
                             if capacity.isdigit()]
            capacities = capacities + newCapacities

        capacities = np.array(capacities)

        numOfWeightsLines = numOfKnapsacks * numOfValuesLines
        lineNum += numOfCapacitiesLines

        knapsackWeightsPerItem = []
        for line in range(lineNum, lineNum + numOfWeightsLines):
            newWeights = [int(val) for val in content[line].replace('\t', ' ').split(' ') if val.isdigit()]
            knapsackWeightsPerItem = knapsackWeightsPerItem + newWeights

        knapsackWeightsPerItem = np.reshape(knapsackWeightsPerItem, (numOfKnapsacks, numOfItems))

        lineNum += numOfWeightsLines + 1

        optimal = int(content[lineNum])

        self._values = np.array(values)
        self._knapsackWeightsPerItem = knapsackWeightsPerItem
        self._numOfKnapsacks = numOfKnapsacks
        self._numOfItems = numOfItems
        self._capacities = capacities
        self._optimalVal = optimal
        self._densities = np.array(self.getDensitiesSum())

    def getNumOfKnapsacks(self):
        return self._numOfKnapsacks

    def isOptimal(self, results):
        return results == self._optimalVal

    def getNumOfItems(self):
        return len(self._values)

    def getWeights(self):
        return self._capacities

    def getValues(self):
        return self._values

    def getMatWeights(self):
        return self._knapsackWeightsPerItem

    def translateVec(self, vec):

        sumVal = 0
        for i, val in enumerate(vec):
            if val:
                sumVal += self._values[i]
        return sumVal


    def getTargetSize(self):
        pass

    def generateRandomVec(self):
        pass

    def calculateFitness(self, newVec):
        pass

    def getDensitiesSum(self):
        denSumArr = []
        for i in range(self._numOfItems):
            denSum = 0
            for j in range(self._numOfKnapsacks):
                if self._numOfKnapsacks > 1:
                    denSum += (self._values[i] / max(self._knapsackWeightsPerItem[j][i], 1))
                else:
                    denSum += self._values[i] / max(self._knapsackWeightsPerItem[i], 1)
            denSumArr.append(denSum)

        return denSumArr

    def getDensities(self):
        return self._densities
