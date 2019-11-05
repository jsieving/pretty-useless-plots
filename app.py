import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
from importlib import import_module
from pprint import pprint

class Canvas(QLabel):
    def __init__(self, screen_res):
        super().__init__()
        self.bg_color = Qt.white
        self.colors = {"White": "#FFFFFF", "Light gray": "#DDDDDD", "Dark gray": "#222222", "Black": "#000000"}
        w, h = screen_res.width(), screen_res.height()
        self.w, self.h = w * .6, h * .8
        pixmap = QtGui.QPixmap(self.w, self.h)
        pixmap.fill(self.bg_color)
        self.setPixmap(pixmap)

    def clear(self):
        self.pixmap().fill(self.bg_color)
        self.update()

class MainWindow(QMainWindow):
    def __init__(self, screen_res):
        super().__init__()

        self.canvas = Canvas(screen_res)
        self.model_names = ["None selected", "Branch", "Conway", "Harmonograph", "Heatmap", "Transform"]
        self.models = self.load_models() # model classes
        self.menus = self.load_menus() # dict of widgets for each model
        self.curr_model = "None selected"
        self.model = None # Model object
        self.model_params = {} # settings for the model to run (not used)

        main_w = QWidget() # create a widget
        main_l = QHBoxLayout() # establish a horiz layout
        main_w.setLayout(main_l) # set the widget's layout as horiz

        control_l = QVBoxLayout()

        model_l = QGridLayout()
        model_drop = QComboBox()
        model_drop.addItems(self.model_names)
        model_drop.activated[str].connect(self.change_model)
        model_label = QLabel("Model:")

        color_drop = QComboBox()
        color_drop.addItems(["White", "Light gray", "Dark gray", "Black"])
        color_drop.activated[str].connect(self.change_color)
        color_label = QLabel("Canvas:")

        random_b = QPushButton('Randomize')
        random_b.clicked.connect(self.on_randomize)

        restart_b = QPushButton('Restart clock')
        restart_b.clicked.connect(self.on_restart)

        reset_b = QPushButton('Reset settings')
        reset_b.clicked.connect(self.on_reset)

        clear_b = QPushButton('Clear screen')
        clear_b.clicked.connect(self.clear_screen)

        go_b = QPushButton('Go!')
        go_b.clicked.connect(self.on_go)

        main_l.addWidget(self.canvas)
        main_l.addLayout(control_l)
        control_l.addLayout(model_l)
        for widget in self.menus.values():
            control_l.addWidget(widget)
        control_l.addWidget(random_b)
        control_l.addWidget(restart_b)
        control_l.addWidget(reset_b)
        control_l.addWidget(clear_b)
        control_l.addWidget(go_b)
        model_l.addWidget(model_label, 0, 0)
        model_l.addWidget(model_drop, 0, 1)
        model_l.addWidget(color_label, 1, 0)
        model_l.addWidget(color_drop, 1, 1)

        self.setCentralWidget(main_w)
        self.change_widget()

    def clear_screen(self):
        self.canvas.clear()

    def on_restart(self):
        if self.model is not None:
            self.model.depth = 0

    def on_reset(self):
        self.model.reset()

    def on_randomize(self):
        self.model.randomize()
        try:
            pass
        except:
            print("This model cannot be randomized.")

    def on_go(self):
        if self.model is not None:
            print("Go!")
            self.on_restart()
            self.clear_screen()
            self.model.go()
        else:
            print("No model selected!")

    def load_models(self):
        models = {}
        for name in self.model_names:
            try:
                ModelClass = getattr(import_module("objects." + name.lower()), name)
                models[name] = ModelClass(self.canvas)
            except:
                models[name] = None
                print("Could not import %s" % name)
        return models

    def load_menus(self):
        menus = {}
        for name in self.model_names:
            menus[name] = QWidget()
            try:
                model = self.models[name]
                menus[name].setLayout(model.init_menu_layout())
            except:
                empty = QVBoxLayout()
                empty.addWidget(QLabel("No settings found"))
                menus[name].setLayout(empty)
                print("No settings menu found for model %s" % name)
        return menus

    def change_model(self, model_name):
        print("Model changed to %s" % model_name)
        self.curr_model = model_name
        self.model = self.models.get(model_name, None)
        self.change_widget()

    def change_widget(self):
        for name, widget in self.menus.items():
            if name == self.curr_model:
                widget.show()
            else:
                widget.hide()

    def change_color(self, name):
        c = self.canvas.colors[name]
        self.canvas.bg_color = QtGui.QColor(c)
        self.clear_screen()

if __name__ == "__main__":

    app = QApplication([])
    screen_res = app.desktop().screenGeometry()
    window = MainWindow(screen_res)
    window.show()
    # app.exec_()
    sys.exit(app.exec_())
