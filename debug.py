import pyautogui
import pytesseract
import cv2
import numpy
import PIL

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

def main():
	y_coords = 226
	while y_coords < 600:
		image = cap_image((697,y_coords), (825, y_coords+29))
		y_coords += 39
		image = process_image(image)
		txt = tesser(image)
		print(txt)
main()