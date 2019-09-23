import os, sys, re
import datetime
import numpy as np
from numpy import exp
from astropy.io import fits
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
        self.next_nodes = []

    def run(self):
        data, views = self.process()

        module_output = {
            'name': self.__class__.__name__,
            'data': [],
            'views': views
        }

        if self.next_nodes:
            extras_arr = []
            for next_node in self.next_nodes:
                next_node.data = data

                for computed_output in self.computed_outputs['output']:
                    print(computed_output)
                    next_node.o[computed_output['name']['value']] = computed_output['value']['value']

                next_module_output = next_node.run()
                extras_arr +=next_module_output
            extras_arr = [[module_output] + a for a in extras_arr]
            return extras_arr
        else:
            return [[module_output]]

    def dumpp(self):
        out = {
            'class': self.__class__.__name__,
            # 'data': self.data,
            'o': self.o,
            'next_nodes': self.next_nodes,
            'gui_props': None,
            'outputs': self.outputs

        }
        if 'gui' in dir(self):
            out['gui_props'] = [self.gui.x(), self.gui.y()]

        return out

    @classmethod
    def save_to_file(cls, modules, path):
        arr = []
        for m in modules:
            t = m.dumpp()
            t['next_nodes'] = [modules.index(n) for n in m.next_nodes]
            for o in t['outputs']:
                o['next_nodes'] = [modules.index(n) for n in o['next_nodes']]
                del o['btn']
            arr.append(t)

        with open(path, 'w') as handle:
            json.dump(arr, handle)

    @classmethod
    def get_all_modules(cls):
        return cls.import_all_modules_from_pickle()


    @classmethod
    def import_all_file_modules(cls):
        modules = map(lambda n: n[1], pkgutil.iter_modules(['modules']))
        return [getattr(importlib.import_module('modules.{0}'.format(m)), m) for m in modules]

    @classmethod
    def import_all_modules_from_pickle(cls):
        arr = []
        path = 'm/'
        es = []
        for m in os.listdir(path):
            if not os.path.isdir(path + m):
                with open(path + m, 'r') as handle:
                    b = json.load(handle)
                    try:
                        if b['active']:
                            arr.append(cls.create_module(b))
                    except:
                        import traceback
                        es.append(traceback.format_exc())
        return arr, es

    @classmethod
    def create_module(cls, opts):
        o = {}
        keys = []

        for nm, key_type, default in opts['keys']:
            o[nm] = default
            keys.append([nm, key_type])

        name = opts['name']
        if name in ['Fitter', 'CreateData']:
            exl = ';from ROOT import TF1, gRandom, TH1F'
        else:
            exl = '\n'
        i = '    '
        before_lines = [
            'from modules.Module import Module',
            'import numpy as np',
            'import copy',
            'import copy' + exl,

            'class {0}(Module):'.format(opts['name']),
            i+ 'def __init__(self):',
            i *2 + 'super().__init__()',
            i * 2 + 'self.o = self.c_o.copy()',
            i * 2 + 'self.keys = self.c_keys.copy()',
            i * 2 + 'self.outputs = copy.deepcopy(self.c_outputs)',
            i + 'def process(self):'


        ]



        init_lines = [
            'if hasattr(self, "data"):'
            '   data = self.data.copy() if getattr(self.data, "copy", False) else copy.deepcopy(self.data)',
            'o = copy.deepcopy(self.o)',
            'for k,v in o.items():',
            i + 'globals()[k] = v'
        ]

        views = json.dumps(cls.h_t_s(opts['views']))
        views = views.replace('"{0}'.format(cls.r), '')
        views = views.replace('{0}"'.format(cls.r), '')
        if 'outputs' in opts:
            computed_outputs = json.dumps(cls.h_t_s(opts['outputs'])).replace('"{0}'.format(cls.r), '').replace('{0}"'.format(cls.r), '')
        else:
            computed_outputs = '{}'
        # outputs_lines = [
        #     ''
        #     'for output in self.outputs:'
        # ]
        outputs_line = f'self.computed_outputs = {computed_outputs}'
        return_line = 'return data, {0}'.format(views)

        lines = before_lines + [i * 2 + l for l in init_lines + opts['code'].split('\n') + [outputs_line, return_line]]

        with open('m/temp/{0}.py'.format(name), 'w') as file:
            file.write('\n'.join(lines))
        p = 'm.temp.{0}'.format(name)
        if p in sys.modules:
            del sys.modules[p]
        m = getattr(importlib.import_module(p), name)

        m.c_o = o
        m.c_keys = keys

        if 'outputs' in opts and 'output' in opts['outputs']:
            m.c_outputs = opts['outputs']['output']
        else:
            m.c_outputs = []

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
    def load_from_file(cls, path): # loads sandbox
        modules_clss, es = cls.get_all_modules()
        try:
            modules = []
            with open(path, 'rb') as handle:
                saved_modules = json.load(handle)
                for saved_hash in saved_modules:
                    m_class = next(x for x in modules_clss if x.__name__ == saved_hash['class'])
                    m = m_class()  # __init__ the module
                    for p in ['o', 'gui_props', 'next_nodes', 'outputs']:
                        setattr(m, p, saved_hash[p])
                    modules.append(m)
                for m in modules:
                    m.next_nodes = [modules[n] for n in m.next_nodes]
                    print(m.outputs)
                    for o in m.outputs:
                        o['next_nodes'] = [modules[n] for n in o['next_nodes']]
                    print(m.outputs)



        except:
            import traceback
            es.append(traceback.format_exc())


        return modules, es



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
    def mask(cls, mat, mask):
        mat = mat.copy()
        a[a - 32 > 3] = np.nan
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