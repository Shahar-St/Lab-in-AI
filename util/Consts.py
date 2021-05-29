import psutil

GA_POP_SIZE = 150  # ga population size
GA_MAX_ITER = 400  # maximum iterations

CLOCK_RATE = psutil.cpu_freq().current * (2 ** 20)  # clock ticks per second

BEST = 0
X = 0
Y = 1

DEFAULT_TARGET = 'FLEI.DAT'

'''------------------DEFAULT_PARSER-------------------'''

DEFAULT_ALGORITHM = 'LDS'
DEFAULT_PROBLEM = 'MultiKnapsack'

'''------------------ALLOWED_PARSER_NAMES-------------------'''

ALLOWED_ALGO_NAMES = ('NSGA2', 'LDS', 'CVRP2PartsSolver')
ALLOWED_PROBLEM_NAMES = ('CVRP', 'MultiKnapsack')
