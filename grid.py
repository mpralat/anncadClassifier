from hypercube import Hypercube
from example import Example
import numpy as np


class Grid:
    def __init__(self, level, bins_number):
        self.level = level
        self.hypercubes = []
        self.bins_number = bins_number
        self.bins_in_dim = int(np.sqrt(self.bins_number))
        self.create_grid()

    def create_grid(self):
        for i in range(self.bins_in_dim):
            for j in range(self.bins_in_dim):
                self.hypercubes.append(Hypercube([i, j]))

    def set_hypercubes_classes(self):
        for hypercube in self.hypercubes:
            hypercube.set_hypercube_class()
            print(hypercube.coords, hypercube.hypercube_class)

    def create_lower_level_grid(self):
        if self.level == 1:
            return


class BasicGrid(Grid):
    def __init__(self, min_attribute_range_list, max_attribute_range_list, bins_number):
        Grid.__init__(self, level=int(np.log2(bins_number)-1), bins_number=bins_number)
        self.min_attribute_range_list = min_attribute_range_list
        self.max_attribute_range_list = max_attribute_range_list
        self.width = (self.max_attribute_range_list[0] - self.min_attribute_range_list[0]) / self.bins_in_dim
        self.height = (self.max_attribute_range_list[1] - self.min_attribute_range_list[1]) / self.bins_in_dim
        self.lower_level_grids = {}
        # self.grids[self.basic_grid.level] = self.basic_grid


    def add_example_to_grid(self, observation):
        example = Example(observation)
        x = example.coords[0] / self.width
        y = example.coords[1] / self.height
        hypercube_index = int(y) * self.bins_in_dim + int(x)
        self.hypercubes[hypercube_index].add_example(example)
        self.hypercubes[hypercube_index].set_hypercube_class()


class HigherLevelGrid(Grid):
    def __init__(self, level, higher_level_bins_number, higher_level_hypercubes):
        bins_number = int(np.sqrt(higher_level_bins_number))
        Grid.__init__(self, level=level, bins_number=bins_number)

        # self.lower_level_grid = lower_level_grid
