from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QAction, QToolBar, QLineEdit
from PyQt5.QtGui import QIcon
from ModulesManager import ModulesManager


class ToolBar(QToolBar):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        sand = parent.sandbox
        sand.toolbar = self
        self.shortcuts_dic = {}
        self.btns = {}
        #  TODO setCheckable insdead of disabled
        self.init_values = [
            ['save', sand.dump_sandbox],
            ['load', sand.load_file_modules, Qt.Key_F4],
            ['clear', sand.clear_sandbox],
            ['start', sand.parent().parent().start_process, Qt.Key_F5],
            ['path', None],
            ['open_file', self.set_path_from_user],
            ['image_save', sand.save_to_jpg],
            ['one_window', self.one_window],
            ['two_windows', self.two_windows],
            ['live_mode', self.live_mode],
            ['simple_mode', self.simple_mode],
            ['ModulesManager', self.modules_manager],
        ]
        for arr in self.init_values:
            action, connect_to = arr[0], arr[1]

            if action not in ['path']:
                btn = QAction(QIcon("assets/icons/{0}.png".format(action)), action, self)
                btn.setStatusTip(action)
                btn.triggered.connect(connect_to)
                self.addAction(btn)

            else:
                self.file_path_input = QLineEdit()
                self.file_path_input.setText('filename.pickle')
                self.addWidget(self.file_path_input)
                btn = self.file_path_input
            self.btns[action] = btn


    def set_path_from_user(self):
        self.file_path_input.setText(QFileDialog.getOpenFileName(self)[0])

    def one_window(self):
        self.parent().modes['outer_window'] = False
        self.btns['one_window'].setDisabled(True)
        self.btns['two_windows'].setDisabled(False)
    def two_windows(self):
        self.parent().modes['outer_window'] = True
        self.btns['two_windows'].setDisabled(True)
        self.btns['one_window'].setDisabled(False)
    def live_mode(self):
        self.parent().modes['live_mode'] = True
        self.btns['live_mode'].setDisabled(True)
        self.btns['simple_mode'].setDisabled(False)
    def simple_mode(self):
        self.parent().modes['live_mode'] = False
        self.btns['live_mode'].setDisabled(False)
        self.btns['simple_mode'].setDisabled(True)

    def modules_manager(self):
        m = ModulesManager(self)
        m.app = self.parent()
        m.show()

    def shortcut(self, key):
        for arr in self.init_values:
            if len(arr) > 2 and arr[2] == key:
                action = arr[1]
                action()
