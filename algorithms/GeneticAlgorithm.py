import random

import numpy as np

from algorithms.Algorithm import Algorithm

from entities.IndividualEntity import IndividualEntity
from util.Consts import BEST


# implements the genetic algorithm
class GeneticAlgorithm(Algorithm):
    ELITE_RATE = 0.2  # elitism rate
    MUTATION_RATE = 0.4  # mutation rate

    def __init__(self, problem, popSize):
        super().__init__(problem)

        self._popSize = popSize
        self._citizens = np.array(
            [IndividualEntity(problem.generateRandomVec()) for _ in
             range(popSize)])

        self._eliteRate = GeneticAlgorithm.ELITE_RATE
        self._mutationRate = GeneticAlgorithm.MUTATION_RATE
        self._problem = problem

    def findSolution(self, maxIter):
        # init the fitness of the citizens
        self.updateFitness()
        best = self._citizens[BEST]

        # iterative improvement
        iterCounter = 0
        while best.getFitness() != 0 and iterCounter < maxIter:
            self._mate()

            self.updateFitness()
            best = self._citizens[BEST]
            iterCounter += 1

            print(f'Best:\n{self._problem.translateVec(best.getVec())}({best.getFitness()})')

        return best.getVec()

    def _mate(self):

        # get elite
        tempPopulation = self._getElite()

        # get the candidates to be parents
        candidates = self._getCandidates()
        candidatesSize = len(candidates)

        # fill in the rest of the population
        while len(tempPopulation) < self._popSize:

            # choose parents and make child
            parent1 = candidates[random.randrange(candidatesSize)]
            parent2 = candidates[random.randrange(candidatesSize)]
            newChild = self._problem.crossover(parent1.getVec(), parent2.getVec())

            # mutation factor
            if random.random() < self._mutationRate:
                newChild.setVec(self._problem.mutate(newChild.getVec()))

            tempPopulation.append(newChild)

        self._citizens = np.array(tempPopulation)

    def updateFitness(self):
        fitnessValues = []
        for citizen in self._citizens:
            fitnessVal = self._problem.calculateFitness(citizen.getVec())
            citizen.setFitness(fitnessVal)
            fitnessValues.append(fitnessVal)

        # calculate mean and std of fitness function across all genes
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
