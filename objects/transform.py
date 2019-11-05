try:
    from objects.generator import Generator
except:
    from generator import Generator

class Transform(Generator):
    def __init__(self, canvas): # add any attributes

        # define functions for this type of generator

        # initialize a generator with these attributes
        Generator.__init__(self)

        # define additional attributes for this type of generator
        self.canvas = canvas

    # define additional utility functions for this type of generator
