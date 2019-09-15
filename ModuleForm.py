from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QGroupBox ,QPushButton, QWidget, QVBoxLayout
from Input import Input
import json
from collections import defaultdict
from InputGraph import InputGroup
class ModuleForm(QMainWindow):
    def __init__(self, parent, dic = defaultdict(lambda: {}),folder = ''):
        self.folder = folder
        super().__init__(parent)
        self.setMinimumSize(700, 400)
        self.setWindowTitle("Module editor")
        main_window = QWidget(self)
        self.setCentralWidget(main_window)
        self.lay = QVBoxLayout()
        main_window.setLayout(self.lay)

        self.o = {}
        self.input_o = {}

        self.o['module name'] = dic['name'] or 'newModule'
        self.o['code'] = dic['code'] or ''
        self.o['active'] = dic['active']

        self.o['views'] = {} or dic['views']

        inputs_group = QGroupBox(self)
        inputs_lay = QVBoxLayout()
        inputs_group.setLayout(inputs_lay)

        Input(self, 'string', 'module name')
        Input(self, 'bool', 'active')

        add_input_btn = QPushButton('add input')
        add_input_btn.clicked.connect(self.add_input)
        add_input_btn.setIcon(QtGui.QIcon('assets/icons/add.png'))
        self.lay.addWidget(add_input_btn)

        add_view_btn = QPushButton('add view')
        add_view_btn.clicked.connect(self.add_view)
        add_view_btn.setIcon(QtGui.QIcon('assets/icons/view.png'))
        # self.lay.addWidget(add_view_btn)

        save_btn = QPushButton('save')
        save_btn.clicked.connect(self.save)
        save_btn.setIcon(QtGui.QIcon('assets/icons/save.png'))
        self.lay.addWidget(save_btn)
        for input_i in dic['keys']:
            Input(self, 'group', None, {'add_delete': True, 'o': self.input_o, 'group_type':'input_definer', 'input_definer_values': input_i})


        Input(self, 'texteditor', 'code')

        h = {
            'string': {
                'string': ['string', 'code']
            },
            'graph':
                {
                    'title': 'string',
                    'func': {
                        'xy': 'code',
                    },
                    'hist': {
                        'data': 'code'
                    }
                },
            'image':
                {
                    'images': ['string', 'code'],
                    'add toolbar': 'bool'
                }

        }

        self.g = InputGroup(self, 'views', h, opts={'o': self.o['views']})

    def add_input(self):
        Input(self, 'group', None,
              {'add_delete': True, 'o': self.input_o, 'group_type': 'input_definer'})


    def add_view(self):
        Input(self, 'group', None,
              {'add_delete': True, 'o': self.views_o, 'general_name': 'view', 'group_type': 'view_definer'})

    def save(self):
        name = self.o['module name']
        keys = [list(v.values()) for _, v in self.input_o.items()]
        with open(self.folder + name, 'w') as outfile:
            json.dump({'name': name, 'keys': keys, 'views': self.o['views'], 'code': self.o['code'], 'active': self.o['active']}, outfile)
        self.parent().load_from_path()
        self.parent().parent().parent().reload()