# Main script that will merch items in the GE

import pyautogui
import time
import os
import random

# below are custom modules
from Custom_Modules import realmouse
from Custom_Modules import pointfrombox
from Custom_Modules import gelimitfinder

def main():
	# maybe we should add a pickle load up here so that we can load in a previous state if we have one?
	# this would mean we can save instances and only have to initialise one if we don't have a save file to load
	# we should also have a variable that tells us whether or not we loaded from a saved instance
	# this is important because if we did we don't want to be scoring items immediately (this would create articifically low scores)
	# ask me for more info on this
	list_of_runescape_windows = detect_runescape_windows() # returns a list of object of runescape windows and all their features
	if len(list_of_runescape_windows) > 1:
		print('We have detected {} windows'.format(len(list_of_runescape_windows)))
	elif len(list_of_runescape_windows) == 1:
		print('We have detected {} window'.format(len(list_of_runescape_windows)))
	elif len(list_of_runescape_windows) == 0:
		print("Failed, we couldn't detect a runescape window, script will now abort")
		quit()
	logout_prevention_random_number = random.randint(150, 250)
	while(True):
		for runescape_window in list_of_runescape_windows:
			if time.time() - runescape_window.last_action_time > logout_prevention_random_number: # prevent auto logout
				logout_prevention_random_number = random.randint(150, 250)
				runescape_window.set_time_of_last_action()
				prevent_logout(runescape_window.top_left_corner, runescape_window.bottom_right_corner)
		# for each window we need to check if there are any completed offers and if so handle them
		for runescape_window in list_of_runescape_windows:
			coords_of_completed_offer = pyautogui.locateOnScreen('Tools/screenshots/green_offer_complete_bar.png', region=(runescape_window.top_left_corner[0], runescape_window.top_left_corner[1], runescape_window.bottom_right_corner[0]-runescape_window.top_left_corner[0], runescape_window.bottom_right_corner[1]-runescape_window.top_left_corner[1]))
			if coords_of_completed_offer == None:
				continue
			else:
				for ge_slot in runescape_window.list_of_ge_slots:
					if ge_slot.top_left_corner[0]<coords_of_completed_offer[0] and ge_slot.top_left_corner[1]<coords_of_completed_offer[1] and ge_slot.bottom_right_corner[0]>coords_of_completed_offer[0] and ge_slot.bottom_right_corner[1]>coords_of_completed_offer[1]:
						collect_items_from_ge_slot(ge_slot, runescape_window)
						# do stuff based on buy or sell



	# if the item was bought then it would simply sell it at the correct price (assuming the order was filled in under
	# a certain amount of time), if the item took too long to buy then we would buy another just to confirm that our 
	# price is right). We would also place the item in the cooldown list as a tuple. this tuple would contain
	# the item name, the time it was bought, the quantity that were bought
	# if the item was sold then we would score the item based on the profit it made us and the time it took to buy and sell
	# then we would simply mark the slot as empty by setting the self.buy_or_sell variable to None and then move on
	# this None would be caught in the next sections of code and a buy order would automatically be placed
	# if there are no completed orders then we need to check for empty ge slots and fill them with orders
	for runescape_window in list_of_runescape_windows:
			if runescape_window.contains_empty_ge_slot: # scans until it finds a window with an empty ge slot
				
				break
	# all orders should be unique, ie not buying coal on 2 windows at once, this would harm profit since they would be
	# competing with eachother. Instead one window should buy it, then once it starts selling the next window can start buying

class item():
	def __init__(self, name, limit):
		self.item_name = name
		self.limit = limit
		self.image_in_ge_search = check_if_image_exists(name)
		self.price_instant_bought_at = None
		self.price_instant_sold_at = None


class ge_slot():
	def __init__(self, position):
		self.top_left_corner = position[0]
		self.bottom_right_corner = position[1]
		self.buy_or_sell = None
		self.item = None


