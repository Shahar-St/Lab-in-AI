import math
import os
import random

import numpy as np

from problems.Problem import Problem
from util.Consts import X, Y
from util.Util import getValidIndexes


# Define the problem and implements methods that algorithms can use
class CVRP(Problem):

    def __init__(self, target, optimalVal=None, dim=None, vehicleCapacity=None, nodesCoordinates=None,
                 nodesDemands=None, initFromFile=True):
        super().__init__(target)
        self._optimalVal = optimalVal
        self._dim = dim
        self._vehicleCapacity = vehicleCapacity
        self._nodesCoordinates = nodesCoordinates
        self._nodesDemands = nodesDemands
        if initFromFile:
            self._initFromFile(target)

    def _initFromFile(self, target):
        super().__init__(target)
        # read and parse input file

        filePath = os.path.join(os.getcwd(), 'problems', 'CVRP', 'inputfiles', str(target) + '.txt')
        inputFile = open(filePath, 'r')

        coordinatesSection = 7
        content = inputFile.readlines()
        content = [line.strip('\n') for line in content]

        # get optimal solution
        self._optimalVal = int(''.join(content[1].strip(')')[content[1].find('value:') + 7:]))

        # get dim
        self._dim = int(''.join(content[3][content[3].find(':') + 2:]))

        # get vehicle capacity
        self._vehicleCapacity = int(''.join(content[5][content[5].find(':') + 2:]))

        nodesCoordinates = []
        # get coords
        for i in range(coordinatesSection, coordinatesSection + self._dim):
            nodeCoordsStr = content[i][content[i].find(' ') + 1:]
            coordsList = nodeCoordsStr.split(' ')
            nodeX = int(coordsList[X])
            nodeY = int(coordsList[Y])
            nodesCoordinates.append((nodeX, nodeY))

        # get capacity
        nodesDemands = []
        for i in range(coordinatesSection + self._dim + 1, coordinatesSection + self._dim * 2 + 1):
            nodeWeight = content[i].split(' ')
            nodesDemands.append(int(nodeWeight[1]))

        self._nodesCoordinates = np.array(nodesCoordinates)
        self._nodesDemands = np.array(nodesDemands)

    def getCoords(self):
        return self._nodesCoordinates.copy()

    def getDemands(self):
        return self._nodesDemands.copy()

    def getVehicleCapacity(self):
        return self._vehicleCapacity

    def generateRandomVec(self):
        # each solution is represented by a permutation [1, dim - 1]
        vec = np.random.permutation(list(range(1, self._dim)))
        return vec.tolist()

    def getVecWithStops(self, vec):
        vecWithStops = [0, vec[0]]
        currentTruckCapacity = self._nodesDemands[vec[0]]

        for i in range(len(vec) - 1):
            # update route capacity
            currentTruckCapacity += self._nodesDemands[vec[i + 1]]
            # check if exceeded capacity
            if currentTruckCapacity > self._vehicleCapacity:
                vecWithStops.append(0)
                currentTruckCapacity = self._nodesDemands[vec[i + 1]]

            vecWithStops.append(vec[i + 1])

        vecWithStops.append(0)
        return vecWithStops

    def calculateFitness(self, vec):

        vecWithStops = self.getVecWithStops(vec)

        distance = 0
        for i in range(len(vecWithStops) - 1):
            distance += self.calcDist(vecWithStops[i], vecWithStops[i + 1])

        return int(distance - self._optimalVal)

    def calcDist(self, node1, node2):
        return math.dist(self._nodesCoordinates[node1], self._nodesCoordinates[node2])

    # takes a vec and print it according to the required output form
    def translateVec(self, vec):
        routesStr = f'{self.calculateFitness(vec) + self._optimalVal}\n0 '
        vecWithStops = self.getVecWithStops(vec)
        for i in range(1, len(vecWithStops) - 1):
            routesStr += f'{vecWithStops[i]} '
            if vecWithStops[i] == 0:
                routesStr += '\n0 '

        routesStr += '0\n'

        return routesStr

    def _sumOfDemands(self, vec):
        demands = 0
        for node in vec:
            demands += self._nodesDemands[node]

        return demands

    # get a 'nearest neighbor' greedy vec
    def generateGreedyVec(self):
        allCities = [i for i in range(1, self._dim)]
        greedyVec = []
        minCity = self._getCityWithMinDistanceToCurrent(0, allCities)
        greedyVec.append(minCity)
        allCities.remove(minCity)

        while len(allCities) > 0:
            minCity = self._getCityWithMinDistanceToCurrent(greedyVec[-1], allCities)
            greedyVec.append(minCity)
            allCities.remove(minCity)

        return greedyVec

    def _getCityWithMinDistanceToCurrent(self, current, cities):
        minCity = cities[0]
        minDis = self.calcDist(current, cities[0])
        for city in cities:
            currDis = self.calcDist(current, city)
            if currDis < minDis:
                minCity = city
                minDis = currDis

        return minCity

    def getTargetSize(self):
        return self._dim - 1

    def calculateObjFunctions(self, vec):
        res = []
        # distance
        dis = self.calculateFitness(vec)
        res.append(dis)

        # num of vehicles
        vecWithStops = self.getVecWithStops(vec)
        numOfVehicles = vecWithStops.count(0) - 1
        res.append(numOfVehicles)

        return res

    # Best Route Better Adjustment recombination
    def crossover(self, parent1Vec, parent2Vec):

        parent1Vec = self.getVecWithStops(parent1Vec)

        parent1Routes = []
        parent1routesDeltas = []

        i = 0
        while i < len(parent1Vec):
            if 0 not in parent1Vec[i:]:
                # last route
                indexOfStop = len(parent1Vec)
            else:
                indexOfStop = parent1Vec.index(0, i)

            route = parent1Vec[i:indexOfStop]
            sumOfRoute = self._sumOfDemands(route)
            delta = self._vehicleCapacity - sumOfRoute
            parent1Routes.append(route)
            parent1routesDeltas.append(delta)

            i = indexOfStop + 1

        # sort the routes based on their deltas
        sortedRoutes = [route for _, route in sorted(zip(parent1routesDeltas, parent1Routes))]

        # move half the routes to new child
        newChildVec = sum(sortedRoutes[:int(len(sortedRoutes) / 2)], [])

        # complete the rest with parent2
        for node in parent2Vec:
            if node not in newChildVec:
                newChildVec.append(node)

        return newChildVec

    def mutate(self, vec):
        if random.random() < 2:
            return self._swapMutation(vec)
        else:
            return self._insertionMutation(vec)

    # pick 2 indexes randomly and swap them
    def _swapMutation(self, vec):
        vecSize = len(vec)
        index1, index2 = getValidIndexes(vecSize)
        vec[index1], vec[index2] = vec[index2], vec[index1]
        return vec

    # takes a random index and insert it to a random location
    def _insertionMutation(self, vec):
        vecSize = len(vec)
        index1, insertionIndex = getValidIndexes(vecSize)
        indexVal = vec[index1]
        vec.pop(index1)
        vec.insert(insertionIndex, indexVal)

        return vec
