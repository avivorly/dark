from Input import Input
from PyQt5.QtWidgets import QPushButton
from functools import partial
from AWidget import AWidget


class InputGroup(AWidget):
    def __init__(self, parent, name, h, margin = 10, opts={}):

        super().__init__(parent, opts={**opts, **{'vertical': True, 'general_name': name}})
        self.setStyleSheet("""

                 margin:{0};

             """.format(margin))
        self.layout().setContentsMargins(margin, 0, 0,0)

        fields = []
        tat_groups = []
        for k, v in h.items():
            if type(v) in [str, list]:
                fields.append([v, k])
            else:
                tat_groups.append([k, v])

        name = self.force_name(name)
        # o[name] = {}
        print("o: {0}".format(self.o))
        if name in self.o:
            self.o = o = self.o[name]
        else:
            self.o[name] = {}
            self.o = o = self.o[name]

        o = self.o

        for tp, nm in fields:
            idv = {}
            if nm in o:
                idv = o[nm]
            Input(self, 'group', nm, {
                                        'group_type': 'h', 'allowed types': tp
            })
            # Input(self, tp, nm)
        for nm, hh in tat_groups:
            b = QPushButton("add {0}".format(nm))
            b.clicked.connect(partial(self.add_group, nm, hh, margin + 10))
            self.layout().addWidget(b)

        self.present()
    def add_group(self, nm,h, margin, name = ''):
        if name:
            InputGroup(self, nm, h, margin, name)

        else:
            InputGroup(self, nm, h, margin)















# class InputGraph()