# module to return a random point from a box
import random

def random_point(top_left, bottom_right):
	x = random.randint(bottom_right[0], top_left[0])
	y = random.randint(bottom_right[1], top_left[1])
	point = (x,y)
	return(point)