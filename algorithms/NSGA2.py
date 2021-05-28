import random
import sys

import numpy as np

from algorithms.Algorithm import Algorithm
from entities.NSGA2Entity import NSGA2Entity

from util.Consts import BEST


# implements the genetic algorithm
class NSGA2(Algorithm):
    ELITE_RATE = 0.2  # elitism rate
    MUTATION_RATE = 0.4  # mutation rate

    def __init__(self, problem, popSize):
        super().__init__(problem)

        self._popSize = popSize
        self._citizens = None
        self._eliteRate = NSGA2.ELITE_RATE
        self._mutationRate = NSGA2.MUTATION_RATE

    def findSolution(self, maxIter):

        self._citizens = np.array(
            [NSGA2Entity(self._problem.generateRandomVec()) for _ in range(self._popSize)]
            # [NSGA2Entity(self._problem.generateGreedyVec())]
        )
        # init the fitness of the citizens
        self.updateFitnessAndDistance()
        best = self._citizens[BEST]

        # iterative improvement
        iterCounter = 0
        while self._problem.calculateFitness(best.getVec()) != 0 and iterCounter < maxIter:
            currPopulation = np.copy(self._citizens)
            self._mate()
            self.updateFitnessAndDistance()

            self._citizens = np.concatenate((currPopulation, self._citizens))
            self._citizens.sort()
            self._citizens = self._citizens[:self._popSize]

            best = self._citizens[BEST]
            iterCounter += 1

            print(f'Best: {self._problem.calculateFitness(best.getVec())}')

        self._citizens = None

        return best.getVec()

    def _mate(self):
        # get elite
        tempPopulation = self._getElite()
        while len(tempPopulation) < self._popSize:

            # choose parents
            parent1, parent2 = self.getParents()

            newChild = NSGA2Entity(self._problem.crossover(parent1.getVec(), parent2.getVec()))

            # mutation factor
            if random.random() < self._mutationRate:
                newChild.setVec(self._problem.mutate(newChild.getVec()))

            tempPopulation.append(newChild)

        self._citizens = np.array(tempPopulation)

    def updateFitnessAndDistance(self):
        # calculate non dominated fitness
        # calc objectives
        objVectors = []
        for citizen in self._citizens:
            citizen.setDistance(0)
            objVec = self._problem.calculateObjFunctions(citizen.getVec())
            objVectors.append(objVec)

        # calc fitness
        nonDominatedFitness = np.zeros(self._citizens.size, dtype=int)
        i = 0
        while i < self._citizens.size:
            objVec1 = objVectors[i]
            j = i + 1
            while j < self._citizens.size:
                objVec2 = objVectors[j]
                if (objVec1[0] < objVec2[0] and objVec1[1] <= objVec2[1]) or (
                        objVec1[1] < objVec2[1] and objVec1[0] <= objVec2[0]):
                    nonDominatedFitness[j] += 1
                elif (objVec2[0] < objVec1[0] and objVec2[1] <= objVec1[1]) or (
                        objVec2[1] < objVec1[1] and objVec2[0] <= objVec1[0]):
                    nonDominatedFitness[i] += 1

                j += 1
            i += 1

        for i, citizen in enumerate(self._citizens):
            citizen.setFitness(nonDominatedFitness[i])

        sortingIndices = self._citizens.argsort()
        objVectors = np.array(objVectors)[sortingIndices]
        self._citizens.sort()
        # partition to fronts
        fronts = []
        frontFitness = 0
        i = 0
        while i < self._citizens.size:
            front = []
            while i < self._citizens.size and self._citizens[i].getFitness() == frontFitness:
                front.append(self._citizens[i])
                i += 1
            if len(front) > 0:
                fronts.append(front)
            frontFitness += 1

        # calculate distance
        citizensSeen = 0
        for citizens in fronts:
            citizens = np.array(citizens)
            for objFunc in range(len(objVectors[0])):

                objValues = objVectors[:, objFunc]
                tempObjValues = objValues[citizensSeen:citizensSeen + citizens.size]

                indices = tempObjValues.argsort()
                sortedFront = citizens[indices]
                tempObjValues.sort()
                sortedFront[0].setDistance(sys.maxsize)
                sortedFront[-1].setDistance(sys.maxsize)
                if sortedFront.size > 2:
                    for i in range(1, sortedFront.size - 1):
                        disIncrease = (tempObjValues[i + 1] - tempObjValues[i - 1]) / \
                                      max((tempObjValues.max() - tempObjValues.min()), 1)
                        disIncrease += sortedFront[i].getDistance()
                        sortedFront[i].setDistance(disIncrease)
            citizensSeen += citizens.size

        self._citizens.sort()

    def _getElite(self):
        eliteSize = int(self._popSize * self._eliteRate)
        return self._citizens[:eliteSize].tolist()

    def _getCandidates(self):
        citizensSize = len(self._citizens)
        candidates = []

        # get half the population
        for i in range(int(citizensSize / 2)):
            candidates.append(self._citizens[i])

        return np.array(candidates)

    def getParents(self):
        firstCandidate = self._citizens[random.randrange(self._citizens.size / 2)]
        secondCandidate = self._citizens[random.randrange(self._citizens.size / 2)]
        if firstCandidate < secondCandidate:
            parent1 = firstCandidate
        else:
            parent1 = secondCandidate

        firstCandidate = self._citizens[random.randrange(self._citizens.size / 2)]
        secondCandidate = self._citizens[random.randrange(self._citizens.size / 2)]
        if firstCandidate < secondCandidate:
            parent2 = firstCandidate
        else:
            parent2 = secondCandidate

        return parent1, parent2
