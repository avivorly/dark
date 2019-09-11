from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QMainWindow, QHBoxLayout,QVBoxLayout, QGridLayout, QDialog
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
import sys, pkgutil
from functools import partial
from PyQt5.QtGui import QPainter, QBrush, QPen
import PyQt5.QtCore

from PyQt5.QtCore import Qt
from PyQt5 import QtGui

from PyQt5.QtWidgets import QApplication, QMainWindow

from PyQt5.QtWidgets import QFileDialog

# exec(open("/home/aviv/avivsroot/lib/aviv_root.py").read())
from PyQt5.QtWidgets import (QMessageBox)
from PyQt5.QtWidgets import QMainWindow, QAction, QToolBar
from PyQt5.QtWidgets import (QApplication, QCheckBox,
                             QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QSizePolicy,
                             QSpinBox, QTableWidget,
                             QVBoxLayout, QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtGui import QIcon

# from ModuleBtn import ModuleBtn
from sandbox import SandBox
from ResultView import ResultView
# from moduleGUI import ModuleGui
# from modal import InvoiceModal
from ModuleBtn import ModuleBtn
from ModulesManager import ModulesManager

from ModuleInputForm import ModuleInputForm

class ToolBar(QToolBar):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        sand = parent.sandbox
        sand.toolbar = self
        self.btns = {}
        # TODO setCheckable insdead of disabled
        for action, connect_to in [  # TODO add key shortcut
            ['save', sand.save_modules_to_file],
            ['load', sand.load_modules_from_file],
            ['clear', sand.clear_all_modules],
            ['start', sand.parent().parent().start_process],
            ['path', None],
            ['open_file', self.set_path_from_user],
            ['image_save', sand.save_to_jpg],
            ['one_window', self.one_window],
            ['two_windows', self.two_windows],
            ['live_mode', self.live_mode],
            ['simple_mode', self.simple_mode],
            ['ModulesManager', self.modules_manager],
        ]:
            if action not in ['path']:
                btn = QAction(QIcon("assets/icons/{0}.png".format(action)), action, self)
                btn.setStatusTip(action)
                btn.triggered.connect(connect_to)
                self.addAction(btn)

            else:
                self.file_path_input = QLineEdit()
                self.file_path_input.setText('filename.pickle')
                self.addWidget(self.file_path_input)
                btn = self.file_path_input
            self.btns[action] = btn


    def set_path_from_user(self):
        self.file_path_input.setText(QFileDialog.getOpenFileName(self)[0])

    def one_window(self):
        self.parent().outer_window = False
        self.btns['one_window'].setDisabled(True)
        self.btns['two_windows'].setDisabled(False)
    def two_windows(self):
        self.parent().outer_window = True
        self.btns['two_windows'].setDisabled(True)
        self.btns['one_window'].setDisabled(False)
    def live_mode(self):
        self.parent().live_mode = True
        self.btns['live_mode'].setDisabled(True)
        self.btns['simple_mode'].setDisabled(False)
    def simple_mode(self):
        self.parent().live_mode = False
        self.btns['live_mode'].setDisabled(False)
        self.btns['simple_mode'].setDisabled(True)

    def modules_manager(self):
        m = ModulesManager(self)
        m.show()






