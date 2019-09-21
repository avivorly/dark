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
import os
import sys
import re


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
            if free:
                mone = 0
            else:
                mone = 1
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


    #  generate str from ROOT func
    def analizeFunc(self, f, places=False, replace = True):
        N = f.GetNpar()
        pars = {}
        fSTR = str(f.GetFormula())[21:]

        if replace:
            for i in range(N):
                p = f.GetParameter(i)
                if places:
                    p = round(pars[N], places)
                fSTR = fSTR.replace('[{0}]'.format(i), str(p))
        return fSTR

    def analizeTextFunc(self,f):
        dic = {}
        prms = re.findall('\[\d\]', f)
        dic['maxpar'] = max(map(lambda par: int(par[1:-1]), prms)) + 1
        dic['formula'] = f
        return dic




