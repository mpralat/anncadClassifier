from example import Example
from grid import BasicGrid
from utils import is_array_numeric

class AnncadClassifier:
    """
    Class providing methods for user to create and use the classifier.
    
    :param threshold:  When difference between cardinalities of two most frequent classes divided by sum of them is greater than threshold, we assign most frequent class.
    :param batch_size: Minimum number of Examples that triggers Update method.
    :param attributes_boundaries: A list of tuples, each consisting of min and max values of the attribute. 
    :param hypercubes_number: Number of hypercubes in the BasicGrid. Default value: 2^(number of Example's attributes).
    :type hypercubes_number: integer or None
    :raises ValueError: When threshold, batch_size or hypercubes_number are not convertible to numeric types.
    """
    def __init__(self, threshold, batch_size, attributes_boundaries, hypercubes_number=None):
        try:
            self.threshold = float(threshold)
            self.batch_size = int(batch_size)
        except:
            raise ValueError("Threshold and batch_size parameters have to be numeric")
        self.example_queue = []
        self.attributes_boundaries = attributes_boundaries
        if hypercubes_number is None:
            self.hypercubes_number = 2 ** (len(self.attributes_boundaries))
        else:
            try:
                self.hypercubes_number = int(hypercubes_number)
            except:
                raise ValueError("Hypercubes_number has to be numeric")
        self.basic_grid = BasicGrid(self.attributes_boundaries, hypercubes_number=self.hypercubes_number, threshold=self.threshold)

    def add_examples(self, list_of_examples):
        """
        Adds all of the provided Examples to BasicGrid.
        
        :param list_of_examples: A list of Examples.
        """
        # Add to basic grid first
        for example_as_a_list in list_of_examples:
            if self.check_if_proper_example_coordinates(example_as_a_list[:-1]):
                self.basic_grid.add_example_to_grid(Example(example_as_a_list))

    def set_hypercubes_classes(self):
        """
        Sets all of the BasicGrid's Hypercubes classes. 
        """
        self.basic_grid.set_hypercubes_classes()

    def test(self, example):
        """
        Given a list of coordinates and a class id at the last index, creates an Example object and classifies it.
        
        :param example: A list of coordinates and a class id at the last index.
        :return: Class id.
        """
        if not is_array_numeric(example[:-1]):
            print("Observation coordinates have to be numeric")
            return None
        example = Example(example)
        return self.classify(example.coords)

    def classify(self, example_coords):
        """
        Given a list of coordinates, classifies the observation.
        
        :param example_coords: Coordinates of the observation.
        :return: Class id.
        """
        if not is_array_numeric(example_coords):
            print("Observation coordinates have to be numeric")
            return None
        return self.basic_grid.test(example_coords)

    def update(self, list_of_examples):
        """
        Adds the Examples to the example_queue.
        
        :param list_of_examples: A list of new Examples.
        """
        for example_as_a_list in list_of_examples:
            if self.check_if_proper_example_coordinates(example_as_a_list[:-1]):
                self.example_queue.append(Example(example_as_a_list))
        self.batch_update()

    def batch_update(self):
        """
        Checks if the number of Examples in the example_queue is sufficient and updates the grids.
        """
        if len(self.example_queue) > self.batch_size:
            self.basic_grid.batch_update(self.example_queue)

    def check_if_proper_example_coordinates(self, coordinates):
        """
        Checks if the list of coordinates contains only numeric values, has adequate length and if all of the provided values are within the attributes boundaries. 
        
        :param coordinates: A list of coordinates.
        :return: True if the list meets all of the conditions, otherwise False.
        """
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
