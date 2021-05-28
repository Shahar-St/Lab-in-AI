from algorithms.Algorithm import Algorithm


class LDS(Algorithm):

    def __init__(self, problem, capacityRelaxation=True):
        super().__init__(problem)

        self._capacityRelaxation = capacityRelaxation
        self._numOfItems = self._problem.getNumOfItems()

    def findSolution(self, maxIter):

        valuesSum = curBest = 0
        weights = self._problem.getWeights()
        estimate = self.getInitialEstimate()  # calc initialEstimate according to heuristicOption

        globalSol = 0

        # num of mistakes
        maxAllowedMistakes = min(maxIter, self._numOfItems)
        allowedMistakes = 0
        while allowedMistakes < maxAllowedMistakes:
            curSol = self.recursiveLds(0, allowedMistakes, valuesSum, weights.copy(), estimate, curBest)
            if curSol > globalSol:
                globalSol = curSol
            allowedMistakes += 1

        return globalSol

    def recursiveLds(self, depth, mistakes, valuesSum, weights, estimate, curBest):

        if depth == self._numOfItems:
            return max(valuesSum, curBest)

        if self._numOfItems - depth < mistakes or estimate < curBest:
            return -1

        # calc estimate according to heuristicOption
        leftEst, rightEst = self.calcEstimates(estimate, depth)

        # go right
        if mistakes > 0:
            newSum1 = self.recursiveLds(depth + 1, mistakes - 1, valuesSum, weights.copy(), rightEst, curBest)
            curBest = max(newSum1, curBest)
            if self._problem.isOptimal(curBest):
                return curBest

        # go left
        weights = self.updateWeights(weights, depth)
        if self.isKnapsackWeightIllegal(weights):
            return curBest

        newSum2 = self.recursiveLds(depth + 1, mistakes, valuesSum + self._problem.getValues()[depth],
                                    weights.copy(), leftEst, curBest)
        curBest = max(newSum2, curBest)

        return curBest

    def getInitialEstimate(self):

        if self._capacityRelaxation:
            return self._problem.getValues().sum()

        # calc second heuristic initialEstimate # todo
        return 0

    def calcEstimates(self, estimate, d):

        if self._capacityRelaxation:
            return estimate, estimate - self._problem.getValues()[d]

        # calc second heuristic estimate # todo
        return 0, 0

    def updateWeights(self, weights, d):
        matWeights = self._problem.getMatWeights()  # m*n
        for j in range(len(weights)):  # len = m (naps)
            weights[j] -= matWeights[j][d]

        return weights

    def isKnapsackWeightIllegal(self, weights):
        for weight in weights:
            if weight < 0:
                return True
        return False
