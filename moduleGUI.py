from functools import partial
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLabel,  QPushButton, QVBoxLayout, QWidget
from ModuleInputForm import ModuleInputForm
import inspect

class ModuleGui(QGroupBox):
    def __init__(self, parent, module):
        self.sand = parent
        super().__init__(parent)
        self.next_node = None
        self.line = None
        if inspect.isclass(module):

            self.module = module()
        else:
            self.module = module
        self.module.gui = self

        mainlay = QHBoxLayout()
        mainlay.setContentsMargins(0, 0, 0, 0)

        mainlay.setSpacing(0)
        self.setLayout(mainlay)
        self.right = QPushButton()
        self.left = QPushButton()

        for q in [self.left,self.right]:
            q.setFixedWidth(15)
            q.setStyleSheet("background-color:white;")
            q.on = False
            q.clicked.connect(partial(self.on_of, q))

        g = QGroupBox()
        self.g = g
        al = QVBoxLayout()
        g.setLayout(al)

        mainlay.addWidget(self.left)
        mainlay.addWidget(g)

        outputs = self.module.outputs
        if outputs:
            o_wid = QWidget()
            o_lay = QVBoxLayout()
            o_wid.setLayout(o_lay)
            al.addWidget(o_wid)
            for output in outputs:
                q = QPushButton(output['name']['value'])
                q.o = output

                q.setStyleSheet(f"background-color: {output['color']['value']}")
                output['on'] = False
                if 'next_nodes' not in output:
                    output['next_nodes'] = []
                output['btn'] = q
                o_lay.addWidget(q)
                q.clicked.connect(partial(self.click_btn, q))


        laybel = QLabel(self.module.__class__.__name__)
        al.addWidget(laybel)
        q = QPushButton('Edit')
        q.clicked.connect(self.open_form)
        al.addWidget(q)
        # color = a.palette().color(QPalette.Window)
        # color.setRed(100)

        # (color.getRgbF())
        mainlay.addWidget(self.right)
        self.resize(20, 20)
        self.show()

    def click_btn(self, btn):
        btn.o['on'] = not btn.o['on']
        self.update_btn(btn)
    def update_btn(self, btn):
        if btn.o['on']:
            btn.setStyleSheet(f"background-color: {'blue'}")
        else:
            btn.setStyleSheet(f"background-color: {btn.o['color']['value']}")
        self.sand.update_btns()



    def on_of(self, side, force_off = False):
        if force_off:
            side.on = False
        else:
            side.on = not side.on
        if side.on:
            color='black'
        else:
            color='white'
        side.setStyleSheet("background-color:{0};".format(color))
        if not force_off:
            self.sand.update_connections()

    def reset_on_of(self):
        for side in [self.right, self.left]:
            self.on_of(side, force_off=True)

    def mousePressEvent(self, event):
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self.__mouseMovePos
            newPos = self.mapFromGlobal(currPos + diff)

            parent_height = self.parent().height()
            parent_width = self.parent().width()
            # if globalPos.x() > parent_width * .95 or globalPos.y() > parent_height * .95 or globalPos.x() < parent_width * .05 or globalPos.y() < parent_height * .05:
            #     return

            self.move(newPos)
            self.__mouseMovePos = globalPos

    def mouseDoubleClickEvent(self, event):
        self.sand.force_starter(self)


    def set_sarter(self, flag):
        if flag:
            color = 'blue'
        else:
            color = 0
        for item in [self, self.g]:
            item.setStyleSheet("background-color:{0};".format(color))

    def open_form(self):
        modul_form = ModuleInputForm(self.sand, self)
        modul_form.show()

    def center(self):
        x1 = self.x()
        x2 = x1 + self.width()
        y1 = self.y()
        y2 = y1 + self.height()
        return [(x2 + x1)/2, (y2 + y1)/2]

    def closest_to(self, xy, side = True):
        lx, ly = xy
        sx, sy = self.center()
        a = sx - lx
        b = sy - ly
        if True:#abs(a) > abs(b):
            y = sy + 9
            if side:#a > 0:
                x = self.x()
            else:
                x = self.x() + self.width()
        else:
            x = sx
            if b > 0:
                y = self.y() + 20
            else:
                y = self.y() + self.height()
        return [x, y]

