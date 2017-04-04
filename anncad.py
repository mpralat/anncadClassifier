from grid import BasicGrid


class AnncadClassifier:
    def __init__(self, threshold, batch_size):
        self.threshold = threshold
        self.batch_size = batch_size
        self.example_queue = []
        # TODO bins_number rename
        self.basic_grid = BasicGrid([0.0, 0.0], [100.0, 100.0], bins_number=8, threshold=self.threshold)

    def add_example(self, example):
        # TODO maybe we should consider wrapping the observation into an example inside anncad?
        # Add to basic grid first
        self.basic_grid.add_example_to_grid(example)

    def build_grids(self):
        self.basic_grid.set_hypercubes_classes()

    def classify(self, example):
        returned_class = self.basic_grid.classify(example=example)
        example.predicted_class_id = returned_class
        print(returned_class)

    def update(self, example):
        self.example_queue.append(example)
        self.batch_update()

    def batch_update(self):
        if len(self.example_queue) > self.batch_size:
            self.basic_grid.batch_update(self.example_queue)