class runescape_instance():
	def __init__(self, position):
		self.bottom_right_corner = position
		self.top_left_corner = (position[0] - 750, position[1] - 450)
		self.member_status = members_status_check(self.top_left_corner, self.bottom_right_corner)
		self.list_of_ge_slots = initialise_ge_slots(self.top_left_corner, self.bottom_right_corner) # this returns a list of ge_slot objects
		self.money = 20000000 # given a default of 20m for now, we could change this later maybe
		self.profit = 0
		self.last_action_time = time.time()
		examine_money(position) # examines money to make the above line accurate
		self.items_to_merch = items_to_merch(self.member_status)
		self.list_of_items_on_cooldown = []
		self.contains_empty_ge_slot = empty_ge_slot_check(self.list_of_ge_slots) # will be true if there is an empty slot in this window, else false

	def set_time_of_last_action(self):
		self.last_action_time = time.time()


def collect_items_from_ge_slot(ge_slot, runescape_window):
	print(ge_slot.top_left_corner, ge_slot.bottom_right_corner)
	point_to_click = pointfrombox.random_point(ge_slot.top_left_corner, ge_slot.bottom_right_corner)
	realmouse.move_mouse_to(point_to_click[0], point_to_click[1])
	pyautogui.click()
	wait_for('Tools/screenshots/completed_offer_page.png', runescape_window)
	point_of_item_collection_box_1 = pointfrombox.random_point((runescape_window.bottom_right_corner[0]-303,runescape_window.bottom_right_corner[1]-166), (runescape_window.bottom_right_corner[0]-273, runescape_window.bottom_right_corner[1]-138))
	point_of_item_collection_box_2 = pointfrombox.random_point((runescape_window.bottom_right_corner[0]-254,runescape_window.bottom_right_corner[1]-166), (runescape_window.bottom_right_corner[0]-222, runescape_window.bottom_right_corner[1]-138))
	realmouse.move_mouse_to(point_of_item_collection_box_2[0], point_of_item_collection_box_2[1])
	pyautogui.click()
	realmouse.move_mouse_to(point_of_item_collection_box_1[0], point_of_item_collection_box_1[1])
	pyautogui.click()
	wait_for('Tools/screenshots/lent_item_box.png', runescape_window)

def wait_for(image, runescape_window):
	# could add a failsafe in here incase we misclick or something, this should be something to come back to
	while(True):
		found = pyautogui.locateOnScreen(image, region=(runescape_window.top_left_corner[0], runescape_window.top_left_corner[1], runescape_window.bottom_right_corner[0]-runescape_window.top_left_corner[0], runescape_window.bottom_right_corner[1]-runescape_window.top_left_corner[1]))
		if found != None:
			break
		
def empty_ge_slot_check(list_of_ge_slots):
	for slot in list_of_ge_slots:
		if slot.buy_or_sell == None:
			return(True)
	return(False)

def prevent_logout(top_left_corner, bottom_right_corner):
	seed = random.random()
	print(seed)
	if seed > 0.5: # opens up the sale history tab for 5 seconds then returns to ge tab
		move_mouse_to_box('Tools/screenshots/sale_history_button.png', top_left_corner, bottom_right_corner)
		pyautogui.click()
		time.sleep(5)
		move_mouse_to_box('Tools/screenshots/grand_exchange_button.png', top_left_corner, bottom_right_corner)
		pyautogui.click()
	else: # examines the money pouch
		examine_money(bottom_right_corner) 

def move_mouse_to_box(image_of_box, top_left_corner, bottom_right_corner): # pass in an image and a search region
	box_to_click = pyautogui.locateOnScreen(image_of_box, region=(top_left_corner[0], top_left_corner[1], bottom_right_corner[0]-top_left_corner[0], bottom_right_corner[1]-top_left_corner[1]))
	random_x = random.randint(0, box_to_click[2])
	random_y = random.randint(0, box_to_click[3])
	realmouse.move_mouse_to(box_to_click[0] + random_x, box_to_click[1] + random_y)

