from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
import json
from ModuleForm import ModuleForm
from ModulesManager import ModulesManager
class ModuleBtn(QLabel):
    def __init__(self, klass):
        title = klass.__name__
        super().__init__(title)
        self.klass = klass
        self.setAlignment(Qt.AlignCenter)

        self.setStyleSheet("""
            width: 50px;
            height: 20px;
            padding: 20px;
            border: 1px black;
            border-style: outset;
            font-size: 13px;
            font-weight: bold;
            text-align: right;
            background-color: #118ab2;
            color: rgb(230,230,230);
            border-radius: 7;
        """)

    def mousePressEvent(self, event):
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()
        if event.button() == Qt.RightButton:
            mm  = ModulesManager(self)
            mm.app = self.parent().parent().parent()
            mm.load_data(loc=f'm/{self.klass.__name__}')

            # with open(p, 'rb') as handle:
            #     b = json.load(handle)
            #
            # m = ModuleForm(None, dic=b, folder=p)
            # m.setStyleSheet('background-color = white')
            # m.show()


    def move_to(self, loc):
            return self.mapFromGlobal(self.get_pos(loc))

    def get_pos(self, e):
        currPos = self.mapToGlobal(self.pos())
        globalPos = e.globalPos()
        diff = globalPos - self.__mouseMovePos
        return self.mapFromGlobal(currPos + diff)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = self.get_pos(event).x()
            y = self.get_pos(event).y()
            sandbox = self.parent().parent().parent().sandbox

            if x > sandbox.x() and y > sandbox.y():
                sandbox.add_module(self.klass, relative_loc=self.get_pos(event))
            else:
                sandbox.parent().parent().statusBar().showMessage('not here', 2000)
