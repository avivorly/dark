from PyQt5.QtWidgets import QGridLayout, QMainWindow, QWidget
from Input import Input


class ModuleInputForm(QMainWindow):
    def __init__(self, parent, gui_modul):
        self.gui_modul = gui_modul
        m = gui_modul.module
        super().__init__(parent)

        main_window = QWidget(self)
        self.setCentralWidget(main_window)
        self.setMinimumSize(300, 100)

        lay = QGridLayout()
        self.lay = lay
        main_window.setLayout(lay)
        for name, tp in m.keys:
            Input(main_window, tp, name, opts = {'o': m.o})

    def save(self):
        app = self.parent().parent().parent()
        if app.modes['live_mode']:
            app.start_process()


