from numpy import exp
from ROOTFitter import ROOTFitter
r = ROOTFitter()
r.ROOT = {'TF1':TF1,'gRandom':gRandom,'TH1F':TH1F}
ROOTFitter.ROOT = {'TF1':TF1,'gRandom':gRandom,'TH1F':TH1F}
# o = {'virtual count': 1, 'number 0': 1000, 'median 0': 0, 'sigma 0': 3}

data = self.data.flatten()

oo = {'virtual count': 1, 'simnum': 0, 'gausCount': 3, 'minRange': -150, 'maxRange': 700, 'y max': 0, 'showMin': -150,
      'showMax': 600, 'bins': 2000, 'decimal places': 3, 'isFree': False, 'gamma': '0.2', 'params': 'N', 'min 0':
          -100, 'max 0': 100, 'min 1': 200, 'max 1': 500, 'min 2': 500, 'max 2': 700, 'number 0': 10000, 'median 0': 0, 'sigma 0': 47}
dic = r.GausFit(data,oo)


ls = []
dic_copy = dic.copy()
dic_copy.pop('func')

for k, vls in dic_copy.items():
    va, er = map(lambda value: str(round(value, 3)), vls)
    ls.append(k)

f = r.analizeFunc(dic['func'], replace=True)




v = np.linspace(-300, 300, 1000)
from numpy import exp
def p(x):
    # from numpy import exp
    y = eval(f)
    return y


xs,ys = [],[]
for val in v:
    xs.append(v)
    ys.append(p(v))





for i in range(0, 3):
    print(i)

