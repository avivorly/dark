from PyQt5 import QtCore, QtGui

from PyQt5.QtWidgets import (QVBoxLayout, QPlainTextEdit, QFileDialog, QComboBox ,QApplication, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QGroupBox, QSpinBox, QWidget)
# TODO  create also oo hash that saves all needed data, so [o,oo] contains all need to save an open anything
class AWidget(QWidget):
    def __init__(self, parent, opts = {}):
        super().__init__(parent)
        self.opts = opts
        if 'vertical' in opts:
            lay = QVBoxLayout()
        else:
            lay = QHBoxLayout()
        self.setLayout(lay)

        self.o = opts['o'] if 'o' in opts else self.parent().o

    def force_name(self, name):
        general_name = self.opts['general_name'] if 'general_name' in self.opts else 'input'

        if not name:
            i = 1
            while '{0}: {1}'.format(general_name, i) in self.o:
                i += 1
            name = '{0}: {1}'.format(general_name, i)
        return name

    def present(self):

        self.show()
        if hasattr(self.parent(), 'lay'):
            l = self.parent().lay
        else:
            l = self.parent().layout()

        if 'index' in self.opts:
            l.insertWidget(self.opts['index'], self)
        else:
            l.addWidget(self)



