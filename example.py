class Example(object):

    def __init__(self, observation):
        # TODO not sure about having both coords and the class in one struct
        if len(observation) < 2:
            raise ValueError \
                ("Observation should have at least two items: corrdinates of the example and its class.")
        self.coords = [float(x) for x in observation[:-1]]
        self.class_id = observation[-1]
        self.predicted_class_id = None  # predicted by specific grid's hypercube

