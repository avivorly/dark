from PyQt5 import QtCore
from PyQt5.QtWidgets import QGridLayout, QDialog, QMainWindow ,QPushButton, QScrollArea, QDesktopWidget, QLabel, QDialogButtonBox, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QApplication, QSpinBox,QCheckBox,QFileDialog
from functools import partial


class ModuleInputForm(QMainWindow):
    def __init__(self, gui_modul, keys, parent):
        self.gui_modul = gui_modul
        super().__init__(parent)
        self.first = True
        self.initUI(keys)

    def open_file(self):
        if not self.first:
            self.file_path = QFileDialog.getOpenFileName(self)
            self.first = True
            self.path_line_edit.setText(self.file_path[0])
            self.save()
        self.first = False

    def initUI(self, keys):
        main_window = QWidget(self)
        self.setCentralWidget(main_window)

        self.setMinimumSize(300, 100)
        lay = QGridLayout()
        main_window.setLayout(lay)
        row = 0
        inputs = []
        self.setts = {}
        for name, soog in keys:
            module_o = self.gui_modul.module.o
            lay.addWidget(QLabel(name), row, 0)
            if soog == 'spin':
                w = QSpinBox()
                w.setRange(-2147483648, 2147483647)
                w.valueChanged.connect(self.save)

            if soog == 'str':
                w = QLineEdit()
                w.textChanged.connect(self.save)

            if soog == 'file':
                w = QLineEdit('open file')
                self.path_line_edit = w
                # print(dir(w))
                w.textChanged.connect(self.open_file)


            self.setts[name] = w
            inputs.append(w)
            lay.addWidget(w, row ,1)

            row = row + 1

            for name, w in self.setts.items():
                if name in module_o.keys():
                    method = 'setValue'
                    mdic = {
                        QCheckBox: 'setChecked',
                        QLineEdit: 'setText'
                    }
                    if type(w) in mdic.keys():
                        method = mdic[type(w)]
                    eval('w.{0}(module_o[name])'.format(method))
    def get_value_from_widget(self, w):
        method = 'value'
        mdic = {
            QCheckBox: 'isChecked',
            QLineEdit: 'text'
        }
        if type(w) in mdic.keys():
            method = mdic[type(w)]
        return eval('w.{0}()'.format(method))
    def save(self):
        app = self.parent().parent().parent()
        if app.live_mode:
            app.start_process()
        for k,v in self.setts.items():
            print(v)
            self.gui_modul.module.o[k] = self.get_value_from_widget(v)

