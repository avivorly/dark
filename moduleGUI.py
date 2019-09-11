from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPalette
import sys
from functools import partial
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication, QMainWindow, QHBoxLayout,QVBoxLayout, QGridLayout, QDialog, QFrame
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
import sys
# from modal import InvoiceModal
from PyQt5.QtGui import QPainter, QBrush, QPen
import PyQt5.QtCore
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

from PyQt5.QtWidgets import QApplication, QMainWindow

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
from ModuleInputForm import ModuleInputForm
import inspect
class ModuleGui(QGroupBox):
    def __init__(self, parent, module):
        self.sand = parent
        super().__init__(parent)
        self.next_node = None
        self.line = None
        if inspect.isclass(module):

            self.module = module()
        else:
            self.module = module
        self.module.gui = self
        self.initUI()

    def initUI(self):
        mainlay = QHBoxLayout()
        mainlay.setContentsMargins(0, 0, 0, 0)
        # self.setContentsMargins(0, 0, 0, 0)

        mainlay.setSpacing(0)
        # mainlay.setMargin(0)
        self.setLayout(mainlay)
        self.right = QPushButton()
        self.left = QPushButton()
        # self.right.setStyleSheet("background-color:rgb(239,193,158);")
        # self.left.setStyleSheet("background-color:rgb(116,138,123);")




        for q in [self.left,self.right]:
            q.setFixedWidth(15)
            q.setStyleSheet("background-color:white;")
            q.on = False
            q.clicked.connect(partial(self.on_of, q))

        g = QGroupBox()
        self.g = g
        al = QVBoxLayout()
        g.setLayout(al)

        mainlay.addWidget(self.left)
        mainlay.addWidget(g)
        mainlay.addWidget(self.right)

        # a.setLayout(loadLay)

        laybel = QLabel(self.module.__class__.__name__)
        al.addWidget(laybel)
        q = QPushButton('Edit')
        q.clicked.connect(self.open_form)
        al.addWidget(q)
        # color = a.palette().color(QPalette.Window)
        # color.setRed(100)

        # print(color.getRgbF())

        self.resize(20, 20)
        self.show()

    def on_of(self, side, force_off = False):
        if force_off:
            side.on = False
        else:
            side.on = not side.on
        if side.on:
            color='black'
        else:
            color='white'
        side.setStyleSheet("background-color:{0};".format(color))
        if not force_off:
            self.sand.update_connections()

    def reset_on_of(self):
        for side in [self.right, self.left]:
            self.on_of(side, force_off=True)

    def mousePressEvent(self, event):
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self.__mouseMovePos
            newPos = self.mapFromGlobal(currPos + diff)

            parent_height = self.parent().height()
            parent_width = self.parent().width()
            # if globalPos.x() > parent_width * .95 or globalPos.y() > parent_height * .95 or globalPos.x() < parent_width * .05 or globalPos.y() < parent_height * .05:
            #     return

            self.move(newPos)
            self.__mouseMovePos = globalPos

    def mouseDoubleClickEvent(self, event):
        self.sand.update_starter(self)


    def set_sarter(self, flag):
        if flag:
            color = 'blue'
        else:
            color = 0
        for item in [self, self.g]:
            item.setStyleSheet("background-color:{0};".format(color))

    def open_form(self):
        # print(table.text())
        modul_form = ModuleInputForm(self, self.module.keys, self.sand)
        res = modul_form.show()
        # if res == QDialog.Accepted:
        #     print("ok")
        # else:
        #     # table.deleteLater()
        #     print("ABORT!")
    def center(self):
        x1 = self.x()
        x2 = x1 + self.width()
        y1 = self.y()
        y2 = y1 + self.height()
        return [(x2 + x1)/2, (y2 + y1)/2]

    def closest_to(self, xy, side = True):
        lx, ly = xy
        sx, sy = self.center()
        a = sx - lx
        b = sy - ly
        if True:#abs(a) > abs(b):
            y = sy + 9
            if side:#a > 0:
                x = self.x()
            else:
                x = self.x() + self.width()
        else:
            x = sx
            if b > 0:
                y = self.y() + 20
            else:
                y = self.y() + self.height()
        return [x, y]

