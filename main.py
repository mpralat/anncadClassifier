from generator import SampleGenerator

if __name__ == "__main__":
    sample_generator = SampleGenerator(0.0, 100.0, "dataset_seed.csv")
    sample_generator.create_dataset()