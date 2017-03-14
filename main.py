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
    # Classifying
    main_grid = BasicGrid([0.0, 0.0], [100.0, 100.0], 16)
    anncad = AnncadClassifier(main_grid)
    while True:
        try:
            observation = next(generator)
            anncad.add_example(observation)
        except StopIteration:
            break
    print("xD")
    # anncad.set_hypercubes_classes()
