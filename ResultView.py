from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from ResultToolbar import ResultToolbar
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import (
    QLabel, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import (QApplication, QCheckBox,
                             QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QSizePolicy,
                             QSpinBox, QTableWidget,
                             QVBoxLayout, QWidget)
from Input import Input

class Image(FigureCanvas):
    def __init__(self,parent, images,width=9, height=4, dpi=50):
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        images = images['images']['value']
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

class Graph(FigureCanvas):
    def __init__(self,parent, opts={}):
        self.opts = opts


        fig = Figure(figsize=(9, 4), dpi=50)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, \
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        ax = self.figure.add_subplot(111)
        # self.figure.title = '123'
        ax.set_title(opts['title']['value'])
        for f in opts['func']:
            xs, ys = f['xy']['value']
        ax.plot(xs, ys, 'ro')

        for h in opts['hist']:
            # int(bins * ((vmax - vmin) / (fmax - fmin))), (vmin, vmax))
            # -300, 300, 1000
            ax.hist(list(h['data']['value']), 1000, (-300, 300))
        self.figure.tight_layout()
        self.draw()
class ResultView(QWidget):

    def __init__(self, parent, extras):
        # self.gui_modul = gui_modul
        super().__init__(parent)

        main_lay = QVBoxLayout()
        self.setLayout(main_lay)
        lay = main_lay
        # toolbar

        self.toolbar = ResultToolbar(self)
        # toolbar.setIconSize(QSize(16, 16))
        main_lay.addWidget(self.toolbar)
        self.o = {}
        for extra in extras:

            for h in extra:
                l = QLabel(h['name'])
                lay.addWidget(l)
                views = h['views']
                for tp, arrs in views.items():
                    if tp == 'string':
                        for h in arrs:
                            l = QLabel(str(h[tp]['value']))
                            lay.addWidget(l)
                    if tp == 'graph':
                        for h in arrs:
                            g = Graph(self, h)
                            lay.addWidget(g)
                    if tp == 'image':

                        for h in arrs:

                            g = Image(self, h)
                            if h['add toolbar']['value']:

                                t = NavigationToolbar(g, self)
                                lay.addWidget(t)
                            lay.addWidget(g)












    def save_to_jpg(self):
        self.grab().save('results.jpg')

