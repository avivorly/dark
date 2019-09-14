import os, sys, re
import datetime
import numpy as np
from numpy import exp
from astropy.io import fits
from matplotlib.figure import Figure
# import ROOT
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
# import pickle
import json
import importlib
import sys, pkgutil

class Module():
    r = '$$$'

    def __init__(self):
        super().__init__()
        if not hasattr(self,'o'):
            self.o = {}
        self.next_node = None

    def run(self):
        data, views = self.process()
        extras = [{
            'name': self.__class__.__name__,
            'data': data,
            'views': views
        }]

        if self.next_node:
            self.next_node.data = data
            next_extras = self.next_node.run()
            extras += next_extras
        return extras

    def dumpp(self):
        out = {
            'class': self.__class__.__name__,
            # 'data': self.data,
            'o': self.o,
            'next_node': self.next_node,
            'gui_props': None

        }
        if 'gui' in dir(self):
            out['gui_props'] = [self.gui.x(), self.gui.y()]

        return out

    @classmethod
    def save_to_file(cls, modules, path):
        arr = []
        for m in modules:
            t = m.dumpp()
            if m.next_node:
                t['next_node'] = modules.index(m.next_node)
            # m.gui = None
            arr.append(t)

        with open(path, 'w') as handle:
            json.dump(arr, handle)

    @classmethod
    def get_all_modules(cls):
        return cls.import_all_file_modules() + cls.import_all_modules_from_pickle()


    @classmethod
    def import_all_file_modules(cls):
        modules = map(lambda n: n[1], pkgutil.iter_modules(['modules']))
        return [getattr(importlib.import_module('modules.{0}'.format(m)), m) for m in modules]

    @classmethod
    def import_all_modules_from_pickle(cls):
        arr = []
        path = 'm/'
        for m in os.listdir(path):
            if not os.path.isdir(path + m):
                with open(path + m, 'r') as handle:
                    b = json.load(handle)
                    try:
                        arr.append(cls.create_module(b))
                    except Exception:
                        import traceback
                        traceback.print_exc()
        return arr

    @classmethod
    def create_module(cls, opts):
        o = {}
        keys = []

        for nm, key_type, default in opts['keys']:
            o[nm] = default
            keys.append([nm, key_type])

        name = opts['name']

        i = '    '
        before_lines = [
            'from modules.Module import Module',
            'import copy',
            'class {0}(Module):'.format(opts['name']),
            i + 'def process(self):',
        ]

        init_lines = [
            'if hasattr(self, "data"):'
            '   data = self.data.copy() if getattr(self.data, "copy", False) else copy.deepcopy(self.data)',
            'o = copy.deepcopy(self.o)'
        ]

        views = json.dumps(cls.h_t_s(opts['views']))
        views = views.replace('"{0}'.format(cls.r), '')
        views = views.replace('{0}"'.format(cls.r), '')


        # for nm, tp, value in opts['views']:
        #     if tp == 'string':
        #         views.append('["{0}","{1}","""{2}"""]'.format(nm, tp, value))
        #     else:
        #         views.append('["{0}","{1}",{2}]'.format(nm, tp, value))

        return_line = 'return data, {0}'.format(views)


        lines = before_lines + [i * 2 + l for l in init_lines + opts['code'].split('\n') + [return_line]]


        with open('m/temp/{0}.py'.format(name), 'w') as file:
            file.write('\n'.join(lines))
        p = 'm.temp.{0}'.format(name)
        if p in sys.modules:
            del sys.modules[p]
        m = getattr(importlib.import_module(p), name)

        m.o = o
        m.keys = keys


        return m

    @classmethod
    def h_t_s(cls, h):

        for k,v in h.items():
            if type(v) == dict and 'value' in v:
                name = k
                value = v['value']
                tp = v['type']
                sb = '"""'
                if tp == 'code':
                    v['value'] = cls.r + value + cls.r
            elif type(v) == list:
                for hash in v:
                    cls.h_t_s(hash)
            else:
                cls.h_t_s(v)
        return h



    @classmethod
    def load_from_file(cls, path):
        modules_clss = cls.get_all_modules()
        modules = []
        with open(path, 'rb') as handle:
            saved_modules = json.load(handle)
            for saved_hash in saved_modules:
                try:
                    m_class = next(x for x in modules_clss if x.__name__ == saved_hash['class'])
                    # m = eval(m_class + '()')
                    m = m_class()
                    # m = m_class.__init__()
                    for p in ['o', 'gui_props', 'next_node']:
                        setattr(m, p, saved_hash[p])

                    modules.append(m)
                except Exception:
                    import traceback
                    traceback.print_exc()

        for m in modules:
            if m.next_node:
                m.next_node = modules[m.next_node]


        return modules



    @classmethod
    def open_file(cls, path, CONST_nonReal = 20):
        m = fits.open(path)[0].data
        rows = len(m)
        cols = len(m[0])

        m = np.delete(m, np.s_[0:CONST_nonReal], axis=0)
        m = np.delete(m, np.s_[0:CONST_nonReal], axis=1)
        m = np.delete(m, np.s_[rows - CONST_nonReal:rows], axis=0)
        m = np.delete(m, np.s_[cols - CONST_nonReal:cols], axis=1)
        return m

    @classmethod
    def mask(cls, mat, mask):
        mat = mat.copy()
        rowsLen = len(mat)
        colsLen = len(mat[0])
        for i in range(0, rowsLen):
            for j in range(0, colsLen):
                if mask[i][j] - 32 not in [0, 1, 2, 3]:
                    mat[i][j] = np.NAN
        return mat

    @classmethod
    def rows_of(cls, mat):
        return mat

    @classmethod
    def columns_of(cls, mat):
        colsLen = len(mat[0])
        rows = []
        for i in range(0, colsLen):
            rows.append(mat[:, i])
        return rows

    @classmethod
    def get_neighbors_indices(cls, i, j, x_max, y_max):
        arr = [
                        [i + 1, j],
                        [i - 1, j],
                        [i + 1, j + 1],
                        [i - 1, j - 1],
                        [i, j - 1],
                        [i, j + 1],
                        [i + 1, j - 1],
                        [i - 1, j + 1],
                    ]
        return [xy for xy in arr if 0 <= xy[0] < x_max and 0 <= xy[1] < y_max]

    @classmethod
    def get_neighbors_indices_by_range(cls, x, y, x_max, y_max, degree):
        indices = [[x, y]]

        for i in range(1, degree + 1):
            temp_indices = []
            for old_xy in indices:
                new_xy_array = cls.get_neighbors_indices(old_xy[0], old_xy[1], x_max, y_max)
                for xy in new_xy_array:
                    if xy not in indices and xy not in indices:
                        temp_indices.append(xy)
            indices += temp_indices

        return indices


 #
 #
 # def create_module(cls, opts):
 #        # name, keys, views, process
 #        module = type(opts['name'], (Module,), {})
 #        o = {}
 #        keys = []
 #        for name, key_type, default in opts['keys']:
 #            o[name] = default
 #            keys.append([name, key_type])
 #        module.o = o
 #        module.keys = keys
 #        # module.views_keys = views
 #        # before_lines -
 #        init_lines = [
 #            'import copy',
 #            'if hasattr(self, "data"):'
 #            '   data = self.data.copy() if getattr(self.data, "copy", False) else copy.deepcopy(self.data)',
 #            'o = copy.deepcopy(self.o)'
 #        ]
 #
 #        views = ['["{0}","{1}",{2}]'.format(*k) for k in opts['views']]
 #        return_line = 'return data, [{0}]'.format(','.join(views))
 #
 #        i = '    '
 #        lines = [i + l for l in init_lines +  opts['code'].split('\n') + [return_line]]
 #
 #
 #        f = '\n'.join(lines)
 #
 #        str = 'def process(self):\n{0}'.format(f)
 #        h = {}
 #        exec(str, globals(), h)
 #
 #        setattr(module, 'process', h['process'])
 #
 #        #  TODO create actual files on temp dir - helps with debugging
 #        return module