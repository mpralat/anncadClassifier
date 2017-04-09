from anncad import AnncadClassifier
from example import Example
from generator import SampleGenerator
from streamEngine import Stream
from utils import plot_dataset

if __name__ == "__main__":
    # Generating the samples
    sample_generator = SampleGenerator(0.0, 100.0, "dataset_seed.csv")
    sample_generator.create_dataset()
    # # Plotting
    # plot_dataset()
    # Streaming the generated observations
    stream = Stream("dataset1.csv")
    generator = stream.emit_observation
    # Creating an empty grid
    threshold = 0.8
    # Creating an instance of ANNCAD classifier
    anncad = AnncadClassifier(threshold, '3', [(0.0, 100.0), (0.0, 100.0)])
    while True:
        try:
            observation = [next(generator)]
            print(observation, type(observation))
            anncad.add_examples(observation)
        except StopIteration:
            break
    print("Build grids")
    anncad.set_hypercubes_classes()
    example = [1, 1, 'R']
    print("Classify")
    class_id = anncad.test(example=example)
    print(class_id, example[-1])
    example = [2, 2]
    class_id = anncad.classify(example)
    print(class_id)
    print("Update")
    examples = [[5, 3, 'R'], [8, 3, 'B'], [1, 2, 'B']]
    anncad.update(examples)
