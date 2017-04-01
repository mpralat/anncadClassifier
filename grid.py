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

    def __init__(self, bins_number, dims, level=None):
        bins_number_log = float(np.log2(bins_number))
        if bins_number_log.is_integer():
            self.bins_number = bins_number
        else:
            self.bins_number = 2**(math.ceil(bins_number / bins_number_log))
        self.dims = dims
        self.bins_in_dim = int(np.power(self.bins_number, 1/self.dims))

        if level is None:
            self.level = int(np.log2(self.bins_in_dim) + 1)
        else:
            self.level = level
        print("New Grid! " + str(self.level))

        shape = tuple([self.bins_in_dim] * self.dims)
        self.hypercubes = np.ones((shape)).astype(Hypercube)

        self.create_grid()
        self.child_grid = self.create_lower_level_grid()

    def create_grid(self):
        for indices, hypercube in np.ndenumerate(self.hypercubes):
            self.hypercubes[indices] = Hypercube(indices)

    def create_lower_level_grid(self):
        if self.level == 1:
            return False
        else:
            return LowerLevelGrid(self.level - 1, self.bins_number, self.hypercubes, self.dims)


    def nearest_neighbours_class(self, example, coords, parents_indices):
        print(parents_indices)

        parents_data = [(self.hypercubes[parent].middle, self.hypercubes[parent].hypercube_class) for parent in parents_indices]
        distances = sorted([(distance.euclidean(example.coords, parent[0]), parent[1]) for parent in parents_data if not parent[1]=='E'])
        print("############")
        print(distances)
        return distances[0][1]

    @abc.abstractmethod
    def set_hypercubes_classes(self):
        return


class BasicGrid(Grid):
    def __init__(self, min_attribute_range_list, max_attribute_range_list, bins_number, threshold):
        self.min_attribute_range_list = min_attribute_range_list
        self.max_attribute_range_list = max_attribute_range_list
        self.dims = len(self.min_attribute_range_list)
        Grid.__init__(self, bins_number=bins_number, dims=self.dims)
        Grid.threshold = threshold
        # TODO better name
        self.hypercube_measurements = [(self.max_attribute_range_list[x] - self.min_attribute_range_list[x]) / self.bins_in_dim for x in range(len(self.min_attribute_range_list))]
        self.set_hypercubes_classes()
        self.compute_middles_of_hypercubes()

    def add_example_to_grid(self, observation):
        example = Example(observation)

        # TODO self-dimensions
        indices = tuple([int(example.coords[x] / self.hypercube_measurements[x]) for x in range(self.dims-1, -1, -1)])
        self.hypercubes[indices].add_example(example)
        self.hypercubes[indices].set_hypercube_class()
        print(self.hypercubes[indices].hypercube_class)


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
            for i in range(self.dims - 1, -1, -1):
                index = self.dims - (i + 1)
                hc.middle[i] = (hc.coords[index] + 0.5) * self.hypercube_measurements[index]
            print(hc.coords, hc.middle, hc.hypercube_class)

    def classify(self, example):
        coords = tuple([int(example.coords[i] / self.hypercube_measurements[i]) for i in range(self.dims-1, -1, -1)])
        print("----------")
        if self.hypercubes[coords].hypercube_class is not 'E':
            return self.hypercubes[coords].hypercube_class
        else:
            print("empty cube")
            print(self.hypercubes[coords].middle)
            clas = self.child_grid.classify(example, coords)
            print(clas)
            if clas[0] == -1:
                clas = self.nearest_neighbours_class(example, coords, clas[1])
            return clas


class LowerLevelGrid(Grid):
    def __init__(self, level, parent_bins_number, parent_hypercubes, dims):
        bins_number = int((parent_bins_number/(2**dims)))
        Grid.__init__(self, bins_number=bins_number,level=level, dims=dims)
        self.parent_hypercubes = parent_hypercubes
        self.set_hypercubes_parents_indices()
        self.compute_middles_of_hypercubes()

    def set_hypercubes_parents_indices(self):
        for hypercube in itertools.chain.from_iterable(self.hypercubes):
            coordinates = []
            print("--------------------------------")
            for coord in hypercube.coords:
                coordinates.append([2 * coord, 2 * coord + 1])
            print("!!!!!!!!!!!!!!!!!!!!")
            parents_list = []
            for indices in list(itertools.product(*coordinates)):
                # creating a list of parent hypercubes
                # parents_list.append(self.parent_hypercubes[tuple(reversed(indices))])
                #print(row, column)
                # current_class = self.parent_hypercubes[row][column].hypercube_class
                # classes[current_class] = classes.get(current_class, 0) + 1  # <3
            #     TU TRZEBA WSZYSTKIE EXAMPLE
                hypercube.parent_hypercubes_indices.append(tuple(indices))
            # hypercube.set_lower_level_hypercube_class(parents_list, self.threshold)
            print(hypercube.parent_hypercubes_indices)


    def set_hypercubes_classes(self):
        print("GRID LEVEL: " + str(self.level))
        for hypercube in itertools.chain.from_iterable(self.hypercubes):
            coordinates = []
            print("--------------------------------")
            for coord in hypercube.coords:
                coordinates.append([2 * coord, 2 * coord + 1])
            print("!!!!!!!!!!!!!!!!!!!!")
            parents_list = []
            for indices in list(itertools.product(*coordinates)):
                # creating a list of parent hypercubes
                parents_list.append(self.parent_hypercubes[tuple(reversed(indices))])
                #print(row, column)
                # current_class = self.parent_hypercubes[row][column].hypercube_class
                # classes[current_class] = classes.get(current_class, 0) + 1  # <3
            #     TU TRZEBA WSZYSTKIE EXAMPLE
            #     hypercube.parent_hypercubes_indices.append(tuple(indices))
            hypercube.set_lower_level_hypercube_class(parents_list, self.threshold)
            print(hypercube.parent_hypercubes_indices)
        print("--------------")
        if self.child_grid:
            self.child_grid.set_hypercubes_classes()

    def compute_middles_of_hypercubes(self):
        for hypercube in itertools.chain.from_iterable(self.hypercubes):
            sumx = 0
            sumy = 0
            rows = [2 * hypercube.coords[0], 2 * hypercube.coords[0] + 1]
            columns = [2 * hypercube.coords[1], 2 * hypercube.coords[1] + 1]
            sums = np.zeros((len(hypercube.coords)))
            print("xdddddd")
            print(hypercube.parent_hypercubes_indices)
            for coords in hypercube.parent_hypercubes_indices:
                for index, summ in enumerate(sums):
                    sums[index] += self.parent_hypercubes[coords].middle[index]
            hypercube.middle = [x/4 for x in sums]

    def classify(self, example, coords):
        coords = tuple([int(x/2) for x in coords])
        print(coords)
        if self.hypercubes[coords].hypercube_class == 'E':
            clas = self.child_grid.classify(example, coords)
            print("CLASSS")
            if clas[0] == -1:
                clas = self.nearest_neighbours_class(example, coords, clas[1])
            return clas
        elif self.hypercubes[coords].hypercube_class == 'M':
            return -1, self.hypercubes[coords].parent_hypercubes_indices # flag indicating that we need to compute distance
        else:
            print("heh")
            return self.hypercubes[coords].hypercube_class
