from modules.Module import Module
import copy
class AddNum(Module):
   def process(self):
        if hasattr(self, "data"):   data = self.data.copy() if getattr(self.data, "copy", False) else copy.deepcopy(self.data)
        o = copy.deepcopy(self.o)
        data = data + 1
        return data, [["a","string",data]]