from hypercube import Hypercube
import numpy as np
import abc
import itertools
import math
from scipy.spatial import distance


class Grid:
    __metaclass__ = abc.ABCMeta
    _threshold = 0.6

    @property
    def threshold(self):
        """
        When difference between cardinalities of two most frequent classes divided by sum of them is greater than
        threshold, we assign the most frequent class.

        :setter: Sets the threshold for the grid
        :type: float
        """
        return self._threshold

    @threshold.setter
    def threshold(self, val):
        self._threshold = val

    def __init__(self, hypercubes_number, dims, level=None):
        hypercubes_number_log = float(np.log2(hypercubes_number))
        if hypercubes_number_log.is_integer():
            self.hypercubes_number = hypercubes_number
        else:
            self.hypercubes_number = 2 ** (math.ceil(hypercubes_number_log))
        self.dims = dims
        self.hypercubes_in_dim = int(np.power(self.hypercubes_number, 1 / self.dims))
        print(self.hypercubes_in_dim, self.dims)
        if level is None:
            self.level = int(np.log2(self.hypercubes_in_dim) + 1)
        else:
            self.level = level
        print("New Grid! " + str(self.level))

        shape = tuple([self.hypercubes_in_dim] * self.dims)
        self.hypercubes = np.ones(shape).astype(Hypercube)

        self.create_grids_structure()
        self.child_grid = self.create_lower_level_grid()

    def create_grids_structure(self):
        """
        Creates Hypercube objects for every index in the multidimensional list self.hypercubes.

        """
        for indices, hypercube in np.ndenumerate(self.hypercubes):
            self.hypercubes[indices] = Hypercube(indices)

    def create_lower_level_grid(self):
        """
        Creates LowerLevelGrid when it is possible - level equal to one means that this is the coarsest level.

        """
        if self.level == 1:
            return False
        else:
            return LowerLevelGrid(self.level - 1, self.hypercubes_number, self.hypercubes, self.dims)

    def nearest_neighbours_class(self, example_coords, parents_indices):
        """
        Creates Hypercube objects for every index in the multidimensional list self.hypercubes.

        :param example_coords: Coordinates of the observation to be classified using distances between him and parents Hypercubes, which are contained in current, coarser level Hypercube.
        :param parents_indices: Indices of 2**dims Hypercubes, contained in current grids Hypercube.

        :return class of the nearest, not empty Hypercube
        """
        print("nearest neighbours class")
        parents_data = [(self.hypercubes[parent].middle, self.hypercubes[parent].hypercube_class) for parent in parents_indices]
        distances = sorted([(distance.euclidean(example_coords, parent[0]), parent[1]) for parent in parents_data if not parent[1] == 'E'])
        print(distances)
        return distances[0][1]

    @abc.abstractmethod
    def update(self, example, hypercubes_coords):
        return

    @abc.abstractmethod
    def set_hypercubes_classes(self):
        return


