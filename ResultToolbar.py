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
# from sandbox import SandBox
# from moduleGUI import ModuleGui
# from modal import InvoiceModal
from ModuleBtn import ModuleBtn
from ModuleInputForm import ModuleInputForm

class ResultToolbar(QToolBar):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)


        for action, connect_to in [
            ['image_save', self.save_to_jpg]
        ]:
            if action not in ['path']:
                btn = QAction(QIcon("assets/icons/{0}.png".format(action)), action, self)
                btn.setStatusTip(action)
                btn.triggered.connect(connect_to)
                # button_action.setCheckable(True)
                self.addAction(btn)
            else:
                self.file_path_input = QLineEdit()
                self.file_path_input.setText('filename.pickle')
                self.addWidget(self.file_path_input)


    def save_to_jpg(self):
        self.hide()
        self.parent().save_to_jpg()
        self.show()




