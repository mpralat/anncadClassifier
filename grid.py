from hypercube import Hypercube
from example import Example
import numpy as np


class Grid:
    def __init__(self, bins_number, min_attribute_range_list, max_attribute_range_list):
        self.level = 0
        self.hypercubes = []
        self.bins_number = bins_number
        self.bins_in_dim = int(np.sqrt(self.bins_number))
        self.min_attribute_range_list = min_attribute_range_list
        self.max_attribute_range_list = max_attribute_range_list
        self.width = (self.max_attribute_range_list[0] - self.min_attribute_range_list[0]) / self.bins_in_dim
        self.height = (self.max_attribute_range_list[1] - self.min_attribute_range_list[1]) / self.bins_in_dim
        self.create_grid()

    def create_grid(self):
        for i in range(self.bins_in_dim):
            for j in range(self.bins_in_dim):
                self.hypercubes.append(Hypercube([i, j]))

    def set_hypercubes_classes(self):
        for hypercube in self.hypercubes:
            hypercube.set_hypercube_class()
            print(hypercube.coords, hypercube.hypercube_class)

    def add_example_to_grid(self, observation):
        example = Example(observation)
        x = example.coords[0] / self.width
        y = example.coords[1] / self.height
        hypercube_index = int(y) * self.bins_in_dim + int(x)
        self.hypercubes[hypercube_index].add_example(example)
        self.hypercubes[hypercube_index].set_hypercube_class()