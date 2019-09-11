from PyQt5 import QtCore
from PyQt5.QtWidgets import QGridLayout, QDialog, QPushButton, QScrollArea, QDesktopWidget, QLabel, QDialogButtonBox, \
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QApplication, QSpinBox, QCheckBox, QGroupBox, QMainWindow
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from functools import partial
import numpy as np
from ResultToolbar import ResultToolbar
from PyQt5.QtWidgets import (QApplication, QCheckBox,
                             QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QSizePolicy,
                             QSpinBox, QTableWidget,
                             QVBoxLayout, QWidget)
from PyQt5.QtGui import QIcon, QScreen, QPixmap
class Graph(FigureCanvas):
    def __init__(self,parent, xys, width=9, height=4, dpi=50):
        xs = xys[0]
        ys = xys[1]
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, \
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        ax = self.figure.add_subplot(111)

        # self.ax.set_xlim(vmin, vmax)

        ax.plot(xs, ys, 'ro')
        self.draw()


class Image(FigureCanvas):
    def __init__(self,parent, images,width=9, height=4, dpi=50):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.axArr = self.figure.subplots(1, len(images))

        if len(images) == 1:
            for i in range(0, len(images)):
                ax = self.axArr
                ax.axis('off')
                ax.imshow(images[i], cmap='hot')

        else:
            for i in range(0, len(images)):
                ax = self.axArr[i]
                ax.axis('off')
                ax.imshow(images[i], cmap='hot')


        self.figure.tight_layout()
        self.draw()

class ResultView(QWidget):
    def __init__(self, extras, parent):
        # self.gui_modul = gui_modul
        super().__init__(parent)
        self.initUI(extras)

    def initUI(self, extras):
        main_lay = QVBoxLayout()
        self.setLayout(main_lay)

        # toolbar

        self.toolbar = ResultToolbar(self)
        # toolbar.setIconSize(QSize(16, 16))
        main_lay.addWidget(self.toolbar)

        for extra in extras:
            name = extra['name']
            data = extra['data']
            views = extra['views']

            extra_box = QGroupBox(name)

            lay = QGridLayout()
            extra_box.setLayout(lay)
            main_lay.addWidget(extra_box)
            row = 0
            for name, type, value in views:
                lay.addWidget(QLabel(name), row, 0)
                if type == 'string':
                    lay.addWidget(QLabel(value), row, 1)
                if type == 'number':
                    lay.addWidget(QLabel(str(value)), row, 1)
                if type == 'graph':
                    lay.addWidget(Graph(extra_box ,value), row, 1)
                if type == 'image':
                    lay.addWidget(Image(extra_box, value), row, 1)

                row += 1

    def save_to_jpg(self):
        self.grab().save('results.jpg')

