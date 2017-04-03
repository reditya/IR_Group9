import pysal
import numpy as np

w = sp.Writer()

x,y=np.indices((5,5))
x.shape=(25,1)
y.shape=(25,1)
data=np.hstack([x,y])

weight = np.ones((50,3))
wknn3 = pysal.weights.KNN(data, k = 3)
r = pysal.Maxp(wknn3, weight, floor = 5, floor_variable = np.ones((50, 1)), initial = 99)

r.regions
print str(r.regions)[1:-1]