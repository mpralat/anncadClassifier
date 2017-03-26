from anncad import AnncadClassifier
from example import Example
from generator import SampleGenerator
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
    threshold = 0.8
    # Creating an instance of ANNCAD classifier
    anncad = AnncadClassifier(threshold)
    while True:
        try:
            observation = next(generator)
            anncad.add_example(observation)
        except StopIteration:
            break
    print("xD")
    anncad.build_grids()
    example = Example([60, 51, 'B'])
    print("go")
    anncad.classify(example=example)