def check_if_image_exists(item_name):
	file_name = 'Tools/screenshots/items/'+item_name.replace(' ','_')+'.png'
	if os.path.isfile(file_name):
		return(file_name)
	else:
		print('You do not have an image file for {} so the script is aborting, to fix this issue either take a screenshot of {} or remove it from the list of items to merch'.format(item_name, item_name))

def items_to_merch(member_status):
	if member_status:
		items_to_merch = []
		# below is a list of members items to merch
		list_of_items = ['Coal', 'Air rune', 'Fire rune', 'Rune bar', 'Airut bones', 'Onyx bolts (e)', 'Grenwall spikes', 'Runite ore', 'Araxyte arrow', 'Infernal ashes', 'Dragon bones']
		list_of_item_limits = gelimitfinder.find_ge_limit(list_of_items)
		for i in range(len(list_of_items)):
			items_to_merch.append(item(list_of_items[i], list_of_item_limits[i]))
		return(items_to_merch) # we are a member so initialise a members item list
	else:
		items_to_merch = []
		# below is a list of f2p items to merch
		list_of_items = ['Coal', 'Air rune', 'Fire rune', 'Rune bar', 'Runite ore', 'Water rune']
		list_of_item_limits = gelimitfinder.find_ge_limit(list_of_items)
		for i in range(len(list_of_items)):
			items_to_merch.append(item(list_of_items[i], list_of_item_limits[i]))
		return(items_to_merch) # we are f2p so initialise a f2p item list

def examine_money(position):
	point = pointfrombox.random_point((138, 94), (189, 109)) # this whole block just examines the amount of money
	money_pouch = (position[0] - point[0], position[1] - point[1]) # that the account has just for auto log out purposes
	realmouse.move_mouse_to(money_pouch[0], money_pouch[1]) # so that it has a recording of the last time an action
	pyautogui.click(button='right') # was taken and can keep track of this value in future to stop logouts occuring
	point = pointfrombox.random_point((-75, -35), (74, -24))
	examine = (money_pouch[0] - point[0], money_pouch[1] - point[1])
	realmouse.move_mouse_to(examine[0], examine[1])
	pyautogui.click()

def initialise_ge_slots(top_left_corner, bottom_right_corner):
	ge_slots = []
	for i in count_ge_slots(top_left_corner, bottom_right_corner):
		ge_slots.append(ge_slot(((i[0],i[1]),(i[0]+i[2],i[1]+i[3]))))
	return(ge_slots)

def members_status_check(top_left_corner, bottom_right_corner):
	width = bottom_right_corner[0]-top_left_corner[0]
	height = bottom_right_corner[1]-top_left_corner[1]
	if len(list(pyautogui.locateAllOnScreen('Tools/screenshots/non_mems_slot.png', region=(top_left_corner[0], top_left_corner[1], width, height)))) != 0:
		return(False)
	else:
		return(True)

def detect_runescape_windows(): # this function will detect how many runescape windows are present and where they are
	list_of_runescape_windows = []
	for i in pyautogui.locateAllOnScreen('Tools/screenshots/collect_all_buttons.png'):
		list_of_runescape_windows.append(runescape_instance((i[0]+i[2], i[1]+i[3])))
	return(list_of_runescape_windows)

def move_and_resize_runescape_windows():
	pass # this will move and resize the detected windows.
	# Initially this will just pass since we don't know how to do this, but further down the road we can add to this and implement it

def count_ge_slots(top_left_corner, bottom_right_corner): # this checks how many slots a particular window has available
	width = bottom_right_corner[0]-top_left_corner[0]
	height = bottom_right_corner[1]-top_left_corner[1]
	list_of_ge_slots = list(pyautogui.locateAllOnScreen('Tools/screenshots/available_ge_slot.png', region=(top_left_corner[0], top_left_corner[1], width, height)))
	return(list_of_ge_slots)
	



if __name__ == '__main__':
	main()
