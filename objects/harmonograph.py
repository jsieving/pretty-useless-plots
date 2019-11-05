from PySide2.QtGui import QColor, QPainter, QPen
from PySide2.QtCore import QPoint, Qt
from PySide2.QtWidgets import *
from time import sleep
from matplotlib import cm
import numpy as np
from random import randint
try:
    from objects.generator import Generator
except:
    from generator import Generator

class Harmonograph(Generator):
    def __init__(self, canvas):
        self.canvas = canvas
        self.x0 = canvas.w // 2
        self.y0 = canvas.h // 2
        self.depth = 0

    def step(self): # calculates parameters of current state
        if self.depth == 0:
            self.curr_x, self.curr_y = self.pos(0)
        else:
            self.prev_x, self.prev_y = self.curr_x, self.curr_y
            self.curr_x, self.curr_y = self.pos(self.depth)
            self.calc_color()
            self.draw()
        self.depth += .01

    def go(self): # propels model forward
        self.running = True
        while self.running:
            self.step()
            # sleep(.01)
            if self.depth > 100:
                self.running = False

    def draw(self): # draws current state
        p = QPainter(self.canvas.pixmap())
        pen = QPen(self.color, self.pen_size)
        p.setPen(pen)
        p.drawLine(self.prev_x, self.prev_y, self.curr_x, self.curr_y)
        p.end()
        self.canvas.repaint()

    def pos(self, t): # calculate position based on parent's position
        p1 = self.amp1 * (np.e ** (self.decay1 * t) * np.cos(t * self.freq1 + self.phase1))
        p2 = self.amp2 * (np.e ** (self.decay2 * t) * np.cos(t * self.freq2 + self.phase2))
        x = self.x0 + p1 * self.p1 + p2 * self.p2

        p3 = self.amp3 * (np.e ** (self.decay3 * t) * np.sin(t * self.freq3 + self.phase3))
        p4 = self.amp4 * (np.e ** (self.decay4 * t) * np.sin(t * self.freq4 + self.phase4))
        y = self.y0 + p3 * self.p3 + p4 * self.p4

        x = max(0, x)
        x = min(x, self.canvas.w)
        y = max(0, y)
        y = min(y, self.canvas.h)
        return x, y

    def calc_color(self): # calculate position based on parent's position
        val = self.depth / 100
        frac = val % 1
        if int(val) % 2 == 1:
            frac = 1-frac
        r, g, b, a = self.cmap(frac)
        self.color = QColor(r * 255, g * 255, b * 255)
        return self.color

    def randomize(self):
        for i in range(1, 5):
            amp = getattr(self, "amp" + str(i) + "_box")
            r = randint(0, 1000)
            amp.setValue(r)
            getattr(self, "set_amp" + str(i))(r)

            freq = getattr(self, "freq" + str(i) + "_box")
            r = randint(0, 40)
            freq.setValue(r)
            getattr(self, "set_freq" + str(i))(r)

            phase = getattr(self, "phase" + str(i) + "_box")
            r = randint(0, 360)
            phase.setValue(r)
            getattr(self, "set_phase" + str(i))(r)

            decay = getattr(self, "decay" + str(i) + "_box")
            r = randint(0, 100)
            decay.setValue(r)
            getattr(self, "set_decay" + str(i))(r)

    def init_menu_layout(self):
        l1 = QGridLayout()
        l2 = QGridLayout()
        l3 = QGridLayout()
        l4 = QGridLayout()
        self.p1_group = QGroupBox("Pendulum 1")
        self.p1_group.setLayout(l1)
        self.p1_group.setCheckable(True)
        self.p2_group = QGroupBox("Pendulum 2")
        self.p2_group.setLayout(l2)
        self.p2_group.setCheckable(True)
        self.p2_group.setChecked(False)
        self.p3_group = QGroupBox("Pendulum 3")
        self.p3_group.setLayout(l3)
        self.p3_group.setCheckable(True)
        self.p4_group = QGroupBox("Pendulum 4")
        self.p4_group.setLayout(l4)
        self.p4_group.setCheckable(True)
        self.p4_group.setChecked(False)

        self.amp1_label = QLabel("Amplitude:")
        self.amp1_box = QSpinBox()
        self.freq1_label = QLabel("Frequency (hz):")
        self.freq1_box = QSpinBox()
        self.phase1_label = QLabel("Phase (deg):")
        self.phase1_box = QSpinBox()
        self.decay1_label = QLabel("Decay:")
        self.decay1_box = QSpinBox()
        l1.addWidget(self.amp1_label, 0, 0)
        l1.addWidget(self.amp1_box, 0, 1)
        l1.addWidget(self.freq1_label, 1, 0)
        l1.addWidget(self.freq1_box, 1, 1)
        l1.addWidget(self.phase1_label, 2, 0)
        l1.addWidget(self.phase1_box, 2, 1)
        l1.addWidget(self.decay1_label, 3, 0)
        l1.addWidget(self.decay1_box, 3, 1)

        self.amp2_label = QLabel("Amplitude:")
        self.amp2_box = QSpinBox()
        self.freq2_label = QLabel("Frequency (hz):")
        self.freq2_box = QSpinBox()
        self.phase2_label = QLabel("Phase (deg):")
        self.phase2_box = QSpinBox()
        self.decay2_label = QLabel("Decay:")
        self.decay2_box = QSpinBox()
        l2.addWidget(self.amp2_label, 0, 0)
        l2.addWidget(self.amp2_box, 0, 1)
        l2.addWidget(self.freq2_label, 1, 0)
        l2.addWidget(self.freq2_box, 1, 1)
        l2.addWidget(self.phase2_label, 2, 0)
        l2.addWidget(self.phase2_box, 2, 1)
        l2.addWidget(self.decay2_label, 3, 0)
        l2.addWidget(self.decay2_box, 3, 1)

        self.amp3_label = QLabel("Amplitude:")
        self.amp3_box = QSpinBox()
        self.freq3_label = QLabel("Frequency (hz):")
        self.freq3_box = QSpinBox()
        self.phase3_label = QLabel("Phase (deg):")
        self.phase3_box = QSpinBox()
        self.decay3_label = QLabel("Decay:")
        self.decay3_box = QSpinBox()
        l3.addWidget(self.amp3_label, 0, 0)
        l3.addWidget(self.amp3_box, 0, 1)
        l3.addWidget(self.freq3_label, 1, 0)
        l3.addWidget(self.freq3_box, 1, 1)
        l3.addWidget(self.phase3_label, 2, 0)
        l3.addWidget(self.phase3_box, 2, 1)
        l3.addWidget(self.decay3_label, 3, 0)
        l3.addWidget(self.decay3_box, 3, 1)

        self.amp4_label = QLabel("Amplitude:")
        self.amp4_box = QSpinBox()
        self.freq4_label = QLabel("Frequency (hz):")
        self.freq4_box = QSpinBox()
        self.phase4_label = QLabel("Phase (deg):")
        self.phase4_box = QSpinBox()
        self.decay4_label = QLabel("Decay:")
        self.decay4_box = QSpinBox()
        l4.addWidget(self.amp4_label, 0, 0)
        l4.addWidget(self.amp4_box, 0, 1)
        l4.addWidget(self.freq4_label, 1, 0)
        l4.addWidget(self.freq4_box, 1, 1)
        l4.addWidget(self.phase4_label, 2, 0)
        l4.addWidget(self.phase4_box, 2, 1)
        l4.addWidget(self.decay4_label, 3, 0)
        l4.addWidget(self.decay4_box, 3, 1)


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
        self.size_label = QLabel("Pen size:")
        self.size_box = QSpinBox()
        self.decay_label = QLabel("Decay rate (%):")
        self.decay_box = QSpinBox()
        l.addWidget(self.cmap_label, 0, 0)
        l.addWidget(self.cmap_box, 0, 1)
        l.addWidget(self.size_label, 1, 0)
        l.addWidget(self.size_box, 1, 1)
        # l.addWidget(self.decay_label, 2, 0)
        # l.addWidget(self.decay_box, 2, 1)
        l.addWidget(self.p1_group, 3, 0, 1, 2)
        l.addWidget(self.p2_group, 4, 0, 1, 2)
        l.addWidget(self.p3_group, 5, 0, 1, 2)
        l.addWidget(self.p4_group, 6, 0, 1, 2)
        self.reset()
        return l

    def reset(self):
        self.cmap_box.setCurrentIndex(0)
        self.cmap_box.activated[str].connect(self.set_cmap)
        self.cmap = cm.get_cmap("viridis")

        self.size_box.setMinimum(1)
        self.size_box.setMaximum(100)
        self.size_box.setValue(5)
        self.size_box.valueChanged.connect(self.set_size)
        self.pen_size = 5

        # self.decay_box.setMinimum(0)
        # self.decay_box.setMaximum(100)
        # self.decay_box.setValue(5)
        # self.decay_box.valueChanged.connect(self.set_decay)
        # self.decay = -.05

        self.p1_group.clicked.connect(self.toggle_p1)
        self.amp1_box.valueChanged.connect(self.set_amp1)
        self.amp1_box.setMinimum(0); self.amp1_box.setMaximum(1000); self.amp1_box.setValue(300)
        self.freq1_box.valueChanged.connect(self.set_freq1)
        self.freq1_box.setMinimum(0); self.freq1_box.setMaximum(40); self.freq1_box.setValue(2)
        self.phase1_box.valueChanged.connect(self.set_phase1)
        self.phase1_box.setMinimum(0); self.phase1_box.setMaximum(360); self.phase1_box.setValue(0)
        self.decay1_box.valueChanged.connect(self.set_decay1)
        self.decay1_box.setMinimum(0); self.decay1_box.setMaximum(100); self.decay1_box.setValue(5)
        self.p1 = True
        self.amp1 = 300
        self.freq1 = 2 * 2 / np.pi
        self.phase1 = 0
        self.decay1 = -5/200

        self.p2_group.clicked.connect(self.toggle_p2)
        self.amp2_box.valueChanged.connect(self.set_amp2)
        self.amp2_box.setMinimum(0); self.amp2_box.setMaximum(1000); self.amp2_box.setValue(150)
        self.freq2_box.valueChanged.connect(self.set_freq2)
        self.freq2_box.setMinimum(0); self.freq2_box.setMaximum(40); self.freq2_box.setValue(4)
        self.phase2_box.valueChanged.connect(self.set_phase2)
        self.phase2_box.setMinimum(0); self.phase2_box.setMaximum(360); self.phase2_box.setValue(0)
        self.decay2_box.valueChanged.connect(self.set_decay2)
        self.decay2_box.setMinimum(0); self.decay2_box.setMaximum(100); self.decay2_box.setValue(5)
        self.p2 = False
        self.amp2 = 150
        self.freq2 = 4 * 2 / np.pi
        self.phase2 = 0
        self.decay2 = -5/200

        self.p3_group.clicked.connect(self.toggle_p3)
        self.amp3_box.valueChanged.connect(self.set_amp3)
        self.amp3_box.setMinimum(0); self.amp3_box.setMaximum(1000); self.amp3_box.setValue(300)
        self.freq3_box.valueChanged.connect(self.set_freq3)
        self.freq3_box.setMinimum(0); self.freq3_box.setMaximum(40); self.freq3_box.setValue(2)
        self.phase3_box.valueChanged.connect(self.set_phase3)
        self.phase3_box.setMinimum(0); self.phase3_box.setMaximum(360); self.phase3_box.setValue(0)
        self.decay3_box.valueChanged.connect(self.set_decay3)
        self.decay3_box.setMinimum(0); self.decay3_box.setMaximum(100); self.decay3_box.setValue(5)
        self.p3 = True
        self.amp3 = 300
        self.freq3 = 2 * 2 / np.pi
        self.phase3 = 0
        self.decay3 = -5/200

        self.p4_group.clicked.connect(self.toggle_p4)
        self.amp4_box.valueChanged.connect(self.set_amp4)
        self.amp4_box.setMinimum(0); self.amp4_box.setMaximum(1000); self.amp4_box.setValue(150)
        self.freq4_box.valueChanged.connect(self.set_freq4)
        self.freq4_box.setMinimum(0); self.freq4_box.setMaximum(40); self.freq4_box.setValue(4)
        self.phase4_box.valueChanged.connect(self.set_phase4)
        self.phase4_box.setMinimum(0); self.phase4_box.setMaximum(360); self.phase4_box.setValue(0)
        self.decay4_box.valueChanged.connect(self.set_decay4)
        self.decay4_box.setMinimum(0); self.decay4_box.setMaximum(100); self.decay4_box.setValue(5)
        self.p4 = False
        self.amp4 = 150
        self.freq4 = 4 * 2 / np.pi
        self.phase4 = 0
        self.decay4 = -5/200

    def toggle_p1(self, state):
        self.p1 = state

    def toggle_p2(self, state):
        self.p2 = state

    def toggle_p3(self, state):
        self.p3 = state

    def toggle_p4(self, state):
        self.p4 = state

    def set_amp1(self, n):
        self.amp1 = n

    def set_amp2(self, n):
        self.amp2 = n

    def set_amp3(self, n):
        self.amp3 = n

    def set_amp4(self, n):
        self.amp4 = n

    def set_freq1(self, n):
        self.freq1 = n * 2 / np.pi

    def set_freq2(self, n):
        self.freq2 = n * 2 / np.pi

    def set_freq3(self, n):
        self.freq3 = n * 2 / np.pi

    def set_freq4(self, n):
        self.freq4 = n * 2 / np.pi

    def set_phase1(self, n):
        self.phase1 = n * np.pi / 180

    def set_phase2(self, n):
        self.phase2 = n * np.pi / 180

    def set_phase3(self, n):
        self.phase3 = n * np.pi / 180

    def set_phase4(self, n):
        self.phase4 = n * np.pi / 180

    def set_decay1(self, n):
        self.decay1 = n / -200

    def set_decay2(self, n):
        self.decay2 = n / -200

    def set_decay3(self, n):
        self.decay3 = n / -200

    def set_decay4(self, n):
        self.decay4 = n / -200

    def set_cmap(self, name):
        self.cmap = cm.get_cmap(name)

    def set_size(self, n):
        self.pen_size = n

    def set_decay(self, n):
        self.decay = -1 * n / 100
