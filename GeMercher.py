# Main script that will merch items in the GE

import pyautogui
import time

# below are custom modules
from Custom_Modules import realmouse
from Custom_Modules import pointfrombox

def main():
	# creates an empty list of runescape windows and then proceeds to populate it using the runescape_instance class
	list_of_runescape_windows = detect_runescape_windows()
	for i in list_of_runescape_windows:
		print(i)
		print(i.list_of_ge_slots)
		print(len(i.list_of_ge_slots))
		print(i.member_status)

class runescape_instance():
	def __init__(self, position):
		self.bottom_right_corner = position
		self.top_left_corner = (position[0] - 750, position[1] - 450)
		self.member_status = members_status_check(self.top_left_corner, self.bottom_right_corner)
		self.list_of_ge_slots = count_ge_slots(self.top_left_corner, self.bottom_right_corner)
		self.money = 20000000 # given a default of 20m for now, we could change this later maybe
		self.profit = 0
		self.last_action_time = time.time()

		point = pointfrombox.random_point((189, 109), (138, 94)) # this whole block just examines the amount of money
		money_pouch = (position[0] - point[0], position[1] - point[1]) # that the account has just for auto log out purposes
		realmouse.move_mouse_to(money_pouch[0], money_pouch[1]) # so that it has a recording of the last time an action
		pyautogui.click(button='right') # was taken and can keep track of this value in future to stop logouts occuring
		point = pointfrombox.random_point((74, -24), (-75, -35))
		examine = (money_pouch[0] - point[0], money_pouch[1] - point[1])
		realmouse.move_mouse_to(examine[0], examine[1])
		pyautogui.click()

def members_status_check(top_left_corner, bottom_right_corner):
	width = bottom_right_corner[0]-top_left_corner[0]
	height = bottom_right_corner[1]-top_left_corner[1]
	if len(list(pyautogui.locateAllOnScreen('tools/screenshots/non_mems_slot.png', region=(top_left_corner[0], top_left_corner[1], width, height)))) != 0:
		return(False)
	else:
		return(True)

def detect_runescape_windows(): # this function will detect how many runescape windows are present and where they are
	list_of_runescape_windows = []
	for i in pyautogui.locateAllOnScreen('tools/screenshots/collect_all_buttons.png'):
		list_of_runescape_windows.append(runescape_instance((i[0]+i[2], i[1]+i[3])))
	return(list_of_runescape_windows)

def move_and_resize_runescape_windows():
	pass # this will move and resize the detected windows.
	# Initially this will just pass since we don't know how to do this, but further down the road we can add to this and implement it

def count_ge_slots(top_left_corner, bottom_right_corner): # this checks how many slots a particular window has available
	width = bottom_right_corner[0]-top_left_corner[0]
	height = bottom_right_corner[1]-top_left_corner[1]
	list_of_ge_slots = list(pyautogui.locateAllOnScreen('tools/screenshots/available_ge_slot.png', region=(top_left_corner[0], top_left_corner[1], width, height)))
	return(list_of_ge_slots)
	



if __name__ == '__main__':
	main()