
from grid import Grid
from example import Example


class AnncadClassifier:
    def __init__(self,grid):
        # self.bins_number = bins_number
        # TODO pow 2
        self.grid = grid
        # self.create_grid()
    #
    # def create_grid(self):
    #     for i in range(self.bins_in_dim):
    #         for j in range(self.bins_in_dim):
    #             self.grid.append(Hypercube([i, j]))

    # def add_example_to_grid(self, observation):
    #     example = Example(observation)
    #     x = example.coords[0] / self.width
    #     y = example.coords[1] / self.height
    #     hypercube_index = int(y) * self.bins_in_dim + int(x)
    #     self.grid[hypercube_index].add_example(example)
    #     self.grid[hypercube_index].set_hypercube_class()
    #
    # def set_hypercubes_classes(self):
    #     for hypercube in self.grid:
    #         hypercube.set_hypercube_class()
    #         print(hypercube.coords, hypercube.hypercube_class)
