from entities.IndividualEntity import IndividualEntity


class NSGA2Entity(IndividualEntity):

    def __init__(self, vec):
        super().__init__(vec)
        self._distance = None

    def getDistance(self):
        return self._distance

    def setDistance(self, newDis):
        self._distance = newDis

    def __lt__(self, other):
        if self._fitness == other.getFitness():
            return self._distance > other.getDistance()

        return self._fitness < other.getFitness()
