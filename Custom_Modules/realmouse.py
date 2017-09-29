#!/usr/bin/python3
import pyautogui
from random import random
import math
from time import sleep

# Adjustable mouse speed variable. Default set to 20.
mouseSpeed = 50
pyautogui.FAILSAFE = False


def move_mouse_to(x, y):
<<<<<<< HEAD
	"""Function to simulate realistic mouse movements in python. The objective of this
	 will be to take in coordinates x,y and move them in a realistic manner. We
	 will be passing in an x,y,  that is already 'random' so this function will
	 move to the exact x,y"""
	# takes current mouse location and stores it
	while(True):
		try:
			curr_x, curr_y = pyautogui.position()
			# calculates the distance from current position to target position
			distance = int(((x - curr_x)**2 + (y - curr_y)**2)**0.5)
			# calculates a random time to make the move take based on the distance
			duration_of_move = (distance * random.random() / 2000) + 0.5
			# move the mouse to our position and takes the time of our duration just
			# calculated
			pyautogui.moveTo(x, y, duration_of_move, pyautogui.easeInOutQuad)
			#pyautogui.moveTo(x, y, duration_of_move, pyautogui.easeOutElastic)
			break
		except:
			print('paused for 10 seconds')
			time.sleep(10)

=======
    global mouseSpeed
    """Function to simulate realistic mouse movements in python. The objective of this
     will be to take in coordinates x,y and move them in a realistic manner. We
     will be passing in an x,y,  that is already 'random' so this function will
     move to the exact x,y"""
    # takes current mouse location and stores it
    #curr_x, curr_y = pyautogui.position()
    # calculates the distance from current position to target position
    #distance = int(((x - curr_x)**2 + (y - curr_y)**2)**0.5)
    # calculates a random time to make the move take based on the distance
    #duration_of_move = (distance * random.random() / 2000) + 0.5
    # move the mouse to our position and takes the time of our duration just
    # calculated
    #pyautogui.moveTo(x, y, duration_of_move, pyautogui.easeInOutQuad)
    #pyautogui.moveTo(x, y, duration_of_move, pyautogui.easeOutElastic)
>>>>>>> 1ebee3ec1b919c5656bd06f9b041160dedbf0df1

    #startCoords = (0, 0)
    #width, height = pyautogui.size()
    #endCoords = (width/2, height/2)

<<<<<<< HEAD
def distance(xs, ys, xe, ye):
	"""returns distance (floating point)  of 2 coordinate points"""
	# distance is equal to the square root of (x2-x1)^2 + (y2-y1)^2
	distance = math.sqrt((((xe - xs) ** 2) + ((ye - ys) ** 2)))
	print("Distance:{}".format(distance))
	return distance
=======
    startCoords = (pyautogui.position())
    endCoords = (x, y)
>>>>>>> 1ebee3ec1b919c5656bd06f9b041160dedbf0df1

    mouseCalc = MouseMovementCalculator(7, 5, mouseSpeed, 10 * mouseSpeed)
    coordsAndDelay = mouseCalc.calcCoordsAndDelay(startCoords, endCoords)

