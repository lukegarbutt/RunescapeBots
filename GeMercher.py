# Main script that will merch items in the GE

import pyautogui
import time

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
	while(True):
		break
	# for each window we need to check if there are any completed offers and if so handle them
	# if the item was bought then it would simply sell it at the correct price (assuming the order was filled in under
	# a certain amount of time), if the item took too long to buy then we would buy another just to confirm that our 
	# price is right). We would also place the item in the cooldown list as a tuple. this tuple would contain
	# the item name, the time it was bought, the quantity that were bought
	# if the item was sold then we would score the item based on the profit it made us and the time it took to buy and sell
	# then we would simply mark the slot as empty by setting the self.buy_or_sell variable to None and then move on
	# this None would be caught in the next sections of code and a buy order would automatically be placed
	# if there are no completed orders then we need to check for empty ge slots and fill them with orders
	# all orders should be unique, ie not buying coal on 2 windows at once, this would harm profit since they would be
	# competing with eachother. Instead one window should buy it, then once it starts selling the next window can start buying
	for i in list_of_runescape_windows: # this little block is purely to get an output and test the code so far
		for j in i.items_to_merch: # it should output the items that each instance of runescape can merch, along with limits
			print(j.item_name, j.limit)

	#print(list_of_runescape_windows[0].items_to_merch[0].item_name, list_of_runescape_windows[0].items_to_merch[0].limit)

class item():
	def __init__(self, name, limit):
		self.item_name = name
		self.limit = limit
		#self.image_in_ge_search = # the image of the item as it appears when searched for in the ge
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


def items_to_merch(member_status):
	if member_status:
		items_to_merch = []
		list_of_items = ['Coal', 'Air rune', 'Fire rune', 'Rune bar', 'Airut bones', 'Onyx bolts (e)', 'Grenwall spikes', 'Runite ore', 'Araxyte arrow', 'Infernal ashes', 'Dragon bones']
		list_of_item_limits = gelimitfinder.find_ge_limit(list_of_items)
		for i in range(len(list_of_items)):
			items_to_merch.append(item(list_of_items[i], list_of_item_limits[i]))
		return(items_to_merch) # we are a member so initialise a members item list
	else:
		items_to_merch = []
		list_of_items = ['Coal', 'Air rune', 'Fire rune', 'Rune bar', 'Runite ore', 'Water rune']
		list_of_item_limits = gelimitfinder.find_ge_limit(list_of_items)
		for i in range(len(list_of_items)):
			items_to_merch.append(item(list_of_items[i], list_of_item_limits[i]))
		return(items_to_merch) # we are f2p so initialise a f2p item list

def examine_money(position):
	point = pointfrombox.random_point((189, 109), (138, 94)) # this whole block just examines the amount of money
	money_pouch = (position[0] - point[0], position[1] - point[1]) # that the account has just for auto log out purposes
	realmouse.move_mouse_to(money_pouch[0], money_pouch[1]) # so that it has a recording of the last time an action
	pyautogui.click(button='right') # was taken and can keep track of this value in future to stop logouts occuring
	point = pointfrombox.random_point((74, -24), (-75, -35))
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