from modules.Module import Module
import copy
class One(Module):
   def process(self):
        if hasattr(self, "data"):   data = self.data.copy() if getattr(self.data, "copy", False) else copy.deepcopy(self.data)
        o = copy.deepcopy(self.o)
        data = 1
        print(3)
        return data, [["my value","integer",1]]