#!/usr/bin/python
from convex import convex_hull
from pprint import pprint
from copy import deepcopy

def parse_obstacles_file():
	o = open('obstacles.txt')
	o.readline()  # ignore first line
	obstacles = []
	for line in o.readlines():
		coords = line.strip('\r\n').split(' ')
		if len(coords) == 1:
			obstacles.append([])
		elif len(coords) == 2:
			obstacles[-1].append(tuple((float(x) for x in coords)))
	return obstacles

def grow_vertices(obstacles, robot, ref_index):
	grown_vertices = deepcopy(obstacles)
	robot.pop(ref_index)
	for i in range(len(obstacles)):
		obstacle = obstacles[i]
		for j in range(len(obstacle)):
			vo = obstacle[j]
			for k in range(len(robot)):
				vr = robot[k]
				grown_vertices[i].append( (vo[0] + vr[0], vo[1] + vr[1]) )
	return grown_vertices




if __name__ == '__main__':
	obstacles = parse_obstacles_file()
	# pprint([len(x) for x in obstacles])
	robot = [[2,2], [2,-1], [-2,-1], [-2,1]]
	rrobot = [[-x,-y] for x,y in robot]  # reflected robot
	grown_vertices = grow_vertices(obstacles, rrobot, ref_index=0)
	# pprint([len(x) for x in grown_vertices])
	grown_obstacles = [ convex_hull(x) for x in grown_vertices ]
	# pprint([len(x) for x in grown_obstacles])
	print('Obstacles:')
	pprint(obstacles)
	print('\nGrown obstacles:')
	pprint(grown_obstacles)