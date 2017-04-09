from utils import EMPTY_HYPERCUBE_INDICATOR, MIXED_HYPERCUBE_INDICATOR

class Hypercube():
    """
    A structure containing Examples. Number of its dimensions depends on how many attributes each Example has.
    
    :param coords: Coordinates of this particular Hypercube in Grid.
     
    """
    def __init__(self, coords):
        self.coords = coords
        self.examples = []
        self.hypercube_class = EMPTY_HYPERCUBE_INDICATOR
        self.class_dict = {}
        self.middle = [0.0] * len(coords)
        self.parent_hypercubes_indices = []

    def add_example(self, example):
        """
        Adds an Example to a Hypercube
        
        :param example: Element object to be added.
        """
        self.examples.append(example)

    def set_hypercube_class(self):
        """
        Sets the class of the Hypercube in the BasicGrid.
        If the Hypercube contains no examples, then the EMPTY_CLASS_INDICATOR is assigned as the class id.
        Otherwise the most frequent class is assigned.
        If they draw, assignment is random.
        
        """
        self.class_dict = dict.fromkeys(list(set([x.class_id for x in self.examples])), 0)
        old_class = self.hypercube_class
        print(old_class)
        if not self.examples:
            self.hypercube_class = EMPTY_HYPERCUBE_INDICATOR
        else:
            max_class = -1
            for class_id in self.class_dict.keys():
                class_size = len(list(filter(lambda x: x.class_id == class_id, self.examples)))
                # adding the number of examples to the class
                self.class_dict[class_id] += class_size
                if class_size > max_class:
                    max_class = class_size
                    self.hypercube_class = class_id
        if not old_class == self.hypercube_class:
            print("Changed hypercube's class!\tCoords: " + str(
                self.coords) + "\tOld class: " + old_class + "\tNew class: " + self.hypercube_class)

    def set_lower_level_hypercube_class(self, parent_hypercubes, threshold):
        '''
        Sets the class of the Hypercube in LowerLevelGrid.
        
        :param parent_hypercubes: list of Hypercubes from finer level, which create current Hypercube.
        :param threshold: algorithm's parameter - if the difference between the cardinalities of the two most frequent classes does not exceed the threshold value, then the MIXED_CLASS_INDICATOR is assigned. 
        '''
        parent_class_dicts = [parent.class_dict for parent in parent_hypercubes]
        # Now the hypercube will get the counters of all classes
        for dicti in parent_class_dicts:
            for parent_class in dicti.keys():
                # add the parent class counter if the key already exists, default zero
                self.class_dict[parent_class] = self.class_dict.get(parent_class, 0) + dicti[parent_class]
        #  Here we've got a dict class:class_counter. to get the class name we have to get the biggest value
        sorted_classes = sorted(self.class_dict.items(), key=lambda x: x[1], reverse=True)
        if len(sorted_classes) == 0:
            self.hypercube_class = EMPTY_HYPERCUBE_INDICATOR
        elif len(sorted_classes) == 1:
            self.hypercube_class = sorted_classes[0][0]
        else:
            if sorted_classes[0][1] - sorted_classes[1][1] > threshold * (sorted_classes[0][1] + sorted_classes[1][1]):
                self.hypercube_class = sorted_classes[0][0]
            else:
                self.hypercube_class = MIXED_HYPERCUBE_INDICATOR

        print("Hypercube's coordinates: " + str(self.coords) +  " Class: "
              + str(self.hypercube_class))

    def update_basic(self, example_list):
        """
        Updates the Hypercube's class after new Examples arrive.
        
        :param example_list: A list consisting of Examples of the same class within the same Hypercube.
        :return: Hypercube's current class.
        """
        # example list consists of examples of the same class
        for example in example_list:
            self.add_example(example)
        main_class = example_list[0].class_id
        if self.hypercube_class == EMPTY_HYPERCUBE_INDICATOR:
            self.hypercube_class = main_class
            self.class_dict[main_class] = len(example_list)
        elif not self.hypercube_class == main_class:
            self.class_dict[main_class] = self.class_dict.get(main_class, 0) + len(example_list)
            if self.class_dict[self.hypercube_class] < self.class_dict[main_class]:
                self.hypercube_class = main_class
        return self.hypercube_class

    def update_lower_level(self, example_class, example_count, threshold):
        """
        Updates the Hypercube's class after new Examples arrive. This method is applicable to Hypercubes of the coarser Grids.
        
        
        :param example_class: Class of provided examples.
        :param example_count: Number of Examples of given class within the Hypercubes of the finer Grid that build the current Hypercube.
        :param threshold: algorithm's parameter - if the difference between the cardinalities of the two most frequent classes does not exceed the threshold value, then the MIXED_CLASS_INDICATOR is assigned. 
        :return: Hypercube's current class.
        """
        if self.hypercube_class == EMPTY_HYPERCUBE_INDICATOR:
            self.hypercube_class = example_class
            self.class_dict[example_class] = example_count
        elif not self.hypercube_class == example_class:
            self.class_dict[example_class] = self.class_dict.get(example_class, 0) + example_count
            sorted_classes = sorted(self.class_dict.items(), key=lambda x: x[1], reverse=True)
            if sorted_classes[0][1] - sorted_classes[1][1] > threshold * (
                        sorted_classes[0][1] + sorted_classes[1][1]):
                self.hypercube_class = sorted_classes[0][1]
            else:
                self.hypercube_class = MIXED_HYPERCUBE_INDICATOR
        return self.hypercube_class
