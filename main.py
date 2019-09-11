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
from modules.Module import Module
# from ModuleBtn import ModuleBtn
from sandbox import SandBox
from ResultView import ResultView
# from moduleGUI import ModuleGui
# from modal import InvoiceModal
from ModuleBtn import ModuleBtn
from toolbar import ToolBar
from ModuleInputForm import ModuleInputForm
from ModuleForm import ModuleForm
class AfelApp(QMainWindow):
    def __init__(self, parent=None):
        super(AfelApp, self).__init__(parent)
        # self.setStyleSheet("""re
        #     .QWidget{
        #         border: 5px solid black;
        #
        #         background-color: gray;
        #         /* background-image: url('./bg.jpg');*/
        #     }
        # """)
        self.setGeometry(10, 10, 1000, 1200)
        self.init_UI()
        # m = ModuleForm(self)
        # m.show()

    def init_UI(self):

        self.outer_window = True
        self.result_box = None
        self.result_box_group = None
        self.live_mode = False
        self.module_btns = []
        mainWindow = QWidget(self)
        self.setCentralWidget(mainWindow)
        mainlay = QHBoxLayout()
        self.mainlay = mainlay
        mainWindow.setLayout(mainlay)

        #  load area
        loadbox = QGroupBox()

        loadLay = QVBoxLayout()

        loadLay.addStretch(1)

        self.loadLay = loadLay

        loadbox.setLayout(loadLay)

        self.load_modules_btns()

        startbtn = QPushButton('start process')
        startbtn.clicked.connect(self.start_process)
        loadLay.addWidget(startbtn)



        #  sandbox area
        self.sandbox = SandBox()
        self.sandboxlay = QVBoxLayout()
        self.sandboxlay.addStretch(209)
        self.sandbox.setLayout(self.sandboxlay)

        # self.sandbox.seth


        mainlay.addWidget(loadbox,1)
        mainlay.addWidget(self.sandbox,10)

        self.setMouseTracking(True)

        # toolbar

        self.toolbar = ToolBar(self)
        # toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(self.toolbar)

    def load_modules_btns(self):
        self.clear_modules_btns()

        for m in Module.get_all_modules():

            # if m.__name__ is 'One':
            #     import inspect
            #     print ( 'One new code is' * 10)
            #     prin t(inspect.getsource(m.process))

            mdlbtn = ModuleBtn(m.__name__, m)
            self.loadLay.insertWidget(0, mdlbtn)
            self.module_btns.append(mdlbtn)

    def clear_modules_btns(self):
        for m in self.module_btns:
            m.setParent(None)

        # self.load_modules_btns()

    def reload(self):
        temp_path = 'm/temp/temporaryModules'
        # print()
        self.sandbox.save_modules_to_file(temp_path)
        self.clear_modules_btns()
        self.load_modules_btns()
        self.sandbox.clear_all_modules(force = True)
        self.sandbox.load_modules_from_file('m/temp/temporaryModules')

    def start_process(self):
        if self.result_box_group:
            self.result_box_group.deleteLater()
            self.result_box_group = None
        self.old_box = self.result_box
        starter = self.sandbox.starter
        if starter:
            extras = starter.module.run()
            self.result_box = ResultView(extras, self)
            if self.outer_window:
                w = QMainWindow(self)
                w.setCentralWidget(self.result_box)
                w.show()
            else:
                g = QGroupBox()
                gl = QHBoxLayout()
                g.setLayout(gl)
                gl.addWidget(self.result_box)
                self.result_box_group = g
                self.mainlay.addWidget(g,5)

        else:
            self.statusBar().showMessage('please define starter', 2000)
            self.sandbox.force_stater()
            self.start_process()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F5:
            self.start_process()
        if event.key() == Qt.Key_F4:
            self.sandbox.load_modules_from_file()


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    win = AfelApp()
    # win.showMaximized()
    win.show()
    app.exec_()

if __name__ == '__main__':
    sys.exit(main())

#  TODO Qt Quick Controls 2 check it