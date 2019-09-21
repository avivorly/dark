from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QPlainTextEdit, QFileDialog, QComboBox, QApplication, QHBoxLayout, QLabel, QLineEdit,
                             QCheckBox,
                             QPushButton, QSpinBox, QWidget, QColorDialog)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
# TODO  create also oo hash that saves all needed data, so [o,oo] contains all need to save an open anything

from AWidget import AWidget
from codeeditor import QCodeEditor

class Input(AWidget):
    def __init__(self, parent, tp, name='', opts={}):
        super().__init__(parent, opts)

        self.opts = opts
        self.tp = tp
        self.my_parent = parent  # try self.parent()

        value = name in self.o and self.o[name]

        self.name = self.force_name(name)
        if not ('hide name' in opts and opts['hide name']):
            self.layout().addWidget(QLabel(self.name))

        if tp in ['string', 'python', 'code']:
            value = value or ''
            func_name, w = ['textChanged', QLineEdit(value)]
        if tp == 'texteditor':
            value = value or ''
            func_name, w = ['textChanged', QCodeEditor(value)]
        if tp == 'integer':
            value = value or 0
            func_name, w = ['valueChanged', QSpinBox()]
            w.setRange(-2147483648, 2147483647)  # TODO add expression for max value
            w.setValue(value)
        if tp == 'color':
            value = value or '#aaaaaa'
            func_name, w = ['textChanged', QLineEdit(value)]
            b = QPushButton('Pick Color')
            self.layout().addWidget(b)
            b.setStyleSheet(f'background-color: {value}')
            b.clicked.connect(lambda: w.setText(QColorDialog().getColor().name()))
            b.clicked.connect(lambda: b.setStyleSheet(f'background-color: {w.text()}'))
        if tp == 'bool':
            value = value or 0
            func_name, w = ['stateChanged', QCheckBox()]
            w.setChecked(value)
        if tp == 'file':
            value = value or ''
            func_name, w = ['textChanged', QLineEdit(value)]
            b = QPushButton('Openn File')
            self.layout().addWidget(b)
            b.clicked.connect(lambda: w.setText(QFileDialog.getOpenFileName(self)[0]))
        if tp in ['select', 'type']:
            if tp == 'type':
                opts['group'] = ('group' in opts and opts['group']) or 'general input'

            groups = {
                'general input': ['string', 'python', 'file', 'integer', 'color']
            }

            func_name, w = ['currentTextChanged', QComboBox()]

            if 'allowed types' in opts:
                at = opts['allowed types']
                if type(at) == str:
                    types = [at]
                else:
                    types = at
            else:
                types = groups[opts['group']]
            [w.addItem(t) for t in types]

            value = value or w.itemText(0)

            index = w.findText(value, QtCore.Qt.MatchFixedString)
            w.setCurrentIndex(index)

        if tp == 'group':
            groups_types = {
                'view_definer': ['title', 'type', 'view data'],
                'input_definer': ['name', 'type', 'value'],
                'h': ['type', 'value']
            }

            hide_name = opts['group_type'] == 'h'

            titles = groups_types[opts['group_type']]
            w = False
            if not value:
                value = {}
                self.o[self.name] = value
            if 'input_definer_values' in opts:
                idv = opts['input_definer_values']

                if type(idv) == list:
                    for i in range(0, len(idv)):
                        value[titles[i]] = idv[i]
                else:  # hash
                    for k, v in idv.items():
                        value[k] = v

            save_until_next = None
            for i in range(0, len(titles)):
                title = titles[i]
                if title is 'type':

                    temp_opts = {'o': value, 'group': 'general input', 'hide name': hide_name}
                    if 'allowed types' in opts:
                        temp_opts['allowed types'] = opts['allowed types']

                    save_until_next = Input(self, 'type', title, temp_opts)
                    #
                    # itle is 'type':
                    # h = {'o': value, 'group': 'general input', 'hide name': hide_name}
                    # if 'allowed types' in opts:
                    #     alwtps = opts['allowed types']
                    #
                    # save_until_next = Input(self, 'select', title, )


                else:
                    if not save_until_next:
                        input = Input(self, 'string', title, {'o': value})
                    else:

                        if 'type' in value:
                            generic_name = value['type']
                        else:
                            generic_name = 'string'

                        input = Input(self, generic_name, title, {'o': value, 'hide name': hide_name})

                        save_until_next.opts['call_on_update'] = input.transform
                        save_until_next = None
        if w:
            self.w = w
            self.layout().addWidget(w)
            getattr(w, func_name).connect(self.update_dic)

            self.o[self.name] = value
        if 'add_delete' in opts:
            btn = QPushButton('clear')
            btn.clicked.connect(self.clear)
            btn.setIcon(QtGui.QIcon('assets/icons/delete.png'))
            self.layout().addWidget(btn)

        self.present()

    def clipboardChanged(self):
        text = QApplication.clipboard().text()
        QApplication.clipboard().setText('banana')

    def update_dic(self, value=None):

        try:
            value = value or self.w.toPlainText()
        except:
            5
        self.o[self.name] = value
        if self.tp == 'text':
            self.o[self.name] = '"""{0}"""'.format(value)

        if 'call_on_update' in self.opts:
            self.opts['call_on_update'](self)

    def clear(self):
        self.setStyleSheet("background-color:{0};".format('blue'))

        if self.name in self.o:
            self.o.pop(self.name)
        self.my_parent.layout().removeWidget(self)
        self.setParent(None)
        self.hide()

    def value(self):
        return self.o[self.name]

    def transform(self, input):
        my_index = self.my_parent.layout().indexOf(self)
        self.clear()
        # self.setStyleSheet("background-color:{0};".format('blue'))
        self.setStyleSheet("background-color:{0};".format('blue'))

        new_input = Input(self.my_parent, input.value(), self.name, {'o': self.o, 'index': my_index, 'hide name': (
                    'hide name' in self.opts and self.opts['hide name'])})
        input.opts['call_on_update'] = new_input.transform
