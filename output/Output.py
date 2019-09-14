from PyQt5 import QtCore, QtGui

from PyQt5.QtWidgets import (QPlainTextEdit, QFileDialog, QComboBox ,QApplication, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QSpinBox, QWidget)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from ResultToolbar import ResultToolbar
from PyQt5.QtWidgets import (
                             QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QSizePolicy,
                             QSpinBox, QTableWidget,
                             QVBoxLayout, QWidget)

class OutputGraph(FigureCanvas):
    def __init__(self,parent, opts={}):
        self.opts = opts

        for plot in opts['plots']:
            fig = Figure(figsize=(9, 4), dpi=50)
            FigureCanvas.__init__(self, fig)
            self.setParent(parent)
            FigureCanvas.setSizePolicy(self, \
                                       QSizePolicy.Expanding,
                                       QSizePolicy.Expanding)
            FigureCanvas.updateGeometry(self)
            ax = self.figure.add_subplot(111)
            ax.plot(plot['xs'], plot['ys'], ro)
            self.draw()













        # self.ax.set_xlim(vmin, vmax)

