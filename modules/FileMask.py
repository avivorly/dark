from modules.Module import Module
import numpy as np
class FileMask(Module):
    keys = [
        ['mask path', 'file']
    ]
    def __init__(self):
        self.next_node = None
        super().__init__()
        self.o['mask path'] = 'may23/mask_skp_2hr_vddOFF_14_12.fits'

    def process(self):
        mask_matrix = self.open_file(self.o['mask path'])
        data = self.mask(self.data, mask_matrix)
        views = [
            ['3 mask', 'image', [data, mask_matrix, self.data]]
        ]

        return data, views