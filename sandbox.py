import datetime
from moduleGUI import ModuleGui
from PyQt5.QtWidgets import QGroupBox, QMessageBox
from PyQt5.QtGui import QPainter, QPen
from modules.Module import Module
import numpy as np
from numpy.linalg import norm
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
class SandBox(QGroupBox):
    def __init__(self):
        super().__init__()
        self.gui_modules = []
        self.starter = None

    def add_module(self, klass, relative_loc=None, xy=None):
        gm = ModuleGui(self, klass)

        if xy:
            gm.move(xy[0], xy[1])
        else:
            x1, y1 = relative_loc.x(), relative_loc.y()
            r1, r2 = self.x(), self.y()
            gm.move(x1 - r1, y1 - r2)
        gm.resize(220, 220)
        gm.show()
        self.gui_modules.append(gm)
        return gm


    def update_btns(self):
        right_module_gui, left_module_gui = None, None
        op = None
        for mg in self.gui_modules:
            for o in mg.module.outputs:
                if o['on']:
                    right_module_gui = mg
                    n_ms = o['next_nodes']
            if mg.left.on:
                left_module_gui = mg
        if right_module_gui and left_module_gui and right_module_gui != left_module_gui:
            if left_module_gui.module not in n_ms:
                n_ms.append(left_module_gui.module)
                o['on'] = False
            else:
                self.break_btn_connection(o, left_module_gui)


                # self.create_connection(right_module_gui, left_module_gui)
            # else:
            #     self.break_connection(right_module_gui, left_module_gui)
            for m in self.gui_modules:
                m.reset_on_of()
                for o in mg.module.outputs:
                    o['on'] = False
                    mg.update_btn(o['btn'])

    def break_btn_connection(self, o, mg):
        print('break')
        o['next_nodes'].remove(mg.module)

        # break_btn_connection
    def update_connections(self):
        right_module_gui, left_module_gui = None, None

        for m in self.gui_modules:
            if m.right.on:
                right_module_gui = m
                for next_node in right_module_gui.module.next_nodes:
                    if next_node:
                        1
                        # next_node.data = None
                        # right_module_gui.module.next_node = None
                        # right_module_gui.reset_on_of()
                        # return
            if m.left.on:
                left_module_gui = m
        if right_module_gui and left_module_gui and right_module_gui != left_module_gui:
            if left_module_gui.module not in right_module_gui.module.next_nodes:
                self.create_connection(right_module_gui, left_module_gui)
            else:
                self.break_connection(right_module_gui, left_module_gui)
            for m in self.gui_modules:
                m.reset_on_of()

    def create_connection(self, right_module_gui, left_module_gui):
        right_module_gui.module.next_nodes.append(left_module_gui.module)


    def break_connection(self, right_module_gui, left_module_gui):
        right_module_gui.module.next_nodes.remove(left_module_gui.module)
        left_module_gui.module.data = None

    def file_path(self):
        return self.parent().parent().toolbar.file_path_input.text()

    def load_file_modules(self, path=None):
        self.clear_sandbox(force=True)
        modules, ex = Module.load_from_file(path or self.file_path())
        for m in modules:
            self.add_module(m, xy=m.gui_props)

    def dump_sandbox(self, path=None):
        modules = []
        for gm in self.gui_modules:
            m = gm.module
            m.gui_props = [gm.x, gm.y]
            modules.append(m)
        Module.save_to_file(modules, path or self.file_path())

    def force_starter(self, starter):
        self.starter = starter
        for m in self.gui_modules:
            m.set_sarter(self.starter == m)

    def clear_sandbox(self, force=False):
        if force or QMessageBox.Yes == QMessageBox.question(self,
                                                            'Clear sandbox',
                                                            "Are you sure that you want to delete all modules?",
                                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No):
            for mg in self.gui_modules:
                mg.setParent(None)
            self.gui_modules = []
            self.starter = None

    # def line(self,m_a, m_b):

    def paintEvent(self, *args, **kwargs):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp = QPainter()
        qp.setPen(pen)
        qp.begin(self)
        for gm in self.gui_modules:
            if gm.module.next_nodes:
                for next_module in gm.module.next_nodes:
                    next_gm = next_module.gui
                    if next_gm:
                        acc = next_gm.closest_to(gm.center(), side=True)
                        bcc = gm.closest_to(next_gm.center(), side=False)
                        line = bcc[0], bcc[1], acc[0], acc[1]

                        # lines[line] = [gm.module, next_gm.module]
                        qp.drawLine(*line)
                        self.update()
                        # self.update()

        for gm in self.gui_modules:
            for o in gm.module.outputs:
                if 'next_nodes' in o:
                    for next_module in o['next_nodes']:
                        next_gm = next_module.gui
                        acc = next_gm.closest_to(gm.center(), side=True)

                        # bcc = gm.closest_to(next_gm.center(), side=False)
                        b = o['btn']
                        bcc = [b.x()+b.width() + gm.x(), o['btn'].y()+70+gm.y()]
                        line = bcc[0], bcc[1], acc[0], acc[1]

                        # lines[line] = [gm.module, next_gm.module]

                        pen.setStyle(Qt.CustomDashLine)
                        pen.setColor(QColor(o['color']['value']))
                        # pen.setColor(self.backgroundRole(), Qt.white)
                        pen.setDashPattern([1, 10, 1, 1])
                        # pen.setDashOffset(50)
                        # pen.dashOffset(100)
                        # pen.setWidth(2)
                        qp.setPen(pen)

                        # pen.setStyle(Qt.DashDotDotLine)
                        # qp.setPen(pen)
                        qp.drawLine(*line)
                        self.update()


    def mousePressEvent(self, event):
        self.last_press = [event.x(), event.y()]
        for gm in self.gui_modules:
            gm.center()
            if gm.module.next_nodes:
                next_nodes = gm.module.next_nodes
                for next_node in next_nodes:
                    next_gm = next_node.gui
                    acc = next_gm.closest_to(gm.center(), side=True)
                    bcc = gm.closest_to(next_gm.center(), side=False)
                    line = bcc[0], bcc[1], acc[0], acc[1]
                    p1 = np.array((bcc[0], bcc[1]))
                    p2 = np.array((acc[0], acc[1]))
                    p3 = np.array((event.x(), event.y()))
                    d = norm(np.cross(p2 - p1, p1 - p3)) / norm(p2 - p1)
                    if d < 35:
                        self.break_connection(gm, next_node.gui)



    def force_stater(self):
        m = [m for m in self.gui_modules if m.module not in map(lambda m: m.module.next_nodes, self.gui_modules)][0]
        self.force_starter(m)

    def save_to_jpg(self):
        self.grab().save('sandbox.png')
