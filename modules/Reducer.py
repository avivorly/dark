from modules.Module import Module
import numpy as np
class Reducer(Module):
    keys = [
        ['top', 'spin'],
        ['bottom', 'spin'],
        ['right', 'spin'],
        ['left', 'spin']
    ]

    o = {
        'top': 240,
        'bottom': 300,
        'right': 60,
        'left': 80
    }
    def __init__(self):
        self.next_node = None
        super().__init__()
        self.o['mask path'] = 'may23/mask_skp_2hr_vddOFF_14_12.fits'

    def process(self):
        m = self.data.copy()
        rows = len(m)
        cols = len(m[0])


        m = np.delete(m, np.s_[0:self.o['top']], axis=0)
        m = np.delete(m, np.s_[len(m) - self.o['bottom']: len(m)], axis=0)

        m = np.delete(m, np.s_[0:self.o['left']], axis=1)
        m = np.delete(m, np.s_[len(m[0]) - self.o['right']: len(m[0])], axis=1)
        views = [
            ['reducer', 'image', [m, self.data]]
        ]

        return m, views