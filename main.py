from generator import SampleGenerator
import csv
from streamEngine import Stream
from grid import Grid, BasicGrid
from anncad import AnncadClassifier
from matplotlib import pyplot as plt
import numpy as np

if __name__ == "__main__":
    # Generating the samples
    sample_generator = SampleGenerator(0.0, 100.0, "dataset_seed.csv")
    sample_generator.create_dataset()
    # Plotting
    b_x = []
    b_y = []
    r_x = []
    r_y = []
    with open("dataset1.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                b_x.append(float(row[0])) if row[-1] == 'B' else r_x.append(float(row[0]))
                b_y.append(float(row[1])) if row[-1] == 'B' else r_y.append(float(row[1]))
    plt.scatter(r_x, r_y, color="red", marker="v")
    plt.scatter(b_x, b_y, color="blue", marker="o")
    axes = plt.gca()
    axes.set_xlim([0, 100])
    axes.set_ylim([0, 100])
    axes.set_xticks(np.arange(0, 100, 25))
    axes.set_yticks(np.arange(0, 100, 25))
    plt.grid()
    plt.savefig("plot.png")
    # Streaming the generated observations
    stream = Stream("dataset1.csv")
    generator = stream.emit_observation
    # Classifying
    main_grid = BasicGrid([0.0, 0.0], [100.0, 100.0], 16)
    anncad = AnncadClassifier(main_grid)
    while True:
        try:
            observation = next(generator)
            anncad.grids[main_grid.level].add_example_to_grid(observation)
        except StopIteration:
            break
    print("xD")
    # anncad.set_hypercubes_classes()
