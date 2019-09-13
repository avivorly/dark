from modules.Module import Module
import numpy as np
class Dist(Module):
    keys = [
        ['bins', 'number']
    ]
    def __init__(self):
        self.next_node = None
        super().__init__()
        self.o['bins'] = 50

    def process(self):
        data = self.data
        res = []
        keys = []
        vals = []
        for i in range(0, len(data)):
            for j in range(0, len(data[i])):
                v = data[i][j]
                if not np.isnan(v):
                    temps = []
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
                        if ii < len(data) and jj < len(data[0]):
                            t = data[ii][jj]
                            if not np.isnan(t):
                                temps.append(t)
                    if temps:
                        res.append([v, np.average(temps)])
                        keys.append(v)
                        vals.append(np.average(temps))
        res = sorted(res, key=lambda val: val[0])


        if False:
            n = self.o['bins']
            new_ress = [res[i::n] for i in range(n)]

            xs = []
            ys = []
            for res in new_ress:
                x = (res[0][0] + res[-1][0]) / 2
                y = np.average(list(map(lambda v: v[1], res)))
                xs.append(x)
                ys.append(y)
        else:

            ranges = np.linspace(np.min(keys), np.max(keys), self.o['bins'])
            # ranges = np.linspace(-200, 400, self.o['bins'])
            xs = []
            ys = []
            l = len(ranges)
            temp = []
            temp_res = []
            for i in range(1, l-1):
                for j in range(0, len(keys)):
                    k = keys[j]
                    v = vals[j]
                    # if i == 0:
                    #     flag = k < ranges[1]
                    #
                    # elif i == l -1:
                    #     flag = k > ranges[l-2]
                    # else:
                    flag = ranges[i - 1] < k < ranges[i + 1]
                    if flag:
                        temp.append(v)
                    else:
                        temp_res.append(v)
                xs.append(ranges[i])
                ys.append(np.average(temp))








        views = [
            ['volt to average', 'graph', [xs, ys]]
        ]

        return data, views