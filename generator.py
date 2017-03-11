import random

class SampleGenerator:
    def __init__(self, min_attribute_range, max_attribute_range, grid_segment_number):
        self.attribute_range = abs(max_attribute_range - min_attribute_range)
        self.grid_segment_number = grid_segment_number
        self.min_attribute_range = min_attribute_range
        self.max_attribute_range = max_attribute_range
        self.grid_width = self.attribute_range / grid_segment_number

    def generate_points(self, i,j,sample_number, class_id):
        return [(random.uniform(i*self.grid_width, (i+1)*self.grid_width),
                 random.uniform(j*self.grid_width, (j+1)*self.grid_width),
                 class_id) for number in range(sample_number)]

    # def save_to_file(self):
    #     filename = "dataset1.csv"
    #     with open(filename) as f:

# sample_gen = SampleGenerator(0.0,100.0,10)
# print(sample_gen.generate_points(0,1,8,'B'))