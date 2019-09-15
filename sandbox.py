import datetime
from moduleGUI import ModuleGui
from PyQt5.QtWidgets import QGroupBox, QMessageBox
from PyQt5.QtGui import QPainter
from modules.Module import Module

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

                if right_module_gui.module.next_node:
                    right_module_gui.module.next_node = None
                    right_module_gui.reset_on_of()
                    return
            if m.left.on:
                left_module_gui = m
        if right_module_gui and left_module_gui and right_module_gui != left_module_gui:

            right_module_gui.module.next_node = left_module_gui.module
            for m in self.gui_modules:
                m.reset_on_of()

    def file_path(self):
        return self.parent().parent().toolbar.file_path_input.text()

    def load_file_modules(self, path = None):
        modules, ex = Module.load_from_file(path or self.file_path())
        for m in modules:
            self.add_module(m, xy = m.gui_props)

    def dump_sandbox(self, path = None):
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

    def clear_sandbox(self, force = False):
        if force or QMessageBox.Yes == QMessageBox.question(self,
                                               'Clear sandbox',
                                               "Are you sure that you want to delete all modules?",
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No):
            for mg in self.gui_modules:
                mg.setParent(None)
            self.gui_modules = []

    def paintEvent(self, *args, **kwargs):
        qp = QPainter()
        qp.begin(self)
        for gm in self.gui_modules:
            gm.center()
            if gm.module.next_node:
                next_gm = gm.module.next_node.gui
                if next_gm:
                    acc = next_gm.closest_to(gm.center(), side=True)
                    bcc = gm.closest_to(next_gm.center(), side=False)
                    line = bcc[0], bcc[1], acc[0], acc[1]
                    qp.drawLine(*line)
                    self.update()

    def force_stater(self):
        m = [m for m in self.gui_modules if m.module not in map(lambda m: m.module.next_node, self.gui_modules)][0]
        self.force_starter(m)

    def save_to_jpg(self):
        self.grab().save('sandbox.png')