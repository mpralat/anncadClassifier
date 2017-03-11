import random
import csv
import numpy as np


class SampleGenerator:
    def __init__(self, min_attribute_range, max_attribute_range, seed_filename):
        self.attribute_range = abs(max_attribute_range - min_attribute_range)
        self.min_attribute_range = min_attribute_range
        self.max_attribute_range = max_attribute_range
        self.seed_filename = seed_filename

    def parse_seed_file(self):
        class_seed = {}
        with open(self.seed_filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                class_seed[row[0]] = [int(x) for x in row[1:]]
        return class_seed

    def generate_points(self, i, j, sample_number, class_id):
        return [(random.uniform(i * self.grid_width, (i + 1) * self.grid_width),
                 random.uniform(j * self.grid_width, (j + 1) * self.grid_width),
                 class_id) for number in range(sample_number)]

    def save_to_file(self, points):
        filename = "dataset1.csv"
        with open(filename, 'a') as csvfile:
            writer = csv.writer(csvfile)
            for observation in points:
                writer.writerow(observation)

    def create_dataset(self):
        class_seed = self.parse_seed_file()
        self.grid_segment_number = np.sqrt(len(list(class_seed.values())[0]))
        self.grid_width = self.attribute_range / self.grid_segment_number
        for class_id in class_seed:
            for index, observations in enumerate(class_seed[class_id]):
                i = index / self.grid_segment_number
                j = index % self.grid_segment_number
                self.save_to_file(self.generate_points(i, j, observations, class_id))
