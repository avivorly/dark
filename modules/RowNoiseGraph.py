from modules.Module import Module
import numpy as np
class RowNoiseGraph(Module):
    keys = [

    ]
    def __init__(self):
        self.next_node = None
        super().__init__()

    def process(self):
        columns = self.columns_of(self.data)
        xs = []
        ys = []
        for i in range(len(columns)):
            nan_filtered = [n for n in columns[i] if not np.isnan(n)]
            xs.append(i)
            ys.append([np.average(nan_filtered)])

        views = [
            ['average as function of row', 'graph', [xs, ys]]
        ]

        return self.data, views