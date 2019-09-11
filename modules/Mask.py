from modules.Module import Module
import numpy as np
class Mask(Module):
    keys = [
        ['l1', 'spin'],
        ['l2', 'spin'],
        ['l3', 'spin'],
        ['degree', 'spin'],
        ['line', 'spin']

    ]
    o = {
        'l1': 20000,
        'l2': 500,
        'l3': 300,
        'degree': 3,
        'line': 0,

    }

    def process(self):
        m = self.data.copy()
        xlen = len(m)
        ylen = len(m[0])
        sm = np.ones((xlen, ylen))
        max = self.o['l1']
        for i in range(xlen):
            for j in range(0, ylen):
                if m[i][j] >= max:
                    m[i][j] = np.nan
                    if self.o['line'] == 1:
                        m[i, j: ylen-1] = np.nan

                    #
                #     for x, y in self.ge
                #     t_neighbors_indices_by_range(i, j, xlen, ylen, 1):


                            #


                        # sm[i][j] = 1



        views = [
            ['3 mask', 'image', [self.data, sm, m]]
        ]

        return self.data, views