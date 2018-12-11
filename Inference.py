class Inference:

    def __init__(self, correct_value, values, observations):
        self.correct_value = correct_value
        self.observations = observations
        self.values = values
        self.computed_value = None

    def __repr__(self):
        representation = "Inference (%s) : (%s) with correct value %s "\
               % (self.values.__repr__(), self.observations.__repr__(), self.correct_value)
        return representation + ("and computed %f" % self.computed_value) if self.computed_value \
            else (representation + "not computed")

    def set_computed_value(self, val):
        self.computed_value = val
