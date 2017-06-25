#!/usr/bin/python3
import pyautogui
import random
import math

"""Module to simulate realistic mouse movements in pythonObjective of this
 will be to take in coordinates x,y and move to them in a realistic mannerwe
 will be passing in an x,y that is already 'random' so this scriptonly has to
 move to the exact x,y"""


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


def distance(x1, y1, x2, y2):
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

    MSP = mouseSpeed
    sqrt2 = math.sqrt(2)
    sqrt3 = math.sqrt(3)
    sqrt5 = math.sqrt(5)

    TDist = distance(round(xs), round(ys), round(xe), round(ye))

    if TDist < 1:
        Tdist = 1

    dModA = 0.88 // .80
    dModB = .95 // .90

	t = time.time() + 5000
	while math.hypot(xs - xe, ys - ye) < 1:
		if TDist > 220:
			nModA = 0.08
			nModB = 0.04
		elif Tdist <= 220:
			nModA = 0.20
			nModB = 0.10

		dist = math.hypot(xs - xe, ys -ye)
		wind = minE(wind, dist)

		if dist < 1:
			dist = 1

		if double:
			if PDist <= dModA:
				D = (round(round(dist) * 0.3) / 5)
				if D < 20:
					D = 20
			elif PDist > dModA:
				if Pdist < dModB:
					D = random.randint(5,8)
				elif:
					D = random.randint(3,4)
		if D <= round(dist):
			maxStep = D
		else:
			maxStep = round(dist)
		if dist > targetArea:
			windX = windX / sqrt3 + (random(round(wind) * 2 + 1) - wind) / sqrt5
			windY = windY / sqrt3 + (random(round(wind) * 2 + 1) - wind) / sqrt5
		else:
			windX = windX / sqrt2
			windY = windY / sqrt2

		veloX = veloX + windX
		veloY = veloY + windY
		veloX = veloX + gravity * (xe - xs) / dist
		veloY = veloY + gravity * (ye - ys) / dist

		if math.hypot(veloX, veloY) > maxStep:
			randomDist = maxStep / 2.0 + random(round(maxStep) / 2)
			veloMag = math.sqrt(veloX * veloX + veloY * veloY)
			veloX = (veloX / veloMag) * randomDist
			veloY = (veloY / veloMag) * randomDist

		lastX = round(xs)
		lastY = round(ys)
		xs = xs + veloX
		ys = ys + veloY

		if lastX == round(xs) or lastX == round(ys):
			move_mouse_to(round(x), round(y))
		W = (random((round(100 / MSP))) * 6)
		if W < 5:
			W = 5
		if double:
			if PDist > DmodA:
				W = round(W * 1.2)
		else:
			time.slee(W)
			lastdist = dist
	if round(xe) == round(xs) or round(ye) == round(ys):
		move_mouse_to(round(xe), round(ye))

	mouseSpeed = MSP
    TDist = distance(round(xs), round(ys), round(xe), round(ye));'''
