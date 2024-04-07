import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import colors

from agent import Agent
from constants import EMPTY_TYPE, UNHAPPY_TYPE


class Grid:
    def __init__(self, rows, columns, types):
        self.rows = rows
        self.columns = columns
        self.types = types
        self.grid = np.zeros((rows, columns), dtype=object)
        self.agents = []

        all_types = [EMPTY_TYPE, UNHAPPY_TYPE] + types

        # pre-compute patches for plot legend
        self.patches = [mpatches.Patch(
            color=type.color, label=type.name) for type in all_types]

        # create a colormap for more efficient plotting
        sorted_types = sorted(all_types, key=lambda type: type.value)
        all_colors = [type.color for type in sorted_types]
        self.cmap = colors.ListedColormap(all_colors)

        vmin = 0
        vmax = len(all_colors) - 1
        # normalization object for color mapping
        self.norm = colors.Normalize(vmin=vmin, vmax=vmax)

    def generate_random_agents(self):
        # check that probabilities sum to 1
        probabilities_sum = EMPTY_TYPE.probability + \
            sum([type.probability for type in self.types])
        if probabilities_sum != 1:
            raise ValueError(f"Typ probabilities do not sum to 1; sum is {
                             probabilities_sum}")

        for i in range(self.rows):
            for j in range(self.columns):
                rand = np.random.rand()
                cumulative_probability = EMPTY_TYPE.probability

                if rand < cumulative_probability:
                    self.add_agent(Agent(EMPTY_TYPE, i, j))
                else:
                    for type in self.types:
                        cumulative_probability += type.probability
                        if rand < cumulative_probability:
                            self.add_agent(Agent(type, i, j))
                            break

    def add_agent(self, agent):
        self.agents.append(agent)
        self.grid[agent.x, agent.y] = agent

    def switch_agents(self, agent1, agent2):
        x1, y1 = agent1.x, agent1.y
        x2, y2 = agent2.x, agent2.y

        self.grid[x1, y1] = agent2
        self.grid[x2, y2] = agent1
        agent1.x, agent1.y = x2, y2
        agent2.x, agent2.y = x1, y1

    def get_empty_agents(self):
        return [agent for agent in self.agents if agent.type == EMPTY_TYPE]

    def get_random_empty_agent(self):
        empty_agents = self.get_empty_agents()
        if len(empty_agents) == 0:
            return None
        return empty_agents[np.random.randint(len(empty_agents))]

    def get_neighbours(self, x, y, radius):
        neighbours = []
        for i in range(-radius, radius + 1):
            for j in range(-radius, radius + 1):
                if i == 0 and j == 0:
                    continue
                # wrap around (torus model)
                xi = (x + i) % self.rows
                yj = (y + j) % self.columns
                neighbours.append(self.grid[xi, yj])
        return neighbours

    def get_neighbour_type_ratio(self, agent, radius):
        neighbours = self.get_neighbours(agent.x, agent.y, radius)
        type_count = 0
        for neighbour in neighbours:
            if neighbour.type == agent.type or neighbour.type == EMPTY_TYPE:
                type_count += 1
        return type_count / len(neighbours)

    def get_happy_agents(self):
        return [agent for agent in self.agents if agent.happy and agent.type != EMPTY_TYPE]

    def get_unhappy_agents(self):
        return [agent for agent in self.agents if not agent.happy]

    def get_random_unhappy_agent(self):
        unhappy_agents = self.get_unhappy_agents()
        if len(unhappy_agents) == 0:
            return None
        return unhappy_agents[np.random.randint(len(unhappy_agents))]

    def set_unhappy_agents(self):
        for agent in self.agents:
            if agent.type == EMPTY_TYPE:
                agent.happy = True
            else:
                agent.happy = self.get_neighbour_type_ratio(
                    agent, 1) >= agent.type.tolerance

    def set_unhappy_agents_in_neighbourhood(self, x, y, radius):
        for i in range(-radius, radius + 1):
            for j in range(-radius, radius + 1):
                xi = (x + i) % self.rows
                yj = (y + j) % self.columns
                agent = self.grid[xi, yj]
                if agent.type == EMPTY_TYPE:
                    agent.happy = True
                else:
                    agent.happy = self.get_neighbour_type_ratio(
                        agent, 1) >= agent.type.tolerance

    def move_random_unhappy_agent(self):
        agent = self.get_random_unhappy_agent()
        if agent is None:
            return None
        empty_agent = self.get_random_empty_agent()
        if empty_agent is not None:
            self.switch_agents(agent, empty_agent)
        return [agent, empty_agent]

    def initialize_plot(self):
        self.fig, self.ax = plt.subplots()
        self.img = self.ax.imshow(
            np.zeros((self.rows, self.columns)), cmap=self.cmap, interpolation='nearest')

        # Color normalization
        self.img.set_norm(self.norm)

    def plot(self):
        if not hasattr(self, 'ax'):
            self.initialize_plot()

        grid_colors = np.array([[agent.get_type_value()
                               for agent in row] for row in self.grid])

        self.img.set_data(grid_colors)

        plt.legend(handles=self.patches, bbox_to_anchor=(
            1.05, 0.5), loc='center left')
        plt.subplots_adjust(right=0.6)

        plt.draw()
        plt.pause(0.000001)

        plt.show()
