from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QListWidget, QGridLayout, QDialog, QMainWindow ,QPushButton, QScrollArea, QDesktopWidget, QLabel, QDialogButtonBox, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QApplication, QSpinBox,QCheckBox,QFileDialog
from functools import partial
from Input import Input
from ModuleForm import ModuleForm
import os
import pickle
class ModulesManager(QMainWindow):
    def __init__(self, parent, name = False, inputs = []):
        super().__init__(parent)
        self.setWindowTitle("Modules Manager")
        main_window = QWidget(self)
        self.setCentralWidget(main_window)

        self.setMinimumSize(300, 100)
        self.lay = QHBoxLayout()
        main_window.setLayout(self.lay)







        self.files = QListWidget()
        self.files.itemDoubleClicked.connect(self.load_data)
        self.lay.addWidget(self.files)
        btn = QPushButton('open folder')
        btn.clicked.connect(self.openFolder)
        self.lay.addWidget(btn)
        self.openFolder('m')

        btn = QPushButton('new')
        btn.clicked.connect(self.new_module)
        self.lay.addWidget(btn)


    def openFolder(self, forcePath=None):
            if forcePath not in (None, False):
                    self.dic = forcePath
                    path = self.dic
            else:
                    path = QFileDialog.getExistingDirectory(None, 'Select Directory')
                    self.dic = path
            self.load_from_path()

    def load_from_path(self):
        path = self.dic
        fls = []
        for f in os.listdir(path):
            if not os.path.isdir(path+'/'+f):
                fls.append(f)
        self.files.clear()
        self.files.addItems(sorted(fls))


    def load_data(self):
        name = self.files.selectedItems()[0].text()
        p = self.dic+'/' + name

        with open(p, 'rb') as handle:
            b = pickle.load(handle)
            if 'views' not in b:
                b['views'] = []
        m = ModuleForm(self, b['name'], b['keys'], b['views'], b['code'], folder=self.dic+'/')
        m.show()

    def new_module(self):
        m = ModuleForm(self, folder=self.dic + '/')
        m.show()
