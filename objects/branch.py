from PySide2.QtGui import QColor, QPainter
from PySide2.QtCore import QPoint, Qt
from PySide2.QtWidgets import *
from time import sleep
from matplotlib import cm
import numpy as np
from random import randint, random
from math import log, floor
try:
    from objects.generator import Generator
except:
    from generator import Generator

class Branch(Generator):
    ''' A model which creates tree-like structures by generating copies of
    itself with modified size, position and color in relation to the parent. '''
    def __init__(self, canvas, parent = None, child_no = 0):
        ''' Create a branch - by default, it will be a head node, but upon
        calling "go", more instances will be created with the creator as the
        parent and a child number indicating position. '''
        self.canvas = canvas
        self.parent = parent
        self.child_no = child_no
        self.max_nodes = 10000

        ''' if this is a child node, these attributes will be inherited from
        the parent. If it were the head, these attributes would have been set
        when the settings panel was created and called "reset". '''
        if parent is not None:
            self.depth = parent.depth + 1
            self.max_depth = parent.max_depth
            self.draw_lines = parent.draw_lines
            self.num_children = parent.num_children
            self.cmap = parent.cmap
            self.curve = parent.curve
            self.fan = parent.fan
            self.size_grow = self.parent.size_grow
            self.length_grow = self.parent.length_grow
            self.branch_prob = self.parent.branch_prob
            self.centerness = self.parent.centerness
            self.distribution = self.parent.distribution
        else: # only these need to be set for the parent, and aren't in reset()
            self.x = canvas.w // 2
            self.y = canvas.h // 2
            self.angle = -90
            self.depth = 0

    def step(self):
        ''' calculates parameters of current state/node instance. Each of these
        methods assign values as well as calculating them. '''
        self.calc_len()
        self.calc_size()
        self.calc_pos()
        self.calc_color()

    def go(self):
        ''' Runs the generation and drawing of the tree. '''
        self.step() # calculate current parameters
        self.children = []
        if self.depth >= self.max_depth: # do not exceed max branch depth
            return
        for i in range(self.num_children): # create children
            if self.node_choice(i): # always true for 1, never for 0
                child = Branch(self.canvas, parent = self, child_no = i)
                self.children.append(child)
                child.go() # run child: calculate parameters, generate children, and draw
        self.draw() # draw self last so that lines drawn by children are covered

    def draw(self):
        ''' Draws this node of the tree and updates the canvas. '''
        p = QPainter(self.canvas.pixmap())
        p.setPen(self.color)
        p.setBrush(self.color)

        # draw a stem if appropriate
        if self.parent is not None and self.draw_lines:
            prevx = self.parent.x + self.parent.size * np.cos(self.angle * np.pi / 180)
            prevy = self.parent.y + self.parent.size * np.sin(self.angle * np.pi / 180)
            p.drawLine(prevx, prevy, self.x, self.y)
        c = QPoint(self.x, self.y)
        p.drawEllipse(c, self.size, self.size)
        p.end()
        # Repaint for every node, so gradual generation can be seen
        self.canvas.repaint()

    def calc_len(self):
        ''' calculate and set branch length based on parent's branch length '''
        if self.depth > 1:
            self.length = self.parent.length * self.length_grow
        if self.depth == 1:
            self.length = self.parent.length

    def calc_pos(self):
        ''' calculate and set position based on parent's position, branch length
        and child number '''
        if self.parent is not None:
            if self.num_children == 1:
                dev = 0
            else:
                dev = self.fan * (self.child_no - ((self.num_children - 1) / 2)) / (self.num_children - 1)
            self.angle = self.parent.angle + self.parent.curve + dev
            self.x = self.parent.x + self.length * np.cos(self.angle * np.pi / 180)
            self.y = self.parent.y + self.length * np.sin(self.angle * np.pi / 180)

    def calc_color(self):
        ''' Calculate and set color based on tree depth of this node '''
        r, g, b, a = self.cmap(self.depth/(self.max_depth - 1))
        self.color = QColor(r * 255, g * 255, b * 255)

    def calc_size(self):
        ''' Calculate and set size based on parent's size '''
        if self.parent is not None:
            self.size = self.parent.size * self.size_grow

    def suggested_max_depth(self, children, upper_limit=False):
        ''' Utility function to compute the suggested maximum branch depth for a
        given number of children per node. This allows some functions to
        automatically find a depth that will result in a reasonable run time.
        "a reasonable run time" means the time it takes to generate max_nodes
        nodes, defined in __init__. '''
        # children = 1 is not a problem in terms of growth, and creates a
        # division by zero error in log.
        if children > 1:
            # compute tree depth of max_nodes with n-way branches
            suggested_depth = floor(log((self.max_nodes * (children-1) + 1), children))
            if not upper_limit:
                # don't adjust the max if the depth is already below it
                suggested_depth = min([self.max_depth, suggested_depth])
            return suggested_depth

    def node_choice(self, child_no):
        vote = random()
        decision = self.branch_prob * self.distribution[child_no]
        if vote < decision:
            return True
        else:
            return False

    def calc_distribution(self):
        distribution = []
        if self.num_children < 3:
            self.distribution = [1 for i in range(self.num_children)]
            return
        for i in range(self.num_children):
            dist = abs(i - (self.num_children - 1.0) / 2)
            span = (self.num_children - 1) // 2
            mid = (self.num_children // 2) / 2
            place = (dist-mid) * -2 / span
            fudge = (self.num_children % 2) * self.centerness / self.num_children
            multiplier = 1 + place * self.centerness + fudge
            distribution.append(multiplier)
        self.distribution = distribution

    def randomize(self):
        ''' Randomize customizable settings of the tree model '''
        if randint(0, 1) > 0:
            self.draw_lines = True
            c = Qt.Checked
        else:
            self.draw_lines = False
            c = Qt.Unchecked
        self.num_children = randint(2, 6)
        suggested_depth = self.suggested_max_depth(self.num_children, upper_limit=True)
        self.max_depth = randint(4, suggested_depth)
        self.branch_prob = randint(5, 10) / 10
        self.centerness = randint(0, 5) / 10
        self.curve = randint(-60, 60)
        suggested_fan = 360 - (360 // self.num_children)
        self.fan = randint(0, suggested_fan)
        self.size = randint(15, 80)
        size_grow_percent = randint(50, 120)
        self.size_grow = size_grow_percent / 100
        # make length more than size of nodes
        self.length = randint(self.size//2, 200)
        # have length grow faster than size
        self.length_grow = randint(size_grow_percent, 150) / 100
        # update branch probability distribution with new parameters
        self.calc_distribution()

        # set all setting controls to reflect this
        self.max_depth_box.setValue(self.max_depth)
        self.draw_lines_box.setCheckState(c)
        self.children_box.setValue(self.num_children)
        self.branch_prob_box.setValue(self.branch_prob)
        self.centerness_box.setValue(self.centerness)
        self.curve_box.setValue(self.curve)
        self.fan_box.setValue(self.fan)
        self.size_box.setValue(self.size)
        self.size_grow_box.setValue(self.size_grow)
        self.len_box.setValue(self.length)
        self.len_grow_box.setValue(self.length_grow)

    def init_menu_layout(self):
        ''' create a menu layout for the settings of this model, reset/
        initialize the model parameters, and pass this layout to the model
        control widget. '''
        l = QGridLayout()
        self.cmap_label = QLabel("Color map:")
        self.cmap_box = QComboBox()
        self.cmap_box.addItems(['viridis', 'plasma', 'inferno', 'magma', 'gray', 'bone', 'pink',
            'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
            'hot', 'afmhot', 'gist_heat', 'copper', 'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
            'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic', 'twilight', 'twilight_shifted', 'hsv',
             'ocean', 'gist_earth', 'terrain', 'gist_stern',
            'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
            'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar'])
        self.cmap_box.activated[str].connect(self.set_cmap)
        self.children_label = QLabel("Children:")
        self.children_box = QSpinBox()
        self.max_depth_label = QLabel("Max branch depth:")
        self.max_depth_box = QSpinBox()
        self.branch_prob_label = QLabel("Branch probability:")
        self.branch_prob_box = QDoubleSpinBox()
        self.centerness_label = QLabel("Centerness:")
        self.centerness_box = QDoubleSpinBox()
        self.draw_lines_label = QLabel("Show lines:")
        self.draw_lines_box = QCheckBox()
        self.size_label = QLabel("Size:")
        self.size_box = QSpinBox()
        self.size_grow_label = QLabel("Size growth:")
        self.size_grow_box = QDoubleSpinBox()
        self.len_label = QLabel("Length:")
        self.len_box = QSpinBox()
        self.len_grow_label = QLabel("Length growth:")
        self.len_grow_box = QDoubleSpinBox()
        self.curve_label = QLabel("Curvature:")
        self.curve_box = QSpinBox()
        self.fan_label = QLabel("Fan:")
        self.fan_box = QSpinBox()
        l.addWidget(self.cmap_label, 0, 0)
        l.addWidget(self.cmap_box, 0, 1)
        l.addWidget(self.children_label, 1, 0)
        l.addWidget(self.children_box, 1, 1)
        l.addWidget(self.max_depth_label, 2, 0)
        l.addWidget(self.max_depth_box, 2, 1)
        l.addWidget(self.branch_prob_label, 3, 0)
        l.addWidget(self.branch_prob_box, 3, 1)
        l.addWidget(self.centerness_label, 4, 0)
        l.addWidget(self.centerness_box, 4, 1)
        l.addWidget(self.draw_lines_label, 5, 0)
        l.addWidget(self.draw_lines_box, 5, 1)
        l.addWidget(self.size_label, 6, 0)
        l.addWidget(self.size_box, 6, 1)
        l.addWidget(self.size_grow_label, 7, 0)
        l.addWidget(self.size_grow_box, 7, 1)
        l.addWidget(self.len_label, 8, 0)
        l.addWidget(self.len_box, 8, 1)
        l.addWidget(self.len_grow_label, 9, 0)
        l.addWidget(self.len_grow_box, 9, 1)
        l.addWidget(self.curve_label, 10, 0)
        l.addWidget(self.curve_box, 10, 1)
        l.addWidget(self.fan_label, 11, 0)
        l.addWidget(self.fan_box, 11, 1)
        self.reset()
        return l

    def reset(self):
        ''' reset all model parameters and their corresponding settings to
        default values. '''
        self.cmap_box.setCurrentIndex(0)
        self.cmap = cm.get_cmap("viridis")

        self.children_box.setMinimum(1)
        self.children_box.setMaximum(12)
        self.children_box.setValue(3)
        self.children_box.valueChanged.connect(self.set_children)
        self.num_children = 3

        self.max_depth_box.setMinimum(1)
        self.max_depth_box.setMaximum(15)
        self.max_depth_box.setValue(9)
        self.max_depth_box.valueChanged.connect(self.set_max_depth)
        self.max_depth = 9

        self.branch_prob_box.setMinimum(.1)
        self.branch_prob_box.setMaximum(1.0)
        self.branch_prob_box.setValue(.6)
        self.branch_prob_box.valueChanged.connect(self.set_branch_prob)
        self.branch_prob = 0.6

        self.centerness_box.setMinimum(0.0)
        self.centerness_box.setMaximum(1.0)
        self.centerness_box.setValue(0.3)
        self.centerness_box.valueChanged.connect(self.set_centerness)
        self.centerness = 0.3
        # calculate branching probability distribution with current number of
        # children and centerness (center-favoring probability)
        self.calc_distribution()

        self.draw_lines_box.setCheckState(Qt.Checked)
        self.draw_lines_box.toggled.connect(self.set_draw_lines)
        self.draw_lines = True

        self.size_box.setMinimum(1)
        self.size_box.setMaximum(400)
        self.size_box.setValue(15)
        self.size_box.valueChanged.connect(self.set_size)
        self.size = 15

        self.size_grow_box.setMinimum(.1)
        self.size_grow_box.setMaximum(2.0)
        self.size_grow_box.setValue(.9)
        self.size_grow_box.valueChanged.connect(self.set_grow_size)
        self.size_grow = .9

        self.len_box.setMinimum(10)
        self.len_box.setMaximum(200)
        self.len_box.setValue(50)
        self.len_box.valueChanged.connect(self.set_len)
        self.length = 50

        self.len_grow_box.setMinimum(.1)
        self.len_grow_box.setMaximum(2.0)
        self.len_grow_box.setValue(.9)
        self.len_grow_box.valueChanged.connect(self.set_grow_len)
        self.length_grow = .9

        self.curve_box.setMinimum(-180)
        self.curve_box.setMaximum(180)
        self.curve_box.setValue(10)
        self.curve_box.valueChanged.connect(self.set_curve)
        self.curve = 10

        self.fan_box.setMinimum(0)
        self.fan_box.setMaximum(360)
        self.fan_box.setValue(90)
        self.fan_box.valueChanged.connect(self.set_fan)
        self.fan = 90

    ''' functions for setting model parameters on interface events. '''
    def set_cmap(self, name):
        self.cmap = cm.get_cmap(name)

    def set_children(self, n):
        self.num_children = n
        # update distribution with new number of children
        self.calc_distribution()
        # automatically adjust depth to improve performance
        # this can be overridden by changing the max branch depth spinner
        if n > 1:
            # compute tree depth of max_nodes with n-way branches
            suggested_depth = floor(log((self.max_nodes * (n-1) + 1), n))
            # if current depth is small, no need to adjust it
            depth = min([self.max_depth, suggested_depth])
            # set value and control box value
            self.set_max_depth(depth)
            self.max_depth_box.setValue(depth)

    def set_max_depth(self, n):
        self.max_depth = n

    def set_branch_prob(self, n):
        self.branch_prob = n

    def set_centerness(self, n):
        self.centerness = n
        # update distribution with new "shape"
        self.calc_distribution()

    def set_draw_lines(self, state):
        self.draw_lines = state

    def set_size(self, n):
        self.size = n

    def set_grow_size(self, n):
        self.size_grow = n

    def set_len(self, n):
        self.length = n

    def set_grow_len(self, n):
        self.length_grow = n

    def set_curve(self, n):
        self.curve = n

    def set_fan(self, n):
        self.fan = n
