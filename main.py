from anncad import AnncadClassifier
import csv
from generator import SampleGenerator
from grid import Grid, BasicGrid
from matplotlib import pyplot as plt
import numpy as np
from streamEngine import Stream
from utils import plot_dataset


if __name__ == "__main__":
    # Generating the samples
    sample_generator = SampleGenerator(0.0, 100.0, "dataset_seed.csv")
    sample_generator.create_dataset()
    # Plotting
    plot_dataset()
    # Streaming the generated observations
    stream = Stream("dataset1.csv")
    generator = stream.emit_observation
    # Creating an empty grid
    main_grid = BasicGrid([0.0, 0.0], [100.0, 100.0], bins_number=16)
    threshold = 0.67
    # Creating an instance of ANNCAD classifier
    anncad = AnncadClassifier(main_grid, threshold)
    while True:
        try:
            observation = next(generator)
            anncad.add_example(observation)
        except StopIteration:
            break
    print("xD")
    main_grid.set_hypercubes_classes()
