import utils

class Example(object):
    def __init__(self, observation):
        # TODO not sure about having both coords and the class in one struct
        if len(observation) < 2:
            raise ValueError \
                ("Observation should have at least two items: corrdinates of the example and its class.")
        if not utils.is_array_numeric(observation[:-1]):
            raise ValueError \
                ("Example's coordinates should be of a numerical type.")
        self.coords = [float(x) for x in observation[:-1]]
        self.class_id = observation[-1]
        self.predicted_class_id = None  # predicted by specific grid's hypercube