class BasicGrid(Grid):
    """
    A representation of attributes space, to be divided into hypercubes. It applies only to the finest level.

    :param list_of_attributes_ranges: A list of ranges of attributes
    :example: list_of_attributes_ranges = [[0.0, 100.0], [5.9, 2030.0], [150.0, 220.0]] - It has three attributes (three dimensions).
    :param hypercubes_number: Number of Hypercubes in the finest level.
    :param threshold: When difference between cardinalities of two most frequent classes divided by sum of them is greater than threshold, we assign the most frequent class.
    """
    def __init__(self, list_of_attributes_ranges, hypercubes_number, threshold):
        self.min_attribute_range_list = [x[0] for x in list_of_attributes_ranges]
        self.max_attribute_range_list = [x[1] for x in list_of_attributes_ranges]
        self.dims = len(self.min_attribute_range_list)
        Grid.__init__(self, hypercubes_number=hypercubes_number, dims=self.dims)
        Grid.threshold = threshold
        # TODO better name
        self.hypercube_measurements = [(self.max_attribute_range_list[x] - self.min_attribute_range_list[x]) / self.hypercubes_in_dim for x in range(len(self.min_attribute_range_list))]
        self.set_hypercubes_classes()
        self.compute_middles_of_hypercubes()

    def add_example_to_grid(self, example):
        """
        Adds provided Example to correct Hypercube in BasicGrid

        :param example: Example to be added to the grid.
        """
        # TODO self-dimensions
        indices = tuple([int(example.coords[x] / self.hypercube_measurements[x]) for x in range(self.dims-1, -1, -1)])
        self.hypercubes[indices].add_example(example)

    def set_hypercubes_classes(self):
        """
        Sets classes for all hypercubes in self and in his child (LowerLevelGrid).

        """
        print("BASEGRID hypercubes")
        list_of_all_hc = list(self.hypercubes.flatten())
        print(" I have " + str(len(list_of_all_hc)) + " hypercubes :3")
        for hypercube in list_of_all_hc:
            hypercube.set_hypercube_class()
        if self.child_grid:
            self.child_grid.set_hypercubes_classes()

    def compute_middles_of_hypercubes(self):
        """
        Computes every hypercube's middle by taking values in the middle between beginning and end of hypercube in
        every dimension.

        """
        for hc in self.hypercubes.flatten():
            for i in range(self.dims - 1, -1, -1):
                index = self.dims - (i + 1)
                hc.middle[i] = (hc.coords[index] + 0.5) * self.hypercube_measurements[index]

    def test(self, example_coords):
        """
        Predicts the class for example with given coordinates.

        :param example_coords: A list of coordinates of an observation.
        :return: returned_class: Class predicted by the classifier.
        """
        hypercubes_coords = tuple([int(example_coords[i] / self.hypercube_measurements[i]) for i in range(self.dims - 1, -1, -1)])
        print("----------")
        if self.hypercubes[hypercubes_coords].hypercube_class is not 'E':
            return self.hypercubes[hypercubes_coords].hypercube_class
        else:
            print("empty cube")
            print(self.hypercubes[hypercubes_coords].middle)
            returned_class = self.child_grid.classify(example_coords, hypercubes_coords)
            print(returned_class)
            if returned_class[0] == -1:
                returned_class = self.nearest_neighbours_class(example_coords, returned_class[1])
            return returned_class

    def update(self, example, hypercubes_coords=None):
        """
        Updates the grid with given Example. If grid has a child, he forces him to update humself with the observation.

        :param example: Example object to be used to update BasicGrid.
        :param hypercubes_coords: Not used in BasicGrid, must be because of Abstract Method in Grid.
        """
        hypercubes_coords = tuple([int(example.coords[i] / self.hypercube_measurements[i]) for i in range(self.dims - 1, -1, -1)])
        new_class = self.hypercubes[hypercubes_coords].update_basic([example])
        print("Changed class of " + str(hypercubes_coords) + " to: " + str(new_class))
        if self.child_grid:
            self.child_grid.update(example, hypercubes_coords)

    def batch_update(self, examples):
        """
        Updates the grid, given batch_size of Examples. It groups Examples into by class_id and by Hypercubes
        containing these Examples. If Grid has a child, he also forces him to update itself.

        :param examples: A list of Examples to be used to update the BasicGrid.
        """
        dicti = {}
        for example in examples:
            hypercubes_coords = tuple(
                [int(example.coords[i] / self.hypercube_measurements[i]) for i in range(self.dims - 1, -1, -1)])
            dicti[(example.class_id, hypercubes_coords)] = dicti.get((example.class_id, hypercubes_coords), [])
            dicti[(example.class_id, hypercubes_coords)].append(example)
        for (class_id, hypercubes_coords), example_list in dicti.items():
            print(class_id, hypercubes_coords, example_list)
            print("---------------")
            self.hypercubes[hypercubes_coords].update_basic(example_list)
            print("Koniec")
        if self.child_grid:
            self.child_grid.batch_update(dicti)


