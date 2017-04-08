from example import Example
from grid import BasicGrid


class AnncadClassifier:
    def __init__(self, threshold, batch_size, attributes_boundaries, hypercubes_number=None):
        self.threshold = threshold
        self.batch_size = batch_size
        self.example_queue = []
        self.attributes_boundaries = attributes_boundaries
        if hypercubes_number is None:
            self.hypercubes_number = 2 ** (len(self.attributes_boundaries))
        else:
            self.hypercubes_number = hypercubes_number
        self.basic_grid = BasicGrid(self.attributes_boundaries, hypercubes_number=self.hypercubes_number, threshold=self.threshold)

    def add_examples(self, list_of_examples):
        # Add to basic grid first
        for example_as_a_list in list_of_examples:
            if self.check_if_proper_example_coordinates(example_as_a_list[:-1]):
                self.basic_grid.add_example_to_grid(Example(example_as_a_list))

    def set_hypercubes_classes(self):
        self.basic_grid.set_hypercubes_classes()

    def test(self, example):
        example = Example(example)
        return self.classify(example.coords)

    def classify(self, example_coords):
        return self.basic_grid.test(example_coords)

    def update(self, list_of_examples):
        for example_as_a_list in list_of_examples:
            if self.check_if_proper_example_coordinates(example_as_a_list[:-1]):
                self.example_queue.append(Example(example_as_a_list))
        self.batch_update()

    def batch_update(self):
        if len(self.example_queue) > self.batch_size:
            self.basic_grid.batch_update(self.example_queue)

    def check_if_proper_example_coordinates(self, coordinates):
        try:
            coordinates = [float(x) for x in coordinates]
        except:
            print("One or more coordinates are inconvertible to float")
            return False
        if not (len(coordinates) == len(self.attributes_boundaries)):
            print("Incorrect number of example's coordinates")
            return False
        for idx, boundary in enumerate(self.attributes_boundaries):
            if not (boundary[0] <= coordinates[idx] <= boundary[1]):
                print("Example's " + str(idx) + " coordinate is beyond attribute's boundaries")
                return False
        return True
