

class Hypercube:
    def __init__(self, coords):
        self.coords = coords
        self.examples = []
        self.hypercube_class = None

    def add_example(self, example):
        self.examples.append(example)

    def set_hypercube_class(self):
        class_B = list(filter(lambda x: x.class_id == 'B', self.examples))
        print(len(class_B))
