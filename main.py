import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QGroupBox, QHBoxLayout, QPushButton, QVBoxLayout, QWidget, QSpinBox
from AMsgBox import AMsgBox
from modules.Module import Module
from sandbox import SandBox
from ResultView import ResultView
from ModuleBtn import ModuleBtn
from toolbar import ToolBar

class AfelApp(QMainWindow):
    def __init__(self, parent=None):
        super(AfelApp, self).__init__(parent)
        self.setGeometry(10, 10, 1000, 1200)
        # self.setStyleSheet("""
        #
        #              background-color: rgb(100,100,100);
        #
        #         """)
        # Flags
        self.modes = {
            'outer_window': True,
            'live_mode': False
        }

        self.result_box_group = None
        self.result_box = None

        self.module_btns = []

        mainWindow = QWidget(self)
        self.setCentralWidget(mainWindow)
        mainlay = QHBoxLayout()

        mainWindow.setLayout(mainlay)

        #  load area
        btns_group = QGroupBox()
        btns_lay = QVBoxLayout()
        btns_group.setLayout(btns_lay)
        btns_lay.addStretch(1)
        self.btns_lay = btns_lay

        self.load_modules_btns()

        startbtn = QPushButton('start process')
        startbtn.clicked.connect(self.start_process)
        btns_lay.addWidget(startbtn)



        #  sandbox area
        self.sandbox = SandBox()
        self.sandboxlay = QVBoxLayout()
        # self.sandboxlay.addStretch(209)
        self.sandbox.setLayout(self.sandboxlay)

        mainlay.addWidget(btns_group,1)
        mainlay.addWidget(self.sandbox,10)

        # toolbar
        # toolbar.setIconSize(QSize(16, 16))
        self.toolbar = ToolBar(self)
        self.addToolBar(self.toolbar)

    def load_modules_btns(self):
        self.clear_modules_btns()
        all_modules, es = Module.get_all_modules()
        for btn in [ModuleBtn(m) for m in all_modules]:
            self.btns_lay.insertWidget(0, btn)
            self.module_btns.append(btn)
        self.pop_errors(es)

    def pop_errors(self, es):
        for e in es:
            w = QMainWindow(self)
            w.setCentralWidget(AMsgBox(self,e))
            w.show()

    def clear_modules_btns(self):
        [b.setParent(None) for b in self.module_btns]
        self.module_btns = []

    def reload(self):  # reload all - sandbox and modules btn
        temp_path = 'm/temp/temporaryModules'  # sandbox cash

        self.sandbox.dump_sandbox(temp_path)
        self.clear_modules_btns()
        self.load_modules_btns()
        self.sandbox.clear_sandbox(force=True)
        self.sandbox.load_file_modules(temp_path)

    def start_process(self):
        if self.result_box_group:  # group to include the results window when not poped
            self.result_box_group.deleteLater()  # improve memory
            self.result_box_group = None
        self.old_box = self.result_box
        starter = self.sandbox.starter
        if starter:
            try:
                extras = starter.module.run()
                self.result_box = ResultView(self, extras)
                if self.modes['outer_window']:
                    w = QMainWindow(self)
                    w.setCentralWidget(self.result_box)
                    w.show()
                else:
                    g = QGroupBox()
                    gl = QHBoxLayout()
                    g.setLayout(gl)
                    gl.addWidget(self.result_box)
                    self.result_box_group = g
                    self.layout().addWidget(g, 5)
            except Exception:
                import traceback
                self.pop_errors([traceback.format_exc()])


        else:
            self.statusBar().showMessage('please define starter', 2000)
            self.sandbox.force_stater()
            self.start_process()

    def keyPressEvent(self, event):
        self.toolbar.shortcut(event.key())

def main():
    app = QApplication(sys.argv)
    AfelApp().show()
    app.exec_()
    # win.showMaximized() app.setStyle('Fusion')

if __name__ == '__main__':
    sys.exit(main())

#  TODO Qt Quick Controls 2 check it