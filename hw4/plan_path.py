#!/usr/bin/python
from convex import convex_hull
from graph import *
from dijkstra import dijkstra
from pprint import pprint
from copy import deepcopy

def parse_obstacles_file():
	#o = open('obstacles.txt')
	o = open('test_obstacles.txt')
	o.readline()  # ignore first line
	obstacles = []
	for line in o.readlines():
		coords = line.strip('\r\n').split(' ')
		if len(coords) == 1:
			obstacles.append([])
		elif len(coords) == 2:
			obstacles[-1].append(tuple((float(x) for x in coords)))
	return obstacles

def parse_goals_file():
	#o = open('goals.txt')
	o = open('test_goals.txt')
	goals = []
	for line in o.readlines():
		coords = line.strip('\r\n').split(' ')
		goals.append([float(x) for x in coords])
	return goals

def grow_vertices(obstacles, robot, ref_index):
	grown_vertices = deepcopy(obstacles)
	new_robot = deepcopy(robot)
	r0 = new_robot.pop(ref_index)

	for i in range(len(new_robot)):  # calculate vector from r0 to each vertex of reflected robot
		new_robot[i] = [ new_robot[i][0] - r0[0], new_robot[i][1] - r0[1] ]
	print("rrobot:")
	pprint(new_robot)

	for i in range(len(obstacles)):
		obstacle = obstacles[i]
		for j in range(len(obstacle)):
			vo = obstacle[j]
			for k in range(len(new_robot)):
				vr = new_robot[k]
				x = (vo[0] + vr[0], vo[1] + vr[1])
				if not x in grown_vertices[i]:
					grown_vertices[i].append( x )
	return grown_vertices


if __name__ == '__main__':
	obstacles = parse_obstacles_file()
	start, end = parse_goals_file()
	robot = [[1,1], [1,-1], [-1,-1], [-1,1]]
	rrobot = [[-x,-y] for x,y in robot]  # reflected robot
	grown_vertices = grow_vertices(obstacles, rrobot, ref_index=0)
	grown_obstacles = [ convex_hull(x) for x in grown_vertices ]
	v,e = visibility_graph(grown_obstacles, start, end)
	d = distance_graph(v,e)
	path = dijkstra(d, start, end)

	print('Obstacles:')
	pprint(obstacles)
	print('Reflected robot:')
	pprint(rrobot)
	print('Grown vertices:')
	pprint(grown_vertices)
	print('Grown obstacles:')
	pprint(grown_obstacles)