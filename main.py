import argparse
import time

from algorithms.Algorithm import Algorithm
from problems.Problem import Problem
from util.Consts import *


def main():
    startTime = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--algo', default=DEFAULT_ALGORITHM)
    parser.add_argument('-p', '--problem', default=DEFAULT_PROBLEM)
    parser.add_argument('-ps', '--popSize', type=int, default=GA_POP_SIZE)
    parser.add_argument('-t', '--target', default=DEFAULT_TARGET)

    args = parser.parse_args()

    # get params
    algoName = args.algo
    popSize = args.popSize
    target = args.target
    problemName = args.problem

    problem = Problem.factory(problemName, target)

    algo = Algorithm.factory(
        algoName=algoName,
        popSize=popSize,
        problem=problem
    )

    # find a solution and print it
    sol, solVec = algo.findSolution(GA_MAX_ITER)
    print(sol)
    print(f'Solution = {problem.translateVec(solVec)}\n')

    # print summery of run
    endTime = time.time()
    elapsedTime = endTime - startTime
    print(f'Total elapsed time in seconds: {elapsedTime}')
    print(f'This process took {elapsedTime * CLOCK_RATE} clock ticks')


if __name__ == '__main__':
    main()
