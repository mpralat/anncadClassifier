from anncad import AnncadClassifier
from example import Example
from generator import SampleGenerator
from streamEngine import Stream
from utils import plot_dataset

if __name__ == "__main__":
    # Generating the samples
    sample_generator = SampleGenerator(min_attribute_value=0.0, max_attribute_value=100.0, seed_filename="dataset_seed.csv")
    sample_generator.create_dataset()
    # # Plotting
    # plot_dataset()
    # Streaming the generated observations
    stream = Stream("dataset1.csv")
    generator = stream.emit_observation
    # Creating an empty grid
    threshold = 0.8
    # Creating an instance of ANNCAD classifier
    anncad = AnncadClassifier(threshold=threshold, batch_size=3, attributes_boundaries=[(0.0, 100.0), (0.0, 100.0)])
    while True:
        try:
            observation = [next(generator)]
            anncad.add_examples(list_of_examples=observation)
        except StopIteration:
            break
    print("-----")
    print("Build grids.")
    anncad.set_hypercubes_classes()
    example = [1, 1, 'R']
    print("-----")
    print("Classify")
    class_id = anncad.test(example=example)
    print(class_id, example[-1])
    example = [2, 2]
    class_id = anncad.classify(example_coords=example)
    print(class_id)
    print("------")
    print("Update")
    examples = [[5, 3, 'R'], [8, 3, 'B'], [1, 2, 'B']]
    anncad.update(list_of_examples=examples)
