import os
from contextlib import contextmanager
from numpy import exp
def fileno(file_or_fd):
    fd = getattr(file_or_fd, 'fileno', lambda: file_or_fd)()
    if not isinstance(fd, int):
        raise ValueError("Expected a file (`.fileno()`) or a file descriptor")
    return fd
@contextmanager
def stdout_redirected(to=os.devnull, stdout=None):
    if stdout is None:
       stdout = sys.stdout

    stdout_fd = fileno(stdout)
    # copy stdout_fd before it is overwritten
    #NOTE: `copied` is inheritable on Windows when duplicating a standard stream
    with os.fdopen(os.dup(stdout_fd), 'wb') as copied:
        stdout.flush()  # flush library buffers that dup2 knows nothing about
        try:
            os.dup2(fileno(to), stdout_fd)  # $ exec >&to
        except ValueError:  # filename
            with open(to, 'wb') as to_file:
                os.dup2(to_file.fileno(), stdout_fd)  # $ exec > to
        try:
            yield stdout # allow code to be run with the redirected stdout
        finally:
            # restore stdout to its previous value
            #NOTE: dup2 makes stdout_fd inheritable unconditionally
            stdout.flush()
            os.dup2(copied.fileno(), stdout_fd)  # $ exec >&copied
from functools import partial
from PyQt5.QtWidgets import QTableWidgetItem
import datetime
from PyQt5 import QtWidgets
import numpy as np
from numpy import exp
from astropy.io import fits
import os
import sys
import re
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QFileDialog

