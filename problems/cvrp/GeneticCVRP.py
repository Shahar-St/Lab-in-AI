import random

from problems.cvrp.CVRP import CVRP
from util.Util import getValidIndexes


class GeneticCVRP(CVRP):

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
