from __future__ import division
from operator import itemgetter

debug = False

def ccw(p1, p2, p3):
	"""
	ccw > 0: counter-clockwise turn
	ccw < 0: clockwise turn
	ccw = 0: colinear
	ccw is a determinant that gives the signed area of the triangle formed by p1, p2 and p3
	"""
	ccw = (p2[0] - p1[0])*(p3[1] - p1[1]) - (p2[1] - p1[1])*(p3[0] - p1[0])

	if debug:
		print 'ccw args:'
		pprint((p1,p2,p3))
		print 'ccw: %s' % ccw

	return ccw

def theta(p0,pi):
	""" This doesn't actually return theta; however, it maintains the same ordering. """
	dx = pi[0]-p0[0]
	dy = pi[1]-p0[1]
	return dy*dy / ( dx*dx + dy*dy )

def dist(p0,p1,p2):
	""" Breaks ties in sorting vertices. Returns -1 if p1 is closer to p0, 1 if p2 is closer to p0 """
	dx1 = p1[0]-p0[0]
	dy1 = p1[1]-p0[1]
	r1 = dx1*dx1 + dy1*dy1

	dx2 = p2[0]-p0[0]
	dy2 = p2[1]-p0[1]
	r2 = dx2*dx2 + dy2*dy2

	if r1 < r2:
		return -1
	else:
		return 1



def convex_hull(vs):
	"""Graham's Convex Hull Algorithm"""

	# if debug:
	# 	print('\nVertices:')
	# 	pprint(vs)

	p0 = min(vs, key=itemgetter(1,0)) # find bottom left point
	i = vs.index(p0)
	vs[0], vs[i] = vs[i], vs[0]  # swap min point with vs[0]
	# Sort remainder of vertices by polar angle with p0. Break ties by distance.
	vs[1:] = sorted(vs[1:], lambda x,y: cmp(theta(p0,x), theta(p0,y)) if cmp(theta(p0,x), theta(p0,y)) else dist(p0,x,y))

	if debug:
		# print('\np0:')
		# pprint(p0)
		print('\nSorted pts:')
		pprint(vs)

	vs.insert(0,vs.pop())  # place final point at vs[0]

	hull = vs[0:2]
	m = 2
	if debug:
		print('Stack:')
	for i in range(m, len(vs)):

		if debug:
			print('i: %d, m: %d ' % (i,m))
			pprint(hull)
		while ccw(hull[-1], hull[-2], vs[i]) >= 0:
			hull.pop()
			m -= 1
			if debug:
				print('m: %d ' % (m))
				pprint(hull)
		hull.append(vs[m])
		m += 1
		vs[i], vs[m] = vs[m], vs[i]
		if debug:
			print('m: %d ' % (m))
			pprint(hull)

	return hull


if __name__ == '__main__':
	from pprint import pprint
	debug = True
	# voila = [[1,1], [2,2], [1,-1], [2,-2], [-1,-1], [-2,-2], [-1,1], [-2,2],]  # concentric squares
	# voila = [(-1.0, 3.0), (-1.0, -1.0), (3.0, -1.0), (3.0, 3.0), (1.0, 3.0)]
	voila = [(-1.0, 3.0), (-1.0, -1.0), (3.0, -1.0), (3.0, 3.0), (1.0, 3.0), (-1.0, 1.0), (3.0, 1.0), (1.0, 1.0), (1.0, -1.0)]
	hull = convex_hull(voila)
	print('Hull:')
	pprint(hull)