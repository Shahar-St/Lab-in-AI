import psutil

GA_POP_SIZE = 300  # ga population size
GA_MAX_ITER = 200  # maximum iterations

CLOCK_RATE = psutil.cpu_freq().current * (2 ** 20)  # clock ticks per second

BEST = 0
X = 0
Y = 1

DEFAULT_TARGET = '1'

'''------------------DEFAULT_PARSER-------------------'''

DEFAULT_ALGORITHM = 'NSGA2'
DEFAULT_PROBLEM = 'CVRP'

'''------------------ALLOWED_PARSER_NAMES-------------------'''

ALLOWED_ALGO_NAMES = ('NSGA2', 'LDS')
ALLOWED_PROBLEM_NAMES = ('CVRP', 'MultiKnapsack', 'CVRP2PartsSolver')
