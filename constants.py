from matplotlib import colors
from type import Type

MAX_ITERATIONS = 50000

# Set to False to disable animation during iterations; will only show final plot and speed up the processing by a lot
ITERATION_ANIMATE = True

GRID_ROWS = 50
GRID_COLUMNS = 50

EMPTY_TYPE = Type("Empty Space", 'white', probability=0.1)
UNHAPPY_TYPE = Type("Unhappy Agent", 'orange', probability=0)

TYPE1 = Type("Type 1", 'red', probability=0.45, tolerance=0.5)
TYPE2 = Type("Type 2", 'blue', probability=0.45, tolerance=0.5)
TYPES = [TYPE1, TYPE2]
