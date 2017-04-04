import utils

class Hypercube(object):
    def __init__(self, coords):
        if (not utils.is_array_numeric(coords)) or len(coords) < 1:
            raise ValueError("Coordinates should be a numerical array with at least one element.")
        self.coords = coords
        self.examples = []
        self.hypercube_class = 'E'
        self.class_dict = {}
        # TODO MIDDLE
        self.middle = [0.0] * len(coords)
        self.parent_hypercubes_indices = []

#TODO test case?
    def add_example(self, example):
        self.examples.append(example)

    def set_hypercube_class(self):
        # Setting up the dictionary - class : 0 for starters
        self.class_dict = dict.fromkeys(list(set([x.class_id for x in self.examples])), 0)
        old_class = self.hypercube_class
        print(old_class)
        if not self.examples:
            self.hypercube_class = 'E'
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
        parent_class_dicts = [parent.class_dict for parent in parent_hypercubes]
        # Now the hypercube will get the counters of all classes
        for dicti in parent_class_dicts:
            for parent_class in dicti.keys():
                # add the parent class counter if the key already exists, default zero
                self.class_dict[parent_class] = self.class_dict.get(parent_class, 0) + dicti[parent_class]
        #  Here we've got a dict class:class_counter. to get the class name we have to get the biggest value
        sorted_classes = sorted(self.class_dict.items(), key=lambda x: x[1], reverse=True)
        if len(sorted_classes) == 0:
            self.hypercube_class = 'E'
        elif len(sorted_classes) == 1:
            self.hypercube_class = sorted_classes[0][0]
        else:
            if sorted_classes[0][1] - sorted_classes[1][1] > threshold * (sorted_classes[0][1] + sorted_classes[1][1]):
                self.hypercube_class = sorted_classes[0][0]
            else:
                self.hypercube_class = 'M'

        print("HYPERCUBE! my coords: " + str(self.coords) + " my counters; " + str(self.class_dict) + " and my class: "
              + str(self.hypercube_class))

    def update_basic(self, example_list):
        # example list consists of examples of the same class
        for example in example_list:
            self.add_example(example)
        main_class = example_list[0].class_id
        if self.hypercube_class == 'E':
            self.hypercube_class = main_class
            self.class_dict[main_class] = len(example_list)
        elif not self.hypercube_class == main_class:
            self.class_dict[main_class] = self.class_dict.get(main_class, 0) + len(example_list)
            if self.class_dict[self.hypercube_class] < self.class_dict[main_class]:
                self.hypercube_class = main_class
        return self.hypercube_class

    def update_lower_level(self, example_class, example_count, threshold):
        if self.hypercube_class == 'E':
            self.hypercube_class = example_class
            self.class_dict[example_class] = example_count
        elif not self.hypercube_class == example_class:
            self.class_dict[example_class] = self.class_dict.get(example_class, 0) + example_count
            sorted_classes = sorted(self.class_dict.items(), key=lambda x: x[1], reverse=True)
            if sorted_classes[0][1] - sorted_classes[1][1] > threshold * (
                        sorted_classes[0][1] + sorted_classes[1][1]):
                self.hypercube_class = sorted_classes[0][1]
            else:
                self.hypercube_class = 'M'
        return self.hypercube_class
