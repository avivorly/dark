from modules.Module import Module
import copy
class A(Module):
    def process(self):
        if hasattr(self, "data"):   data = self.data.copy() if getattr(self.data, "copy", False) else copy.deepcopy(self.data)
        o = copy.deepcopy(self.o)
        1234
        return data, []