from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QGridLayout, QDialog, QMainWindow ,QPushButton, QScrollArea, QDesktopWidget, QLabel, QDialogButtonBox, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QApplication, QSpinBox,QCheckBox,QFileDialog
from functools import partial
from Input import Input
# import pickle
import json
class ModuleForm(QMainWindow):
    def __init__(self, parent, name = False, inputs = [], views = [], code = '', folder = ''):
        self.folder = folder
        super().__init__(parent)
        self.setWindowTitle("Module editor")
        self.input_h = {}
        self.input_v = {}
        main_window = QWidget(self)
        self.setCentralWidget(main_window)

        self.setMinimumSize(700, 400)
        self.lay = QVBoxLayout()
        main_window.setLayout(self.lay)
        self.o = {}

        self.o['module name'] = name or 'new Module'
        self.o['code'] = code or ''

        Input(self, 'string', 'module name')

        add_input_btn = QPushButton('add input')
        add_input_btn.clicked.connect(self.add_input)
        add_input_btn.setIcon(QtGui.QIcon('assets/icons/add.png'))
        self.lay.addWidget(add_input_btn)

        add_view_btn = QPushButton('add view')
        add_view_btn.clicked.connect(self.add_view)
        add_view_btn.setIcon(QtGui.QIcon('assets/icons/view.png'))
        self.lay.addWidget(add_view_btn)

        save_btn = QPushButton('save')
        save_btn.clicked.connect(self.save)
        save_btn.setIcon(QtGui.QIcon('assets/icons/save.png'))
        self.lay.addWidget(save_btn)
        for input_i in inputs:
            Input(self, 'group', None, {'add_delete': True, 'o': self.input_h, 'group_type':'input_definer', 'input_definer_values': input_i})

        for input_v in views:
            Input(self, 'group', None, {'add_delete': True, 'o': self.input_v, 'general_name': 'view', 'group_type':'view_definer', 'input_definer_values': input_v})

        Input(self, 'texteditor', 'code')



    def add_input(self):
        Input(self, 'group', None,
              {'add_delete': True, 'o': self.input_h, 'group_type': 'input_definer'})


    def add_view(self):
        Input(self, 'group', None,
              {'add_delete': True, 'o': self.input_v, 'general_name': 'view', 'group_type': 'view_definer'})


    def save(self):
        name = self.o['module name']
        print(self.input_h)
        # keys = [[] for _,v in self.input_h.values()]
        keys = [list(v.values()) for _, v in self.input_h.items()]

        views = [list(v.values()) for _, v in self.input_v.items()]
        with open(self.folder + name, 'w') as outfile:
            json.dump({'name': name, 'keys': keys, 'views': views, 'code': self.o['code']}, outfile)

        self.parent().load_from_path()
        self.parent().parent().parent().reload()






