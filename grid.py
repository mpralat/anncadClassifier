from hypercube import Hypercube
from example import Example
import numpy as np
import abc
import itertools


class Grid:
    __metaclass__ = abc.ABCMeta

    def __init__(self, bins_number, level=None):

        self.bins_number = bins_number
        self.bins_in_dim = int(np.sqrt(self.bins_number))
        if level is None:
            self.level = int(np.log2(self.bins_in_dim) + 1)
        else:
            self.level = level
        print("New Grid! " + str(self.level))
        self.hypercubes = [[0 for x in range(self.bins_in_dim)] for y in range(self.bins_in_dim)]
        # print(self.hypercubes)
        self.create_grid()
        self.child_grid = self.create_lower_level_grid()

    def create_grid(self):
        for i in range(self.bins_in_dim):
            for j in range(self.bins_in_dim):
                self.hypercubes[i][j] = Hypercube([i, j])

    def create_lower_level_grid(self):
        if self.level == 1:
            return False
        else:
            print(self.bins_number)
            print("~~~~~~~~~~")
            return LowerLevelGrid(self.level - 1, self.bins_number, self.hypercubes)

    @abc.abstractmethod
    def set_hypercubes_classes(self):
        return


class BasicGrid(Grid):
    def __init__(self, min_attribute_range_list, max_attribute_range_list, bins_number):
        Grid.__init__(self, bins_number=bins_number)
        self.min_attribute_range_list = min_attribute_range_list
        self.max_attribute_range_list = max_attribute_range_list
        self.width = (self.max_attribute_range_list[0] - self.min_attribute_range_list[0]) / self.bins_in_dim
        self.height = (self.max_attribute_range_list[1] - self.min_attribute_range_list[1]) / self.bins_in_dim
        self.lower_level_grids = {}
        # self.grids[self.basic_grid.level] = self.basic_grid

    def add_example_to_grid(self, observation):
        example = Example(observation)
        x = int(example.coords[0] / self.width)
        y = int(example.coords[1] / self.height)
        hypercube_index = int(y) * self.bins_in_dim + int(x)
        self.hypercubes[y][x].add_example(example)
        self.hypercubes[y][x].set_hypercube_class()

    def set_hypercubes_classes(self):
        print("BASEGRID hypercubes")
        list_of_all_hc = list(itertools.chain.from_iterable(self.hypercubes))
        print(" I have " + str(len(list_of_all_hc)) + " hypercubes :3")
        for hypercube in list_of_all_hc:
            hypercube.set_hypercube_class()
            print(hypercube.coords, hypercube.hypercube_class)
        print("------------------")
        self.child_grid.set_hypercubes_classes()


class LowerLevelGrid(Grid):
    def __init__(self, level, parent_bins_number, parent_hypercubes):
        bins_number = int((parent_bins_number/4))
        Grid.__init__(self, bins_number=bins_number,level=level)
        self.parent_hypercubes = parent_hypercubes

        # self.lower_level_grid = lower_level_grid

    def set_hypercubes_classes(self):
        print("GRID LEVEL: " + str(self.level))
        for hypercube in itertools.chain.from_iterable(self.hypercubes):
            classes = {}
            rows = [2*hypercube.coords[0], 2 * hypercube.coords[0] + 1]
            columns = [2*hypercube.coords[1], 2 * hypercube.coords[1] + 1]
            for row, column in list(itertools.product(rows, columns)):
                print(row, column)
                current_class = self.parent_hypercubes[row][column].hypercube_class
                classes[current_class] = classes.get(current_class, 0) + 1  # <3

            print(classes)
        print("--------------")
        if self.child_grid:
            self.child_grid.set_hypercubes_classes()

