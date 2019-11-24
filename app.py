import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt, QTimer
from importlib import import_module
from pprint import pprint

class Canvas(QLabel):
    ''' The canvas, on which any model loaded by the application will draw. '''
    def __init__(self, screen_res):
        super().__init__()
        self.bg_color = Qt.white
        self.colors = {"White": "#FFFFFF", "Light gray": "#DDDDDD", "Dark gray": "#222222", "Black": "#000000"}
        w, h = screen_res.width(), screen_res.height()
        self.w, self.h = w * .6, h * .6
        pixmap = QtGui.QPixmap(self.w, self.h)
        pixmap.fill(self.bg_color)
        self.setPixmap(pixmap)

    def clear(self):
        ''' Clears and updates the canvas. '''
        self.pixmap().fill(self.bg_color)
        self.update()

class MainWindow(QMainWindow):
    ''' The main application window, which manages the canvas, keeps track of
    and manages all imported models, manages the overall controls, and displays
    or hides model-specific controls. '''
    def __init__(self, screen_res):
        super().__init__()

        self.canvas = Canvas(screen_res)
        self.model_names = ["None selected", "Branch", "Conway", "Harmonograph", "Heatmap", "Transform"]
        self.models = self.load_models() # model classes
        self.menus = self.load_menus() # dict of widgets for each model
        self.curr_model = "None selected"
        self.model = None # Model object
        self.model_params = {} # settings for the model to run (not used)

        main_w = QWidget() # create a widget to contain canvas and all controls
        main_l = QHBoxLayout()
        main_w.setLayout(main_l)

        control_l = QVBoxLayout() # layout for canvas & overall controls
        buttons_l = QHBoxLayout() # layout for main control buttons, under control_l
        model_l = QVBoxLayout() # layout for model-specific controls

        # create layout for choosing model and color scheme
        choose_model_l = QGridLayout()
        model_drop = QComboBox()
        model_drop.addItems(self.model_names)
        model_drop.activated[str].connect(self.change_model)
        model_label = QLabel("Model:")

        color_drop = QComboBox()
        color_drop.addItems(["White", "Light gray", "Dark gray", "Black"])
        color_drop.activated[str].connect(self.change_color)
        color_label = QLabel("Canvas:")

        # create control buttons
        random_b = QPushButton('Randomize')
        random_b.clicked.connect(self.on_randomize)

        restart_b = QPushButton('Restart clock')
        restart_b.clicked.connect(self.on_restart)

        reset_b = QPushButton('Reset settings')
        reset_b.clicked.connect(self.on_reset)

        clear_b = QPushButton('Clear screen')
        clear_b.clicked.connect(self.clear_screen)

        save_b = QPushButton('Save')
        save_b.clicked.connect(self.save_image)

        go_b = QPushButton('Go!')
        go_b.clicked.connect(self.on_go)

        main_l.addLayout(control_l) # add canvas & controls, left
        main_l.addLayout(model_l) # add model-specific controls, right

        control_l.addWidget(self.canvas) # add canvas
        control_l.addLayout(buttons_l) # add main control layout

        model_l.addLayout(choose_model_l) # add model chooser to controls
        # add model/color selection to model chooser
        choose_model_l.addWidget(model_label, 0, 0)
        choose_model_l.addWidget(model_drop, 0, 1)
        choose_model_l.addWidget(color_label, 1, 0)
        choose_model_l.addWidget(color_drop, 1, 1)

        # add widgets for individual models
        for widget in self.menus.values():
            model_l.addWidget(widget)

        # add buttons to controls
        buttons_l.addWidget(random_b)
        buttons_l.addWidget(restart_b)
        buttons_l.addWidget(reset_b)
        buttons_l.addWidget(clear_b)
        buttons_l.addWidget(save_b)
        buttons_l.addWidget(go_b)

        self.setCentralWidget(main_w)

        self.change_widget()

    def clear_screen(self):
        ''' Clears the canvas. '''
        self.canvas.clear()

    def on_restart(self):
        ''' Restarts model at depth 0 (how far it is in drawing). This will
        allow the user to restart the drawing of a model after stopping it
        mid-drawing. '''
        if self.model is not None:
            self.model.depth = 0

    def on_reset(self):
        ''' Resets all customizable settings for the current model. '''
        if self.model is not None:
            self.model.reset()

    def on_randomize(self):
        ''' Randomizes the customizable settings of the current model, if the
        model has randomization implemented. '''
        try:
            self.model.randomize()
        except:
            print("This model cannot be randomized.")

    def on_go(self):
        ''' Restarts the drawing progress of the current model, clears the
        canvas, and starts the model generating/drawing. '''
        if self.model is not None:
            print("Go!")
            self.on_restart()
            self.clear_screen()
            self.model.go()
        else:
            print("No model selected!")

    def save_image(self):
        ''' Opens a file saving dialog and saves the current canvas image to the
        chosen file. '''
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self,"Save File","","Image files (*.jpeg *.jpg *.gif *.png *.JPEG *.JPG *.GIF *.PNG)", options=options)
        if file_name:
            pixels = self.canvas.pixmap()
            s = pixels.save(file_name)
        if s:
            print("Image saved as %s" % file_name)
        else:
            print("Error saving %s" % file_name)

    def load_models(self):
        ''' For each model name listed in the __init__ method of this class,
        the model is imported from the "objects" folder and an instance of it is
        created. The same instances will be reused throughout the program, and
        the "model" attribute of this class will indicate which one is in use.
        '''
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
        ''' For each model name listed in the __init__ method of this class,
        a QWidget is created. Then, the init_menu_layout function is called on
        the model to set the layout (buttons, text, controls) of the widget for
        that model. If the model was not imported successfully or does not have
        an init_menu_layout function, an empty panel will be displayed. '''
        menus = {}
        for name in self.model_names:
            widget = QWidget()
            menus[name] = widget
            try:
                model = self.models[name]
                widget.setLayout(model.init_menu_layout())
            except:
                empty = QVBoxLayout()
                empty.addWidget(QLabel("No settings found"))
                widget.setLayout(empty)
                print("No settings menu found for model %s" % name)
        return menus

    def change_model(self, model_name):
        ''' Changes the current active model according to the name selected, and
        updated the model-specific settings display. '''
        print("Model changed to %s" % model_name)
        self.curr_model = model_name
        self.model = self.models.get(model_name, None)
        self.change_widget()

    def change_widget(self):
        ''' Looks through the dictionary of model names and setting panel
        widgets to find the widget matching the current model, makes it visible
        while hiding all others. '''
        for name, widget in self.menus.items():
            if name == self.curr_model:
                widget.show()
            else:
                widget.hide()

    def change_color(self, name):
        ''' Changes the canvas' background color according to the drop-down
        selection, and clears the canvas to update it. '''
        c = self.canvas.colors[name]
        self.canvas.bg_color = QtGui.QColor(c)
        self.clear_screen()

if __name__ == "__main__":

    app = QApplication([]) # create the application
    screen_res = app.desktop().screenGeometry() # get screen size
    window = MainWindow(screen_res) # create the main window
    window.show() # display the window
    sys.exit(app.exec_()) # run the main event loop