import random
# exec(open("/home/aviv/avivsroot/lib/aviv_root.py").read())
from PyQt5.QtWidgets import (QMessageBox)
from PyQt5.QtWidgets import QMainWindow, QAction
from PyQt5.QtWidgets import (QApplication, QCheckBox,
                             QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QSizePolicy,
                             QSpinBox, QTableWidget,
                             QVBoxLayout, QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=9, height=4, dpi=50):
        fig = Figure(figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, \
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.ax = None
        self.axArr = None

    def plot(self, data, f, bins, vmin, vmax,fmin,fmax,ymax):
        v = np.linspace(vmin, vmax, 1000)
        def p(x):
            y = eval(f)
            return y

        if not self.ax:
            self.ax = self.figure.add_subplot(111)
        self.ax.clear()
        self.ax.set_xlim(vmin, vmax)

        self.ax.plot(v, p(v).astype(np.float))

        self.ax.hist(list(data), int(bins*((vmax-vmin)/(fmax-fmin))), (vmin, vmax))
        self.figure.tight_layout()

        self.ax.set_ylim(bottom=0)
        if ymax != 0:
            self.ax.set_ylim(top=ymax)
        self.draw()



    def plot2(self, matArr, gamma):
        newMatarr = []
        for mat in matArr:
            nm = np.power(np.absolute(mat), gamma)
            for i in range(0, len(mat)):
                nm[i] *= np.sign(mat[i])
            newMatarr.append(nm)



        if self.axArr is not None:
            for i in range(0, len(self.axArr)):
                ax = self.axArr[i]
                self.figure.delaxes(ax)

        self.axArr = self.figure.subplots(1, 3)


        for i in range(0, len(self.axArr)):
            ax = self.axArr[i]
            ax.clear()
            ax.axis('off')

            # ax.margins(1000)
            ax.imshow(newMatarr[i], cmap='hot')
        self.figure.tight_layout()
        self.draw()


class ROOTFitter:
    def make_gaus(self, sigma_index, names, ii):
        if sigma_index is not None:
            name_of_gauss = str(int(ii / 2))
            names[sigma_index] = 'global sigma'
            names[ii] = 'amp {0}'.format(name_of_gauss)
            names[ii + 1] = 'median {0}'.format(name_of_gauss)
            return ['[{0}]*exp(-0.5*((x-[{1}])/[{2}])**2)'.format(ii, ii + 1, sigma_index), 2]
        else:
            name_of_gauss = str(int(ii / 3))
            names[ii] = 'amp {0}'.format(name_of_gauss)
            names[ii + 1] = 'median {0}'.format(name_of_gauss)
            names[ii + 2] = 'sigma {0}'.format(name_of_gauss)
            return ['[{0}]*exp(-0.5*((x-[{1}])/[{2}])**2)'.format(ii, ii + 1, ii + 2), 3]

    def GausFit(self, data, o, manual = False):
        h1 = self.ROOT['TH1F']('Volts fit', 'histogram fit; volts [e]; num of events', o['bins'], o['minRange'], o['maxRange'])
        for val in data:
            h1.Fill(val)
        if not manual:
            free = o['isFree']

            num_of_gauses = o['gausCount']
            fits = []
            for i in range(num_of_gauses):
                fit = self.ROOT['TF1']("gaus-{0}".format(i), 'gaus', o['min {0}'.format(i)], o['max {0}'.format(i)])
                fit.SetParName(0, 'amp {0}'.format(i))
                fit.SetParName(1, 'median {0}'.format(i))
                fit.SetParName(2, 'sigma {0}'.format(i))
                fits.append(fit)

            formulas = []
            names = {}
            mone = 0
            if not free:
                mone += 1
            for i in range(num_of_gauses):
                if free:
                    d = self.make_gaus(None, names, mone)
                    formulas += [d[0]]
                    mone += d[1]
                else:
                    d = self.make_gaus(0, names, mone)
                    formulas += [d[0]]
                    mone += d[1]
            formula = '+'.join(formulas)
            total = self.ROOT['TF1']("mstotal", formula, o['minRange'], o['maxRange'])

            for gausFit in fits:
                h1.Fit(gausFit, 'RNQ')

            for i, par_name in names.items():
                total.SetParName(i, par_name)

            if not free:
                total.SetParameter(0, fits[0].GetParameter(2))
                total.SetParName(mone, 'Global Sigma ' + str(i))

            for fit in fits:
                for i in [0, 1, 2]:
                    indx = total.GetParNumber(fit.GetParName(i))
                    total.SetParameter(indx, fit.GetParameter(i))
        else:
            total = self.ROOT['TF1']("mstotal", manual['formula'], o['minRange'], o['maxRange'])
            names = {}
            for i in range(manual['maxpar']):
                total.SetParameter(i, manual['inits'][i])
                total.SetParName(i, manual['names'][i])
                names[i] = manual['names'][i]

# call limit - 4, STATUS=CONVERGED = 0
        with open('a', 'w') as f, stdout_redirected(f):
            x = h1.Fit(total, 'R+S' + o['params'])

        with open('a', 'r') as f:
            self.logged = f.read()

        res = {}
        res['func'] = total

        for i, par_name in names.items():
            res[par_name] = [total.GetParameter(i), total.GetParError(i)]
        return res

    def analizeFunc(self, f, places=False, replace = True):
        N = f.GetNpar()
        pars = {}
        fSTR = str(f.GetFormula())[21:]
        for i in range(0, N):
            if replace:
                pars[N] = f.GetParameter(i)
                if places:
                    pars[N] = round(pars[N], places)
                fSTR = fSTR.replace('[{0}]'.format(i), str(pars[N]))
        return fSTR

    def analizeTextFunc(self,f):
        dic = {}
        prms = re.findall('\[\d\]', f)
        dic['maxpar'] = max(map(lambda par: int(par[1:-1]), prms)) + 1
        dic['formula'] = f
        return dic

    def fromfunc(self):
        funcstr = self.get_value_from_widget(self.formulainputbox)
        fdit = self.analizeTextFunc(funcstr)
        self.create_dynamic_sett_for_func(fdit)

    def create_data(self, o):
        data = []
        for j in range(o['virtual count']):
            j = j
            n = o['number {0}'.format(j)]
            for i in range(n):
                data.append(self.ROOT['gRandom'].Gaus(o['median {0}'.format(j)], o['sigma {0}'.format(j)]))
        return (data)

# #
# r = ROOTFitter()
# o = {'virtual count': 1, 'number 0': 1000, 'median 0': 0, 'sigma 0': 3}
#
# data = r.create_data(o)
#
# oo = {'virtual count': 1, 'simnum': 0, 'gausCount': 3, 'minRange': -150, 'maxRange': 700, 'y max': 0, 'showMin': -150, 'showMax': 600, 'bins': 2000, 'decimal places': 3, 'isFree': False, 'gamma': '0.2', 'params': 'N', 'min 0': -100, 'max 0': 100, 'min 1': 200, 'max 1': 500, 'min 2': 500, 'max 2': 700, 'number 0': 10000, 'median 0': 0, 'sigma 0': 47}
# dic = r.GausFit(data,oo)
#
#
# ls = []
# dic_copy = dic.copy()
# dic_copy.pop('func')
#
# for k, vls in dic_copy.items():
#     va, er = map(lambda value: str(round(value, 3)), vls)
#     ls.append(k)
#
# f = r.analizeFunc(dic['func'], replace=False)
#
#
#
#
#
# v = np.linspace(-300, 300, 1000)
# def p(x):
#     y = eval(f)
#     return y
#
#
# xs,ys = [],[]
# for val in v:
#     xs.append(v)
#     ys.append(v)
#
#


