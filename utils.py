import csv
from matplotlib import pyplot as plt
import numpy as np


def plot_dataset():
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    with open("dataset1.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                x1.append(float(row[0])) if row[-1] == 'B' else x2.append(float(row[0]))
                y1.append(float(row[1])) if row[-1] == 'B' else y2.append(float(row[1]))
    plt.scatter(x1, y1, color="red", marker="v")
    plt.scatter(x2, y2, color="blue", marker="o")
    axes = plt.gca()
    axes.set_xlim([0, 100])
    axes.set_ylim([0, 100])
    axes.set_xticks(np.arange(0, 100, 25))
    axes.set_yticks(np.arange(0, 100, 25))
    plt.grid()
    plt.savefig("plot.png")
