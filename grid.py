from hypercube import Hypercube
from example import Example
import numpy as np
import abc
import itertools
import math
from scipy.spatial import distance
import sys


class Grid:
    __metaclass__ = abc.ABCMeta
    _threshold = 0.6

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, val):
        self._threshold = val

    def __init__(self, bins_number, level=None):
        bins_number_log = float(np.log2(bins_number))
        if bins_number_log.is_integer():
            self.bins_number = bins_number
        else:
            self.bins_number = 2**(math.ceil(bins_number / bins_number_log))
        self.bins_in_dim = int(np.sqrt(self.bins_number))
        if level is None:
            self.level = int(np.log2(self.bins_in_dim) + 1)
        else:
            self.level = level
        print("New Grid! " + str(self.level))
        self.hypercubes = [[0 for _ in range(self.bins_in_dim)] for _ in range(self.bins_in_dim)]
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

    def nearest_neighbours_class(self, example, x, y):
        nearest_class = ''
        if x % 2:
            xs = [x - 1, x]
        else:
            xs = [x, x + 1]
        if y % 2:
            ys = [y - 1, y]
        else:
            ys = [y, y + 1]
        min_dist = sys.maxsize
        for row, column in list(itertools.product(xs, ys)):
            print(row, column, self.hypercubes[row][column].hypercube_class, self.hypercubes[row][column].middle)
            if row is not x or column is not y:
                distnc = distance.euclidean([example.coords[0], example.coords[1]], [self.hypercubes[row][column].middle[0],
                        self.hypercubes[row][column].middle[1]])
                if distnc < min_dist \
                        and self.hypercubes[row][column].hypercube_class is not 'E':
                    min_dist = distnc
                    nearest_class = self.hypercubes[row][column].hypercube_class
        return nearest_class

    @abc.abstractmethod
    def set_hypercubes_classes(self):
        return


class BasicGrid(Grid):
    def __init__(self, min_attribute_range_list, max_attribute_range_list, bins_number, threshold):
        Grid.__init__(self, bins_number=bins_number)
        Grid.threshold = threshold
        self.min_attribute_range_list = min_attribute_range_list
        self.max_attribute_range_list = max_attribute_range_list
        self.width = (self.max_attribute_range_list[0] - self.min_attribute_range_list[0]) / self.bins_in_dim
        self.height = (self.max_attribute_range_list[1] - self.min_attribute_range_list[1]) / self.bins_in_dim
        # self.lower_level_grids = {}
        # self.grids[self.basic_grid.level] = self.basic_grid
        self.compute_middles_of_hypercubes()

    def add_example_to_grid(self, observation):
        example = Example(observation)
        x = int(example.coords[0] / self.width)
        y = int(example.coords[1] / self.height)
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

    def compute_middles_of_hypercubes(self):
        for hc in itertools.chain.from_iterable(self.hypercubes):
            hc.middle[1] = hc.coords[0] * self.width + self.width/2
            hc.middle[0] = hc.coords[1] * self.height + self.height/2
            print(hc.coords, hc.middle, hc.hypercube_class)

    def classify(self, example):
        x = int(example.coords[0] / self.width)
        y = int(example.coords[1] / self.height)
        print("----------")
        print(x, y)
        if self.hypercubes[y][x].hypercube_class is not 'E':
            return self.hypercubes[y][x].hypercube_class
        else:
            print("empty cube")
            print(self.hypercubes[y][x].middle)
            clas = self.child_grid.classify(example, x, y)
            print(clas)
            if clas == -1:
                clas = self.nearest_neighbours_class(example, x, y)
            return clas


class LowerLevelGrid(Grid):
    def __init__(self, level, parent_bins_number, parent_hypercubes):
        bins_number = int((parent_bins_number/4))
        Grid.__init__(self, bins_number=bins_number,level=level)
        self.parent_hypercubes = parent_hypercubes
        self.compute_middles_of_hypercubes()

    def set_hypercubes_classes(self):
        print("GRID LEVEL: " + str(self.level))
        for hypercube in itertools.chain.from_iterable(self.hypercubes):
            rows = [2*hypercube.coords[0], 2 * hypercube.coords[0] + 1]
            columns = [2*hypercube.coords[1], 2 * hypercube.coords[1] + 1]
            parents_list = []
            for row, column in list(itertools.product(rows, columns)):
                # creating a list of parent hypercubes
                parents_list.append(self.parent_hypercubes[row][column])
                print(row, column)
                # current_class = self.parent_hypercubes[row][column].hypercube_class
                # classes[current_class] = classes.get(current_class, 0) + 1  # <3
            #     TU TRZEBA WSZYSTKIE EXAMPLE
            hypercube.set_lower_level_hypercube_class(parents_list, self.threshold)
        print("--------------")
        if self.child_grid:
            self.child_grid.set_hypercubes_classes()

    def compute_middles_of_hypercubes(self):
        for hypercube in itertools.chain.from_iterable(self.hypercubes):
            sumx = 0
            sumy = 0
            rows = [2 * hypercube.coords[0], 2 * hypercube.coords[0] + 1]
            columns = [2 * hypercube.coords[1], 2 * hypercube.coords[1] + 1]
            parents_list = []
            for row, column in list(itertools.product(rows, columns)):
                sumx += self.parent_hypercubes[row][column].middle[0]
                sumy += self.parent_hypercubes[row][column].middle[1]
            hypercube.middle[0] = sumx / 4
            hypercube.middle[1] = sumy / 4

    def classify(self, example, x, y):
        x = int(x/2)
        y = int(y/2)
        print(x, y)
        if self.hypercubes[y][x].hypercube_class == 'E':
            clas = self.child_grid.classify(example, x, y)
            if clas == -1:
                clas = self.nearest_neighbours_class(example, x, y)
            return clas
        elif self.hypercubes[y][x].hypercube_class == 'M':
            return -1  # flag indicating that we need to compute distance
        else:
            print("heh")
            return self.hypercubes[y][x].hypercube_class
