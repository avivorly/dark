from modules.Module import Module
import numpy as np
class OpenFile(Module):
    keys = [
        ['path', 'file']
    ]
    o = {'path' : 'may23/proc_skp_2hr_vddOFF_14_12.fits'}

    def process(self):
        data = self.open_file(self.o['path'])
        views = [
            ['open file', 'image', [data]]
        ]


        return data, views