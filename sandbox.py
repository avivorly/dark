import datetime
from moduleGUI import ModuleGui
from PyQt5.QtWidgets import QGroupBox, QMessageBox
from PyQt5.QtGui import QPainter
from modules.Module import Module
import numpy as np
from numpy.linalg import norm


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
                right_module_gui.module.next_nodes.append(left_module_gui.module)
            for m in self.gui_modules:
                m.reset_on_of()

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
        qp = QPainter()
        qp.begin(self)
        for gm in self.gui_modules:
            gm.center()
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
                        next_nodes.remove(next_node)

    def mouseReleaseEvent(self, event):
        print('2')
    #     l1 = self.last_press[0], self.last_press[1], event.x(), event.y()
    #     for gm in self.gui_modules:
    #         gm.center()
    #         if gm.module.next_nodes:
    #             next_nodes = gm.module.next_nodes
    #             for next_node in next_nodes:
    #                 next_gm = next_node.gui
    #                 acc = next_gm.closest_to(gm.center(), side=True)
    #                 bcc = gm.closest_to(next_gm.center(), side=False)
    #                 l2 = bcc[0], bcc[1], acc[0], acc[1]
    #
    #                 m_of_line = lambda x1, y1, x2, y2: (y2 - y1) / (x2 - x1)
    #                 c_of_line = lambda x1, y1, x2, y2: -m_of_line(x1, y1, x2, y2) * x1 + y1
    #
    #                 # m1 = m_of_line(*l1)
    #                 # c1 = c_of_line(*l1)
    #
    #                 m2 = m_of_line(*l2)
    #                 c2 = c_of_line(*l2)
    #
    #                 # x = (c2 - c1) / (m1 - m2)
    #                 # print(m1,c1)
    #                 print(m2, c2)
    #                 print('wow')
    #                 # if l1[0] < x < l1[3] and l2[0] < x < l2[3]:
    #                 #     print('wow')
    #                 #     next_nodes.remove(next_node)

    def force_stater(self):
        m = [m for m in self.gui_modules if m.module not in map(lambda m: m.module.next_nodes, self.gui_modules)][0]
        self.force_starter(m)

    def save_to_jpg(self):
        self.grab().save('sandbox.png')
