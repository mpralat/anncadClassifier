class Hypercube:
    def __init__(self, coords):
        self.coords = coords
        self.examples = []
        self.hypercube_class = 'E'
        self.list_of_classes = []

    def add_example(self, example):
        self.examples.append(example)

    def set_hypercube_class(self):
        self.list_of_classes = list(set([x.class_id for x in self.examples]))
        old_class = self.hypercube_class
        max_class = -1
        if not self.examples:
            self.hypercube_class = 'E'
        else:
            for class_id in self.list_of_classes:
                class_size = len(list(filter(lambda x: x.class_id == class_id, self.examples)))
                if class_size > max_class:
                    max_class = class_size
                    self.hypercube_class = class_id
        if not old_class == self.hypercube_class:
            print("Changed hypercube's class!\tCoords: " + str(
                self.coords) + "\tOld class: " + old_class + "\tNew class: " + self.hypercube_class)

    def get_hypercube_examples(self):
        pass
