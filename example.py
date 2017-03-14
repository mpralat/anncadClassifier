class Example:
    def __init__(self, observation):
        self.coords = [float(x) for x in observation[:-1]]
        self.class_id = observation[-1]
        self.predicted_class_id = None  # predicted by specific grid's hypercube
