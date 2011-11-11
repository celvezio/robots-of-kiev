from math import sqrt
from convex import ccw
from pprint import pprint

def distance(v,w):
	""" Returns the distance between the two vertices"""
	dx = w[0] - v[0]
	dy = w[1] - v[1]
	return sqrt( dx*dx + dy*dy )

def distance_graph(v,e):
	n = len(v)
	d = []
	for i in range(n):
		d.append([])
		for j in range(n):
			if e[i][j]:
				d[i].append( distance(v[i],v[j]) )
			else:
				d[i].append( -1 )
	return d



def ccw(A,B,C):
	""" Returns a boolean indicating whether A-B-C is a CCW turn. """
	return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])

def intersects(v,w,x,y):
	""" Simple intersection for non-parallel, non-colinear line segments. """
	return ccw(v,x,y) != ccw(w,x,y) and ccw(v,w,x) != ccw(v,w,y)

def visible(v,w, obstacles):
	""" Checks whether any obstacle edges intersect the v-x edge. """
	for o in obstacles:
		for i in range(len(o)):
			x = o[i]
			y = o[ (i+1) % len(o) ]
			if intersects(v,w,x,y):
					return False
	return True

def visibility_graph(obstacles, start, end):
	""" A visibility graph is an undirected graph G = (V, E) where the
		- V is the set of vertices of the grown obstacles plus the start and goal points, 
		- E is a set of edges consisting of:
			- all obstacle boundary edges, 
			- or an edge between any 2 vertices in V that lies entirely in free space except for its endpoints.
			[XXX] Note: we don't yet thoroughly meet the "free space" conditions.
		"""
	# Vertices
	v = [start]
	for o in obstacles:
		for ov in o:
			v.append(ov)
	v.append(end)

	# Edges
	e = []

	# free space vertices set to True
	for i in range(len(v)):
		e.append([])
		for j in range(len(v)):
			e[i].append( visible( v[i], v[j], obstacles ) )

	# obstacle boundary edges also set to True
	for o in obstacles:
		for i in range(len(o)):
			x = o[i]
			y = o[ (i+1) % len(o) ]

			x_index = v.index(x)
			y_index = v.index(y)

			e[x_index][y_index] = True
			e[y_index][x_index] = True
			
	return v, e



if __name__ == '__main__':
	# o = [[[0,1], [1,0], [-1,0]],]
	o = [[[0,-1], [1,0], [-1,0]],]
	start = [-2,0]
	end = [1,-1]
	print( visible(start, end, o) )