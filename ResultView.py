from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from ResultToolbar import ResultToolbar
from PyQt5.QtWidgets import (
                             QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QSizePolicy,
                             QSpinBox, QTableWidget,
                             QVBoxLayout, QWidget)
from output.Output import OutputGraph

from InputGraph import InputGroup


class Image(FigureCanvas):
    def __init__(self,parent, images,width=9, height=4, dpi=50):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.axArr = self.figure.subplots(1, len(images))

        if len(images) == 1:
            for i in range(0, len(images)):
                ax = self.axArr
                ax.axis('off')
                ax.imshow(images[i], cmap='hot')

        else:
            for i in range(0, len(images)):
                ax = self.axArr[i]
                ax.axis('off')
                ax.imshow(images[i], cmap='hot')


        self.figure.tight_layout()
        self.draw()

class ResultView(QWidget):
    def __init__(self, extras, parent):
        # self.gui_modul = gui_modul
        super().__init__(parent)
        self.initUI(extras)

    def initUI(self, extras):
        main_lay = QVBoxLayout()
        self.setLayout(main_lay)

        # toolbar

        self.toolbar = ResultToolbar(self)
        # toolbar.setIconSize(QSize(16, 16))
        main_lay.addWidget(self.toolbar)
        self.o = {}




        # for extra in extras:
        #     name = extra['name']
        #     data = extra['data']
        #     views = extra['views']
        #
        #     extra_box = QGroupBox(name)
        #
        #     lay = QGridLayout()
        #     extra_box.setLayout(lay)
        #     main_lay.addWidget(extra_box)
        #     row = 0
        #     for name, type, value in views:
        #         lay.addWidget(QLabel(name), row, 0)
        #         if type == 'string':
        #             lay.addWidget(QLabel(value), row, 1)
        #         if type == 'number':
        #             lay.addWidget(QLabel(str(value)), row, 1)
        #         if type == 'graph':
        #             lay.addWidget(OutputGraph(extra_box ,value), row, 1)
        #         if type == 'image':
        #             lay.addWidget(Image(extra_box, value), row, 1)
        #
        #         row += 1

        # h = {
        #     'simple output': {
        #         'str':['python']
        #     },
        #     'graph':
        #         {
        #         'title': 'string',
        #         'func': {
        #             'xy': 'code',
        #             'xlim': ['integer', 'code']
        #         },
        #         'hist': {
        #             'xs': 'string'
        #         }
        # } }
        #

        #






    def save_to_jpg(self):
        self.grab().save('results.jpg')

