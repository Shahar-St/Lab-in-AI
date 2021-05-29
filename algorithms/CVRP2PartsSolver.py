import sys

import numpy as np

from algorithms.Algorithm import Algorithm
from algorithms.LDS import LDS
from algorithms.NSGA2 import NSGA2
from problems.CVRP.CVRP import CVRP
from problems.MultiKnapsack.MultiKnapsack import MultiKnapsack
from util.Consts import GA_POP_SIZE


class CVRP2PartsSolver(Algorithm):

    def findSolution(self, maxIter):

        routes = []
        size = self._problem.getTargetSize()
        unvisitedCities = [i for i in range(size)]
        while len(unvisitedCities) > 0:

            demands = []
            for i in range(len(self._problem.getDemands())):
                if i in unvisitedCities:
                    demands.append(self._problem.getDemands()[i + 1])

            knapsackProblem = MultiKnapsack(
                values=np.ones(len(unvisitedCities)),
                knapsackWeightsPerItem=np.array(demands),
                numOfKnapsacks=1,
                numOfItems=len(unvisitedCities),
                capacities=[self._problem.getVehicleCapacity()],
                optimal=np.inf,
                target=None,
                initFromFile=False
            )

            lds = LDS(knapsackProblem)
            sol = lds.run(maxIter, withEarlyStopping=True)
            route = [unvisitedCities[i] for i in range(len(sol)) if sol[i] == 1]
            routes.append(route)

            for city in route:
                unvisitedCities.remove(city)

        finalSol = []
        for route in routes:
            coords = self._problem.getCoords()
            newCoords = []
            for i in range(len(coords)):
                if i in route:
                    newCoords.append(coords[i + 1])
            newCoords.insert(0, coords[0])

            demands = self._problem.getDemands()
            newDemands = []
            for i in range(len(demands)):
                if i in route:
                    newDemands.append(demands[i + 1])
            newDemands.insert(0, 0)

            cvrp = CVRP(
                optimalVal=-sys.maxsize,
                dim=len(route) + 1,
                vehicleCapacity=self._problem.getVehicleCapacity(),
                nodesCoordinates=np.array(newCoords),
                nodesDemands=np.array(newDemands),
                initFromFile=False,
                target=None
            )

            nsga = NSGA2(cvrp, GA_POP_SIZE)
            sol = nsga.findSolution(maxIter / 2)
            # transfer back to original cities
            indices = np.array(sol).argsort()
            originalCities = np.array(route)[indices]

            for city in originalCities:
                finalSol.append(city)

        return finalSol
