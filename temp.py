import numpy as np
from numpy.linalg import norm
p1 = np.array((1,2))
p2 = np.array((3,4))
p3 = np.array((5,5))
print(p2-p1)
d = norm(np.cross(p2-p1, p1-p3))/norm(p2-p1)
print(d)

