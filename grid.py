from hypercube import Hypercube
import numpy as np


class Grid:
    def __init__(self, bins_number):
        self.hypercubes = []
        self.bins_number = bins_number
        self.create_grid()

    def create_grid(self):
        for i in range(np.sqrt(self.bins_number)):
            for j in range(np.sqrt(self.bins_number)):
                self.hypercubes.append(Hypercube([i, j]))
