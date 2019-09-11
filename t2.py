import os
from contextlib import contextmanager

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

import ROOT
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




class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'dark matter'
        self.initUI()

    def initUI(self):
        self.setGeometry(10, 10, 2500, 1600)
        self.setts = {}
        self.rangesPars = {}
        self.virtuals = {}
        self.results = QTableWidget()
        self.groups = {}


        wid = QWidget(self)
        self.setCentralWidget(wid)
        grid = QGridLayout()
        wid.setLayout(grid)
        grid.setSpacing(10)




        # files group

        loadbox = QGroupBox()
        loadLay = QHBoxLayout()
        loadbox.setLayout(loadLay)
        grid.addWidget(loadbox, 0, 0)

        self.groups['files'] = loadbox

        g = QGroupBox()
        l = QVBoxLayout() ;
        loadLay.addWidget(g)
        g.setLayout(l)


        self.files = QtWidgets.QListWidget()
        self.files.itemDoubleClicked.connect(self.loadData)
        l.addWidget(self.files)

        self.pushButton = QtWidgets.QPushButton('open folder')
        self.pushButton.clicked.connect(self.openFolder)
        l.addWidget(self.pushButton)

        # virtuals

        virgroup = QGroupBox()
        virlaybox = QHBoxLayout()
        virgroup.setLayout(virlaybox)

        loadLay.addWidget(virgroup)



        g = QGroupBox()
        l = QVBoxLayout();

        g.setLayout(l)

        virlaybox.addWidget(g)



        self.addSpins(l,['virtual count'], defval = 1)

        vg = QGroupBox()
        vl = QGridLayout()
        vg.setLayout(vl)
        l.addWidget(vg)

        self.dynamicVirtualBox = vl
        l.setSpacing(0)

        self.virtualSend = QtWidgets.QPushButton('analyze virtual data')
        self.virtualSend.clicked.connect(self.virtualBtn)
        l.addWidget(self.virtualSend)

        # multi virtuals

        g = QGroupBox()
        multilay = QVBoxLayout()

        g.setLayout(multilay)
        virlaybox.addWidget(g)

        multilay.addWidget(QLabel("simulation num"))

        self.addSpins(multilay, ['simnum'])
        multilay.addWidget(QLabel("param"))
        self.par = QLineEdit()
        multilay.addWidget(self.par)
        self.simbtn = QtWidgets.QPushButton('start simulation')
        self.simbtn.clicked.connect(self.start_sim)
        multilay.addWidget(self.simbtn)
        # settings group

        g = QGroupBox()
        self.groups['setts'] = g
        l = QHBoxLayout()
        g.setLayout(l)
        grid.addWidget(g, 1, 1)

        gg = QGroupBox()
        ll = QGridLayout()
        gg.setLayout(ll)
        l.addWidget(gg)



        spin_names = ["gausCount", "minRange", "maxRange",'y max', 'showMin', 'showMax', 'bins', 'decimal places']
        rows = self.addSpins(ll, spin_names)

        sigmaBox = QCheckBox("united sigma")
        self.setts['sigmaBox'] = sigmaBox
        ll.addWidget(QLabel("united sigma"), rows, 0)
        ll.addWidget(sigmaBox, rows, 1)
        rows += 1

        gammaLine = QLineEdit()
        self.setts['gamma'] = gammaLine
        ll.addWidget(QLabel("gamma"), rows, 0)
        ll.addWidget(gammaLine, rows, 1)
        rows += 1
        gammaLine = QLineEdit()
        self.setts['params'] = gammaLine
        ll.addWidget(QLabel("params"), rows, 0)
        ll.addWidget(gammaLine, rows, 1)

        defs = {
            'bins': 2000,
            'gausCount': 3,
            'sigmaBox': True,
            'gamma': '0.2',
            'minRange': -150,
            'maxRange': 700,
            'showMin': -150,
            'showMax': 600,
            'decimal places': 3,
            'params': 'N'
        }
        self.set_defs_on_widgets(defs, self.setts)

        self.setts['gausCount'].valueChanged.connect(self.create_dynamic_sett)
        self.setts['virtual count'].valueChanged.connect(self.create_virtual_sett)


        gg = QGroupBox()
        ll = QGridLayout()
        gg.setLayout(ll)
        l.addWidget(gg)



        self.dynamicBox = ll
        ll.setSpacing(0)

        c = 'skp_2hr_vddOFF_20_15'
        self.dic = 'may23'
        self.create_dynamic_sett()

        # results group
        g = QGroupBox();
        self.groups['results'] = g
        l = QVBoxLayout();
        g.setLayout(l)
        grid.addWidget(g, 2, 0)



        self.logbtn = QPushButton('show log')
        self.logbtn.clicked.connect(self.showLog)

        self.thisfunc = QPushButton('use this func')
        self.thisfunc.clicked.connect(self.fromfunc)


        l.addWidget(self.results)
        self.formulainputbox = QLineEdit()
        self.formulabox = QLineEdit()
        l.addWidget(self.formulainputbox)

        l.addWidget(self.formulabox)
        l.addWidget(self.logbtn)
        l.addWidget(self.thisfunc)
        # mask group

        g = QGroupBox();
        self.groups['mask'] = g
        l = QVBoxLayout();
        g.setLayout(l)
        grid.addWidget(g, 0, 1)


        self.mask_box = l

        self.reset_mask()

        # fit group


        g = QGroupBox();
        self.groups['fit'] = g
        l = QVBoxLayout();
        g.setLayout(l)
        grid.addWidget(g, 1, 0)
        self.fit = PlotCanvas(self)
        l.addWidget(self.fit)
        g.setObjectName("StatusGroupBox")  # Changed here...
        self.statusgb = g

        self.show()
        self.create_virtual_sett()
        # self.openFolder(forcePath='may23')

        menubar = self.menuBar()
        SkipsMenu = menubar.addMenu('Skips')


        a = QAction('skip all mask', self, checkable=True)
        # viewStatAct.triggered.connect(self.toggleMenu)

        SkipsMenu.addAction(a)
        self.maskskip = a


        b = QAction('skip analyze mask', self, checkable=True)
        b.setChecked(True)
        # viewStatAct.triggered.connect(self.toggleMenu)

        SkipsMenu.addAction(b)
        self.sdmask = b

        ShowMenu = menubar.addMenu('Show')
        self.views = {}
        for group in self.groups.keys():
            QA = QAction(group, self, checkable=True)
            QA.setChecked(True)
            QA.triggered.connect(self.viewUpdate)
            ShowMenu.addAction(QA)
            self.views[group] = QA

        QA = QAction('show all', self)
        QA.triggered.connect(partial(self.updateAllViews, True))
        ShowMenu.addAction(QA)

        QA = QAction('hide all', self)
        QA.triggered.connect(partial(self.updateAllViews, False))
        ShowMenu.addAction(QA)

    def updateAllViews(self, isON):
        for name, group in self.groups.items():
            group.setVisible(isON)
            self.views[name].setChecked(isON)

    def viewUpdate(self):
        for name, group in self.groups.items():
            group.setVisible(self.views[name].isChecked())

    def addSpins(self, l,names, logger = None, defval = False):
        rows = 0
        for name in names:
            spin = QSpinBox()
            spin.setRange(-10000, 10000)
            if defval:
                spin.setValue(defval)
            if type(l) is QGridLayout:
                l.addWidget(QLabel(name), rows, 0)
                l.addWidget(spin, rows, 1)
            else:
                l.addWidget(QLabel(name))
                l.addWidget(spin)


            self.setts[name] = spin
            rows += 1
        return rows

    def red(self):
        self.statusgb.setStyleSheet("QGroupBox#StatusGroupBox { border: 1px solid red;}")
        self.statusgb.repaint()


    def green(self):
        self.statusgb.setStyleSheet("QGroupBox#StatusGroupBox { border: 1px solid green;}")
        self.statusgb.repaint()

    def reset_mask(self):
        box = self.mask_box

        self.clean_box(box)
        l = box.layout()

        w = 38
        h = 59
        z = 0.12
        self.combCN = PlotCanvas(width=w * z * 2, height=h * z, dpi=1)
        self.toolbar = NavigationToolbar(self.combCN, self)
        l.addWidget(self.toolbar)
        l.addWidget(self.combCN)

        self.maskRatio = QtWidgets.QLabel()
        l.addWidget(self.maskRatio)


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

    def virtualBtn(self):
        self.loadData(fromfile = False)

    def GausFit(self, data, o, manual = False):
        h1 = ROOT.TH1F('Volts fit', 'histogram fit; volts [e]; num of events', o['bins'], o['minRange'], o['maxRange'])
        for val in data:
            h1.Fill(val)
        if not manual:
            free = not self.getSet('sigmaBox')

            num_of_gauses = o['gausCount']
            fits = []
            for i in range(num_of_gauses):
                fit = ROOT.TF1("gaus-{0}".format(i), 'gaus', o['min {0}'.format(i)], o['max {0}'.format(i)])
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
            total = ROOT.TF1("mstotal", formula, o['minRange'], o['maxRange'])

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
            total = ROOT.TF1("mstotal", manual['formula'], o['minRange'], o['maxRange'])
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
            # print([i,par_name])
            res[par_name] = [total.GetParameter(i), total.GetParError(i)]
        return res

    #  create virtual data of two histograms
    def create_data(self, o):
        data = []
        for j in range(self.getSet('virtual count')):
            j = j
            n = o['number {0}'.format(j)]
            for i in range(n):
                data.append(ROOT.gRandom.Gaus(o['median {0}'.format(j)], o['sigma {0}'.format(j)]))
        return (data)

    def start_sim(self, par = 'median 0'):
        self.setts['gausCount'].setValue(1)

        n = self.getSet('simnum')
        pars = []
        for i in range(n):
            o = self.getAllPars()
            pars.append(self.GausFit(self.create_data(o), o)[self.get_value_from_widget(self.par)][0])
        self.loadData(fromfile=False, data_force=pars)

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

    def file_matrix(self, quad, path):
        return fits.open(path)[quad].data

    def readfile(self, c, quad=0):

        CONST_nonReal = 7  # used to skipped virtual values
        with fits.open(self.dic + '/proc_' + c + '.fits') as data:
            events_matrix = data[quad].data
            with fits.open(self.dic + '/mask_' + c + '.fits') as mask:
                mask_matrix = mask[quad].data
                rowsLen = len(events_matrix)
                colsLen = len(events_matrix[0])
                events = np.full((rowsLen, colsLen), np.nan)

                for i in range(0, rowsLen):
                    for j in range(CONST_nonReal, colsLen):
                        if mask_matrix[i][j] - 32 in [0, 1, 2, 3]:
                            events[i][j] = events_matrix[i][j]
        return events

    def showLog(self):
        mb =  QMessageBox
        # mb.setBaseSize(QtCore.QSize(600, 120));
        mb.about(self, "ROOT original logs", self.logged)

    def flat(self, matrix):
        return filter(lambda cell: not np.isnan(cell), matrix.flatten())

    def create_dynamic_sett_for_func(self, func_dit):
        defs = {
            'min 0': -100,
            'max 0': 100,
            'min 1': 200,
            'max 1': 500,
            'min 2': 500,
            'max 2': 700,
        }


        self.rangesPars = {}
        self.create_box(['init'], func_dit['maxpar'], defs, self.dynamicBox, self.rangesPars, addName=True)


        self.virb = QPushButton('manual analyze file')
        self.virb.clicked.connect(self.loadManualFilelData)
        self.dynamicBox.addWidget(self.virb)


        self.filb = QPushButton('manual analyze virtual')
        self.filb.clicked.connect(self.loadManuaLVirtualData)
        self.dynamicBox.addWidget(self.filb)

    def create_dynamic_sett(self):
        defs = {
            'min 0': -100,
            'max 0': 100,
            'min 1': 200,
            'max 1': 500,
            'min 2': 500,
            'max 2': 700,
        }

        self.rangesPars = {}
        self.create_box(['min', 'max'], self.getSet('gausCount'), defs, self.dynamicBox, self.rangesPars)



        self.rfilb = QPushButton('analyze virtual')
        self.rfilb.clicked.connect(self.loadVirtuallData)
        self.dynamicBox.addWidget(self.rfilb)

        self.rvirb = QPushButton('analyze file')
        self.rvirb.clicked.connect(self.loadFilelData)
        self.dynamicBox.addWidget(self.rvirb)

    def create_virtual_sett(self):
        defs = {
            'number 0': 10000,
            'median 0': 0,
            'sigma 0': 47,
            'number 1': 1000,
            'median 1': 300,
            'sigma 1': 47,
            'number 2': 100,
            'median 2': 600,
            'sigma 2': 47,
        }
        self.virtuals = {}
        self.create_box(['number', 'median', 'sigma'], self.getSet('virtual count'), defs,self.dynamicVirtualBox, self.virtuals)

    def clean_box(self,box):
        for i in reversed(range(box.layout().count())):
            box.itemAt(i).widget().setParent(None)

    def create_box(self, vars, count, defs, box, dic, addName = False):
        self.clean_box(box)
        rows = 0

        for i in range(count):
            for name in vars:
                full_name = name + ' ' + str(i)
                temp = self.create_spin()
                if type(box.layout()) is QGridLayout:
                    box.addWidget(QLabel(full_name), rows, 0)
                    box.addWidget(temp, rows, 1)
                    if addName:
                        n = 'name {0}'.format(i)
                        tempbox = QLineEdit()
                        tempbox.setText(n)
                        dic[n]=tempbox
                        box.addWidget(tempbox, rows, 2)

                else:
                    box.addWidget(QLabel(full_name))
                    box.addWidget(temp)

                rows += 1

                dic[full_name] = temp


                self.set_defs_on_widgets(defs, dic)

    def create_spin(self):
        temp = QSpinBox()
        temp.setRange(-2147483648, 2147483647)
        return temp

    def set_defs_on_widgets(self, defs, ws):
        for name, w in ws.items():
            if name in defs.keys():

                method = 'setValue'
                mdic = {
                    QCheckBox: 'setChecked',
                    QLineEdit: 'setText'
                }
                if type(w) in mdic.keys():
                    method = mdic[type(w)]
                eval('w.{0}(defs[name])'.format(method))

    def get_value_from_widget(self, w):
        method = 'value'
        mdic = {
            QCheckBox: 'isChecked',
            QLineEdit: 'text'
        }
        if type(w) in mdic.keys():
            method = mdic[type(w)]
        return eval('w.{0}()'.format(method))

    def buildManualDict(self):
        funcstr = self.get_value_from_widget(self.formulainputbox)
        fdit = self.analizeTextFunc(funcstr)
        nms = []
        inits  = []
        for i in range(fdit['maxpar']):
            nms.append(self.get_value_from_widget(self.rangesPars['name {0}'.format(i)]))
            inits.append(self.get_value_from_widget(self.rangesPars['init {0}'.format(i)]))
        fdit['names'] = nms
        fdit['inits'] = inits
        return fdit

    def loadManuaLVirtualData(self, dic):
        self.loadData(manprs=self.buildManualDict(), fromfile=False)

    def loadManualFilelData(self):
        self.loadData(manprs=self.buildManualDict(), fromfile=True)

    def loadFilelData(self):
        self.loadData(fromfile=True)

    def loadVirtuallData(self):
        self.loadData(fromfile=False)


    def loadData(self, fromfile = True, manprs=None,path = None, data_force = None):
        self.red()
        roundTo = self.getSet('decimal places')
        self.s = datetime.datetime.now()
        o = self.getAllPars()
        if fromfile and path is None:

            path = self.files.selectedItems()[0].text()
        if path:
            fromfile = True
        if fromfile:
            self.reset_mask()
            c = path
            self.combMat = self.readfile(c)
            if not self.maskskip.isChecked():



                self.procMat = self.file_matrix(0, self.dic + '/proc_' + c + '.fits')
                self.maskMat = self.file_matrix(0, self.dic + '/mask_' + c + '.fits')

                self.combCN.plot2([self.procMat, self.combMat, self.maskMat], float(self.getSet('gamma')))
                print(self.maskskip.isChecked())
                print(self.sdmask.isChecked())
                if not self.sdmask.isChecked():
                    maskSum = 0.0
                    maskMone = 0
                    stamSum = 0.0
                    stamMone = 0
                    stamarr = []
                    maskarr = []
                    for i in range(0, len(self.combMat)):
                        for j in range(0, len(self.combMat[0])):
                            v = self.combMat[i][j]
                            if not np.isnan(v):
                                flag = True
                                for (ii, jj) in [
                                    [i + 1, j],
                                    [i - 1, j],
                                    [i + 1, j + 1],
                                    [i - 1, j - 1],
                                    [i, j - 1],
                                    [i, j + 1],
                                    [i + 1, j - 1],
                                    [i - 1, j + 1],
                                ]:
                                    if np.isnan(self.combMat[ii][jj]):
                                        flag = False
                                if flag:
                                    stamarr.append(v)
                                    stamSum += v # TODO add power number to maximize to differnce like v**gamma
                                    stamMone += 1
                                else:
                                    maskarr.append(v)
                                    maskSum += v
                                    maskMone += 1
                    args = [maskSum / maskMone, np.std(maskarr), maskMone, stamSum / stamMone, np.std(stamarr), stamMone]
                    print(args)
                    args = map(lambda f: str(round(f, roundTo)), args)
                    arr = []
                    for a in args:
                        arr.append(a)
                    print(arr)
                    self.maskRatio.setText("mask: {0} SD: {1} count: {2} | normal: {3} SD: {4} count: {5}".format(*list(arr)))

            # print(datetime.datetime.now() - self.s)
            # TODO add min max to mask
            data = self.flat(self.combMat)
        elif not data_force:
            data = self.create_data(o)
        else:
            data = data_force


        dic = self.GausFit(data, o, manprs)

        mone = 0
        ls = []
        dic_copy = dic.copy()
        dic_copy.pop('func')

        self.results.setRowCount(100)
        self.results.setColumnCount(2)

        for k, vls in dic_copy.items():
            va, er = map(lambda value: str(round(value, roundTo)), vls)
            ls.append(k)

            self.results.setItem(mone, 0, QTableWidgetItem(va))
            self.results.setItem(mone, 1, QTableWidgetItem(er))

            mone += 1
        self.results.setHorizontalHeaderLabels(['value', 'error'])
        self.results.setVerticalHeaderLabels(ls)
        self.results.setRowCount(mone)
        self.results.update()


        self.formulabox.setText(self.analizeFunc(dic['func'], places=roundTo))
        self.formulainputbox.setText(self.analizeFunc(dic['func'], replace=False))

        # data = self.flat(self.combMat)
        if fromfile: # TODO wht again
            data = self.flat(self.combMat)
        elif not data_force:
            data = self.create_data(o)
        else:
            data = data_force


        self.fit.plot(data, self.analizeFunc(dic['func'], replace=True), self.getSet('bins'),
                      self.getSet('showMin'), self.getSet('showMax'),self.getSet('minRange'),self.getSet('maxRange'), self.getSet('y max'))

        self.green()
    def getSet(self, strr):
        return self.get_value_from_widget(self.setts[strr])

    def getAllPars(self):
        o = {}
        for dic in [self.setts, self.rangesPars, self.virtuals]:
            for k, w in dic.items():
                o[k] = self.get_value_from_widget(w)


        return o

    def openFolder(self, forcePath = None):
        if forcePath not in (None,False):
            self.dic = forcePath
            path = self.dic
        else:
            path = QFileDialog.getExistingDirectory(None, 'Select Directory')
            self.dic = path
        fls = []
        conts = []
        for f in os.listdir(path):
            fls.append(f)
        for f in fls:
            type = os.path.splitext(f)[1][1:]

            if type == 'fits':

                makaf = f.find('_')
                content = f[makaf + 1:-5]
                if not content in conts:
                    if ('mask_' + content + '.fits') in fls and ('proc_' + content + '.fits') in fls:
                        conts.append(content)
        self.files.clear()
        self.files.addItems(sorted(conts))

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


# TODO add chi^2 even on L
# TODO check liron task - to continuee until converged
# TODO add min max mask
# TODO check fit program mini ?
# TODO ask tomer if investing time for tests
# TODO add selected file name
# TODO add export results to file