<<<<<<< HEAD
def humanWindMouse(xs, ys, xe, ye, gravity, wind, minWait, maxWait, MaxStep):
	""" Moves the mouse like a human"""
	global mouseSpeed

	MSP = mouseSpeed
	veloX = 1
	veloY = 1
	windX = 1
	windY = 1
	sqrt2 = math.sqrt(2)
	sqrt3 = math.sqrt(3)
	sqrt5 = math.sqrt(5)

	total_distance = distance(round(xs), round(ys), round(xe), round(ye))
	t = time.time() + 10000

	while math.hypot(xs - xe, ys - ye) > 1:
		print('Hypotnus: ',math.hypot(xs - xe, ys - ye))
		if time.time() > t:
			print('time is greater, breaking')
			break

		dist = math.hypot(xs - xe, ys - ye)
		wind = min(wind, dist)
		if dist < 1: 
			dist = 1
				
		D = (round((round(total_distance) * 0.3)) // 7)
		
		if D > 25:
			D = 25
		if D < 5:
			D = 5

		rCnc = random.randint(1,6)
		if rCnc == 1:
			D = 2

		if D <= round(dist):
			maxStep = D
		else:
			maxStep = round(dist)

		#if dist >= targetArea:
		if dist >= 2:
			windX = windX / sqrt3 + (random.randint(1,round(wind) * 2 + 1) - wind) / sqrt5
			windY = windY / sqrt3 + (random.randint(1,round(wind) * 2 + 1) - wind) / sqrt5
		else:
			windX = windX / sqrt2
			windY = windY / sqrt2

		veloX = veloX + windX
		veloY = veloY + windY
		veloX = veloX + gravity * (xe - xs) / dist
		veloY = veloY + gravity * (ye - ys) / dist

		if math.hypot(veloX, veloY) > maxStep:
			try:
				randomDist = maxStep / 2.0 + random.randrange(round(maxStep) / 2)
			except:
				continue
			veloMag = math.sqrt(veloX * veloX + veloY * veloY)
			veloX = (veloX / veloMag) * randomDist
			veloY = (veloY / veloMag) * randomDist


		lastX = round(xs)
		lastY = round(ys)
		xs = xs + veloX
		ys = ys + veloY

		if lastX != round(xs) or lastY != round(ys):
			print("IN")
			#move(round(xs), round(ys), 1)
			pyautogui.moveTo(xe,ye)

		W = (random.randrange(round(100/MSP)) * 6)

		if W < 5:
			W = 5
		W = round(W * 0.9)
		# fis this to miliseconds not seconds
		time.sleep(W/60)
		lastdist = dist
							 #or
	if round(xe) != round(xs) or round(ye) != round(ys):
		print("OFF")
		print(xe,xs, ye, ys)
		pyautogui.moveTo(x,y)
		#move_mouse_to(round(xe), round(ye))
		#move(round(xs), round(ys), 1)

	mouseSpeed = MSP


def move(xe, ye, button):
	global mouseSpeed

	if button != (1 or 2):
		return

	ms = mouseSpeed
	randSpeed = (random.randrange(mouseSpeed) / 2.0 + mouseSpeed) / 10.0
	# get Cur mouse position
	xs,ys = pyautogui.position()

	humanWindMouse(xs, ys, xe, ye, 1, 5, 10.0/randSpeed, 15.0/randSpeed, 10.0*randSpeed)
	mouseSpeed = ms
	# click here.  Add Code



if __name__ == "__main__":
	pass
	#for _ in range(1):
	#    x = random.randint(0,1920)
	#    y = random.randint(0,1080)
	#
	#    print('NEW coord:{},{}\n'.format(x,y))
	#    time.sleep(1)
	#    move(x,y, 1)
=======
    pyautogui.moveTo(startCoords[0], startCoords[1])

    for x, y, delay in coordsAndDelay:
        delay = delay / 10000
        delay += random()
        pyautogui.moveTo(x, y)
        sleep(delay)


class MouseMovementCalculator:

    def __init__(self, gravity, wind, mouseSpeed, targetError):
        self.gravity = gravity
        self.wind = wind
        self.mouseSpeed = mouseSpeed
        self.targetError = targetError

    def calcCoordsAndDelay(self, startCoords, endCoords):
        veloX, veloY = (0, 0)
        coordsAndDelay = []
        xs, ys = startCoords
        xe, ye = endCoords
        totalDist = math.hypot(xs - xe, ys - ye)

        self._windX = 0
        self._windY = 0

        while True:
            veloX, veloY = self._calcVelocity(
                (xs, ys), (xe, ye), veloX, veloY, totalDist)
            xs += veloX
            ys += veloY

            w = round(
                max(randint(0, max(0, round(100 / self.mouseSpeed) - 1)) * 6, 5) * 0.9)

            coordsAndDelay.append((xs, ys, w))

            if math.hypot(xs - xe, ys - ye) < 1:
                break

        if round(xe) != round(xs) or round(ye) != round(ys):
            coordsAndDelay.append((round(xe), round(ye), 0))

        return coordsAndDelay

    def _calcVelocity(self, curCoords, endCoords, veloX, veloY, totalDist):
        xs, ys = curCoords
        xe, ye = endCoords
        dist = math.hypot(xs - xe, ys - ye)
        self.wind = max(min(self.wind, dist), 1)

        if dist == 0:
            return (veloX, veloY)

        maxStep = None
        D = max(min(round(round(totalDist) * 0.3) / 7, 25), 5)
        rCnc = randint(0, 5)

        if rCnc == 1:
            D = 2

        if D <= round(dist):
            maxStep = D
        else:
            maxStep = round(dist)

        if dist >= self.targetError:
            self._windX = self._windX / \
                math.sqrt(3) + (randint(0, round(self.wind) * 2) -
                                self.wind) / math.sqrt(5)
            self._windY = self._windY / \
                math.sqrt(3) + (randint(0, round(self.wind) * 2) -
                                self.wind) / math.sqrt(5)
        else:
            self._windX = self._windX / math.sqrt(2)
            self._windY = self._windY / math.sqrt(2)

        veloX = veloX + self._windX
        veloY = veloY + self._windY
        veloX = veloX + self.gravity * (xe - xs) / dist
        veloY = veloY + self.gravity * (ye - ys) / dist

        if math.hypot(veloX, veloY) > maxStep:
            randomDist = maxStep / 2.0 + \
                randint(0, math.floor(round(maxStep) / 2))
            veloMag = math.sqrt(veloX * veloX + veloY * veloY)
            veloX = (veloX / veloMag) * randomDist
            veloY = (veloY / veloMag) * randomDist

        return (veloX, veloY)


if __name__ == "__main__":
    pass
>>>>>>> 1ebee3ec1b919c5656bd06f9b041160dedbf0df1
