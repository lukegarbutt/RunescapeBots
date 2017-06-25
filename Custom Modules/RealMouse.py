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


def sMouse(xs, ys, xe, ye, gravity, wind, minWait, maxWait, targetArea, extended, double):
	"""Mouse movement based on distance to determine speed. Default slowed
	speed at 20% from destination, if 'double' is set to true then slowed
	speed also starts at origin and ends 80% to destination."""

	# Adjustable global mouse speed variable. Default set to 20.

	mouseSpeed = 20

    MSP = mouseSpeed;
    sqrt2 = sqrt(2);
    sqrt3 = sqrt(3);
    sqrt5 = sqrt(5);

	  TDist: = distance(round(xs), round(ys), round(xe), round(ye));
	  if (TDist < 1) then
	    TDist: = 1;

	  dModA:= 0.88; // .80
	  dModB:= 0.95; // .90

	  if (TDist > 220) then
	  begin
	    nModA: = 0.08;
	    nModB: = 0.04;
	  end else if (TDist <= 220) then
	  begin
	    nModA: = 0.20;
	    nModB: = 0.10;
	  end;

	  t: = getSystemTime() + 5000;
	  repeat
	    if (getSystemTime() > t) then
	      break;

	    dist:= hypot(xs - xe, ys - ye);
	    wind:= minE(wind, dist);
	    if (dist < 1) then
	      dist: = 1;
	    PDist: = (dist / TDist);
	    if (PDist < 0.01) then
	      PDist: = 0.01;

	    if double then
	    begin
	      if (PDist <= dModA) then
	      begin
	        D: = (round((round(dist) * 0.3)) / 5);
	        if (D < 20) then
	          D: = 20;

	      end else if (PDist > dModA) then
	      begin
	        if (PDist < dModB) then
	          D: = randomRange(5, 8)
	        else if (PDist >= dModB) then
	          D: = randomRange(3, 4);
	      end;
	    end;

	    if (PDist >= nModA) then
	    begin
	       D: = (round((round(dist) * 0.3)) / 5);
	      if (D < 20) then
	        D: = 20;
	    end else if (PDist < nModA) then
	    begin
	      if (PDist >= nModB) then
	        D: = randomRange(5, 8)
	      else if (PDist < nModB) then
	        D: = randomRange(3, 4);
	    end;

	    if (D <= round(dist)) then
	      maxStep: = D
	    else
	      maxStep: = round(dist);

	    if dist >= targetArea then
	    begin
	      windX:= windX / sqrt3 + (random(round(wind) * 2 + 1) - wind) / sqrt5;
	      windY:= windY / sqrt3 + (random(round(wind) * 2 + 1) - wind) / sqrt5;
	    end else
	    begin
	      windX:= windX / sqrt2;
	      windY:= windY / sqrt2;
	    end;

	    veloX:= veloX + windX;
	    veloY:= veloY + windY;
	    veloX:= veloX + gravity * (xe - xs) / dist;
	    veloY:= veloY + gravity * (ye - ys) / dist;

	    if (hypot(veloX, veloY) > maxStep) then
	    begin
	      randomDist:= maxStep / 2.0 + random(round(maxStep) div 2);
	      veloMag:= sqrt(veloX * veloX + veloY * veloY);
	      veloX:= (veloX / veloMag) * randomDist;
	      veloY:= (veloY / veloMag) * randomDist;
	    end;

	    lastX:= round(xs);
	    lastY:= round(ys);
	    xs:= xs + veloX;
	    ys:= ys + veloY;

	    if (lastX <> round(xs)) or (lastY <> round(ys)) then
	      moveMouse(round(xs), round(ys));

	    W: = (random((round(100 / MSP))) * 6);
	    if (W < 5) then
	      W: = 5;
	    if double then
	      if (PDist > dModA) then
	        W: = round(W * 2.5)
	    else
	      W: = round(W * 1.2);
	    wait(W);
	    lastdist:= dist;
	  until(hypot(xs - xe, ys - ye) < 1)

	  if (round(xe) <> round(xs)) or (round(ye) <> round(ys)) then
	    moveMouse(round(xe), round(ye));

	  mouseSpeed: = MSP;
	end;

	{*
	_humanWindMouse
	~~~~~~~~~~~~~~~

	.. code-block:: pascal

	    procedure _humanWindMouse(xs, ys, xe, ye, gravity, wind, minWait,
	      maxWait, targetArea: extended);

	Moves the mouse like a human

	.. note::

	    - by BenLand100 & Flight

	Example:

	.. code-block:: pascal

	    See mouse().
	*}
	procedure _humanWindMouse(xs, ys, xe, ye, gravity, wind, minWait, maxWait, targetArea: extended);
	var
	  veloX, veloY, windX, windY, veloMag, dist, randomDist, lastDist, D: extended;
	  lastX, lastY, MSP, W, TDist: integer;
	  T: LongWord;
	  sqrt2, sqrt3, sqrt5, maxStep, rCnc: extended;
	begin
	  MSP: = mouseSpeed;
	  sqrt2: = sqrt(2);
	  sqrt3: = sqrt(3);
	  sqrt5: = sqrt(5);

	  TDist: = distance(round(xs), round(ys), round(xe), round(ye));
	  t: = getSystemTime() + 10000;
	  repeat
	    if (getSystemTime() > t) then
	      break;

	    dist: = hypot(xs - xe, ys - ye);
	    wind: = minE(wind, dist);
	    if (dist < 1) then
	      dist: = 1;

	    D: = (round((round(TDist) * 0.3)) / 7);
	    if (D > 25) then
	      D: = 25;
	    if (D < 5) then
	      D: = 5;

	    rCnc: = random(6);
	    if (rCnc=1) then
	      D: = randomRange(2, 3);

	    if (D <= round(dist)) then
	      maxStep: = D
	    else
	      maxStep: = round(dist);

	    if dist >= targetArea then
	    begin
	      windX: = windX / sqrt3 + (random(round(wind) * 2 + 1) - wind) / sqrt5;
	      windY: = windY / sqrt3 + (random(round(wind) * 2 + 1) - wind) / sqrt5;
	    end else
	    begin
	      windX: = windX / sqrt2;
	      windY: = windY / sqrt2;
	    end;

	    veloX: = veloX + windX;
	    veloY: = veloY + windY;
	    veloX: = veloX + gravity * (xe - xs) / dist;
	    veloY: = veloY + gravity * (ye - ys) / dist;

	    if (hypot(veloX, veloY) > maxStep) then
	    begin
	      randomDist: = maxStep / 2.0 + random(round(maxStep) div 2);
	      veloMag: = sqrt(veloX * veloX + veloY * veloY);
	      veloX: = (veloX / veloMag) * randomDist;
	      veloY: = (veloY / veloMag) * randomDist;
	    end;

	    lastX: = round(xs);
	    lastY: = round(ys);
	    xs: = xs + veloX;
	    ys: = ys + veloY;

	    if (lastX <> round(xs)) or (lastY <> round(ys)) then
	      moveMouse(round(xs), round(ys));

	    W: = (random((round(100 / MSP))) * 6);
	    if (W < 5) then
	      W: = 5;
	    W: = round(W * 0.9);
	    wait(W);
	    lastdist: = dist;
	  until(hypot(xs - xe, ys - ye) < 1)

	  if (round(xe) <> round(xs)) or (round(ye) <> round(ys)) then
	    moveMouse(round(xe), round(ye));

	  mouseSpeed: = MSP;
	end;
