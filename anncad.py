import numpy as np
from hypercube import Hypercube
from grid import Grid
from example import Example

class AnncadClassifier:
    def __init__(self, bins_number, min_attribute_range_list, max_attribute_range_list):
        self.bins_number = bins_number
        # TODO pow 2
        self.min_attribute_range_list = min_attribute_range_list
        self.max_attribute_range_list = max_attribute_range_list
        self.bins_in_dim = int(np.sqrt(self.bins_number))
        self.width = (self.max_attribute_range_list[0] - self.min_attribute_range_list[0]) / self.bins_in_dim
        self.height = (self.max_attribute_range_list[1] - self.min_attribute_range_list[1]) / self.bins_in_dim
        self.grid = []
        self.create_grid()

    def create_grid(self):
        for i in range(self.bins_in_dim):
            for j in range(self.bins_in_dim):
                self.grid.append(Hypercube([i, j]))

    def add_example_to_grid(self, observation):
        example = Example(observation)
        x = example.coords[0] / self.width
        y = example.coords[1] / self.height
        self.grid[int(y) * self.bins_in_dim + int(x)].add_example(example)
        print(self.grid)

    def set_hypercubes_classes(self):
        for hypercube in self.grid:
            # print(hypercube.coords)
            hypercube.set_hypercube_class()
            print(hypercube.coords, hypercube.hypercube_class)