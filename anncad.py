from grid import BasicGrid

class AnncadClassifier:
    def __init__(self, threshold):
        # self.bins_number = bins_number
        self.threshold = threshold
        self.basic_grid = BasicGrid([0.0, 0.0], [100.0, 100.0], bins_number=14, threshold=self.threshold)


    def add_example(self, example):
        # Add to basic grid first
        # self.grids[self.basic_grid.level].add_example_to_grid(example)
        self.basic_grid.add_example_to_grid(example)

    def build_grids(self):
        self.basic_grid.set_hypercubes_classes()

# main_grid.set_hypercubes_classes()