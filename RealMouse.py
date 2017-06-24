# Module to simulate realistic mouse movements in python
# Objective of this will be to take in coordinates x,y and move to them in a realistic manner
# we will be passing in an x,y that is already 'random' so this script only has to move to the exact x,y

import pyautogui
import random

def move_mouse_to(x, y):
	curr_x, curr_y = pyautogui.position()
	distance = int(((x-curr_x)**2 + (y-curr_y)**2)**0.5)
	duration_of_move = (distance*random.random()/2000)+0.5
	pyautogui.moveTo(x,y,duration_of_move,pyautogui.easeInOutQuad)