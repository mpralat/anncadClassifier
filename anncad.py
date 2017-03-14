
from grid import Grid
from example import Example


class AnncadClassifier:
    def __init__(self, grid):
        # self.bins_number = bins_number
        # TODO pow 2
        self.grids = {}
        self.basic_grid = grid
        self.grids[self.basic_grid.level] = self.basic_grid



    def add_example(self, example):
        # Add to basic grid first
        self.grids[self.basic_grid.level].add_example_to_grid(example)



