#short script that will take in a list of items and search for them in the ge to be screenshot
import pyautogui
import time
import random
import os

def main():
	box_1_coords = (43,850,150,40)
	box_2_coords = (215,850,150,40)
	box_3_coords = (387,850,150,40)
	box_4_coords = (43,905,150,40)
	box_5_coords = (215,905,150,40)
	box_6_coords = (387,905,150,40)
	time.sleep(3)
	list_of_items = ['Coal', 'Air rune', 'Fire rune', 'Rune bar', 'Runite ore', 'Water rune']
	list_of_file_names = []
	for i in range(len(list_of_items)):
		list_of_file_names.append(list_of_items[i].replace(' ', '_')+'.png')
	print(list_of_items)
	print(list_of_file_names)
	for i in range(len(list_of_items)):
		file_name = 'screenshots/items/'+list_of_file_names[i]
		if os.path.isfile(file_name):
			print('file exists', file_name)
			continue
		x = len(list_of_items[i])
		pyautogui.typewrite(list_of_items[i], random.random())
		time.sleep(2)
		pyautogui.screenshot(file_name, region=(box_1_coords))
		for x in range(x):
			pyautogui.press('backspace')
			time.sleep(random.random())
		#time.sleep(10)



main()
