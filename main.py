import matplotlib.pyplot as plt

# local imports
from grid import Grid

# Constants
from constants import GRID_ROWS, GRID_COLUMNS, TYPES, MAX_ITERATIONS, ITERATION_ANIMATE

plt.ion()


def step(grid):
    moved_agents = grid.move_random_unhappy_agent()
    if moved_agents is None:
        return False
    grid.set_unhappy_agents_in_neighbourhood(
        moved_agents[0].x, moved_agents[0].y, 1)
    grid.set_unhappy_agents_in_neighbourhood(
        moved_agents[1].x, moved_agents[1].y, 1)
    return True


grid = Grid(GRID_ROWS, GRID_COLUMNS, TYPES)
grid.generate_random_agents()
grid.set_unhappy_agents()
grid.plot()

i = 0
history = []
while True:
    history.append(len(grid.get_happy_agents()))
    if not step(grid):
        break

    if ITERATION_ANIMATE:
        grid.plot()
    i += 1
    if i >= MAX_ITERATIONS:
        raise Exception("Max iterations reached")

grid.plot()

# Plot history
plt.figure()
plt.plot(history)
plt.xlabel('Iterations')
plt.ylabel('Happy agents')
plt.show(block=True)
