# Module to simulate realistic mouse movements in python
# Objective of this will be to take in coordinates x,y and move to them in a realistic manner
# we will be passing in an x,y that is already 'random' so this script
# only has to move to the exact x,y

import pyautogui
import random


def move_mouse_to(x, y):
	# takes current mouse location and stores it
	curr_x, curr_y = pyautogui.position()
	# calculates the distance from current position to target position
	distance = int(((x - curr_x)**2 + (y - curr_y)**2)**0.5)
	# calculates a random time to make the move take based on the distance
	duration_of_move = (distance * random.random() / 2000) + 0.5
	# move the mouse to our position and takes the time of our duration just
	# calculated
	pyautogui.moveTo(x, y, duration_of_move, pyautogui.easeInOutQuad)


def distance(x1,y1,x2,y2):
    """returns distance (floating point)  of 2 coordinate points"""
    # distance is equal to the square root of (x2-x1)^2 + (y2-y1)^2
    distance = math.sqrt((((x2 - x1) ** 2) + ((y2 - y1) ** 2)))
    return distance


# Had to comment below out until it's working
'''def sMouse(xs, ys, xe, ye, gravity, wind, minWait, maxWait, targetArea, extended, double):
	"""Mouse movement based on distance to determine speed. Default slowed
	speed at 20% from destination, if 'double' is set to true then slowed
	speed also starts at origin and ends 80% to destination."""

	# Adjustable global mouse speed variable. Default set to 20.

	mouseSpeed = 20

    MSP = mouseSpeed;
    sqrt2 = sqrt(2);
    sqrt3 = sqrt(3);
    sqrt5 = sqrt(5);

    TDist = distance(round(xs), round(ys), round(xe), round(ye));'''