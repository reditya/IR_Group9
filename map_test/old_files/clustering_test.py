import pysal
import shapefile as sp
import numpy as np

w = sp.Writer(sp.POLYGON)

"""
w.poly(parts=[[[1,1],[1,1],[1,1],[1,1],[1,1]]], shapeType=sp.POLYLINE)
w.poly(parts=[[[2,2],[2,2],[2,2],[2,2],[2,2]]], shapeType=sp.POLYLINE)

size = 5
point1 = []
for x in range(0,size):
	point1.append([4,4])
point1 = [point1]

point2 = []
for x in range(0,size):
	point2.append([4.5,4.5])
point2 = [point2]

point3 = []
for x in range(0,size):
	point3.append([4.8,4.8])
point3 = [point3]

w.poly(parts=point1, shapeType=sp.POLYLINE)
w.poly(parts=point3, shapeType=sp.POLYLINE)
w.poly(parts=point2, shapeType=sp.POLYLINE)
"""

for i in range(0,10):
	for j in range(0,10):
		point = [[[i,j],[i+1,j],[i+1,j+1],[i,j+1],[i,j]]]
		w.poly(parts=point, shapeType=sp.POLYLINE)
weight_list = np.ones((100,3))
point = 0;
for i in range(0,10):
	for j in range(0,10):
		if i < 5:
			weight_list[point][1] = 0
		point = point + 1

w.save("Document/test4/poly1")
w = pysal.weights.Queen.from_shapefile("Document/test4/poly1.shp")
pci = np.array([[1,1,1],[0,0,0], [0,1,0], [0,1,0], [0,1,0] ])

r = pysal.Maxp(w, pci, floor = 1, floor_variable = np.ones((5, 1)), initial = 20)
r.regions
print str(r.regions)[1:-1]