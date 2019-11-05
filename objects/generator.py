from matplotlib import cm
from time import sleep

class Generator:
    def __init__(self, depth = 0, max_depth = 1,
                go_func = None, step_func = None,
                draw_func = None,
                size = 1, cmap = None):
        self.depth = depth
        self.max_depth = max_depth
        self.cmap = cm.get_cmap("jet")
        self.go_func = go_func
        self.step_func = step_func
        self.draw_func = draw_func

    def go(self):
        self.go_func(self)

    def step(self): # may not be needed / makes "self" passing in implicit
        sleep(.1)
        self.step_func(self)

    def draw(self): # may not be needed / makes "self" passing in implicit
        self.draw_func(self)

    # def __repr__(self):
    #     return "'%s' at depth %i of max %i" % (type(self).__name__, self.depth, self.max_depth)
