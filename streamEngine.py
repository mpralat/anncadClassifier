import csv


class Stream:
    def __init__(self, dataset_filename):
        self.dataset_filename = dataset_filename

    @property
    def emit_observation(self):
        with open(self.dataset_filename, 'r') as datafile:
            reader = csv.reader(datafile)
            for row in reader:
                if not row:
                    continue
                yield row
        return 0
