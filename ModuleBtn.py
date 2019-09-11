from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
import sys
from moduleGUI import ModuleGui

class ModuleBtn(QGroupBox):
    def __init__(self, title, klass):
        super().__init__(title)
        self.klass = klass
        self.initUI()

    def initUI(self):
        # self.setIcon(QIcon('table.png'))
        # self.setIconSize(QSize(100,100))
        self.setStyleSheet("""
            width: 50px;
            height: 50px;
            
            font-size: 13px;
            font-weight: bold;
        """)

    def mousePressEvent(self, event):
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()

        # super(modolebtn, self).mousePressEvent(event)

    def move_to(self, loc):
        return self.mapFromGlobal(self.get_pos(loc))

    def get_pos(self, e):
        currPos = self.mapToGlobal(self.pos())
        globalPos = e.globalPos()
        diff = globalPos - self.__mouseMovePos
        return self.mapFromGlobal(currPos + diff)

    def mouseReleaseEvent(self, event):
        x = self.get_pos(event).x()
        y = self.get_pos(event).y()
        sandbox = self.parent().parent().parent().sandbox

        if x > sandbox.x() and y > sandbox.y():
            sandbox.add_module(self.klass, relative_loc=self.get_pos(event))

        else:

            sandbox.parent().parent().statusBar().showMessage('not here', 2000)



