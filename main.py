import argparse
import time

from algorithms.Algorithm import Algorithm
from problems.cvrp.CVRP import CVRP
from problems.cvrp.GeneticCVRP import GeneticCVRP
from problems.multiknapsack.MultiKnapsack import MultiKnapsack
from util.Consts import *


def main():
    startTime = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--algo', default=DEFAULT_ALGORITHM)
    parser.add_argument('-ps', '--popSize', type=int, default=GA_POP_SIZE)
    parser.add_argument('-t', '--target', default=DEFAULT_TARGET)

    args = parser.parse_args()

    # get params
    algoName = args.algo
    popSize = args.popSize
    target = args.target

    problem = GeneticCVRP(target)

    algo = Algorithm.factory(
        algoName=algoName,
        popSize=popSize,
        problem=problem
    )

    # find a solution and print it
    solVec = algo.findSolution(GA_MAX_ITER)
    print(f'Solution = {problem.translateVec(solVec)}\n')

    # print summery of run
    endTime = time.time()
    elapsedTime = endTime - startTime
    print(f'Total elapsed time in seconds: {elapsedTime}')
    print(f'This process took {elapsedTime * CLOCK_RATE} clock ticks')


if __name__ == '__main__':
    main()
