#!/usr/bin/python3
import pyautogui
from random import random
import math
from time import sleep

# Adjustable mouse speed variable. Default set to 20.
mouseSpeed = 50
pyautogui.FAILSAFE = False


def move_mouse_to(x, y):
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

    #startCoords = (0, 0)
    #width, height = pyautogui.size()
    #endCoords = (width/2, height/2)

    startCoords = (pyautogui.position())
    endCoords = (x, y)

    mouseCalc = MouseMovementCalculator(7, 5, mouseSpeed, 10 * mouseSpeed)
    coordsAndDelay = mouseCalc.calcCoordsAndDelay(startCoords, endCoords)

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
