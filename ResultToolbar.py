from PyQt5.QtWidgets import QLineEdit, QAction, QToolBar
from PyQt5.QtGui import QIcon

class ResultToolbar(QToolBar):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)


        for action, connect_to in [
            ['image_save', self.save_to_jpg]
        ]:
            if action not in ['path']:
                btn = QAction(QIcon("assets/icons/{0}.png".format(action)), action, self)
                btn.setStatusTip(action)
                btn.triggered.connect(connect_to)
                # button_action.setCheckable(True)
                self.addAction(btn)
            else:
                self.file_path_input = QLineEdit()
                self.file_path_input.setText('filename.pickle')
                self.addWidget(self.file_path_input)


    def save_to_jpg(self):
        self.hide()
        self.parent().save_to_jpg()
        self.show()




