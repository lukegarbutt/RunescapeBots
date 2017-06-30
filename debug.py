import pyautogui
import pytesseract
import cv2
import numpy
import PIL
import pickle
import operator
import random

def cap_image(top_left, bottom_right):
	image = pyautogui.screenshot(region=(top_left[0], top_left[1], bottom_right[0]-top_left[0], bottom_right[1]-top_left[1]))
	return(image)

def tesser(image):
	txt = pytesseract.image_to_string(image, config='-psm 7')
	return(txt)

def process_image(image):
	array_image = numpy.array(image)
	array_image = cv2.resize(array_image, (0,0), fx=2, fy=2)
	image = PIL.Image.fromarray(array_image)
	return(image)

def item_score_test():
	y_coords = 226
	while y_coords < 600:
		image = cap_image((697,y_coords), (825, y_coords+29))
		y_coords += 39
		image = process_image(image)
		txt = tesser(image)
		print(txt)

def other_tesser_tests():
	image = cap_image((599,891), (653,906))
	image = process_image(image)
	txt = tesser(image)
	print(txt)

def loc_image():
	print(pyautogui.locateOnScreen('Tools/screenshots/money_icon.png'))

def list_test():
	x = [['Coal', 1], ['Iron', 2], ['Dragon Bones', 4], ['Air rune', 3]]
	list_of_items = []
	list_of_scores = []
	for i in range(len(x)):
		list_of_items.append(x[i][0])
		list_of_scores.append(x[i][1])
	normalised_scores = []
	for i in range(len(list_of_scores)):
		normalised_scores.append(list_of_scores[i]/sum(list_of_scores))
	x = 0
	list_of_returned_items = []
	while x<100000:
		seed = random.random()
		for i in range(len(normalised_scores)):
			seed -= normalised_scores[i]
			if seed < 0:
				#print('The item returned was {}'.format(list_of_items[i]))
				list_of_returned_items.append(list_of_items[i])
				break
		x += 1
	print('Coal was returned {} times'.format(list_of_returned_items.count('Coal')))
	print('Iron was returned {} times'.format(list_of_returned_items.count('Iron')))
	print('Dragon Bones was returned {} times'.format(list_of_returned_items.count('Dragon Bones')))
	print('Air rune was returned {} times'.format(list_of_returned_items.count('Air rune')))

list_test()
