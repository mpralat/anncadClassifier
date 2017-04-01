from anncad import AnncadClassifier
from example import Example
from generator import SampleGenerator
from streamEngine import Stream
from utils import plot_dataset

if __name__ == "__main__":
    # Generating the samples
    # sample_generator = SampleGenerator(0.0, 100.0, "dataset_seed.csv")
    # sample_generator.create_dataset()
    # # Plotting
    # plot_dataset()
    # Streaming the generated observations
    stream = Stream("dataset1.csv")
    generator = stream.emit_observation
    # Creating an empty grid
    threshold = 0.8
    # Creating an instance of ANNCAD classifier
    anncad = AnncadClassifier(threshold, 2)
    while True:
        try:
            observation = next(generator)
            anncad.add_example(observation)
        except StopIteration:
            break
    print("Build grids")
    anncad.build_grids()
    example = Example([1, 1, 1, 'R'])
    print("Classify")
    anncad.classify(example=example)
    print("Update")
    examples = [example, Example([5, 3, 3, 'R']), Example([3, 3, 3, 'B'])]
    for example in examples:
        anncad.update(example)
