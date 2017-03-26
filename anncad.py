from grid import BasicGrid


class AnncadClassifier:
    def __init__(self, threshold):
        self.threshold = threshold
        self.basic_grid = BasicGrid([0.0, 0.0], [100.0, 100.0], bins_number=14, threshold=self.threshold)

    def add_example(self, example):
        # Add to basic grid first
        self.basic_grid.add_example_to_grid(example)

    def build_grids(self):
        self.basic_grid.set_hypercubes_classes()

    def classify(self, example):
        returned_class = self.basic_grid.classify(example=example)
        example.predicted_class_id = returned_class
        print(returned_class)
