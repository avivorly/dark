import ROOT
import dill


with open('ROO', 'rb') as file:
    B = dill.load(file)


