from PyQt5 import QtCore, QtGui

from PyQt5.QtWidgets import (QPlainTextEdit, QFileDialog, QComboBox ,QApplication, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QSpinBox, QWidget)
# TODO  create also oo hash that saves all needed data, so [o,oo] contains all need to save an open anything
class Input(QWidget):
    def __init__(self, parent, type, name = '', opts = {}):
        super().__init__(parent)
        lay = QHBoxLayout()
        self.setLayout(lay)
        self.name = name
        self.opts = opts
        self.type = type
        self.my_parent = parent
        value = None
        o = self.o = opts['o'] if 'o' in opts else self.parent().o

        groups_types = {
            'view_definer': ['title', 'type', 'view data'],
            'input_definer': ['name', 'type', 'value']
        }

        # 1 if True else 2
        general_name = opts['general_name'] if 'general_name' in opts else 'input'

        if not name:
            i = 1
            while '{0}: {1}'.format(general_name, i) in o:
                i += 1
            name = '{0}: {1}'.format(general_name, i)
        else:
            if name in o:
                value = o[name]



        if '!label' not in opts:
            lay.addWidget(QLabel(name))
        if type in ['string', 'python']:
            value = value or ''
            func_name, w = ['textChanged', QLineEdit(value)]
        if type == 'texteditor':
            value = value or ''
            func_name, w = ['textChanged', QPlainTextEdit(value)]
        if type == 'integer':
            value = value or 0
            func_name, w = ['valueChanged', QSpinBox()]
            w.setRange(-2147483648, 2147483647)
            w.setValue(value)
        if type == 'file':
            value = value or ''
            func_name, w = ['textChanged', QLineEdit(value)]
            b = QPushButton('Openn File')
            lay.addWidget(b)
            b.clicked.connect(lambda: w.setText(QFileDialog.getOpenFileName(self)[0]))
        if type in ['select', 'type']:
            if type == 'type':
                opts['group'] = 'general input'
            groups = {
                'general input': ['string', 'python', 'file', 'integer']
            }

            func_name, w = ['currentTextChanged', QComboBox()]
            for t in groups[opts['group']]:
                w.addItem(t)

            value = value or w.itemText(0)

            index = w.findText(value, QtCore.Qt.MatchFixedString)
            w.setCurrentIndex(index)




        if type == 'group':
            titles = groups_types[opts['group_type']]
            w = False
            if not value:
                value = {}
                self.o[self.name] = value
            if 'input_definer_values' in opts:


                for i in range(0, len(opts['input_definer_values'])):

                    value[titles[i]] = opts['input_definer_values'][i]



            save_until_next = None
            for i in range(0,len(titles)):
                title = titles[i]
                if title is 'type':
                    save_until_next = Input(self, 'select', title, {'o': value, 'group': 'general input'})
                else:
                    if not save_until_next:
                        input = Input(self, 'string', title, {'o': value})
                    else:
                        if 'type' in value:
                            generic_name = value['type']
                        else:
                            generic_name = 'string'
                        input = Input(self, generic_name, title, {'o': value})


                        save_until_next.opts['call_on_update'] = input.transform
                        save_until_next = None
        if w:
            self.w = w
            lay.addWidget(w)
            getattr(w, func_name).connect(self.update_dic)

            self.o[self.name] = value
        if 'add_delete' in opts:
            btn = QPushButton('clear')
            btn.clicked.connect(self.clear)
            btn.setIcon(QtGui.QIcon('assets/icons/delete.png'))
            lay.addWidget(btn)

        # self.update_dic(self.o)


        self.show()
        if hasattr(self.parent(), 'lay'):
            l = self.parent().lay
        else:
            l = self.parent().layout()
        if 'index' in opts:
            l.insertWidget(opts['index'], self)
        else:
            l.addWidget(self)

    def clipboardChanged(self):
        text = QApplication.clipboard().text()
        QApplication.clipboard().setText('banana')
    def update_dic(self, value = None):


        try:
            value = value or self.w.toPlainText()
        except:
            5
        self.o[self.name] = value
        if self.type == 'text':
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


        new_input = Input(self.my_parent, input.value(), self.name, {'o': self.o, 'index': my_index})
        input.opts['call_on_update'] = new_input.transform
