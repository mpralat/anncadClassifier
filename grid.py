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
            self.bins_number = 2**(math.ceil(bins_number_log))
        self.dims = dims
        self.bins_in_dim = int(np.power(self.bins_number, 1/self.dims))
        print(self.bins_in_dim, self.dims)
        if level is None:
            self.level = int(np.log2(self.bins_in_dim) + 1)
        else:
            self.level = level
        print("New Grid! " + str(self.level))

        shape = tuple([self.bins_in_dim] * self.dims)
        self.hypercubes = np.ones(shape).astype(Hypercube)

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

    def nearest_neighbours_class(self, example, parents_indices):
        print("nearest neighbours class")
        parents_data = [(self.hypercubes[parent].middle, self.hypercubes[parent].hypercube_class) for parent in parents_indices]
        distances = sorted([(distance.euclidean(example.coords, parent[0]), parent[1]) for parent in parents_data if not parent[1]=='E'])
        print(distances)
        return distances[0][1]

    @abc.abstractmethod
    def update(self, example, coords):
        return

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

    def set_hypercubes_classes(self):
        print("BASEGRID hypercubes")
        list_of_all_hc = list(self.hypercubes.flatten())
        print(" I have " + str(len(list_of_all_hc)) + " hypercubes :3")
        for hypercube in list_of_all_hc:
            hypercube.set_hypercube_class()
        if self.child_grid:
            self.child_grid.set_hypercubes_classes()

    def compute_middles_of_hypercubes(self):
        for hc in self.hypercubes.flatten():
            for i in range(self.dims - 1, -1, -1):
                index = self.dims - (i + 1)
                hc.middle[i] = (hc.coords[index] + 0.5) * self.hypercube_measurements[index]

    def classify(self, example):
        coords = tuple([int(example.coords[i] / self.hypercube_measurements[i]) for i in range(self.dims-1, -1, -1)])
        print("----------")
        if self.hypercubes[coords].hypercube_class is not 'E':
            return self.hypercubes[coords].hypercube_class
        else:
            print("empty cube")
            print(self.hypercubes[coords].middle)
            returned_class = self.child_grid.classify(example, coords)
            print(returned_class)
            if returned_class[0] == -1:
                returned_class = self.nearest_neighbours_class(example, returned_class[1])
            return returned_class

    def update(self, example, coords=None):
        coords = tuple([int(example.coords[i] / self.hypercube_measurements[i]) for i in range(self.dims - 1, -1, -1)])
        new_class = self.hypercubes[coords].update_basic([example])
        print("Changed class of " + str(coords) + " to: " + str(new_class))
        if self.child_grid:
         self.child_grid.update(example, coords)

    def batch_update(self, examples):
        dicti = {}
        for example in examples:
            coords = tuple(
                [int(example.coords[i] / self.hypercube_measurements[i]) for i in range(self.dims - 1, -1, -1)])
            dicti[(example.class_id, coords)] = dicti.get((example.class_id, coords), [])
            dicti[(example.class_id, coords)].append(example)
        for (class_id, coords), example_list in dicti.items():
            print(class_id, coords, example_list)
            print("---------------")
            self.hypercubes[coords].update_basic(example_list)
            print("Koniec")
        if self.child_grid:
            self.child_grid.batch_update(dicti)


class LowerLevelGrid(Grid):
    def __init__(self, level, parent_bins_number, parent_hypercubes, dims):
        bins_number = int((parent_bins_number/(2**dims)))
        Grid.__init__(self, bins_number=bins_number,level=level, dims=dims)
        self.parent_hypercubes = parent_hypercubes
        self.set_hypercubes_parents_indices()
        self.compute_middles_of_hypercubes()

    def set_hypercubes_parents_indices(self):
        for hypercube in self.hypercubes.flatten():
            coordinates = []
            for coord in hypercube.coords:
                coordinates.append([2 * coord, 2 * coord + 1])
            for indices in list(itertools.product(*coordinates)):
                hypercube.parent_hypercubes_indices.append(tuple(indices))

    def set_hypercubes_classes(self):
        print("GRID LEVEL: " + str(self.level))
        for hypercube in self.hypercubes.flatten():
            coordinates = []
            for coord in hypercube.coords:
                coordinates.append([2 * coord, 2 * coord + 1])
            parents_list = []
            for indices in list(itertools.product(*coordinates)):
                parents_list.append(self.parent_hypercubes[tuple(reversed(indices))])
            hypercube.set_lower_level_hypercube_class(parents_list, self.threshold)
        print("--------------")
        if self.child_grid:
            self.child_grid.set_hypercubes_classes()

    def compute_middles_of_hypercubes(self):
        for hypercube in self.hypercubes.flatten():
            sums = np.zeros((len(hypercube.coords)))
            for coords in hypercube.parent_hypercubes_indices:
                for index, summ in enumerate(sums):
                    sums[index] += self.parent_hypercubes[coords].middle[index]
            hypercube.middle = [x/4 for x in sums]

    def classify(self, example, coords):
        coords = tuple([int(x/2) for x in coords])
        print(coords)
        if self.hypercubes[coords].hypercube_class == 'E':
            returned_class = self.child_grid.classify(example, coords)
            if returned_class[0] == -1:
                returned_class = self.nearest_neighbours_class(example, returned_class[1])
            return returned_class
        elif self.hypercubes[coords].hypercube_class == 'M':
            return -1, self.hypercubes[coords].parent_hypercubes_indices # flag indicating that we need to compute distance
        else:
            return self.hypercubes[coords].hypercube_class

    def update(self, example, coords):
        coords = tuple([int(x / 2) for x in coords])
        new_class = self.hypercubes[coords].update_lower_level(example.class_id, 1, self.threshold)
        print("Changed class of " + str(coords) + " to: " + str(new_class))
        if self.child_grid:
            self.child_grid.update(example, coords)

    def batch_update(self, dicti):
        for (class_id, coords), examples in dicti.items():
            coords = tuple([int(x / 2) for x in coords])
            self.hypercubes[coords].update_lower_level(class_id, len(examples), self.threshold)
        if self.child_grid:
            self.child_grid.batch_update(dicti)
