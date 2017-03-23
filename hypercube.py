import operator
class Hypercube:
    def __init__(self, coords):
        self.coords = coords
        self.examples = []
        self.hypercube_class = 'E'
        self.class_dict = {}

    def add_example(self, example):
        self.examples.append(example)

    def set_hypercube_class(self):
        # Setting up the dictionary - class : 0 for starters
        self.class_dict = dict.fromkeys(list(set([x.class_id for x in self.examples])), 0)
        old_class = self.hypercube_class
        max_class = -1
        if not self.examples:
            self.hypercube_class = 'E'
        else:
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
        # print("Hello hypercube! Coords: " + str(self.coords) + "\t Class dict: " + str(self.class_dict))

    def set_lower_level_hypercube_class(self, parent_hypercubes, threshold):
        parent_class_dicts = [parent.class_dict for parent in parent_hypercubes]
        # Now the hypercube will get the counters of all classes
        print("parents")
        for dict in parent_class_dicts:
            for parent_class in dict.keys():
                # add the parent class counter if the key already exists, default zero
                self.class_dict[parent_class] = self.class_dict.get(parent_class, 0) + dict[parent_class]


        #  Here we've got a dict class:class_counter. to get the class name we have to get the biggest value
        sorted_classes = sorted(self.class_dict.items(), key=lambda x: x[1], reverse=True)
        print(sorted_classes)

        print( sorted_classes[0][1] - sorted_classes[1][1])
        if sorted_classes[0][1] - sorted_classes[1][1] > threshold * (sorted_classes[0][1] + sorted_classes[1][1]):
            self.hypercube_class = sorted_classes[0][0]
        else:
            self.hypercube_class = 'M'
        print("HYPERCUBE! my coords: " + str(self.coords) + " my counters; " + str(self.class_dict) + " and my class: "
              + str(self.hypercube_class))
