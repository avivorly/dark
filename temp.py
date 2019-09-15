data = []
for j in range(o['virtual count']):
    j = j
    n = o['number {0}'.format(j)]
    for i in range(n):
        data.append(self.ROOT['gRandom'].Gaus(o['median {0}'.format(j)], o['sigma {0}'.format(j)]))
data = np.reshape(A, (o['row len'], len(data)/o['row len']))