import importlib
from abc import ABC, abstractmethod


# An abstract class that implements and declares common functionality to all algorithms
class Algorithm(ABC):

    def __init__(self, problem):
        self._problem = problem

    # This function should run the algorithm
    @abstractmethod
    def findSolution(self, maxIter):
        raise NotImplementedError

    @staticmethod
    def factory(algoName, popSize, problem):
        module = importlib.import_module('algorithms.' + algoName)

        algo = getattr(module, algoName)

        if algoName == 'NSGA2':
            return algo(
                problem=problem,
                popSize=popSize
            )

        return algo(
            problem=problem,
        )
