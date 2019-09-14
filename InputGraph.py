from Input import Input
from PyQt5.QtWidgets import QPushButton, QGroupBox
from functools import partial
from AWidget import AWidget

class InputGroup(AWidget):
    def __init__(self, parent, name, h, margin = 10, opts={}):
        super().__init__(parent, opts={**opts, **{'vertical': True, 'general_name': name}})
        self.setStyleSheet("""
                 margin:{0};
               
             """.format(margin, margin*3))

        self.layout().setContentsMargins(margin, 0, 0,0)

        fields = []
        tat_groups = []
        for k, v in h.items():
            if type(v) in [str, list]:
                fields.append([v, k])
            else:
                tat_groups.append([k, v])


        # if type(self.o) == list:
        #     o = {}
        #     self.o.append(o)
        #     self.o = o
        # else:
        #     if name in self.o:
        #         o = {}
        #         self.o[name].append(o)
        #         self.o = o
        #     else:
        #         self.o[name] = {}
        #         self.o = self.o[name]
        #     if type(self.o) == list:
        #

        o = self.o

        for tp, nm in fields:
            Input(self, 'group', nm, {'group_type': 'h', 'allowed types': tp})
        for nm, hh in tat_groups:
            b = QPushButton("add {0}".format(nm))
            b.clicked.connect(partial(self.add_group, nm, hh, margin + 10, {}))
            self.layout().addWidget(b)



            if nm in o:
            # for hhh in o[nm]:
            #     for k,v in hhh.items():
                for oo in o[nm]:
                    print(oo)
                    self.add_group(nm, h[nm], margin + 10, opts={'o': oo})
                #         1
                #         self.add_group(nm, h[nm], margin + 10, opts={'o':v})

            # if nm in o:
            #     for hhh in o[nm]:
            #         oo = o[nm][0]
            #         # self.add_group(nm, hhh, margin + 10, opts={'o': oo})

        self.present()
    def add_group(self, nm,h, margin = 0, opts = {}):
        # if nm not in self.o:
        #     self.o[nm] = []
        if 'o' in opts:  # not new
            InputGroup(self, nm, h, margin, opts)
        else: #  i am new
            if nm in self.o:
                1
            else:
                self.o[nm] = []
            n_o = {}
            self.o[nm].append(n_o)
            opts['o'] = n_o
            InputGroup(self, nm, h, margin, opts)















# class InputGraph()