class LowerLevelGrid(Grid):
    """
    A representation of attributes space, to be divided into hypercubes. It applies to coarser levels that the first.

    :param level: Number from BasicGrid.level to 1, the lower, the coarser. The higher, the finer the grid is.
    :param parent_hypercubes_number: Number of parent's hypercubes.
    :param parent_hypercubes: Hypercubes from finer level grid.
    :param dims: Number of attributes (of dimensions).
    """
    def __init__(self, level, parent_hypercubes_number, parent_hypercubes, dims):
        bins_number = int((parent_hypercubes_number / (2 ** dims)))
        Grid.__init__(self, hypercubes_number=bins_number, level=level, dims=dims)
        self.parent_hypercubes = parent_hypercubes
        self.set_hypercubes_parents_indices()
        self.compute_middles_of_hypercubes()

    def set_hypercubes_parents_indices(self):
        """
        Computes coordinates of 2**dims parent's Hypercubes for every Hypercube in the grid.
        Each coarser Hypercube consists of 2**dims finer level Hypercubes.

        """
        for hypercube in self.hypercubes.flatten():
            coordinates = []
            for coord in hypercube.coords:
                coordinates.append([2 * coord, 2 * coord + 1])
            for indices in list(itertools.product(*coordinates)):
                hypercube.parent_hypercubes_indices.append(tuple(indices))

    def set_hypercubes_classes(self):
        """
        Sets classes for all hypercubes in self and in his child (another LowerLevelGrid) if he exists.

        """
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
        """
        Computes every hypercube's middle by taking values in the middle between beginning and end of hypercube in
        every dimension.

        """
        for hypercube in self.hypercubes.flatten():
            sums = np.zeros((len(hypercube.coords)))
            for coords in hypercube.parent_hypercubes_indices:
                for index, summ in enumerate(sums):
                    sums[index] += self.parent_hypercubes[coords].middle[index]
            hypercube.middle = [x/4 for x in sums]

    def classify(self, example_coords, hypercubes_coords):
        """
        Classifies observation with given coordinates.

        :param example_coords: Coordinates of observation to be classified.
        :param hypercubes_coords: Coordinates of Hypercube, which contained the observation on finer level.

        :return nothin
        """
        hypercubes_coords = tuple([int(x / 2) for x in hypercubes_coords])
        print(hypercubes_coords)
        if self.hypercubes[hypercubes_coords].hypercube_class == 'E':
            returned_class = self.child_grid.classify(example_coords, hypercubes_coords)
            if returned_class[0] == -1:
                returned_class = self.nearest_neighbours_class(example_coords, returned_class[1])
            return returned_class
        elif self.hypercubes[hypercubes_coords].hypercube_class == 'M':
            return -1, self.hypercubes[hypercubes_coords].parent_hypercubes_indices
            # -1 is a flag indicating that we need to compute distances
        else:
            return self.hypercubes[hypercubes_coords].hypercube_class

    def update(self, example, hypercubes_coords):
        """
        Updates the grid with given Example and then forces child_grid (if he exists) to update himself with this Example.

        :param example: Example object to be used to update BasicGrid.
        :param hypercubes_coords: Coordinates of Hypercube, which contained the Example on finer level.
        """
        hypercubes_coords = tuple([int(x / 2) for x in hypercubes_coords])
        new_class = self.hypercubes[hypercubes_coords].update_lower_level(example.class_id, 1, self.threshold)
        print("Changed class of " + str(hypercubes_coords) + " to: " + str(new_class))
        if self.child_grid:
            self.child_grid.update(example, hypercubes_coords)

    def batch_update(self, dicti):
        """
        Updates the grid, given dictionary with key (class_id, hypercube_coords) and value as list of Example objects.
        If Grid has a child, he also forces him to update itself.

        :param dicti: A list of Examples to be used to update the BasicGrid.
        """
        for (class_id, coords), examples in dicti.items():
            coords = tuple([int(x / 2) for x in coords])
            self.hypercubes[coords].update_lower_level(class_id, len(examples), self.threshold)
        if self.child_grid:
            self.child_grid.batch_update(dicti)
