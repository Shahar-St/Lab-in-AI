import importlib
from abc import ABC, abstractmethod


# An abstract class that implements and declares common functionality to all problems
class Problem(ABC):

    def __init__(self, target):
        self._target = target

    @abstractmethod
    def getTargetSize(self):
        raise NotImplementedError

    @abstractmethod
    def translateVec(self, vec):
        raise NotImplementedError

    @abstractmethod
    def generateRandomVec(self):
        raise NotImplementedError

    @abstractmethod
    def calculateFitness(self, newVec):
        raise NotImplementedError

    @staticmethod
    def factory(problemName, target):
        module = importlib.import_module('problems.' + problemName + '.' + problemName)
        problem = getattr(module, problemName)
        return problem(target)
