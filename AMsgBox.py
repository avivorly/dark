from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import re
from ResultToolbar import ResultToolbar
from PyQt5.QtWidgets import (
    QLabel, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import (QApplication, QCheckBox,
                             QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QSizePolicy,
                             QSpinBox, QTableWidget,
                             QVBoxLayout, QWidget)
from Input import Input

class AMsgBox(QWidget):

    def __init__(self, parent, s):
        super().__init__(parent)
        self.setStyleSheet("""
            border: 100px black;
           
            font-size: 22px;
            font-weight: bold;
            text-align: right;
            background-color: rgb(200,200,200);
            color: rgb(180,50,50);
        """)

        new_lines = []
        for line in s.splitlines():
            if '/m/temp' in line:
                r = re.search("line \d+", line).group()
                if r:
                    old_r = r
                    l = int(r[5:])
                    g = "line {0}/{1}".format(l - 7, l)
                    line = line.replace(old_r, g)
            new_lines.append(line)

        lay = QVBoxLayout()
        self.setLayout(lay)
        l = QLabel('\n'.join(new_lines))
        lay.addWidget(l)









    def save_to_jpg(self):
        self.grab().save('results.jpg')

