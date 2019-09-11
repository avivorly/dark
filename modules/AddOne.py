from modules.Module import Module

class AddOne(Module):
    keys = [

    ]
    o = {'number': 2}
    def process(self):
        views = [
            ['I Just add 1', 'string', 'told you, i add one']
        ]

        data = self.data + 1

        return data, views