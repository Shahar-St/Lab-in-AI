import numpy as np

from algorithms.Algorithm import Algorithm


class LDS(Algorithm):

    # estimate functions:
    # True = capacityRelaxation
    # False = knapsackIntegrityRelaxation
    def __init__(self, problem, estimateFunc=False):
        super().__init__(problem)

        self._estimateFunc = estimateFunc
        self._numOfItems = self._problem.getNumOfItems()
        self._withEarlyStopping = False
        self._maxIter = 0

    def findSolution(self, maxIter):
        return self.run(maxIter)

    def run(self, maxIter, withEarlyStopping=False):
        valuesSum = 0
        weights = self._problem.getWeights()
        self._maxIter = maxIter
        self._withEarlyStopping = withEarlyStopping

        globalSol = 0

        globalVecSol = np.zeros(self._problem.getNumOfItems(), dtype=int)
        zeroVec = np.zeros(self._problem.getNumOfItems(), dtype=int)

        # num of mistakes
        maxAllowedMistakes = min(maxIter, self._numOfItems)
        allowedMistakes = 0
        while allowedMistakes < maxAllowedMistakes:
            curSol, curVecSol = self.recursiveLds(0, allowedMistakes, valuesSum, weights.copy(), globalSol,
                                                  zeroVec.copy(), globalVecSol.copy())
            if curSol > globalSol:
                globalSol = curSol
                globalVecSol = curVecSol
            allowedMistakes += 1

        return globalVecSol

    def recursiveLds(self, depth, mistakes, valuesSum, weights, curBest, curVec, curBestVec):

        self._maxIter -= 1
        if depth == self._numOfItems or (self._withEarlyStopping and self._maxIter <= 0):
            if valuesSum >= curBest:
                return valuesSum, curVec
            return curBest, curBestVec

        # calc estimate according to heuristicOption
        if self._estimateFunc:
            est = valuesSum + self._getMaxValues(depth)
        else:
            est = self._knapsackIntegrityRelaxation(depth, valuesSum, weights.copy())

        if self._numOfItems - depth < mistakes or est < curBest:
            return curBest, curBestVec

        # go right
        if mistakes > 0:
            newSum1, temp1Vec = self.recursiveLds(depth + 1, mistakes - 1, valuesSum, weights.copy(), curBest,
                                                  curVec.copy(), curBestVec.copy())

            if newSum1 >= curBest:
                curBest, curBestVec = newSum1, temp1Vec

            if self._problem.isOptimal(curBest):
                return curBest, curBestVec

        # go left
        weights = self.updateWeights(weights, depth)
        if self.isKnapsackWeightIllegal(weights):
            return curBest, curBestVec

        curVec[depth] = 1
        newSum2, temp2Vec = self.recursiveLds(depth + 1, mistakes, valuesSum + self._problem.getValues()[depth],
                                              weights.copy(), curBest, curVec.copy(), curBestVec.copy())

        if newSum2 >= curBest:
            curBest, curBestVec = newSum2, temp2Vec

        return curBest, curBestVec

    def _capacityRelaxation(self, estimate, d):
        return estimate, estimate - self._problem.getValues()[d]

    def updateWeights(self, weights, d):
        matWeights = self._problem.getMatWeights()  # m*n
        for j in range(len(weights)):
            if self._problem.getNumOfKnapsacks() > 1:
                weights[j] -= matWeights[j][d]
            else:
                weights[j] -= matWeights[d]

        return weights

    def isKnapsackWeightIllegal(self, weights):
        for weight in weights:
            if weight < 0:
                return True
        return False

    def _knapsackIntegrityRelaxation(self, d, valuesSum, weights):
        denArr = self._problem.getDensities()[d:]
        indices = np.argsort(denArr)

        newEstimate = 0
        legal = True
        i = len(indices) - 1
        while i >= 0 and legal:
            bestItem = d + np.where(indices == i)[0][0]
            weights = self.updateWeights(weights, bestItem)
            if self.isKnapsackWeightIllegal(weights):
                legalPart = 1 - self.maxLegalPart(weights, bestItem)
                newEstimate += legalPart * self._problem.getValues()[bestItem]
                legal = False
            else:
                newEstimate += self._problem.getValues()[bestItem] + newEstimate
            i -= 1

        return newEstimate + valuesSum

    def maxLegalPart(self, weights, bestItem):
        matWeights = self._problem.getMatWeights()  # m*n
        maxLegalPart = 0
        for i in range(len(weights)):
            if weights[i] < 0:
                if self._problem.getNumOfKnapsacks() > 1:
                    legalPart = (-weights[i]) / matWeights[i][bestItem]
                else:
                    legalPart = (-weights[i]) / matWeights[bestItem]
                if legalPart > maxLegalPart:
                    maxLegalPart = legalPart

        return maxLegalPart

    def _getMaxValues(self, depth):
        sumOfValues = 0
        for i in range(depth, self._problem.getNumOfItems()):
            sumOfValues += self._problem.getValues()[i]
        return sumOfValues
