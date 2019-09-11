from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
import sys
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QMainWindow, QHBoxLayout,QVBoxLayout, QGridLayout, QDialog
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
import sys
import datetime
from moduleGUI import ModuleGui
from PyQt5.QtGui import QPainter, QBrush, QPen
import PyQt5.QtCore
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

from PyQt5.QtWidgets import QApplication, QMainWindow
from Input import Input
from PyQt5.QtWidgets import QFileDialog

# exec(open("/home/aviv/avivsroot/lib/aviv_root.py").read())
from PyQt5.QtWidgets import (QMessageBox)
from PyQt5.QtWidgets import QMainWindow, QAction
from PyQt5.QtWidgets import (QApplication, QCheckBox,
                             QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QSizePolicy,
                             QSpinBox, QTableWidget,
                             QVBoxLayout, QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from modules.Module import Module
from PyQt5.QtGui import QPainter, QColor, QBrush
class SandBox(QGroupBox):
    def __init__(self):

        super().__init__()
        # self.setStyleSheet("""
        #     .QWidget{
        #         border: 5px solid black;
        #
        #         background-color: black;
        #         /* background-image: url('./bg.jpg');*/
        #     }
        # """)
        self.gui_modules = []
        self.paints = []
        self.starter = None


    def add_module(self, klass, relative_loc = None, xy = None):
        gm = ModuleGui(self, klass)

        if xy:
            gm.move(xy[0], xy[1])
        else:
            x1, y1 = relative_loc.x(), relative_loc.y()
            r1, r2 = self.x(), self.y()
            gm.move(x1 - r1, y1 - r2)
        gm.resize(220, 220)
        gm.show()
        self.gui_modules.append(gm)
        return gm

    def update_connections(self):
        self.last = datetime.datetime.now()
        right_module_gui = None
        left_module_gui = None

        for m in self.gui_modules:
            if m.right.on:
                right_module_gui = m

                if right_module_gui.module.next_node:
                    right_module_gui.module.next_node = None
                    right_module_gui.reset_on_of()
                    return
            if m.left.on:
                left_module_gui = m
        if right_module_gui and left_module_gui and right_module_gui != left_module_gui:

            right_module_gui.module.next_node = left_module_gui.module
            self.paints.append([right_module_gui.x(),right_module_gui.y(),left_module_gui.x(),left_module_gui.y()])
            for m in self.gui_modules:
                m.reset_on_of()


    def file_path(self):
        return self.parent().parent().toolbar.file_path_input.text()

    def load_modules_from_file(self, path = None):
        modules = Module.load_from_file(path or self.file_path())
        for m in modules:
            self.add_module(m, xy = m.gui_props)

    def save_modules_to_file(self, path = None):
        modules = []
        for gm in self.gui_modules:
            m = gm.module
            m.gui_props = [gm.x, gm.y]
            modules.append(m)
        Module.save_to_file(modules, path or self.file_path())

    def update_starter(self, starter):

        import inspect
        print('222222222222')
        starter.module.process()
        print('222222222222')
        print(inspect.getsource(starter.module.process))
        self.starter = starter
        # print(self.starter.data)
        for m in self.gui_modules:
            m.set_sarter(self.starter == m)

    def clear_all_modules(self, force = False):
        buttonReply = force or QMessageBox.question(self, 'Clear sandbox', "Are you sure that you want to delete all modules?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            for mg in self.gui_modules:
                mg.setParent(None)
            self.gui_modules = []

    def paintEvent(self, *args, **kwargs):
        qp = QPainter()
        qp.begin(self)
        # print(datetime.datetime.now())
        # if datetime.datetime.now().timestamp() - self.last.timestamp() < 10:
        for gm in self.gui_modules:
            gm.center()
            if gm.module.next_node:

                # print(gm.module.next_node.gui)
                next_gm = gm.module.next_node.gui
                if next_gm:
                    a = gm
                    b = next_gm
                    ac = gm.center()
                    bc = gm.center()
                    acc = next_gm.closest_to(gm.center(), side=True)
                    bcc = gm.closest_to(next_gm.center(), side=False)


                    line = bcc[0], bcc[1], acc[0], acc[1]

                    qp.drawLine(*line)
                    # line = bcc[0], bcc[0], acc[0], acc[0]
                    # qp.setPen(QColor(168, 34, 3))
                    # qp.drawLine(*line)
                    # print([gm.x()+ 120, gm.y()+ 120, next_gm.x()+120, next_gm.y()+ 120])
                    self.update()
    def force_stater(self):
        print(map(lambda m: m.module.next_node, self.gui_modules))
        m = [m for m in self.gui_modules if m.module not in map(lambda m: m.module.next_node, self.gui_modules)][0]
        self.update_starter(m)

    def save_to_jpg(self):
        self.grab().save('sandbox.png')
