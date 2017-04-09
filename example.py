class Example(object):
    """
    A representation of an observation.
    
    :param observation: A list of example's coordinates and its class on the last position.
    :example: observation = [2, 3, 'B']
    :raises ValueError: Raises an exception when len(observation) < 2
    """
    def __init__(self, observation):
        if len(observation) < 2:
            raise ValueError \
                ("Observation should have at least two items: corrdinates of the example and its class.")
        self.coords = [float(x) for x in observation[:-1]]
        self.class_id = observation[-1]
        self.predicted_class_id = None  # predicted by specific grid's hypercube

